#!/usr/bin/env python3
"""Import Obsidian markdown notes into PostgreSQL with pgvector embeddings."""

import os
import re
import sys
import time
import json
import yaml
import logging
import requests
import psycopg2
from psycopg2.extras import execute_values
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger(__name__)

DATABASE_URL = os.environ["DATABASE_URL"]
OPENROUTER_API_KEY = os.environ["OPENROUTER_API_KEY"]
NOTES_PATH = "/notes"
EMBEDDING_MODEL = "openai/text-embedding-3-small"
EMBEDDING_DIM = 512
BATCH_SIZE = 50  # texts per embedding request

# Stats
stats = {"docs": 0, "terms": 0, "links": 0, "quiz": 0, "embeddings": 0, "by_tier": {}}


def get_connection():
    """Get database connection with retries."""
    for attempt in range(10):
        try:
            conn = psycopg2.connect(DATABASE_URL)
            conn.autocommit = False
            return conn
        except psycopg2.OperationalError:
            log.warning(f"DB not ready, retry {attempt+1}/10...")
            time.sleep(2)
    raise Exception("Could not connect to database")


def get_embeddings(texts, retries=3):
    """Get embeddings from OpenRouter API with batching and retry."""
    if not texts:
        return []

    results = []
    for i in range(0, len(texts), BATCH_SIZE):
        batch = texts[i:i+BATCH_SIZE]
        # Truncate long texts to avoid token limits
        batch = [t[:8000] if len(t) > 8000 else t for t in batch]

        for attempt in range(retries):
            try:
                resp = requests.post(
                    "https://openrouter.ai/api/v1/embeddings",
                    headers={
                        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": EMBEDDING_MODEL,
                        "input": batch,
                        "dimensions": EMBEDDING_DIM,
                    },
                    timeout=60,
                )
                resp.raise_for_status()
                data = resp.json()
                embeddings = [item["embedding"] for item in sorted(data["data"], key=lambda x: x["index"])]
                results.extend(embeddings)
                stats["embeddings"] += len(embeddings)
                log.info(f"Embedded batch {i//BATCH_SIZE + 1}: {len(embeddings)} texts")
                break
            except Exception as e:
                log.warning(f"Embedding attempt {attempt+1} failed: {e}")
                if attempt < retries - 1:
                    time.sleep(2 ** (attempt + 1))
                else:
                    log.error(f"Failed to embed batch after {retries} attempts, using zeros")
                    results.extend([[0.0] * EMBEDDING_DIM] * len(batch))

    return results


def parse_frontmatter(content):
    """Extract YAML frontmatter from markdown."""
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if match:
        try:
            fm = yaml.safe_load(match.group(1))
            body = content[match.end():]
            return fm or {}, body
        except yaml.YAMLError:
            return {}, content
    return {}, content


def extract_tldr(body):
    """Extract TL;DR from note body."""
    match = re.search(r'>\s*\*\*TL;DR[:\s]*\*\*\s*(.*?)(?:\n\n|\n>|\Z)', body, re.DOTALL)
    if match:
        return re.sub(r'\s+', ' ', match.group(1).strip())
    return None


def extract_definition(body):
    """Extract definition from note."""
    match = re.search(r'\*\*Definition[:\s]*\*\*\s*(.*?)(?:\n\n|\Z)', body, re.DOTALL)
    if match:
        return re.sub(r'\s+', ' ', match.group(1).strip())
    return None


def extract_key_insight(body):
    """Extract key insight from note."""
    match = re.search(r'\*\*Key [Ii]nsight[:\s]*\*\*\s*(.*?)(?:\n\n|\Z)', body, re.DOTALL)
    if match:
        return re.sub(r'\s+', ' ', match.group(1).strip())
    return None


def extract_situation(body):
    """Extract situation/use case from note."""
    match = re.search(r'\*\*Situation[:\s]*\*\*\s*(.*?)(?:\n\n|\Z)', body, re.DOTALL)
    if match:
        return re.sub(r'\s+', ' ', match.group(1).strip())
    return None


def extract_essential_terms(body):
    """Extract essential terms table from note."""
    terms = []
    # Match markdown table rows after "Essential Terms" header
    in_terms = False
    for line in body.split('\n'):
        if re.search(r'essential\s+terms', line, re.IGNORECASE):
            in_terms = True
            continue
        if in_terms:
            if line.startswith('|') and '---' not in line:
                cells = [c.strip() for c in line.split('|')[1:-1]]
                if len(cells) >= 2 and cells[0] and cells[1]:
                    term_name = re.sub(r'\*\*|\[\[.*?\|?(.*?)\]\]', r'\1', cells[0]).strip()
                    term_def = re.sub(r'\*\*|\[\[.*?\|?(.*?)\]\]', r'\1', cells[1]).strip()
                    if term_name.lower() not in ('term', 'name', ''):
                        terms.append({"term": term_name, "definition": term_def})
            elif not line.startswith('|') and line.strip() and not line.startswith('#'):
                in_terms = False
    return terms


def extract_wiki_links(body):
    """Extract wiki-links [[target]] or [[target|display]]."""
    links = []
    for match in re.finditer(r'\[\[(.*?)(?:\|.*?)?\]\]', body):
        target = match.group(1).strip()
        # Normalize: remove tier prefix if present
        target = re.sub(r'^(micro-context|quick-context|small-context)/', '', target)
        links.append(target)
    return list(set(links))


def extract_quiz_questions(body):
    """Extract Q&A pairs from 'Test Your Understanding' sections.

    Actual format in notes:
      **Q1:** question text
      <details>
      <summary>Answer</summary>
      **answer text**
      </details>
    """
    questions = []

    # Find the Test Your Understanding section (may be inside a <details> or under ##)
    # Pattern: look for "Test Your Understanding" anywhere, then parse Q&A after it
    tyu_match = re.search(r'Test Your Understanding', body, re.IGNORECASE)
    if not tyu_match:
        return questions

    qa_text = body[tyu_match.end():]

    # Pattern: **Q1:** or **Q2:** etc. followed by question text,
    # then <details><summary>Answer</summary> answer text </details>
    pattern = re.compile(
        r'\*\*Q\d+[:\s]*\*\*\s*(.*?)\s*'       # Question: **Q1:** question text
        r'<details>\s*'                           # Opening details tag
        r'<summary>\s*Answer\s*</summary>\s*'     # Summary with "Answer"
        r'(.*?)\s*'                               # Answer content
        r'</details>',                            # Closing details tag
        re.DOTALL | re.IGNORECASE
    )

    for match in pattern.finditer(qa_text):
        q = match.group(1).strip()
        a = match.group(2).strip()
        # Clean up markdown formatting
        q = re.sub(r'\s+', ' ', q)
        a = re.sub(r'<[^>]+>', '', a)  # Remove HTML tags
        a = re.sub(r'\s+', ' ', a).strip()
        # Remove leading ** from answers
        a = re.sub(r'^\*\*', '', a)
        a = re.sub(r'\*\*$', '', a)
        a = a.strip()
        if q and a:
            questions.append({"question": q, "answer": a, "level": estimate_bloom_level(q)})

    return questions


def estimate_bloom_level(question):
    """Estimate Bloom's taxonomy level from question text."""
    q = question.lower()
    if any(w in q for w in ['define', 'list', 'name', 'what is', 'identify']):
        return 1  # Remember
    if any(w in q for w in ['explain', 'describe', 'summarize', 'why does', 'how does']):
        return 2  # Understand
    if any(w in q for w in ['calculate', 'apply', 'use', 'solve', 'demonstrate']):
        return 3  # Apply
    if any(w in q for w in ['compare', 'contrast', 'analyze', 'differentiate', 'examine']):
        return 4  # Analyze
    if any(w in q for w in ['evaluate', 'judge', 'assess', 'justify', 'which is better']):
        return 5  # Evaluate
    if any(w in q for w in ['design', 'create', 'propose', 'construct', 'develop']):
        return 6  # Create
    return 2  # Default to Understand


def detect_tier(file_path):
    """Detect tier from parent folder name."""
    parts = Path(file_path).parts
    for part in parts:
        if 'micro' in part.lower():
            return 'micro'
        if 'small' in part.lower():
            return 'small'
        if 'quick' in part.lower():
            return 'quick'
    return 'quick'  # default


def strip_markdown_formatting(text):
    """Remove markdown formatting but keep content."""
    text = re.sub(r'^---\s*\n.*?\n---\s*\n', '', text, flags=re.DOTALL)  # frontmatter
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)  # code blocks
    text = re.sub(r'<details>.*?</details>', '', text, flags=re.DOTALL)  # details
    text = re.sub(r'<[^>]+>', '', text)  # HTML tags
    text = re.sub(r'\[\[(.*?)(?:\|(.+?))?\]\]', lambda m: m.group(2) or m.group(1), text)  # wiki links
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)  # images
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)  # links
    text = re.sub(r'[*_]{1,3}', '', text)  # bold/italic
    text = re.sub(r'#{1,6}\s+', '', text)  # headers
    text = re.sub(r'^\s*[-*+]\s', '', text, flags=re.MULTILINE)  # list markers
    text = re.sub(r'^\s*>\s?', '', text, flags=re.MULTILINE)  # blockquotes
    text = re.sub(r'\n{3,}', '\n\n', text)  # excess newlines
    return text.strip()


def import_notes():
    """Main import function."""
    conn = get_connection()
    cur = conn.cursor()

    log.info(f"Scanning notes from {NOTES_PATH}")

    # Collect all markdown files
    md_files = []
    for root, dirs, files in os.walk(NOTES_PATH):
        for f in files:
            if f.endswith('.md') and not f.startswith('.'):
                md_files.append(os.path.join(root, f))

    log.info(f"Found {len(md_files)} markdown files")

    # Phase 1: Parse and insert documents
    doc_records = []
    all_terms = []
    all_links = []
    all_quiz = []

    for fpath in sorted(md_files):
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        fm, body = parse_frontmatter(content)
        tier = detect_tier(fpath)
        topic = fm.get('topic', fm.get('term', Path(fpath).stem.replace('-', ' ').title()))
        created = fm.get('created')

        tldr = extract_tldr(body)
        definition = extract_definition(body)
        key_insight = extract_key_insight(body)
        situation = extract_situation(body)
        full_content = strip_markdown_formatting(content)

        # Extract related data
        terms = extract_essential_terms(body)
        links = extract_wiki_links(body)
        quiz = extract_quiz_questions(body)

        rel_path = os.path.relpath(fpath, NOTES_PATH)

        doc_records.append({
            "file_path": rel_path,
            "tier": tier,
            "topic": topic,
            "created_date": created,
            "tldr": tldr,
            "definition": definition,
            "key_insight": key_insight,
            "situation": situation,
            "full_content": full_content,
        })

        all_terms.append({"file_path": rel_path, "terms": terms})
        all_links.append({"file_path": rel_path, "links": links})
        all_quiz.append({"file_path": rel_path, "questions": quiz})

        stats["by_tier"][tier] = stats["by_tier"].get(tier, 0) + 1

    # Insert documents
    log.info("Inserting documents...")
    for doc in doc_records:
        cur.execute("""
            INSERT INTO context_documents (file_path, tier, topic, created_date, tldr, definition, key_insight, situation, full_content)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (file_path) DO UPDATE SET
                tier = EXCLUDED.tier,
                topic = EXCLUDED.topic,
                created_date = EXCLUDED.created_date,
                tldr = EXCLUDED.tldr,
                definition = EXCLUDED.definition,
                key_insight = EXCLUDED.key_insight,
                situation = EXCLUDED.situation,
                full_content = EXCLUDED.full_content
        """, (doc["file_path"], doc["tier"], doc["topic"], doc["created_date"],
              doc["tldr"], doc["definition"], doc["key_insight"], doc["situation"],
              doc["full_content"]))
        stats["docs"] += 1

    conn.commit()
    log.info(f"Inserted {stats['docs']} documents")

    # Build file_path -> id mapping
    cur.execute("SELECT id, file_path FROM context_documents")
    path_to_id = {row[1]: row[0] for row in cur.fetchall()}

    # Insert essential terms
    log.info("Inserting essential terms...")
    for item in all_terms:
        doc_id = path_to_id.get(item["file_path"])
        if not doc_id:
            continue
        for t in item["terms"]:
            cur.execute("""
                INSERT INTO essential_terms (document_id, term, definition)
                VALUES (%s, %s, %s)
            """, (doc_id, t["term"], t["definition"]))
            stats["terms"] += 1
    conn.commit()
    log.info(f"Inserted {stats['terms']} essential terms")

    # Insert document links
    log.info("Inserting document links...")
    # Build a topic-name -> id lookup (normalized)
    topic_to_id = {}
    cur.execute("SELECT id, file_path, topic FROM context_documents")
    for row in cur.fetchall():
        doc_id, fp, topic = row
        # Index by filename stem (without extension and tier prefix)
        stem = Path(fp).stem
        topic_to_id[stem.lower()] = doc_id
        topic_to_id[topic.lower()] = doc_id

    for item in all_links:
        source_id = path_to_id.get(item["file_path"])
        if not source_id:
            continue
        for link_target in item["links"]:
            # Try to resolve link target to a document id
            normalized = link_target.lower().replace(' ', '-')
            target_id = topic_to_id.get(normalized) or topic_to_id.get(link_target.lower())
            if target_id and target_id != source_id:
                try:
                    cur.execute("""
                        INSERT INTO document_links (source_id, target_id, link_context)
                        VALUES (%s, %s, %s)
                        ON CONFLICT DO NOTHING
                    """, (source_id, target_id, link_target))
                    stats["links"] += 1
                except psycopg2.errors.ForeignKeyViolation:
                    conn.rollback()
    conn.commit()
    log.info(f"Inserted {stats['links']} document links")

    # Insert quiz questions
    log.info("Inserting quiz questions...")
    for item in all_quiz:
        doc_id = path_to_id.get(item["file_path"])
        if not doc_id:
            continue
        for q in item["questions"]:
            cur.execute("""
                INSERT INTO quiz_questions (document_id, level, question, answer)
                VALUES (%s, %s, %s, %s)
            """, (doc_id, q["level"], q["question"], q["answer"]))
            stats["quiz"] += 1
    conn.commit()
    log.info(f"Inserted {stats['quiz']} quiz questions")

    # Phase 2: Generate embeddings
    log.info("Generating embeddings for documents...")

    # Embed TLDRs (or topic + definition as fallback)
    cur.execute("SELECT id, topic, tldr, definition, key_insight FROM context_documents ORDER BY id")
    docs = cur.fetchall()

    tldr_texts = []
    tldr_ids = []
    full_texts = []
    full_ids = []

    for doc_id, topic, tldr, definition, key_insight in docs:
        # For TLDR embedding: use tldr, or fallback to definition, or topic
        text = tldr or definition or key_insight or topic
        tldr_texts.append(f"{topic}: {text}")
        tldr_ids.append(doc_id)

    # Get full content for full embedding
    cur.execute("SELECT id, full_content FROM context_documents ORDER BY id")
    for doc_id, full_content in cur.fetchall():
        full_texts.append(full_content[:4000])  # truncate for embedding
        full_ids.append(doc_id)

    # Batch embed TLDRs
    log.info(f"Embedding {len(tldr_texts)} TLDR texts...")
    tldr_embeddings = get_embeddings(tldr_texts)
    for doc_id, emb in zip(tldr_ids, tldr_embeddings):
        cur.execute("UPDATE context_documents SET embedding_tldr = %s WHERE id = %s",
                    (json.dumps(emb), doc_id))
    conn.commit()

    # Batch embed full content
    log.info(f"Embedding {len(full_texts)} full content texts...")
    full_embeddings = get_embeddings(full_texts)
    for doc_id, emb in zip(full_ids, full_embeddings):
        cur.execute("UPDATE context_documents SET embedding_full = %s WHERE id = %s",
                    (json.dumps(emb), doc_id))
    conn.commit()

    # Embed essential terms
    cur.execute("SELECT id, term, definition FROM essential_terms ORDER BY id")
    term_rows = cur.fetchall()
    if term_rows:
        log.info(f"Embedding {len(term_rows)} essential terms...")
        term_texts = [f"{row[1]}: {row[2]}" for row in term_rows]
        term_embeddings = get_embeddings(term_texts)
        for (term_id, _, _), emb in zip(term_rows, term_embeddings):
            cur.execute("UPDATE essential_terms SET embedding = %s WHERE id = %s",
                        (json.dumps(emb), term_id))
        conn.commit()

    # Embed quiz questions
    cur.execute("SELECT id, question, answer FROM quiz_questions ORDER BY id")
    quiz_rows = cur.fetchall()
    if quiz_rows:
        log.info(f"Embedding {len(quiz_rows)} quiz questions...")
        quiz_texts = [f"{row[1]} {row[2]}" for row in quiz_rows]
        quiz_embeddings = get_embeddings(quiz_texts)
        for (quiz_id, _, _), emb in zip(quiz_rows, quiz_embeddings):
            cur.execute("UPDATE quiz_questions SET embedding = %s WHERE id = %s",
                        (json.dumps(emb), quiz_id))
        conn.commit()

    # Final stats
    cur.execute("SELECT COUNT(*) FROM context_documents WHERE embedding_tldr IS NOT NULL")
    embedded_count = cur.fetchone()[0]

    log.info("=" * 60)
    log.info("IMPORT COMPLETE")
    log.info(f"  Documents: {stats['docs']} (by tier: {stats['by_tier']})")
    log.info(f"  Essential terms: {stats['terms']}")
    log.info(f"  Document links: {stats['links']}")
    log.info(f"  Quiz questions: {stats['quiz']}")
    log.info(f"  Embeddings generated: {stats['embeddings']}")
    log.info(f"  Documents with embeddings: {embedded_count}/{stats['docs']}")
    log.info("=" * 60)

    cur.close()
    conn.close()


if __name__ == "__main__":
    import_notes()
