-- Brand Voice Tables - SADECE YENİ TABLOLAR
-- Mevcut hiçbir tabloya dokunmaz

BEGIN;

CREATE TABLE IF NOT EXISTS brand_corpus (
    id SERIAL PRIMARY KEY,
    client_id VARCHAR(255) NOT NULL,
    source VARCHAR(50) DEFAULT 'instagram',
    text TEXT NOT NULL,
    url VARCHAR(500),
    ts TIMESTAMP DEFAULT NOW(),
    engagement_score NUMERIC DEFAULT 0
);

CREATE INDEX idx_brand_corpus_client ON brand_corpus(client_id);

CREATE TABLE IF NOT EXISTS brand_voice_profiles (
    client_id VARCHAR(255) PRIMARY KEY,
    profile JSONB NOT NULL,
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS brand_embeddings (
    id SERIAL PRIMARY KEY,
    client_id VARCHAR(255) NOT NULL,
    text TEXT NOT NULL,
    vector TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_brand_embeddings_client ON brand_embeddings(client_id);

CREATE TABLE IF NOT EXISTS gen_outputs (
    id SERIAL PRIMARY KEY,
    client_id VARCHAR(255) NOT NULL,
    request_payload JSONB NOT NULL,
    output JSONB NOT NULL,
    scores JSONB DEFAULT '{}',
    ts TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS feedback (
    id SERIAL PRIMARY KEY,
    gen_output_id INTEGER NOT NULL,
    field VARCHAR(50),
    action VARCHAR(20) NOT NULL,
    comment TEXT,
    user_id VARCHAR(100),
    ts TIMESTAMP DEFAULT NOW()
);

COMMIT;
