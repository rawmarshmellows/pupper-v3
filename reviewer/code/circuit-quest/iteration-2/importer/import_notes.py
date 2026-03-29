#!/usr/bin/env python3
"""Import Obsidian markdown notes into PostgreSQL with pgvector embeddings.
v2: Fixed quiz question extraction to match actual note format (**Q1:** + <details>)."""

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
BATCH_SIZE = 50

# ── helpers ──────────────────────────────────────────────────────────

def get_embedding_batch(texts, retries=3):
    url = "https://openrouter.ai/api/v1/embeddings"
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}
    clean_texts = [t[:8000] if t else "empty" for t in texts]
    payload = {"model": EMBEDDING_MODEL, "input": clean_texts, "dimensions": EMBEDDING_DIM}
    for attempt in range(retries):
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=60)
            resp.raise_for_status()
            data = resp.json()
            return [item["embedding"] for item in sorted(data["data"], key=lambda x: x["index"])]
        except Exception as e:
            log.warning(f"Embedding attempt {attempt+1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(2 ** (attempt + 1))
            else:
                raise

def parse_frontmatter(content):
    if not content.startswith("---"):
        return {}, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    try:
        meta = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        meta = {}
    return meta, parts[2].strip()

def detect_tier(file_path):
    parent = Path(file_path).parent.name
    if "micro" in parent: return "micro"
    elif "small" in parent: return "small"
    elif "quick" in parent: return "quick"
    return "quick"

def extract_tldr(body):
    match = re.search(r'(?:##?\s*)?(?:TL;?DR|TLDR|tl;?dr)[:\s]*\n?(.*?)(?=\n##|\n---|\Z)', body, re.DOTALL)
    if match:
        return match.group(1).strip()[:500]
    paragraphs = [p.strip() for p in body.split('\n\n') if p.strip() and not p.strip().startswith('#')]
    return paragraphs[0][:500] if paragraphs else None

def extract_definition(body):
    match = re.search(r'(?:##?\s*)?(?:Definition|What is)[:\s]*\n?(.*?)(?=\n##|\n---|\Z)', body, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip()[:500] if match else None

def extract_key_insight(body):
    match = re.search(r'(?:##?\s*)?(?:Key Insight|Core Insight|Main Idea)[:\s]*\n?(.*?)(?=\n##|\n---|\Z)', body, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip()[:500] if match else None

def extract_situation(body):
    match = re.search(r'(?:##?\s*)?(?:Situation|When|Context|Use Case)[:\s]*\n?(.*?)(?=\n##|\n---|\Z)', body, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip()[:500] if match else None

def extract_essential_terms(body):
    terms = []
    table_pattern = re.compile(r'(?:##?\s*)?(?:Essential Terms|Key Terms|Vocabulary|Terms)[:\s]*\n(.*?)(?=\n##|\n---|\Z)', re.DOTALL | re.IGNORECASE)
    table_match = table_pattern.search(body)
    if table_match:
        rows = re.findall(r'\|\s*\*?\*?([^|*]+?)\*?\*?\s*\|\s*([^|]+?)\s*\|', table_match.group(1))
        for term, defn in rows:
            term, defn = term.strip(), defn.strip()
            if term and defn and term.lower() not in ('term', 'concept', 'name', '---', ':-') and not re.match(r'^[-:]+$', term):
                terms.append({"term": term, "definition": defn})
    return terms

def extract_quiz_questions(body):
    """Extract quiz questions — handles the actual note format:
    **Q1:** question text
    <details>
    <summary>Answer</summary>
    answer text
    </details>
    """
    questions = []

    # Find the Test Your Understanding section (may be inside <details> or a heading)
    tyu_pattern = re.compile(
        r'(?:Test Your Understanding|Quiz|Practice Questions|Check Your Understanding).*?\n(.*)',
        re.DOTALL | re.IGNORECASE
    )
    tyu_match = tyu_pattern.search(body)
    quiz_text = tyu_match.group(1) if tyu_match else body

    # Primary pattern: **Q1:** question\n<details>\n<summary>Answer</summary>\nanswer\n</details>
    qa_pattern = re.compile(
        r'\*\*Q\d+:\*\*\s*(.*?)\n\s*<details>\s*\n\s*<summary>\s*Answer\s*</summary>\s*\n(.*?)</details>',
        re.DOTALL
    )
    for match in qa_pattern.finditer(quiz_text):
        q = match.group(1).strip()
        a = re.sub(r'<[^>]+>', '', match.group(2)).strip()
        # Clean markdown bold from answer
        a = re.sub(r'\*\*(.*?)\*\*', r'\1', a)
        if q and a and len(a) > 5:
            questions.append({"question": q, "answer": a[:1000], "level": estimate_blooms_level(q)})

    # Fallback pattern: numbered questions with > blockquote answers
    if not questions:
        qa_block = re.findall(
            r'(?:^|\n)\s*\d+\.\s*\*?\*?(?:Q(?:uestion)?)?:?\s*\*?\*?\s*(.*?)\n\s*>\s*(.*?)(?=\n\s*\d+\.|\Z)',
            quiz_text, re.DOTALL
        )
        for q, a in qa_block:
            q, a = q.strip(), a.strip()
            if q and a and len(a) > 5:
                questions.append({"question": q, "answer": a[:1000], "level": estimate_blooms_level(q)})

    # Fallback: bold question then paragraph answer
    if not questions:
        qa_bold = re.findall(r'\*\*([^*]+?)\*\*\s*\n\s*((?:(?!\*\*).)+)', quiz_text, re.DOTALL)
        for q, a in qa_bold:
            q, a = q.strip(), a.strip()
            if q and a and len(a) > 20 and '?' in q:
                questions.append({"question": q, "answer": a[:1000], "level": estimate_blooms_level(q)})

    return questions

def estimate_blooms_level(question):
    q = question.lower()
    if any(w in q for w in ['define', 'list', 'name', 'what is', 'identify', 'recall']):
        return 1
    elif any(w in q for w in ['explain', 'describe', 'summarize', 'compare', 'interpret', 'why does', 'how does', 'why can']):
        return 2
    elif any(w in q for w in ['calculate', 'apply', 'use', 'solve', 'compute', 'determine', 'implement', 'what resistor', 'what value']):
        return 3
    elif any(w in q for w in ['analyze', 'differentiate', 'distinguish', 'examine', 'break down', 'what would happen', 'what happens if', 'if you removed']):
        return 4
    elif any(w in q for w in ['evaluate', 'justify', 'argue', 'which is better', 'assess', 'critique', 'judge', 'why might']):
        return 5
    return 3

def extract_wiki_links(body):
    return re.findall(r'\[\[([^\]]+)\]\]', body)

def strip_markdown(text):
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    return text

# ── main ─────────────────────────────────────────────────────────────

def main():
    log.info("Starting note import (v2 — improved quiz extraction)...")
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = False
    cur = conn.cursor()

    notes_path = Path(NOTES_PATH)
    if not notes_path.exists():
        log.error(f"Notes path does not exist: {notes_path}")
        sys.exit(1)

    md_files = sorted(notes_path.rglob("*.md"))
    log.info(f"Found {len(md_files)} markdown files")

    stats = {"docs_imported": 0, "terms_imported": 0, "links_found": 0,
             "quiz_questions": 0, "embeddings_generated": 0,
             "by_tier": {"micro": 0, "quick": 0, "small": 0}}

    doc_ids = {}
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
                tier=EXCLUDED.tier, topic=EXCLUDED.topic, created_date=EXCLUDED.created_date,
                tldr=EXCLUDED.tldr, definition=EXCLUDED.definition, key_insight=EXCLUDED.key_insight,
                situation=EXCLUDED.situation, full_content=EXCLUDED.full_content
            RETURNING id
        """, (rel_path, tier, topic, created_date, tldr, definition, key_insight, situation, full_content))
        doc_id = cur.fetchone()[0]
        doc_ids[rel_path] = doc_id
        stats["docs_imported"] += 1
        stats["by_tier"][tier] += 1

        all_docs.append({
            "id": doc_id, "rel_path": rel_path, "tldr": tldr or "",
            "full_content": full_content[:4000],
            "terms": extract_essential_terms(body),
            "questions": extract_quiz_questions(body),
            "wiki_links": extract_wiki_links(body),
        })

    conn.commit()
    log.info(f"Imported {stats['docs_imported']} documents: {stats['by_tier']}")

    # Phase 2: terms
    for doc in all_docs:
        for td in doc["terms"]:
            cur.execute("INSERT INTO essential_terms (document_id, term, definition) VALUES (%s, %s, %s)",
                        (doc["id"], td["term"], td["definition"]))
            stats["terms_imported"] += 1
    conn.commit()
    log.info(f"Imported {stats['terms_imported']} essential terms")

    # Phase 3: quiz questions
    for doc in all_docs:
        for qq in doc["questions"]:
            cur.execute("INSERT INTO quiz_questions (document_id, level, question, answer) VALUES (%s, %s, %s, %s)",
                        (doc["id"], qq["level"], qq["question"], qq["answer"]))
            stats["quiz_questions"] += 1
    conn.commit()
    log.info(f"Imported {stats['quiz_questions']} quiz questions")

    # Phase 4: wiki links
    slug_to_id = {}
    for rel_path, doc_id in doc_ids.items():
        slug = Path(rel_path).stem.lower()
        slug_to_id[slug] = doc_id
        parts = rel_path.split("/")
        if len(parts) >= 2:
            slug_to_id[f"{parts[0]}/{Path(rel_path).stem}".lower()] = doc_id

    for doc in all_docs:
        for link_target in doc["wiki_links"]:
            link_slug = link_target.lower().replace(" ", "-")
            target_id = slug_to_id.get(link_slug) or slug_to_id.get(link_slug.split("/")[-1])
            if target_id and target_id != doc["id"]:
                try:
                    cur.execute("INSERT INTO document_links (source_id, target_id, link_context) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
                                (doc["id"], target_id, link_target))
                    stats["links_found"] += 1
                except Exception:
                    pass
    conn.commit()
    log.info(f"Created {stats['links_found']} document links")

    # Phase 5: embeddings
    log.info("Generating embeddings...")

    doc_tldr_texts = [(d["id"], d["tldr"] or "no summary") for d in all_docs]
    doc_full_texts = [(d["id"], d["full_content"][:4000] or "no content") for d in all_docs]

    for label, texts, col in [("TLDR", doc_tldr_texts, "embedding_tldr"), ("Full", doc_full_texts, "embedding_full")]:
        for i in range(0, len(texts), BATCH_SIZE):
            batch = texts[i:i+BATCH_SIZE]
            try:
                embeddings = get_embedding_batch([b[1] for b in batch])
                for (doc_id, _), emb in zip(batch, embeddings):
                    cur.execute(f"UPDATE context_documents SET {col} = %s WHERE id = %s", (json.dumps(emb), doc_id))
                    stats["embeddings_generated"] += 1
                conn.commit()
                log.info(f"  {label} embeddings: {min(i+BATCH_SIZE, len(texts))}/{len(texts)}")
            except Exception as e:
                log.error(f"Failed {label} batch at {i}: {e}")
                conn.rollback()

    cur.execute("SELECT id, term || ': ' || definition FROM essential_terms")
    term_rows = cur.fetchall()
    log.info(f"Generating embeddings for {len(term_rows)} terms...")
    for i in range(0, len(term_rows), BATCH_SIZE):
        batch = term_rows[i:i+BATCH_SIZE]
        try:
            embeddings = get_embedding_batch([b[1] for b in batch])
            for (tid, _), emb in zip(batch, embeddings):
                cur.execute("UPDATE essential_terms SET embedding = %s WHERE id = %s", (json.dumps(emb), tid))
                stats["embeddings_generated"] += 1
            conn.commit()
            log.info(f"  Term embeddings: {min(i+BATCH_SIZE, len(term_rows))}/{len(term_rows)}")
        except Exception as e:
            log.error(f"Failed term batch at {i}: {e}")
            conn.rollback()

    cur.execute("SELECT id, question FROM quiz_questions")
    quiz_rows = cur.fetchall()
    log.info(f"Generating embeddings for {len(quiz_rows)} quiz questions...")
    for i in range(0, len(quiz_rows), BATCH_SIZE):
        batch = quiz_rows[i:i+BATCH_SIZE]
        try:
            embeddings = get_embedding_batch([b[1] for b in batch])
            for (qid, _), emb in zip(batch, embeddings):
                cur.execute("UPDATE quiz_questions SET embedding = %s WHERE id = %s", (json.dumps(emb), qid))
                stats["embeddings_generated"] += 1
            conn.commit()
            log.info(f"  Quiz embeddings: {min(i+BATCH_SIZE, len(quiz_rows))}/{len(quiz_rows)}")
        except Exception as e:
            log.error(f"Failed quiz batch at {i}: {e}")
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
