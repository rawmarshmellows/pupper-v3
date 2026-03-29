#!/usr/bin/env python3
"""Import Obsidian markdown notes into PostgreSQL with pgvector embeddings."""

import os
import re
import sys
import time
import json
import yaml
import logging
import psycopg2
import psycopg2.extras
import requests
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger(__name__)

DATABASE_URL = os.environ["DATABASE_URL"]
OPENROUTER_API_KEY = os.environ["OPENROUTER_API_KEY"]
NOTES_PATH = "/notes"
EMBEDDING_MODEL = "openai/text-embedding-3-small"
EMBEDDING_DIM = 512
BATCH_SIZE = 50  # texts per embedding request

# ── helpers ──────────────────────────────────────────────────────────

def get_embedding_batch(texts, retries=3):
    """Get embeddings for a batch of texts via OpenRouter."""
    url = "https://openrouter.ai/api/v1/embeddings"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    # Filter empty texts
    clean_texts = [t[:8000] if t else "empty" for t in texts]
    payload = {
        "model": EMBEDDING_MODEL,
        "input": clean_texts,
        "dimensions": EMBEDDING_DIM,
    }
    for attempt in range(retries):
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=60)
            resp.raise_for_status()
            data = resp.json()
            embeddings = [item["embedding"] for item in sorted(data["data"], key=lambda x: x["index"])]
            return embeddings
        except Exception as e:
            log.warning(f"Embedding attempt {attempt+1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(2 ** (attempt + 1))
            else:
                raise


def parse_frontmatter(content):
    """Extract YAML frontmatter from markdown."""
    if not content.startswith("---"):
        return {}, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    try:
        meta = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        meta = {}
    body = parts[2].strip()
    return meta, body


def detect_tier(file_path):
    """Detect tier from parent folder name."""
    parent = Path(file_path).parent.name
    if "micro" in parent:
        return "micro"
    elif "small" in parent:
        return "small"
    elif "quick" in parent:
        return "quick"
    return "quick"


def extract_tldr(body):
    """Extract TL;DR section."""
    match = re.search(r'(?:##?\s*)?(?:TL;?DR|TLDR|tl;?dr)[:\s]*\n?(.*?)(?=\n##|\n---|\Z)', body, re.DOTALL)
    if match:
        return match.group(1).strip()[:500]
    # Try first paragraph as fallback
    paragraphs = [p.strip() for p in body.split('\n\n') if p.strip() and not p.strip().startswith('#')]
    return paragraphs[0][:500] if paragraphs else None


def extract_definition(body):
    """Extract definition section."""
    match = re.search(r'(?:##?\s*)?(?:Definition|What is)[:\s]*\n?(.*?)(?=\n##|\n---|\Z)', body, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()[:500]
    return None


def extract_key_insight(body):
    """Extract key insight section."""
    match = re.search(r'(?:##?\s*)?(?:Key Insight|Core Insight|Main Idea)[:\s]*\n?(.*?)(?=\n##|\n---|\Z)', body, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()[:500]
    return None


def extract_situation(body):
    """Extract situation/context section."""
    match = re.search(r'(?:##?\s*)?(?:Situation|When|Context|Use Case)[:\s]*\n?(.*?)(?=\n##|\n---|\Z)', body, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()[:500]
    return None


def extract_essential_terms(body):
    """Extract essential terms from markdown tables."""
    terms = []
    # Match markdown table rows: | term | definition |
    table_pattern = re.compile(r'(?:##?\s*)?(?:Essential Terms|Key Terms|Vocabulary|Terms)[:\s]*\n(.*?)(?=\n##|\n---|\Z)', re.DOTALL | re.IGNORECASE)
    table_match = table_pattern.search(body)
    if table_match:
        table_text = table_match.group(1)
        rows = re.findall(r'\|\s*\*?\*?([^|*]+?)\*?\*?\s*\|\s*([^|]+?)\s*\|', table_text)
        for term, defn in rows:
            term = term.strip()
            defn = defn.strip()
            if term and defn and term.lower() not in ('term', 'concept', 'name', '---', ':-'):
                if not re.match(r'^[-:]+$', term):
                    terms.append({"term": term, "definition": defn})
    return terms


def extract_quiz_questions(body):
    """Extract quiz questions from Test Your Understanding sections."""
    questions = []
    quiz_pattern = re.compile(
        r'(?:##?\s*)?(?:Test Your Understanding|Quiz|Practice|Check Your Understanding|Questions)[:\s]*\n(.*?)(?=\n##[^#]|\Z)',
        re.DOTALL | re.IGNORECASE
    )
    quiz_match = quiz_pattern.search(body)
    if quiz_match:
        quiz_text = quiz_match.group(1)
        # Pattern 1: numbered Q&A with details
        qa_pairs = re.findall(
            r'(?:^|\n)\s*\d+\.\s*\*?\*?(?:Q(?:uestion)?)?:?\s*\*?\*?\s*(.*?)(?:\n\s*(?:>|<details|A(?:nswer)?:?\s*)(.*?)(?=\n\s*\d+\.|\Z))',
            quiz_text, re.DOTALL
        )
        for q, a in qa_pairs:
            q = re.sub(r'<[^>]+>', '', q).strip()
            a = re.sub(r'<[^>]+>', '', a).strip()
            if q and a:
                level = estimate_blooms_level(q)
                questions.append({"question": q, "answer": a, "level": level})

        # Pattern 2: bold Q then answer
        if not questions:
            qa_pairs = re.findall(
                r'\*\*(.+?)\*\*\s*\n\s*(.*?)(?=\n\s*\*\*|\Z)',
                quiz_text, re.DOTALL
            )
            for q, a in qa_pairs:
                q = q.strip()
                a = a.strip()
                if q and a and len(a) > 10:
                    level = estimate_blooms_level(q)
                    questions.append({"question": q, "answer": a, "level": level})

    return questions


def estimate_blooms_level(question):
    """Estimate Bloom's taxonomy level from question text."""
    q = question.lower()
    if any(w in q for w in ['define', 'list', 'name', 'what is', 'identify', 'recall']):
        return 1  # Remember
    elif any(w in q for w in ['explain', 'describe', 'summarize', 'compare', 'interpret', 'why does', 'how does']):
        return 2  # Understand
    elif any(w in q for w in ['calculate', 'apply', 'use', 'solve', 'compute', 'determine', 'implement']):
        return 3  # Apply
    elif any(w in q for w in ['analyze', 'differentiate', 'distinguish', 'examine', 'break down', 'what would happen']):
        return 4  # Analyze
    elif any(w in q for w in ['evaluate', 'justify', 'argue', 'which is better', 'assess', 'critique', 'judge']):
        return 5  # Evaluate
    return 3  # Default to Apply


def extract_wiki_links(body):
    """Extract wiki-style links [[target]]."""
    return re.findall(r'\[\[([^\]]+)\]\]', body)


def strip_markdown(text):
    """Remove markdown formatting for plain text storage."""
    text = re.sub(r'<[^>]+>', '', text)       # HTML tags
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)  # images
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)  # links
    return text


# ── main import ──────────────────────────────────────────────────────

def main():
    log.info("Starting note import...")
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = False
    cur = conn.cursor()

    notes_path = Path(NOTES_PATH)
    if not notes_path.exists():
        log.error(f"Notes path does not exist: {notes_path}")
        sys.exit(1)

    md_files = sorted(notes_path.rglob("*.md"))
    log.info(f"Found {len(md_files)} markdown files")

    stats = {
        "docs_imported": 0,
        "terms_imported": 0,
        "links_found": 0,
        "quiz_questions": 0,
        "embeddings_generated": 0,
        "by_tier": {"micro": 0, "quick": 0, "small": 0},
    }

    # ── Phase 1: Import documents ────────────────────────────────
    doc_ids = {}  # file_path -> id
    all_docs = []

    for md_file in md_files:
        rel_path = str(md_file.relative_to(notes_path))
        content = md_file.read_text(encoding="utf-8", errors="replace")
        meta, body = parse_frontmatter(content)
        tier = detect_tier(str(md_file))
        topic = meta.get("topic", md_file.stem.replace("-", " ").replace("_", " ").title())
        created_date = meta.get("created", meta.get("date", None))
        tldr = extract_tldr(body)
        definition = extract_definition(body)
        key_insight = extract_key_insight(body)
        situation = extract_situation(body)
        full_content = strip_markdown(body)[:50000]

        if not full_content.strip():
            log.warning(f"Skipping empty file: {rel_path}")
            continue

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
            RETURNING id
        """, (rel_path, tier, topic, created_date, tldr, definition, key_insight, situation, full_content))
        doc_id = cur.fetchone()[0]
        doc_ids[rel_path] = doc_id
        stats["docs_imported"] += 1
        stats["by_tier"][tier] += 1

        all_docs.append({
            "id": doc_id,
            "rel_path": rel_path,
            "tldr": tldr or "",
            "full_content": full_content[:4000],
            "terms": extract_essential_terms(body),
            "questions": extract_quiz_questions(body),
            "wiki_links": extract_wiki_links(body),
        })

    conn.commit()
    log.info(f"Imported {stats['docs_imported']} documents: {stats['by_tier']}")

    # ── Phase 2: Import terms ────────────────────────────────────
    for doc in all_docs:
        for term_data in doc["terms"]:
            cur.execute("""
                INSERT INTO essential_terms (document_id, term, definition)
                VALUES (%s, %s, %s)
                RETURNING id
            """, (doc["id"], term_data["term"], term_data["definition"]))
            stats["terms_imported"] += 1
    conn.commit()
    log.info(f"Imported {stats['terms_imported']} essential terms")

    # ── Phase 3: Import quiz questions ───────────────────────────
    for doc in all_docs:
        for qq in doc["questions"]:
            cur.execute("""
                INSERT INTO quiz_questions (document_id, level, question, answer)
                VALUES (%s, %s, %s, %s)
            """, (doc["id"], qq["level"], qq["question"], qq["answer"]))
            stats["quiz_questions"] += 1
    conn.commit()
    log.info(f"Imported {stats['quiz_questions']} quiz questions")

    # ── Phase 4: Import wiki links ───────────────────────────────
    # Build a lookup from topic slug to doc id
    slug_to_id = {}
    for rel_path, doc_id in doc_ids.items():
        slug = Path(rel_path).stem.lower()
        slug_to_id[slug] = doc_id
        # Also store with tier prefix
        parts = rel_path.split("/")
        if len(parts) >= 2:
            full_slug = f"{parts[0]}/{Path(rel_path).stem}".lower()
            slug_to_id[full_slug] = doc_id

    for doc in all_docs:
        source_id = doc["id"]
        for link_target in doc["wiki_links"]:
            link_slug = link_target.lower().replace(" ", "-")
            # Try exact match, then stem only
            target_id = slug_to_id.get(link_slug) or slug_to_id.get(link_slug.split("/")[-1])
            if target_id and target_id != source_id:
                try:
                    cur.execute("""
                        INSERT INTO document_links (source_id, target_id, link_context)
                        VALUES (%s, %s, %s)
                        ON CONFLICT DO NOTHING
                    """, (source_id, target_id, link_target))
                    stats["links_found"] += 1
                except Exception:
                    pass
    conn.commit()
    log.info(f"Created {stats['links_found']} document links")

    # ── Phase 5: Generate embeddings ─────────────────────────────
    log.info("Generating embeddings for documents...")

    # Collect all texts that need embeddings
    doc_tldr_texts = [(doc["id"], doc["tldr"] or "no summary") for doc in all_docs]
    doc_full_texts = [(doc["id"], doc["full_content"][:4000] or "no content") for doc in all_docs]

    # Batch embed TLDRs
    for i in range(0, len(doc_tldr_texts), BATCH_SIZE):
        batch = doc_tldr_texts[i:i+BATCH_SIZE]
        ids = [b[0] for b in batch]
        texts = [b[1] for b in batch]
        try:
            embeddings = get_embedding_batch(texts)
            for doc_id, emb in zip(ids, embeddings):
                cur.execute("UPDATE context_documents SET embedding_tldr = %s WHERE id = %s",
                            (json.dumps(emb), doc_id))
                stats["embeddings_generated"] += 1
            conn.commit()
            log.info(f"  TLDR embeddings: {min(i+BATCH_SIZE, len(doc_tldr_texts))}/{len(doc_tldr_texts)}")
        except Exception as e:
            log.error(f"Failed to embed TLDR batch starting at {i}: {e}")
            conn.rollback()

    # Batch embed full content
    for i in range(0, len(doc_full_texts), BATCH_SIZE):
        batch = doc_full_texts[i:i+BATCH_SIZE]
        ids = [b[0] for b in batch]
        texts = [b[1] for b in batch]
        try:
            embeddings = get_embedding_batch(texts)
            for doc_id, emb in zip(ids, embeddings):
                cur.execute("UPDATE context_documents SET embedding_full = %s WHERE id = %s",
                            (json.dumps(emb), doc_id))
                stats["embeddings_generated"] += 1
            conn.commit()
            log.info(f"  Full embeddings: {min(i+BATCH_SIZE, len(doc_full_texts))}/{len(doc_full_texts)}")
        except Exception as e:
            log.error(f"Failed to embed full batch starting at {i}: {e}")
            conn.rollback()

    # Embed essential terms
    cur.execute("SELECT id, term || ': ' || definition FROM essential_terms")
    term_rows = cur.fetchall()
    log.info(f"Generating embeddings for {len(term_rows)} terms...")
    for i in range(0, len(term_rows), BATCH_SIZE):
        batch = term_rows[i:i+BATCH_SIZE]
        ids = [b[0] for b in batch]
        texts = [b[1] for b in batch]
        try:
            embeddings = get_embedding_batch(texts)
            for term_id, emb in zip(ids, embeddings):
                cur.execute("UPDATE essential_terms SET embedding = %s WHERE id = %s",
                            (json.dumps(emb), term_id))
                stats["embeddings_generated"] += 1
            conn.commit()
            log.info(f"  Term embeddings: {min(i+BATCH_SIZE, len(term_rows))}/{len(term_rows)}")
        except Exception as e:
            log.error(f"Failed to embed terms batch starting at {i}: {e}")
            conn.rollback()

    # Embed quiz questions
    cur.execute("SELECT id, question FROM quiz_questions")
    quiz_rows = cur.fetchall()
    log.info(f"Generating embeddings for {len(quiz_rows)} quiz questions...")
    for i in range(0, len(quiz_rows), BATCH_SIZE):
        batch = quiz_rows[i:i+BATCH_SIZE]
        ids = [b[0] for b in batch]
        texts = [b[1] for b in batch]
        try:
            embeddings = get_embedding_batch(texts)
            for q_id, emb in zip(ids, embeddings):
                cur.execute("UPDATE quiz_questions SET embedding = %s WHERE id = %s",
                            (json.dumps(emb), q_id))
                stats["embeddings_generated"] += 1
            conn.commit()
            log.info(f"  Quiz embeddings: {min(i+BATCH_SIZE, len(quiz_rows))}/{len(quiz_rows)}")
        except Exception as e:
            log.error(f"Failed to embed quiz batch starting at {i}: {e}")
            conn.rollback()

    cur.close()
    conn.close()

    log.info("=" * 60)
    log.info("IMPORT COMPLETE")
    log.info(f"  Documents: {stats['docs_imported']} ({stats['by_tier']})")
    log.info(f"  Terms:     {stats['terms_imported']}")
    log.info(f"  Links:     {stats['links_found']}")
    log.info(f"  Quizzes:   {stats['quiz_questions']}")
    log.info(f"  Embeddings:{stats['embeddings_generated']}")
    log.info("=" * 60)


if __name__ == "__main__":
    main()
