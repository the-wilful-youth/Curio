# Curio — Personal AI Content Vault

> **Capture once. Understand automatically. Store permanently. Act when necessary. Find it later.**

A private, single-user system for capturing, extracting, and understanding content from YouTube, websites, event pages, articles, and more. Curio automatically extracts structured summaries, preserves images, detects events & deadlines, organizes action items, and lets you query your personal knowledge base using conversational AI.

---

## Key Features

- **Multi-Source Extraction**: Intelligent article and YouTube extraction powered by `trafilatura` and `yt-dlp`.
- **Automated Insights**: Generates titles, summaries, topic categories, and key facts.
- **Event & Deadline Detection**: Chronological calendar view with confidence scoring and calendar scheduling.
- **Action Item Tracker**: Tracks tasks with priorities and quick completion toggles.
- **Fast Search**: Instant keyword search across all saved content with automatic debouncing.
- **Ask My Vault (AI Chat)**: Grounded conversational Q&A over your saved library.
- **Flexible Storage**: Zero-config SQLite for instant local development; PostgreSQL + pgvector for production deployments.

---

## Quick Start (Local Development)

### 1. Prerequisites
- Python 3.11+
- Node.js 18+ and npm

### 2. Configure Environment
```bash
cp .env.example .env
```

Curio supports open-weights models out of the box with any of the following providers:
- **Groq** (Llama 3.3 70B, Mixtral): Set `GROQ_API_KEY=gsk_...`
- **OpenRouter** (Llama 3.3, DeepSeek, Qwen, Mistral): Set `OPENROUTER_API_KEY=sk-or-...`
- **Together AI** (Open source models): Set `TOGETHER_API_KEY=...`
- **Local Ollama / vLLM / LM Studio**: Set `AI_BASE_URL=http://localhost:11434/v1`
*(You can also set `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` if desired).*

### 3. Run Everything with One Command
```bash
./dev.sh
```
This starts both the FastAPI backend and Next.js frontend concurrently:
- **Frontend Web UI**: [http://localhost:3000](http://localhost:3000)
- **FastAPI Backend**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive Swagger Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Docker Deployment (Production / Full Stack)

To run the full stack with PostgreSQL, pgvector, and Redis:

```bash
./start.sh
```

To stop all services:
```bash
./stop.sh
```

---

## Running Tests

Run the in-process API test suite:
```bash
cd backend
python3 test_api.py
```

Run frontend typecheck and production build:
```bash
cd frontend
npm run build
```

---

## Project Structure

```
Curio/
├── backend/
│   ├── app/
│   │   ├── ai/            # OpenAI & Anthropic provider implementations
│   │   ├── api/v1/        # REST endpoints (sources, notes, events, deadlines, tasks, chat, search, tags)
│   │   ├── extractors/    # Web & YouTube extractors (trafilatura, yt-dlp, BeautifulSoup)
│   │   ├── workers/       # Unified processing pipeline & Celery tasks
│   │   ├── config.py      # Pydantic v2 settings & configuration
│   │   ├── database.py    # SQLAlchemy database engine & auto-init
│   │   ├── models.py      # Database models (User, Source, ContentItem, Note, Event, Deadline, ActionItem, Tag)
│   │   └── schemas.py     # Pydantic v2 request/response schemas
│   ├── celery_worker.py   # Celery worker entrypoint
│   ├── requirements.txt   # Python dependencies
│   └── test_api.py        # Automated API test suite
├── frontend/
│   ├── src/app/           # Next.js App Router (Dashboard, Library, Calendar, Tasks, Search, Chat)
│   ├── next.config.ts     # Next.js configuration & API proxy rewrites
│   └── package.json       # Node.js dependencies & scripts
├── prompts/               # System prompts for structured analysis & extraction
├── dev.sh                 # Fast local development runner
├── start.sh               # Docker Compose launcher
├── stop.sh                # Docker Compose shutdown script
└── docker-compose.yml     # Multi-container orchestration (Frontend, Backend, Celery, Postgres pgvector, Redis)
```