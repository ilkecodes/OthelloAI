# Othello AI Marketing Platform

AI-powered social media intelligence and content generation platform for Instagram marketing.

## Features

- **Trend Scanning**: Real-time Instagram trend analysis using Apify
- **Deep Content Analysis**: AI-powered pattern recognition in high-performing posts
- **Brand Voice Learning**: Automatic brand personality extraction from Instagram profiles
- **Smart Content Generation**: AI creates on-brand content based on winning patterns
- **Strategic Insights**: Actionable recommendations based on data analysis

## Tech Stack

**Backend:**
- FastAPI (Python)
- PostgreSQL
- OpenAI GPT-4
- Apify API
- SQLAlchemy

**Frontend:**
- React + Vite
- Lucide Icons

## Setup

### Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
docker-compose up -d
uvicorn app.main:app --reload

### Frontend
cd frontend
npm install
npm run dev

## Environment Variables

Backend `.env`:
DATABASE_URL=postgresql://othello:othello123@localhost:5432/othello_ai
OPENAI_API_KEY=your_openai_key
APIFY_API_TOKEN=your_apify_token

Frontend `.env`:
VITE_API_URL=http://localhost:8000/api

## API Documentation

- API Docs: http://localhost:8000/docs
- Frontend: http://localhost:5173

## License

Private project for Othello Digital clients.
