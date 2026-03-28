CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE context_documents (
    id SERIAL PRIMARY KEY,
    file_path TEXT UNIQUE NOT NULL,
    tier TEXT NOT NULL CHECK (tier IN ('micro', 'small', 'quick')),
    topic TEXT NOT NULL,
    created_date DATE,
    tldr TEXT,
    definition TEXT,
    key_insight TEXT,
    situation TEXT,
    full_content TEXT NOT NULL,
    embedding_tldr vector(512),
    embedding_full vector(512),
    search_vector tsvector GENERATED ALWAYS AS (
        setweight(to_tsvector('english', topic), 'A') ||
        setweight(to_tsvector('english', COALESCE(tldr, '')), 'B') ||
        setweight(to_tsvector('english', COALESCE(definition, '')), 'B') ||
        setweight(to_tsvector('english', full_content), 'C')
    ) STORED
);

CREATE TABLE essential_terms (
    id SERIAL PRIMARY KEY,
    document_id INT REFERENCES context_documents(id),
    term TEXT NOT NULL,
    definition TEXT NOT NULL,
    embedding vector(512)
);

CREATE TABLE document_links (
    source_id INT REFERENCES context_documents(id),
    target_id INT REFERENCES context_documents(id),
    link_context TEXT,
    PRIMARY KEY (source_id, target_id)
);

CREATE TABLE quiz_questions (
    id SERIAL PRIMARY KEY,
    document_id INT REFERENCES context_documents(id),
    level INT CHECK (level BETWEEN 1 AND 6),
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    embedding vector(512)
);

CREATE INDEX ON context_documents USING hnsw (embedding_tldr vector_cosine_ops) WITH (m = 16, ef_construction = 64);
CREATE INDEX ON context_documents USING hnsw (embedding_full vector_cosine_ops) WITH (m = 16, ef_construction = 64);
CREATE INDEX ON context_documents USING gin (search_vector);
CREATE INDEX ON essential_terms USING hnsw (embedding vector_cosine_ops);
CREATE INDEX ON quiz_questions USING hnsw (embedding vector_cosine_ops);
