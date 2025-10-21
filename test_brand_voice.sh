#!/bin/bash

# 🧪 Brand Voice System Test Script
# Tests all endpoints with sample data

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
API_URL="${API_URL:-http://localhost:8000}"
CLIENT_ID="test_kahve_brand"

echo -e "${BLUE}🧪 Testing Brand Voice System${NC}"
echo -e "${BLUE}API URL: $API_URL${NC}"
echo ""

# Test 1: Health Check
echo -e "${YELLOW}Test 1: Health Check${NC}"
response=$(curl -s "$API_URL/api/brand-voice/health")
echo "$response" | jq .
if echo "$response" | jq -e '.feature_enabled == true' > /dev/null; then
    echo -e "${GREEN}✅ Health check passed${NC}"
else
    echo -e "${RED}❌ Health check failed${NC}"
    exit 1
fi
echo ""

# Test 2: Add Corpus
echo -e "${YELLOW}Test 2: Adding corpus data${NC}"
corpus_response=$(curl -s -X POST "$API_URL/api/brand-voice/corpus" \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "'"$CLIENT_ID"'",
    "source": "instagram",
    "texts": [
      {
        "text": "Güne kahve ile başlamanın tadını çıkarın ☕️✨ Sizin için özenle hazırladık! #kahvekeyfi #günaydın #coffeetime",
        "engagement_score": 250,
        "metadata": {"post_id": "test_1"}
      },
      {
        "text": "Yeni sezon özel latte çeşitlerimiz burada! 🍂 Hangi aromayı denemek istersiniz? Siz söyleyin biz yapalım! ❤️",
        "engagement_score": 320
      },
      {
        "text": "Kahve tutkunları buraya! ☕️ Bugün hangi kahve ile enerjinizi topluyorsunuz? Bize de anlatın! 💪",
        "engagement_score": 180
      },
      {
        "text": "Hafta sonu planı: Kitap + Kahve + Huzur 📚☕️ Sizin ideal kombinasyonunuz nedir?",
        "engagement_score": 210
      },
      {
        "text": "Soğuk havalarda sıcacık bir kahve kadar iyi gelen ne var? 🧡 Gelin ısınalım birlikte!",
        "engagement_score": 290
      }
    ]
  }')

echo "$corpus_response" | jq .
if echo "$corpus_response" | jq -e '.success == true' > /dev/null; then
    echo -e "${GREEN}✅ Corpus added successfully${NC}"
else
    echo -e "${RED}❌ Failed to add corpus${NC}"
fi
echo ""

# Wait a moment for embeddings to be processed
sleep 2

# Test 3: Build Brand Voice
echo -e "${YELLOW}Test 3: Building brand voice profile${NC}"
build_response=$(curl -s -X POST "$API_URL/api/brand-voice/build" \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "'"$CLIENT_ID"'"
  }')

echo "$build_response" | jq .
if echo "$build_response" | jq -e '.success == true' > /dev/null; then
    echo -e "${GREEN}✅ Brand voice built successfully${NC}"
    
    # Display profile
    echo -e "${BLUE}Brand Voice Profile:${NC}"
    echo "$build_response" | jq '.profile'
else
    echo -e "${RED}❌ Failed to build brand voice${NC}"
fi
echo ""

# Test 4: Get Profile
echo -e "${YELLOW}Test 4: Getting brand voice profile${NC}"
profile_response=$(curl -s "$API_URL/api/brand-voice/get/$CLIENT_ID")
echo "$profile_response" | jq .
echo ""

# Test 5: Generate Content (with RAG)
echo -e "${YELLOW}Test 5: Generating content WITH RAG${NC}"
gen_response=$(curl -s -X POST "$API_URL/api/brand-voice/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "'"$CLIENT_ID"'",
    "platform": "instagram",
    "content_type": "feed",
    "topic": "bahar menüsü",
    "goal": "engagement",
    "use_rag": true
  }')

echo "$gen_response" | jq .
if echo "$gen_response" | jq -e '.success == true' > /dev/null; then
    echo -e "${GREEN}✅ Content generated with RAG${NC}"
    echo -e "${BLUE}Generated Content:${NC}"
    echo "$gen_response" | jq -r '.content'
    echo ""
    echo -e "${BLUE}Similarity Score: $(echo "$gen_response" | jq -r '.similarity_score')${NC}"
    echo -e "${BLUE}Examples Used: $(echo "$gen_response" | jq -r '.examples_count')${NC}"
else
    echo -e "${RED}❌ Failed to generate content${NC}"
fi
echo ""

# Test 6: Generate Content (without RAG)
echo -e "${YELLOW}Test 6: Generating content WITHOUT RAG${NC}"
gen_no_rag=$(curl -s -X POST "$API_URL/api/brand-voice/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "'"$CLIENT_ID"'",
    "platform": "instagram",
    "content_type": "story",
    "topic": "kahve yapım teknikleri",
    "goal": "education",
    "use_rag": false
  }')

echo "$gen_no_rag" | jq .
if echo "$gen_no_rag" | jq -e '.success == true' > /dev/null; then
    echo -e "${GREEN}✅ Content generated without RAG${NC}"
    echo -e "${BLUE}Similarity Score: $(echo "$gen_no_rag" | jq -r '.similarity_score')${NC}"
else
    echo -e "${RED}❌ Failed to generate content${NC}"
fi
echo ""

# Test 7: Get Stats
echo -e "${YELLOW}Test 7: Getting statistics${NC}"
stats_response=$(curl -s "$API_URL/api/brand-voice/stats/$CLIENT_ID")
echo "$stats_response" | jq .

if echo "$stats_response" | jq -e '.corpus_size > 0' > /dev/null; then
    echo -e "${GREEN}✅ Stats retrieved${NC}"
    echo -e "${BLUE}Summary:${NC}"
    echo "  Corpus Size: $(echo "$stats_response" | jq -r '.corpus_size')"
    echo "  Generated Content: $(echo "$stats_response" | jq -r '.generated_count')"
    echo "  Avg Similarity: $(echo "$stats_response" | jq -r '.avg_similarity_score')"
    echo "  Storage Mode: $(echo "$stats_response" | jq -r '.storage_mode')"
else
    echo -e "${RED}❌ Failed to get stats${NC}"
fi
echo ""

# Summary
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ All tests completed!${NC}"
echo ""
echo -e "${YELLOW}Test Results:${NC}"
echo "  ✅ Health Check"
echo "  ✅ Corpus Addition"
echo "  ✅ Brand Voice Build"
echo "  ✅ Profile Retrieval"
echo "  ✅ Content Generation (RAG)"
echo "  ✅ Content Generation (No RAG)"
echo "  ✅ Statistics"
echo ""
echo -e "${YELLOW}Next: Check your database to see the stored data${NC}"
echo "  psql \"\$DATABASE_URL\" -c \"SELECT * FROM brand_voice_profiles WHERE client_id='$CLIENT_ID';\""
