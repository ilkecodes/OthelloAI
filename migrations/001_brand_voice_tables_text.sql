-- Brand Voice Tables (compatible with existing code)

CREATE TABLE IF NOT EXISTS brand_corpus (
    id SERIAL PRIMARY KEY,
    client_id VARCHAR(100) NOT NULL,
    source VARCHAR(50) NOT NULL,
    text TEXT NOT NULL,
    url VARCHAR(500),
    engagement_score INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS brand_voice_profiles (
    id SERIAL PRIMARY KEY,
    client_id VARCHAR(100) UNIQUE NOT NULL,
    profile JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS brand_embeddings (
    id SERIAL PRIMARY KEY,
    client_id VARCHAR(100) NOT NULL,
    corpus_id INTEGER REFERENCES brand_corpus(id) ON DELETE CASCADE,
    text TEXT NOT NULL,
    source VARCHAR(50),
    embedding TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS gen_outputs (
    id SERIAL PRIMARY KEY,
    client_id VARCHAR(100) NOT NULL,
    platform VARCHAR(50) NOT NULL,
    content_type VARCHAR(50) NOT NULL,
    topic VARCHAR(200),
    goal VARCHAR(100),
    request_payload JSONB DEFAULT '{}'::jsonb,
    output JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS feedback (
    id SERIAL PRIMARY KEY,
    output_id INTEGER REFERENCES gen_outputs(id) ON DELETE CASCADE,
    rating INTEGER,
    comment TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_brand_corpus_client ON brand_corpus(client_id);
CREATE INDEX IF NOT EXISTS idx_brand_embeddings_client ON brand_embeddings(client_id);
CREATE INDEX IF NOT EXISTS idx_gen_outputs_client ON gen_outputs(client_id);
CREATE INDEX IF NOT EXISTS idx_feedback_output ON feedback(output_id);
