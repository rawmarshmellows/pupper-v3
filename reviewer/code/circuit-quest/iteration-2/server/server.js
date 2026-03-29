const express = require('express');
const { Pool } = require('pg');
const path = require('path');

const app = express();
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

const pool = new Pool({ connectionString: process.env.DATABASE_URL });
const OPENROUTER_API_KEY = process.env.OPENROUTER_API_KEY;
const PORT = process.env.PORT || 3000;

// ── Embedding helper ────────────────────────────────────────────────

async function getEmbedding(text) {
  const resp = await fetch('https://openrouter.ai/api/v1/embeddings', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${OPENROUTER_API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      model: 'openai/text-embedding-3-small',
      input: text.slice(0, 8000),
      dimensions: 512,
    }),
  });
  const data = await resp.json();
  return data.data[0].embedding;
}

// ── API Routes ──────────────────────────────────────────────────────

app.get('/api/health', async (req, res) => {
  try {
    await pool.query('SELECT 1');
    res.json({ status: 'ok', timestamp: new Date().toISOString() });
  } catch (e) {
    res.status(500).json({ status: 'error', error: e.message });
  }
});

app.get('/api/stats', async (req, res) => {
  try {
    const docs = await pool.query('SELECT COUNT(*) as count FROM context_documents');
    const terms = await pool.query('SELECT COUNT(*) as count FROM essential_terms');
    const links = await pool.query('SELECT COUNT(*) as count FROM document_links');
    const quizzes = await pool.query('SELECT COUNT(*) as count FROM quiz_questions');
    const embeddedDocs = await pool.query('SELECT COUNT(*) as count FROM context_documents WHERE embedding_tldr IS NOT NULL');
    const embeddedTerms = await pool.query('SELECT COUNT(*) as count FROM essential_terms WHERE embedding IS NOT NULL');
    const tiers = await pool.query('SELECT tier, COUNT(*) as count FROM context_documents GROUP BY tier ORDER BY tier');

    res.json({
      documents: parseInt(docs.rows[0].count),
      terms: parseInt(terms.rows[0].count),
      links: parseInt(links.rows[0].count),
      quiz_questions: parseInt(quizzes.rows[0].count),
      embedded_documents: parseInt(embeddedDocs.rows[0].count),
      embedded_terms: parseInt(embeddedTerms.rows[0].count),
      by_tier: Object.fromEntries(tiers.rows.map(r => [r.tier, parseInt(r.count)])),
    });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

app.get('/api/topics', async (req, res) => {
  try {
    const { rows } = await pool.query(
      'SELECT id, topic, tier, tldr, definition FROM context_documents ORDER BY tier, topic'
    );
    res.json(rows);
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

app.get('/api/topics/random', async (req, res) => {
  try {
    const tier = req.query.tier;
    let query = 'SELECT id, topic, tier, tldr, definition, key_insight, full_content FROM context_documents';
    const params = [];
    if (tier) {
      query += ' WHERE tier = $1';
      params.push(tier);
    }
    query += ' ORDER BY RANDOM() LIMIT 1';
    const { rows } = await pool.query(query, params);
    res.json(rows[0] || null);
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

app.get('/api/topics/:id', async (req, res) => {
  try {
    const { rows } = await pool.query(
      'SELECT * FROM context_documents WHERE id = $1',
      [req.params.id]
    );
    if (rows.length === 0) return res.status(404).json({ error: 'Not found' });
    res.json(rows[0]);
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

app.get('/api/search', async (req, res) => {
  try {
    const q = req.query.q;
    if (!q) return res.status(400).json({ error: 'Missing query parameter q' });

    // Hybrid search: semantic + full-text with RRF
    const embedding = await getEmbedding(q);
    const embStr = '[' + embedding.join(',') + ']';

    const { rows } = await pool.query(`
      WITH semantic AS (
        SELECT id, ROW_NUMBER() OVER (ORDER BY embedding_tldr <=> $1::vector) AS rank
        FROM context_documents WHERE embedding_tldr IS NOT NULL LIMIT 20
      ),
      fulltext AS (
        SELECT id, ROW_NUMBER() OVER (ORDER BY ts_rank(search_vector, query) DESC) AS rank
        FROM context_documents, plainto_tsquery('english', $2) query
        WHERE search_vector @@ query LIMIT 20
      )
      SELECT COALESCE(s.id, f.id) AS id,
             COALESCE(1.0 / (60 + s.rank), 0) + COALESCE(1.0 / (60 + f.rank), 0) AS rrf_score
      FROM semantic s FULL OUTER JOIN fulltext f ON s.id = f.id
      ORDER BY rrf_score DESC LIMIT 10
    `, [embStr, q]);

    // Fetch full docs for results
    if (rows.length === 0) return res.json([]);
    const ids = rows.map(r => r.id);
    const docs = await pool.query(
      'SELECT id, topic, tier, tldr, definition FROM context_documents WHERE id = ANY($1)',
      [ids]
    );
    // Maintain RRF order
    const docMap = Object.fromEntries(docs.rows.map(d => [d.id, d]));
    const results = ids.map(id => ({ ...docMap[id], rrf_score: rows.find(r => r.id === id)?.rrf_score })).filter(Boolean);
    res.json(results);
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

app.get('/api/similar/:id', async (req, res) => {
  try {
    const { rows } = await pool.query(`
      SELECT b.id, b.topic, b.tier, b.tldr,
             1 - (a.embedding_tldr <=> b.embedding_tldr) AS similarity
      FROM context_documents a, context_documents b
      WHERE a.id = $1 AND b.id != $1 AND a.embedding_tldr IS NOT NULL AND b.embedding_tldr IS NOT NULL
      ORDER BY a.embedding_tldr <=> b.embedding_tldr
      LIMIT 5
    `, [req.params.id]);
    res.json(rows);
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

app.get('/api/terms', async (req, res) => {
  try {
    const { rows } = await pool.query(
      'SELECT et.id, et.term, et.definition, cd.topic FROM essential_terms et JOIN context_documents cd ON et.document_id = cd.id ORDER BY et.term'
    );
    res.json(rows);
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

app.get('/api/terms/random', async (req, res) => {
  try {
    const { rows } = await pool.query(
      'SELECT et.id, et.term, et.definition, cd.topic FROM essential_terms et JOIN context_documents cd ON et.document_id = cd.id ORDER BY RANDOM() LIMIT 1'
    );
    res.json(rows[0] || null);
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

app.get('/api/quiz/random', async (req, res) => {
  try {
    const level = req.query.level;
    let query = 'SELECT qq.*, cd.topic FROM quiz_questions qq JOIN context_documents cd ON qq.document_id = cd.id';
    const params = [];
    if (level) {
      query += ' WHERE qq.level = $1';
      params.push(parseInt(level));
    }
    query += ' ORDER BY RANDOM() LIMIT 1';
    const { rows } = await pool.query(query, params);
    res.json(rows[0] || null);
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

app.get('/api/quiz/topic/:id', async (req, res) => {
  try {
    const { rows } = await pool.query(
      'SELECT * FROM quiz_questions WHERE document_id = $1 ORDER BY level',
      [req.params.id]
    );
    res.json(rows);
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

app.get('/api/quiz/similar', async (req, res) => {
  try {
    const q = req.query.q;
    if (!q) return res.status(400).json({ error: 'Missing q' });
    const embedding = await getEmbedding(q);
    const embStr = '[' + embedding.join(',') + ']';
    const { rows } = await pool.query(`
      SELECT qq.*, cd.topic,
             1 - (qq.embedding <=> $1::vector) AS similarity
      FROM quiz_questions qq
      JOIN context_documents cd ON qq.document_id = cd.id
      WHERE qq.embedding IS NOT NULL
      ORDER BY qq.embedding <=> $1::vector
      LIMIT 5
    `, [embStr]);
    res.json(rows);
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

app.get('/api/links/:id', async (req, res) => {
  try {
    const { rows } = await pool.query(`
      SELECT cd.id, cd.topic, cd.tier, cd.tldr, dl.link_context
      FROM document_links dl
      JOIN context_documents cd ON dl.target_id = cd.id
      WHERE dl.source_id = $1
      UNION
      SELECT cd.id, cd.topic, cd.tier, cd.tldr, dl.link_context
      FROM document_links dl
      JOIN context_documents cd ON dl.source_id = cd.id
      WHERE dl.target_id = $1
    `, [req.params.id]);
    res.json(rows);
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

app.post('/api/evaluate-llm', async (req, res) => {
  try {
    const { question, correct_answer, player_answer } = req.body;
    if (!question || !correct_answer || !player_answer) {
      return res.status(400).json({ error: 'Missing fields' });
    }
    const resp = await fetch('https://openrouter.ai/api/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${OPENROUTER_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: 'google/gemini-2.0-flash-001',
        messages: [
          {
            role: 'system',
            content: `You are an electronics tutor evaluating a student's answer. Compare their answer to the correct answer and respond with JSON only:
{"grade": "correct"|"partial"|"incorrect", "feedback": "specific feedback", "misconception": "if detected, null otherwise"}
Be encouraging but accurate. A partial answer shows some understanding but misses key points.`
          },
          {
            role: 'user',
            content: `Question: ${question}\nCorrect answer: ${correct_answer}\nStudent answer: ${player_answer}`
          }
        ],
        temperature: 0.3,
        max_tokens: 300,
      }),
    });
    const data = await resp.json();
    const content = data.choices[0].message.content;
    // Try to parse JSON from the response
    const jsonMatch = content.match(/\{[\s\S]*\}/);
    if (jsonMatch) {
      res.json(JSON.parse(jsonMatch[0]));
    } else {
      res.json({ grade: 'partial', feedback: content, misconception: null });
    }
  } catch (e) {
    // Fallback: cosine similarity
    res.json({ grade: 'partial', feedback: 'Could not evaluate — try again.', misconception: null, error: e.message });
  }
});

// Serve index.html for root
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(PORT, () => {
  console.log(`Circuit Quest server running on port ${PORT}`);
});
