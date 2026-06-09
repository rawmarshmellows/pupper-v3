#!/usr/bin/env python3
"""Semantic link proposer for learning notes.

Usage:
    python tools/link_semantic.py propose                    # Full proposal (JSON)
    python tools/link_semantic.py related path/to/file.md    # Related docs for one file (JSON)
    python tools/link_semantic.py links path/to/file.md      # Inline link proposals (JSON)
"""

import json
import sys
import sqlite3
import struct
import argparse
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "learning" / ".embeddings" / "embeddings.db"

RELATED_THRESHOLD = 0.55  # cosine threshold for related docs
INLINE_THRESHOLD = 0.65   # cosine threshold for inline term links
MAX_RELATED = 5


def unpack_embedding(blob):
    """Unpack a binary blob into a numpy array."""
    n = len(blob) // 4
    return np.array(struct.unpack(f'{n}f', blob), dtype=np.float32)


def cosine_similarity(a, b):
    dot = np.dot(a, b)
    norm = np.linalg.norm(a) * np.linalg.norm(b)
    if norm == 0:
        return 0.0
    return float(dot / norm)


def get_conn():
    if not DB_PATH.exists():
        print(json.dumps({"error": "Embeddings database not found. Run 'python tools/embed.py sync' first."}))
        sys.exit(1)
    return sqlite3.connect(str(DB_PATH))


def resolve_path(file_path):
    """Convert any path to a project-relative path."""
    p = Path(file_path)
    if not p.is_absolute():
        p = PROJECT_ROOT / p
    try:
        return str(p.relative_to(PROJECT_ROOT))
    except ValueError:
        return file_path


def cmd_related(file_path):
    """Return top-5 related documents for a file based on TLDR embedding similarity."""
    conn = get_conn()
    rel = resolve_path(file_path)

    source = conn.execute(
        "SELECT topic, embedding_tldr FROM documents WHERE file_path = ?", (rel,)
    ).fetchone()

    if not source or not source[1]:
        print(json.dumps({"error": f"No embedding found for {rel}"}))
        return

    query_vec = unpack_embedding(source[1])

    all_docs = conn.execute(
        "SELECT file_path, topic, tier, tldr, embedding_tldr FROM documents WHERE file_path != ? AND embedding_tldr IS NOT NULL",
        (rel,)
    ).fetchall()

    scored = []
    for row in all_docs:
        s = cosine_similarity(query_vec, unpack_embedding(row[4]))
        if s >= RELATED_THRESHOLD:
            scored.append({
                "file_path": row[0],
                "topic": row[1],
                "tier": row[2],
                "tldr": row[3] or "",
                "similarity": round(s, 4),
            })

    scored.sort(key=lambda x: x["similarity"], reverse=True)
    print(json.dumps(scored[:MAX_RELATED], indent=2))
    conn.close()


def cmd_links(file_path):
    """Propose inline wiki links for a file based on term embeddings."""
    conn = get_conn()
    rel = resolve_path(file_path)

    # Get the source document's full content embedding
    source = conn.execute(
        "SELECT topic, full_content, embedding_full FROM documents WHERE file_path = ?", (rel,)
    ).fetchone()

    if not source or not source[2]:
        print(json.dumps({"error": f"No embedding found for {rel}"}))
        return

    source_content_lower = source[1].lower() if source[1] else ""

    # Get all terms from OTHER documents
    term_rows = conn.execute("""
        SELECT t.term, t.definition, t.embedding, t.file_path, d.topic
        FROM terms t
        JOIN documents d ON t.file_path = d.file_path
        WHERE t.file_path != ? AND t.embedding IS NOT NULL
    """, (rel,)).fetchall()

    source_vec = unpack_embedding(source[2])
    proposals = []

    for term, definition, emb_blob, term_fp, term_topic in term_rows:
        # Check if the term text actually appears in the source content
        if term.lower() not in source_content_lower:
            continue

        term_vec = unpack_embedding(emb_blob)
        s = cosine_similarity(term_vec, source_vec)

        if s >= INLINE_THRESHOLD:
            proposals.append({
                "term": term,
                "definition": definition,
                "target_file": term_fp,
                "target_topic": term_topic,
                "similarity": round(s, 4),
            })

    # Deduplicate: keep highest similarity per term
    seen = {}
    for p in proposals:
        key = p["term"].lower()
        if key not in seen or p["similarity"] > seen[key]["similarity"]:
            seen[key] = p

    result = sorted(seen.values(), key=lambda x: x["similarity"], reverse=True)
    print(json.dumps(result, indent=2))
    conn.close()


def cmd_propose():
    """Full proposal: for every document, suggest related docs and inline links."""
    conn = get_conn()

    all_docs = conn.execute(
        "SELECT file_path, topic, tier, embedding_tldr, embedding_full, full_content FROM documents WHERE embedding_tldr IS NOT NULL"
    ).fetchall()

    all_terms = conn.execute("""
        SELECT t.term, t.definition, t.embedding, t.file_path, d.topic
        FROM terms t
        JOIN documents d ON t.file_path = d.file_path
        WHERE t.embedding IS NOT NULL
    """).fetchall()

    # Pre-compute TLDR vectors
    doc_vecs = {}
    doc_full_vecs = {}
    doc_meta = {}
    for row in all_docs:
        fp = row[0]
        doc_vecs[fp] = unpack_embedding(row[3])
        doc_full_vecs[fp] = unpack_embedding(row[4]) if row[4] else None
        doc_meta[fp] = {"topic": row[1], "tier": row[2], "content_lower": (row[5] or "").lower()}

    proposals = {}

    for fp in doc_vecs:
        # Related docs
        query_vec = doc_vecs[fp]
        related = []
        for fp2 in doc_vecs:
            if fp2 == fp:
                continue
            s = cosine_similarity(query_vec, doc_vecs[fp2])
            if s >= RELATED_THRESHOLD:
                related.append({
                    "file_path": fp2,
                    "topic": doc_meta[fp2]["topic"],
                    "similarity": round(s, 4),
                })
        related.sort(key=lambda x: x["similarity"], reverse=True)

        # Inline links
        source_full_vec = doc_full_vecs.get(fp)
        content_lower = doc_meta[fp]["content_lower"]
        inline = []

        if source_full_vec is not None:
            for term, definition, emb_blob, term_fp, term_topic in all_terms:
                if term_fp == fp:
                    continue
                if term.lower() not in content_lower:
                    continue
                term_vec = unpack_embedding(emb_blob)
                s = cosine_similarity(term_vec, source_full_vec)
                if s >= INLINE_THRESHOLD:
                    inline.append({
                        "term": term,
                        "target_file": term_fp,
                        "target_topic": term_topic,
                        "similarity": round(s, 4),
                    })

        # Deduplicate inline by term
        seen = {}
        for p in inline:
            key = p["term"].lower()
            if key not in seen or p["similarity"] > seen[key]["similarity"]:
                seen[key] = p
        inline = sorted(seen.values(), key=lambda x: x["similarity"], reverse=True)

        if related or inline:
            proposals[fp] = {
                "topic": doc_meta[fp]["topic"],
                "related": related[:MAX_RELATED],
                "inline_links": inline,
            }

    print(json.dumps(proposals, indent=2))
    conn.close()


def main():
    parser = argparse.ArgumentParser(description="Semantic link proposer for learning notes")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("propose", help="Full proposal for all docs (JSON)")

    rel_p = sub.add_parser("related", help="Related docs for one file (JSON)")
    rel_p.add_argument("path", help="File path")

    link_p = sub.add_parser("links", help="Inline link proposals for one file (JSON)")
    link_p.add_argument("path", help="File path")

    args = parser.parse_args()
    if args.command == "propose":
        cmd_propose()
    elif args.command == "related":
        cmd_related(args.path)
    elif args.command == "links":
        cmd_links(args.path)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
