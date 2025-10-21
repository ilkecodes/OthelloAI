-- migrations/001_brand_voice_tables.sql

-- 1) pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- 2) brand_corpus
CREATE TABLE IF NOT EXISTS brand_corpus (
    id SERIAL PRIMARY KEY,
    client_id VARCHAR(255) NOT NULL,
    source VARCHAR(50) DEFAULT 'instagram',
    text TEXT NOT NULL,
    url TEXT,
    engagement_score INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_brand_corpus_client ON brand_corpus(client_id);

-- 3) brand_voice_profiles
CREATE TABLE IF NOT EXISTS brand_voice_profiles (
    id SERIAL PRIMARY KEY,
    client_id VARCHAR(255) UNIQUE NOT NULL,
    profile JSONB NOT NULL DEFAULT '{}',
    updated_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_bvp_client ON brand_voice_profiles(client_id);

-- 4) brand_embeddings
-- NOTE: 384 boyutlu vektör için vector(384) tanımladık.
CREATE TABLE IF NOT EXISTS brand_embeddings (
    id SERIAL PRIMARY KEY,
    client_id VARCHAR(255) NOT NULL,
    text TEXT NOT NULL,
    source VARCHAR(50) DEFAULT 'manual',
    embedding vector(384),                         -- ✅ pgvector tipi ve isim 'embedding'
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_brand_embeddings_client ON brand_embeddings(client_id);

-- IVF Flat index (hız için)
-- nlist parametresini veri hacmine göre ayarlayın (örn: 100, 200, 1000 ...)
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_class c
        JOIN pg_namespace n ON n.oid = c.relnamespace
        WHERE c.relname = 'idx_brand_embeddings_embedding_ivf'
    ) THEN
        CREATE INDEX idx_brand_embeddings_embedding_ivf
        ON brand_embeddings USING ivfflat (embedding vector_l2_ops)
        WITH (lists = 100);
    END IF;
END$$;

-- 5) gen_outputs
CREATE TABLE IF NOT EXISTS gen_outputs (
    id SERIAL PRIMARY KEY,
    client_id VARCHAR(255) NOT NULL,
    platform VARCHAR(50),         -- ✅ eklendi
    content_type VARCHAR(50),     -- ✅ eklendi
    topic VARCHAR(255),           -- ✅ eklendi
    goal VARCHAR(50),             -- ✅ eklendi
    request_payload JSONB NOT NULL,
    output JSONB NOT NULL,
    scores JSONB DEFAULT '{}',
    ts TIMESTAMP DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_gen_outputs_client ON gen_outputs(client_id);

-- 6) feedback
CREATE TABLE IF NOT EXISTS feedback (
    id SERIAL PRIMARY KEY,
    client_id VARCHAR(255) NOT NULL,
    output_id INT,
    rating INT,
    comment TEXT,
    meta JSONB DEFAULT '{}',
    ts TIMESTAMP DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_feedback_client ON feedback(client_id);

