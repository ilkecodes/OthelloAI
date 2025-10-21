#!/bin/bash

# 🎯 Brand Voice TEXT Setup Script
# Kullanım: ./setup_brand_voice.sh

set -e  # Exit on error

echo "🚀 Setting up Brand Voice System (TEXT mode)..."

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo -e "${RED}❌ Error: main.py not found. Run this from OTHELLOson/ directory${NC}"
    exit 1
fi

# 1. Create directories
echo -e "${YELLOW}📁 Creating directories...${NC}"
mkdir -p migrations
mkdir -p models
mkdir -p services

# 2. Create migration file
echo -e "${YELLOW}📝 Creating migration file...${NC}"
cat > migrations/001_brand_voice_tables_text.sql << 'EOF'
-- Brand Voice Tables - TEXT Fallback Version
CREATE TABLE IF NOT EXISTS brand_corpus (
    id SERIAL PRIMARY KEY,
    client_id VARCHAR(100) NOT NULL,
    source VARCHAR(50) NOT NULL,
    content_text TEXT NOT NULL,
    engagement_score INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'::jsonb
);

CREATE TABLE IF NOT EXISTS brand_voice_profiles (
    id SERIAL PRIMARY KEY,
    client_id VARCHAR(100) UNIQUE NOT NULL,
    tone VARCHAR(100),
    language_style VARCHAR(100),
    emoji_usage VARCHAR(50),
    content_themes JSONB DEFAULT '[]'::jsonb,
    brand_personality JSONB DEFAULT '[]'::jsonb,
    hashtag_strategy VARCHAR(200),
    sample_caption_style TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS brand_embeddings (
    id SERIAL PRIMARY KEY,
    client_id VARCHAR(100) NOT NULL,
    corpus_id INTEGER REFERENCES brand_corpus(id) ON DELETE CASCADE,
    embedding TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS gen_outputs (
    id SERIAL PRIMARY KEY,
    client_id VARCHAR(100) NOT NULL,
    platform VARCHAR(50) NOT NULL,
    content_type VARCHAR(50) NOT NULL,
    generated_text TEXT NOT NULL,
    topic VARCHAR(200),
    goal VARCHAR(100),
    similarity_score FLOAT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS feedback (
    id SERIAL PRIMARY KEY,
    output_id INTEGER REFERENCES gen_outputs(id) ON DELETE CASCADE,
    rating INTEGER CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_brand_corpus_client ON brand_corpus(client_id);
CREATE INDEX IF NOT EXISTS idx_brand_embeddings_client ON brand_embeddings(client_id);
CREATE INDEX IF NOT EXISTS idx_gen_outputs_client ON gen_outputs(client_id);
CREATE INDEX IF NOT EXISTS idx_feedback_output ON feedback(output_id);
EOF

echo -e "${GREEN}✅ Migration file created${NC}"

# 3. Update requirements.txt
echo -e "${YELLOW}📦 Updating requirements.txt...${NC}"
if ! grep -q "numpy" requirements.txt 2>/dev/null; then
    echo "numpy>=1.24.0" >> requirements.txt
    echo -e "${GREEN}✅ Added numpy to requirements.txt${NC}"
else
    echo -e "${GREEN}✅ numpy already in requirements.txt${NC}"
fi

# 4. Check environment variables
echo -e "${YELLOW}🔑 Checking environment variables...${NC}"

if [ -f ".env" ]; then
    if ! grep -q "ENABLE_BRAND_VOICE" .env; then
        echo "ENABLE_BRAND_VOICE=true" >> .env
        echo -e "${GREEN}✅ Added ENABLE_BRAND_VOICE to .env${NC}"
    fi
    
    if ! grep -q "OPENAI_API_KEY" .env || grep -q "OPENAI_API_KEY=$" .env; then
        echo -e "${YELLOW}⚠️  OPENAI_API_KEY not set in .env${NC}"
        echo -e "${YELLOW}   Add: OPENAI_API_KEY=sk-proj-...${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  .env file not found. Creating...${NC}"
    cat > .env << EOF
DATABASE_URL=postgresql://localhost:5432/othelloai
OPENAI_API_KEY=
APIFY_API_TOKEN=
ENABLE_BRAND_VOICE=true
ENVIRONMENT=development
EOF
    echo -e "${GREEN}✅ Created .env file${NC}"
fi

# 5. Run migration if DATABASE_URL is set
echo -e "${YELLOW}🗄️  Database setup...${NC}"

if [ -z "$DATABASE_URL" ]; then
    # Try to load from .env
    if [ -f ".env" ]; then
        export $(grep -v '^#' .env | xargs)
    fi
fi

if [ ! -z "$DATABASE_URL" ]; then
    echo -e "${YELLOW}Running migration...${NC}"
    
    # Check if psql is available
    if command -v psql &> /dev/null; then
        psql "$DATABASE_URL" -f migrations/001_brand_voice_tables_text.sql
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✅ Migration completed successfully${NC}"
            
            # Verify tables
            echo -e "${YELLOW}Verifying tables...${NC}"
            psql "$DATABASE_URL" -c "\dt brand_*" -c "\dt gen_outputs" -c "\dt feedback"
        else
            echo -e "${RED}❌ Migration failed${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️  psql not found. Please run migration manually:${NC}"
        echo -e "   psql \"\$DATABASE_URL\" -f migrations/001_brand_voice_tables_text.sql"
    fi
else
    echo -e "${YELLOW}⚠️  DATABASE_URL not set. Please run migration manually:${NC}"
    echo -e "   export DATABASE_URL=\"postgresql://...\"${NC}"
    echo -e "   psql \"\$DATABASE_URL\" -f migrations/001_brand_voice_tables_text.sql${NC}"
fi

# 6. Install dependencies
echo -e "${YELLOW}📦 Installing dependencies...${NC}"
if command -v pip &> /dev/null; then
    pip install -q numpy openai
    echo -e "${GREEN}✅ Dependencies installed${NC}"
else
    echo -e "${YELLOW}⚠️  pip not found. Install manually: pip install numpy openai${NC}"
fi

# 7. Git status
echo ""
echo -e "${GREEN}✅ Setup complete!${NC}"
echo ""
echo -e "${YELLOW}📋 Next steps:${NC}"
echo "1. Set your OPENAI_API_KEY in .env"
echo "2. If migration didn't run, execute:"
echo "   psql \"\$DATABASE_URL\" -f migrations/001_brand_voice_tables_text.sql"
echo "3. Deploy to Railway:"
echo "   git add ."
echo "   git commit -m \"Add brand voice system with TEXT fallback\""
echo "   git push origin main"
echo "4. Set Railway environment variables:"
echo "   ENABLE_BRAND_VOICE=true"
echo "   OPENAI_API_KEY=sk-proj-..."
echo ""
echo -e "${YELLOW}🧪 Test with:${NC}"
echo "   uvicorn main:app --reload"
echo "   curl http://localhost:8000/api/brand-voice/health"
echo ""
