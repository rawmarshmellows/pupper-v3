const express = require('express');
const { Pool } = require('pg');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

const pool = new Pool({ connectionString: process.env.DATABASE_URL });

app.use(express.static(path.join(__dirname, 'public')));
app.use(express.json());

// Helper: get embedding from OpenRouter
async function getEmbedding(text) {
  const resp = await fetch('https://openrouter.ai/api/v1/embeddings', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.OPENROUTER_API_KEY}`,
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

// Health check
app.get('/api/health', async (req, res) => {
  try {
    await pool.query('SELECT 1');
    res.json({ status: 'ok', timestamp: new Date().toISOString() });
  } catch (err) {
    res.status(500).json({ status: 'error', message: err.message });
  }
});

// Stats
app.get('/api/stats', async (req, res) => {
  try {
    const docs = await pool.query('SELECT COUNT(*) as count FROM context_documents');
    const embedded = await pool.query('SELECT COUNT(*) as count FROM context_documents WHERE embedding_tldr IS NOT NULL');
    const terms = await pool.query('SELECT COUNT(*) as count FROM essential_terms');
    const links = await pool.query('SELECT COUNT(*) as count FROM document_links');
    const quiz = await pool.query('SELECT COUNT(*) as count FROM quiz_questions');
    const tiers = await pool.query('SELECT tier, COUNT(*) as count FROM context_documents GROUP BY tier');
    const cats = await pool.query('SELECT category, COUNT(*) as count FROM context_documents GROUP BY category');
    const quizSources = await pool.query('SELECT source, COUNT(*) as count FROM quiz_questions GROUP BY source');

    res.json({
      documents: parseInt(docs.rows[0].count),
      documents_with_embeddings: parseInt(embedded.rows[0].count),
      essential_terms: parseInt(terms.rows[0].count),
      document_links: parseInt(links.rows[0].count),
      quiz_questions: parseInt(quiz.rows[0].count),
      by_tier: Object.fromEntries(tiers.rows.map(r => [r.tier, parseInt(r.count)])),
      by_category: Object.fromEntries(cats.rows.map(r => [r.category, parseInt(r.count)])),
      quiz_by_source: Object.fromEntries(quizSources.rows.map(r => [r.source, parseInt(r.count)])),
    });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// List all topics
app.get('/api/topics', async (req, res) => {
  try {
    const { rows } = await pool.query(
      'SELECT id, topic, tier, category, tldr, definition, created_date FROM context_documents ORDER BY topic'
    );
    res.json(rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Random topic
app.get('/api/topics/random', async (req, res) => {
  try {
    const conditions = [];
    const params = [];
    let idx = 1;
    if (req.query.tier) { conditions.push(`tier = $${idx++}`); params.push(req.query.tier); }
    if (req.query.categories) {
      const cats = req.query.categories.split(',');
      const placeholders = cats.map((_, i) => `$${idx + i}`).join(',');
      conditions.push(`category IN (${placeholders})`);
      params.push(...cats);
      idx += cats.length;
    }
    if (!req.query.categories && req.query.category) {
      conditions.push(`category = $${idx++}`);
      params.push(req.query.category);
    }
    const where = conditions.length > 0 ? 'WHERE ' + conditions.join(' AND ') : '';
    const { rows } = await pool.query(
      `SELECT id, topic, tier, category, tldr, definition, key_insight, summary FROM context_documents ${where} ORDER BY RANDOM() LIMIT 1`,
      params
    );
    if (rows.length === 0) return res.status(404).json({ error: 'No topics found' });
    res.json(rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Cross-domain reference: get key insights from multiple topics
app.get('/api/topics/insights', async (req, res) => {
  try {
    const categories = req.query.categories ? req.query.categories.split(',') : [];
    if (categories.length === 0) return res.json([]);
    const placeholders = categories.map((_, i) => `$${i + 1}`).join(',');
    const { rows } = await pool.query(
      `SELECT id, topic, category, tldr, key_insight, definition
       FROM context_documents WHERE category IN (${placeholders})
       AND (key_insight IS NOT NULL OR tldr IS NOT NULL)
       ORDER BY RANDOM() LIMIT 6`,
      categories
    );
    res.json(rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Get single topic
app.get('/api/topics/:id', async (req, res) => {
  try {
    const { rows } = await pool.query(
      'SELECT * FROM context_documents WHERE id = $1', [req.params.id]
    );
    if (rows.length === 0) return res.status(404).json({ error: 'Not found' });
    const doc = rows[0];
    delete doc.embedding_tldr;
    delete doc.embedding_full;
    delete doc.search_vector;
    res.json(doc);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Semantic search (hybrid: vector + fulltext with RRF)
app.get('/api/search', async (req, res) => {
  try {
    const q = req.query.q;
    if (!q) return res.status(400).json({ error: 'Query parameter q is required' });

    const embedding = await getEmbedding(q);
    const embStr = '[' + embedding.join(',') + ']';

    const catValue = req.query.categories || req.query.category || null;
    let catFilter = '';
    const params = [embStr, q];
    if (catValue) {
      params.push(catValue);
      catFilter = `AND category = $${params.length}`;
    }

    const { rows } = await pool.query(`
      WITH semantic AS (
        SELECT id, ROW_NUMBER() OVER (ORDER BY embedding_tldr <=> $1::vector) AS rank
        FROM context_documents WHERE embedding_tldr IS NOT NULL ${catFilter} LIMIT 20
      ),
      fulltext AS (
        SELECT id, ROW_NUMBER() OVER (ORDER BY ts_rank(search_vector, query) DESC) AS rank
        FROM context_documents, plainto_tsquery('english', $2) query
        WHERE search_vector @@ query ${catFilter} LIMIT 20
      )
      SELECT COALESCE(s.id, f.id) AS id,
             COALESCE(1.0 / (60 + s.rank), 0) + COALESCE(1.0 / (60 + f.rank), 0) AS rrf_score
      FROM semantic s FULL OUTER JOIN fulltext f ON s.id = f.id
      ORDER BY rrf_score DESC LIMIT 10
    `, params);

    if (rows.length === 0) return res.json([]);

    const ids = rows.map(r => r.id);
    const scoreMap = Object.fromEntries(rows.map(r => [r.id, r.rrf_score]));

    const docs = await pool.query(
      'SELECT id, topic, tier, category, tldr, definition, key_insight, summary FROM context_documents WHERE id = ANY($1)',
      [ids]
    );

    const results = docs.rows.map(d => ({ ...d, score: scoreMap[d.id] }));
    results.sort((a, b) => b.score - a.score);
    res.json(results);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Similar documents
app.get('/api/similar/:id', async (req, res) => {
  try {
    const { rows } = await pool.query(`
      SELECT c2.id, c2.topic, c2.tier, c2.category, c2.tldr, c2.definition, c2.key_insight,
             1 - (c1.embedding_tldr <=> c2.embedding_tldr) AS similarity
      FROM context_documents c1, context_documents c2
      WHERE c1.id = $1 AND c2.id != $1 AND c1.embedding_tldr IS NOT NULL AND c2.embedding_tldr IS NOT NULL
      ORDER BY c1.embedding_tldr <=> c2.embedding_tldr
      LIMIT 5
    `, [req.params.id]);
    res.json(rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// All terms
app.get('/api/terms', async (req, res) => {
  try {
    const catFilter = req.query.category
      ? 'WHERE cd.category = $1' : '';
    const params = req.query.category ? [req.query.category] : [];
    const { rows } = await pool.query(
      `SELECT et.id, et.term, et.definition, cd.topic as document_topic, cd.category
       FROM essential_terms et JOIN context_documents cd ON et.document_id = cd.id
       ${catFilter} ORDER BY et.term`,
      params
    );
    res.json(rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Random term
app.get('/api/terms/random', async (req, res) => {
  try {
    let catFilter = '';
    let params = [];
    if (req.query.categories) {
      const cats = req.query.categories.split(',');
      const placeholders = cats.map((_, i) => `$${i + 1}`).join(',');
      catFilter = `WHERE cd.category IN (${placeholders})`;
      params = cats;
    }
    const { rows } = await pool.query(
      `SELECT et.id, et.term, et.definition, cd.topic as document_topic, cd.category, cd.id as document_id,
              cd.key_insight, cd.tldr
       FROM essential_terms et JOIN context_documents cd ON et.document_id = cd.id
       ${catFilter} ORDER BY RANDOM() LIMIT 1`,
      params
    );
    if (rows.length === 0) return res.status(404).json({ error: 'No terms found' });
    res.json(rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Random quiz question
app.get('/api/quiz/random', async (req, res) => {
  try {
    const conditions = [];
    const params = [];
    let idx = 1;
    if (req.query.level) { conditions.push(`qq.level = $${idx++}`); params.push(parseInt(req.query.level)); }
    if (req.query.categories) {
      const cats = req.query.categories.split(',');
      const placeholders = cats.map((_, i) => `$${idx + i}`).join(',');
      conditions.push(`cd.category IN (${placeholders})`);
      params.push(...cats);
      idx += cats.length;
    }
    const where = conditions.length > 0 ? 'WHERE ' + conditions.join(' AND ') : '';
    const { rows } = await pool.query(
      `SELECT qq.id, qq.question, qq.answer, qq.level, qq.source, cd.topic as document_topic, cd.category, cd.id as document_id,
              cd.key_insight, cd.tldr, cd.definition
       FROM quiz_questions qq JOIN context_documents cd ON qq.document_id = cd.id
       ${where} ORDER BY RANDOM() LIMIT 1`,
      params
    );
    if (rows.length === 0) return res.status(404).json({ error: 'No quiz questions found' });
    res.json(rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Quiz questions for a topic
app.get('/api/quiz/topic/:id', async (req, res) => {
  try {
    const { rows } = await pool.query(
      'SELECT id, question, answer, level, source FROM quiz_questions WHERE document_id = $1 ORDER BY level',
      [req.params.id]
    );
    res.json(rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Semantically similar quiz questions
app.get('/api/quiz/similar', async (req, res) => {
  try {
    const q = req.query.q;
    if (!q) return res.status(400).json({ error: 'Query parameter q is required' });

    const embedding = await getEmbedding(q);
    const embStr = '[' + embedding.join(',') + ']';

    const { rows } = await pool.query(`
      SELECT qq.id, qq.question, qq.answer, qq.level, cd.topic as document_topic,
             1 - (qq.embedding <=> $1::vector) AS similarity
      FROM quiz_questions qq JOIN context_documents cd ON qq.document_id = cd.id
      WHERE qq.embedding IS NOT NULL
      ORDER BY qq.embedding <=> $1::vector
      LIMIT 5
    `, [embStr]);
    res.json(rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Evaluate answer using semantic similarity
app.post('/api/evaluate', async (req, res) => {
  try {
    const { playerAnswer, correctAnswer } = req.body;
    if (!playerAnswer || !correctAnswer) {
      return res.status(400).json({ error: 'playerAnswer and correctAnswer are required' });
    }

    const [playerEmb, correctEmb] = await Promise.all([
      getEmbedding(playerAnswer),
      getEmbedding(correctAnswer),
    ]);

    let dotProduct = 0, normA = 0, normB = 0;
    for (let i = 0; i < playerEmb.length; i++) {
      dotProduct += playerEmb[i] * correctEmb[i];
      normA += playerEmb[i] * playerEmb[i];
      normB += correctEmb[i] * correctEmb[i];
    }
    const similarity = dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));

    let grade;
    if (similarity >= 0.75) grade = 'correct';
    else if (similarity >= 0.55) grade = 'partial';
    else grade = 'incorrect';

    res.json({ similarity: Math.round(similarity * 1000) / 1000, grade });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Misconception matching: compare player's wrong answer against known misconceptions
app.post('/api/misconception-match', async (req, res) => {
  try {
    const { playerAnswer, misconceptions } = req.body;
    if (!playerAnswer || !misconceptions || !Array.isArray(misconceptions)) {
      return res.status(400).json({ error: 'playerAnswer and misconceptions array are required' });
    }

    const playerEmb = await getEmbedding(playerAnswer);
    const miscTexts = misconceptions.map(m => m.text);

    // Batch embed all misconceptions
    const resp = await fetch('https://openrouter.ai/api/v1/embeddings', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${process.env.OPENROUTER_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: 'openai/text-embedding-3-small',
        input: miscTexts.slice(0, 20),
        dimensions: 512,
      }),
    });
    const data = await resp.json();
    const miscEmbeddings = data.data.sort((a, b) => a.index - b.index).map(d => d.embedding);

    // Find best matching misconception
    let bestSim = -1, bestIdx = -1;
    for (let m = 0; m < miscEmbeddings.length; m++) {
      let dot = 0, nA = 0, nB = 0;
      for (let i = 0; i < playerEmb.length; i++) {
        dot += playerEmb[i] * miscEmbeddings[m][i];
        nA += playerEmb[i] * playerEmb[i];
        nB += miscEmbeddings[m][i] * miscEmbeddings[m][i];
      }
      const sim = dot / (Math.sqrt(nA) * Math.sqrt(nB));
      if (sim > bestSim) { bestSim = sim; bestIdx = m; }
    }

    // Threshold: 0.60 similarity means the player's answer aligns with this misconception
    if (bestSim >= 0.60 && bestIdx >= 0) {
      res.json({
        matched: true,
        similarity: Math.round(bestSim * 1000) / 1000,
        misconception: misconceptions[bestIdx],
      });
    } else {
      res.json({ matched: false, similarity: Math.round(bestSim * 1000) / 1000 });
    }
  } catch (err) {
    // If misconception matching fails, just return no match
    res.json({ matched: false, similarity: 0 });
  }
});

// Document links (graph neighbors)
app.get('/api/links/:id', async (req, res) => {
  try {
    const { rows } = await pool.query(`
      SELECT cd.id, cd.topic, cd.tier, cd.tldr, cd.definition, cd.key_insight, dl.link_context
      FROM document_links dl JOIN context_documents cd ON dl.target_id = cd.id
      WHERE dl.source_id = $1
      UNION
      SELECT cd.id, cd.topic, cd.tier, cd.tldr, cd.definition, cd.key_insight, dl.link_context
      FROM document_links dl JOIN context_documents cd ON dl.source_id = cd.id
      WHERE dl.target_id = $1
    `, [req.params.id]);
    res.json(rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Distractors: prefer linked docs, fall back to similar
app.get('/api/distractors/:id', async (req, res) => {
  try {
    const count = parseInt(req.query.count) || 3;
    const linked = await pool.query(`
      SELECT * FROM (
        SELECT cd.id, cd.topic, cd.tldr, cd.definition, cd.key_insight
        FROM document_links dl JOIN context_documents cd ON dl.target_id = cd.id
        WHERE dl.source_id = $1 AND cd.id != $1
        UNION
        SELECT cd.id, cd.topic, cd.tldr, cd.definition, cd.key_insight
        FROM document_links dl JOIN context_documents cd ON dl.source_id = cd.id
        WHERE dl.target_id = $1 AND cd.id != $1
      ) linked_docs ORDER BY RANDOM() LIMIT $2
    `, [req.params.id, count]);

    let distractors = linked.rows;

    if (distractors.length < count) {
      const remaining = count - distractors.length;
      const existingIds = [parseInt(req.params.id), ...distractors.map(d => d.id)];
      const similar = await pool.query(`
        SELECT c2.id, c2.topic, c2.tldr, c2.definition, c2.key_insight
        FROM context_documents c1, context_documents c2
        WHERE c1.id = $1 AND c2.id != ALL($2::int[])
          AND c1.embedding_tldr IS NOT NULL AND c2.embedding_tldr IS NOT NULL
        ORDER BY c1.embedding_tldr <=> c2.embedding_tldr
        LIMIT $3
      `, [req.params.id, existingIds, remaining]);
      distractors = distractors.concat(similar.rows);
    }

    res.json(distractors);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Serve index.html
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Knowledge Quest server running on port ${PORT}`);
});
