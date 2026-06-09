#!/usr/bin/env python3
"""Local embedding manager for learning notes.

Usage:
    python tools/embed.py sync                     # Embed new/changed files
    python tools/embed.py sync path/to/file.md     # Single file
    python tools/embed.py related path/to/file.md  # Top-5 similar docs
    python tools/embed.py stats                    # Coverage stats
    python tools/embed.py calibrate                # Sample similarity pairs for threshold tuning
"""

import os
import sys
import json
import struct
import hashlib
import sqlite3
import logging
import argparse
from pathlib import Path
from datetime import datetime

import requests
import numpy as np

# Add tools/ to path so we can import note_parser
sys.path.insert(0, str(Path(__file__).parent))
import note_parser

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "learning" / ".embeddings" / "embeddings.db"
NOTES_ROOT = PROJECT_ROOT / "learning" / "notes"
EMBEDDING_MODEL = "openai/text-embedding-3-small"
EMBEDDING_DIM = 512
BATCH_SIZE = 50
SIMILARITY_THRESHOLD = 0.3

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")

NOTE_DIRS = ["micro-context", "quick-context", "small-context"]


def pack_embedding(vec):
    """Pack a list of floats into a binary blob."""
    return struct.pack(f'{len(vec)}f', *vec)


def unpack_embedding(blob):
    """Unpack a binary blob into a numpy array."""
    n = len(blob) // 4
    return np.array(struct.unpack(f'{n}f', blob), dtype=np.float32)


def cosine_similarity(a, b):
    """Compute cosine similarity between two vectors."""
    dot = np.dot(a, b)
    norm = np.linalg.norm(a) * np.linalg.norm(b)
    if norm == 0:
        return 0.0
    return float(dot / norm)


def init_db(db_path=None):
    """Create SQLite database and tables if they don't exist."""
    path = db_path or DB_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS file_hashes (
            file_path TEXT PRIMARY KEY,
            content_hash TEXT NOT NULL,
            last_embedded TEXT NOT NULL,
            tier TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS documents (
            file_path TEXT PRIMARY KEY,
            tier TEXT NOT NULL,
            topic TEXT NOT NULL,
            category TEXT NOT NULL DEFAULT 'other',
            created_date TEXT,
            tldr TEXT,
            definition TEXT,
            key_insight TEXT,
            full_content TEXT NOT NULL,
            embedding_tldr BLOB,
            embedding_full BLOB
        );

        CREATE TABLE IF NOT EXISTS terms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path TEXT NOT NULL REFERENCES documents(file_path),
            term TEXT NOT NULL,
            definition TEXT NOT NULL,
            embedding BLOB
        );

        CREATE TABLE IF NOT EXISTS quiz_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path TEXT NOT NULL REFERENCES documents(file_path),
            level INTEGER,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            source TEXT DEFAULT 'test_your_understanding',
            embedding BLOB
        );

        CREATE TABLE IF NOT EXISTS doc_similarities (
            source_path TEXT NOT NULL,
            target_path TEXT NOT NULL,
            similarity REAL NOT NULL,
            PRIMARY KEY (source_path, target_path)
        );
    """)
    conn.commit()
    return conn


def file_hash(path):
    """SHA-256 hash of file contents."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def find_note_files(single_path=None):
    """Find all .md files in note directories, or a single file."""
    if single_path:
        p = Path(single_path)
        if not p.is_absolute():
            p = PROJECT_ROOT / p
        if p.exists() and p.suffix == '.md':
            return [p]
        log.error(f"File not found or not .md: {p}")
        return []

    files = []
    for d in NOTE_DIRS:
        dir_path = NOTES_ROOT / d
        if dir_path.exists():
            files.extend(sorted(dir_path.glob("*.md")))
    return files


def get_embeddings(texts, retries=3):
    """Call OpenRouter API for embeddings."""
    if not texts:
        return []
    if not OPENROUTER_API_KEY:
        log.error("OPENROUTER_API_KEY not set")
        sys.exit(1)

    results = []
    for i in range(0, len(texts), BATCH_SIZE):
        batch = texts[i:i + BATCH_SIZE]
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
                log.info(f"  Embedded batch {i // BATCH_SIZE + 1}: {len(embeddings)} texts")
                break
            except Exception as e:
                log.warning(f"  Embedding attempt {attempt + 1} failed: {e}")
                if attempt < retries - 1:
                    import time
                    time.sleep(2 ** (attempt + 1))
                else:
                    log.error(f"  Failed batch after {retries} attempts, using zeros")
                    results.extend([[0.0] * EMBEDDING_DIM] * len(batch))
    return results


def sync(single_path=None):
    """Embed new or changed files."""
    conn = init_db()
    files = find_note_files(single_path)
    if not files:
        log.info("No files to process.")
        return

    # Check which files need updating
    changed = []
    for f in files:
        h = file_hash(f)
        rel = str(f.relative_to(PROJECT_ROOT))
        row = conn.execute("SELECT content_hash FROM file_hashes WHERE file_path = ?", (rel,)).fetchone()
        if row is None or row[0] != h:
            changed.append((f, rel, h))

    if not changed:
        log.info(f"All {len(files)} files up to date.")
        return

    log.info(f"{len(changed)} files to embed (out of {len(files)} total)")

    # Parse all changed files
    doc_records = []
    all_terms = []
    all_quiz = []

    for fpath, rel, h in changed:
        content = fpath.read_text(encoding='utf-8')
        fm, body = note_parser.parse_frontmatter(content)
        tier = note_parser.detect_tier(rel)
        topic = fm.get('topic', fm.get('term', fpath.stem.replace('-', ' ').title()))
        created = fm.get('created')

        tldr = note_parser.extract_tldr(body)
        definition = note_parser.extract_definition(body)
        key_insight = note_parser.extract_key_insight(body)
        full_content = note_parser.strip_markdown_formatting(content)
        category = note_parser.classify_category(rel, topic)
        terms = note_parser.extract_essential_terms(body)
        quiz = note_parser.extract_quiz_questions(body)

        # Generate additional quiz questions
        summary = note_parser.extract_summary(body)
        quiz.extend(note_parser.generate_summary_questions(topic, summary))
        quiz.extend(note_parser.generate_insight_questions(topic, key_insight, definition))
        quiz.extend(note_parser.generate_term_questions(topic, terms))
        quiz.extend(note_parser.generate_section_questions(topic, body))

        doc_records.append({
            "file_path": rel,
            "tier": tier,
            "topic": topic,
            "category": category,
            "created_date": created,
            "tldr": tldr,
            "definition": definition,
            "key_insight": key_insight,
            "full_content": full_content,
            "content_hash": h,
        })
        all_terms.append({"file_path": rel, "terms": terms})
        all_quiz.append({"file_path": rel, "questions": quiz})

    # Generate embeddings
    log.info("Generating TLDR embeddings...")
    tldr_texts = []
    for doc in doc_records:
        text = doc["tldr"] or doc["definition"] or doc["key_insight"] or doc["topic"]
        tldr_texts.append(f"{doc['topic']}: {text}")
    tldr_embeddings = get_embeddings(tldr_texts)

    log.info("Generating full-content embeddings...")
    full_texts = [doc["full_content"][:4000] for doc in doc_records]
    full_embeddings = get_embeddings(full_texts)

    # Embed terms
    all_term_texts = []
    term_index = []  # (doc_idx, term_idx)
    for di, item in enumerate(all_terms):
        for ti, t in enumerate(item["terms"]):
            all_term_texts.append(f"{t['term']}: {t['definition']}")
            term_index.append((di, ti))

    term_embeddings = []
    if all_term_texts:
        log.info(f"Generating embeddings for {len(all_term_texts)} terms...")
        term_embeddings = get_embeddings(all_term_texts)

    # Embed quiz questions
    all_quiz_texts = []
    quiz_index = []
    for di, item in enumerate(all_quiz):
        for qi, q in enumerate(item["questions"]):
            all_quiz_texts.append(f"{q['question']} {q['answer']}")
            quiz_index.append((di, qi))

    quiz_embeddings = []
    if all_quiz_texts:
        log.info(f"Generating embeddings for {len(all_quiz_texts)} quiz questions...")
        quiz_embeddings = get_embeddings(all_quiz_texts)

    # Write to DB
    log.info("Writing to database...")
    now = datetime.utcnow().isoformat()

    for i, doc in enumerate(doc_records):
        fp = doc["file_path"]

        # Upsert document
        conn.execute("""
            INSERT INTO documents (file_path, tier, topic, category, created_date,
                                   tldr, definition, key_insight, full_content,
                                   embedding_tldr, embedding_full)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(file_path) DO UPDATE SET
                tier=excluded.tier, topic=excluded.topic, category=excluded.category,
                created_date=excluded.created_date, tldr=excluded.tldr,
                definition=excluded.definition, key_insight=excluded.key_insight,
                full_content=excluded.full_content,
                embedding_tldr=excluded.embedding_tldr, embedding_full=excluded.embedding_full
        """, (fp, doc["tier"], doc["topic"], doc["category"], doc["created_date"],
              doc["tldr"], doc["definition"], doc["key_insight"], doc["full_content"],
              pack_embedding(tldr_embeddings[i]), pack_embedding(full_embeddings[i])))

        # Update file hash
        conn.execute("""
            INSERT INTO file_hashes (file_path, content_hash, last_embedded, tier)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(file_path) DO UPDATE SET
                content_hash=excluded.content_hash, last_embedded=excluded.last_embedded,
                tier=excluded.tier
        """, (fp, doc["content_hash"], now, doc["tier"]))

        # Replace terms for this doc
        conn.execute("DELETE FROM terms WHERE file_path = ?", (fp,))
        conn.execute("DELETE FROM quiz_questions WHERE file_path = ?", (fp,))

    # Insert terms with embeddings
    te_idx = 0
    for di, item in enumerate(all_terms):
        fp = doc_records[di]["file_path"]
        for ti, t in enumerate(item["terms"]):
            emb = pack_embedding(term_embeddings[te_idx]) if te_idx < len(term_embeddings) else None
            conn.execute(
                "INSERT INTO terms (file_path, term, definition, embedding) VALUES (?, ?, ?, ?)",
                (fp, t["term"], t["definition"], emb))
            te_idx += 1

    # Insert quiz questions with embeddings
    qe_idx = 0
    for di, item in enumerate(all_quiz):
        fp = doc_records[di]["file_path"]
        for qi, q in enumerate(item["questions"]):
            emb = pack_embedding(quiz_embeddings[qe_idx]) if qe_idx < len(quiz_embeddings) else None
            conn.execute(
                "INSERT INTO quiz_questions (file_path, level, question, answer, source, embedding) VALUES (?, ?, ?, ?, ?, ?)",
                (fp, q["level"], q["question"], q["answer"], q.get("source", "test_your_understanding"), emb))
            qe_idx += 1

    conn.commit()

    # Recompute similarities for all docs (cheap for ~200 docs)
    log.info("Computing document similarities...")
    rows = conn.execute("SELECT file_path, embedding_tldr FROM documents WHERE embedding_tldr IS NOT NULL").fetchall()
    if rows:
        paths = [r[0] for r in rows]
        vecs = np.array([unpack_embedding(r[1]) for r in rows])
        # Normalize
        norms = np.linalg.norm(vecs, axis=1, keepdims=True)
        norms[norms == 0] = 1
        vecs_norm = vecs / norms
        # All-pairs cosine similarity
        sim_matrix = vecs_norm @ vecs_norm.T

        conn.execute("DELETE FROM doc_similarities")
        pairs = []
        for i in range(len(paths)):
            for j in range(i + 1, len(paths)):
                s = float(sim_matrix[i, j])
                if s >= SIMILARITY_THRESHOLD:
                    pairs.append((paths[i], paths[j], s))
                    pairs.append((paths[j], paths[i], s))

        conn.executemany(
            "INSERT INTO doc_similarities (source_path, target_path, similarity) VALUES (?, ?, ?)",
            pairs)
        conn.commit()
        log.info(f"  Stored {len(pairs) // 2} similarity pairs above {SIMILARITY_THRESHOLD}")

    total_terms = conn.execute("SELECT COUNT(*) FROM terms").fetchone()[0]
    total_quiz = conn.execute("SELECT COUNT(*) FROM quiz_questions").fetchone()[0]
    total_docs = conn.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
    log.info(f"Done. {len(changed)} files embedded. DB totals: {total_docs} docs, {total_terms} terms, {total_quiz} quiz questions.")
    conn.close()


def related(file_path):
    """Show top-5 similar documents for a given file."""
    conn = init_db()
    rel = file_path
    if not rel.startswith("learning/"):
        p = Path(file_path)
        if not p.is_absolute():
            p = PROJECT_ROOT / p
        rel = str(p.relative_to(PROJECT_ROOT))

    rows = conn.execute("""
        SELECT target_path, similarity FROM doc_similarities
        WHERE source_path = ? ORDER BY similarity DESC LIMIT 5
    """, (rel,)).fetchall()

    if not rows:
        # Try semantic search by topic
        doc = conn.execute("SELECT topic, embedding_tldr FROM documents WHERE file_path = ?", (rel,)).fetchone()
        if doc and doc[1]:
            query_vec = unpack_embedding(doc[1])
            all_rows = conn.execute(
                "SELECT file_path, topic, embedding_tldr FROM documents WHERE file_path != ? AND embedding_tldr IS NOT NULL",
                (rel,)).fetchall()
            scored = []
            for r in all_rows:
                s = cosine_similarity(query_vec, unpack_embedding(r[2]))
                if s > 0.3:
                    scored.append({"file_path": r[0], "topic": r[1], "similarity": round(s, 4)})
            scored.sort(key=lambda x: x["similarity"], reverse=True)
            print(json.dumps(scored[:5], indent=2))
        else:
            print(json.dumps([], indent=2))
    else:
        results = []
        for target, sim in rows:
            topic_row = conn.execute("SELECT topic FROM documents WHERE file_path = ?", (target,)).fetchone()
            results.append({
                "file_path": target,
                "topic": topic_row[0] if topic_row else "",
                "similarity": round(sim, 4),
            })
        print(json.dumps(results, indent=2))
    conn.close()


def stats():
    """Print coverage statistics."""
    if not DB_PATH.exists():
        print("No embeddings database found. Run 'python tools/embed.py sync' first.")
        return

    conn = sqlite3.connect(str(DB_PATH))
    total_docs = conn.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
    by_tier = conn.execute("SELECT tier, COUNT(*) FROM documents GROUP BY tier ORDER BY tier").fetchall()
    by_cat = conn.execute("SELECT category, COUNT(*) FROM documents GROUP BY category ORDER BY COUNT(*) DESC").fetchall()
    total_terms = conn.execute("SELECT COUNT(*) FROM terms").fetchone()[0]
    total_quiz = conn.execute("SELECT COUNT(*) FROM quiz_questions").fetchone()[0]
    total_sims = conn.execute("SELECT COUNT(*) FROM doc_similarities").fetchone()[0]
    embedded = conn.execute("SELECT COUNT(*) FROM documents WHERE embedding_tldr IS NOT NULL").fetchone()[0]

    print(f"Documents: {total_docs} ({embedded} with embeddings)")
    print(f"  By tier: {', '.join(f'{t}={c}' for t, c in by_tier)}")
    print(f"  By category: {', '.join(f'{t}={c}' for t, c in by_cat)}")
    print(f"Terms: {total_terms}")
    print(f"Quiz questions: {total_quiz}")
    print(f"Similarity pairs: {total_sims // 2}")

    # Files on disk vs in DB
    on_disk = len(find_note_files())
    print(f"Files on disk: {on_disk}, in DB: {total_docs}, gap: {on_disk - total_docs}")
    conn.close()


def calibrate():
    """Show sample similarity pairs for threshold tuning."""
    if not DB_PATH.exists():
        print("No embeddings database found. Run 'python tools/embed.py sync' first.")
        return

    conn = sqlite3.connect(str(DB_PATH))
    rows = conn.execute("SELECT file_path, topic, embedding_tldr FROM documents WHERE embedding_tldr IS NOT NULL").fetchall()
    if len(rows) < 2:
        print("Need at least 2 embedded documents.")
        return

    paths = [r[0] for r in rows]
    topics = [r[1] for r in rows]
    vecs = np.array([unpack_embedding(r[2]) for r in rows])
    norms = np.linalg.norm(vecs, axis=1, keepdims=True)
    norms[norms == 0] = 1
    vecs_norm = vecs / norms
    sim_matrix = vecs_norm @ vecs_norm.T

    # Collect all pairs
    pairs = []
    for i in range(len(paths)):
        for j in range(i + 1, len(paths)):
            pairs.append((topics[i], topics[j], float(sim_matrix[i, j])))

    pairs.sort(key=lambda x: x[2], reverse=True)

    print("=== TOP 15 MOST SIMILAR ===")
    for a, b, s in pairs[:15]:
        print(f"  {s:.4f}  {a}  <->  {b}")

    print("\n=== AROUND THRESHOLD (0.50-0.60) ===")
    mid = [p for p in pairs if 0.50 <= p[2] <= 0.60]
    for a, b, s in mid[:10]:
        print(f"  {s:.4f}  {a}  <->  {b}")

    print(f"\n=== BOTTOM 5 ===")
    for a, b, s in pairs[-5:]:
        print(f"  {s:.4f}  {a}  <->  {b}")

    print(f"\nTotal pairs: {len(pairs)}")
    print(f"Above 0.3: {sum(1 for _,_,s in pairs if s >= 0.3)}")
    print(f"Above 0.5: {sum(1 for _,_,s in pairs if s >= 0.5)}")
    print(f"Above 0.65: {sum(1 for _,_,s in pairs if s >= 0.65)}")
    conn.close()


def main():
    parser = argparse.ArgumentParser(description="Embedding manager for learning notes")
    sub = parser.add_subparsers(dest="command")

    sync_p = sub.add_parser("sync", help="Embed new/changed files")
    sync_p.add_argument("path", nargs="?", help="Single file path to sync")

    rel_p = sub.add_parser("related", help="Top-5 similar docs")
    rel_p.add_argument("path", help="File path to find related docs for")

    sub.add_parser("stats", help="Coverage statistics")
    sub.add_parser("calibrate", help="Sample similarity pairs for threshold tuning")

    args = parser.parse_args()
    if args.command == "sync":
        sync(args.path)
    elif args.command == "related":
        related(args.path)
    elif args.command == "stats":
        stats()
    elif args.command == "calibrate":
        calibrate()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
