# AI News Aggregator

AI News Aggregator is a Python 3.12 app that collects AI-related articles from RSS feeds, summarizes them with a pluggable LLM provider, stores results in PostgreSQL, and delivers a daily digest by email. It also includes a FastAPI web interface for browsing articles and managing subscriptions.

## Features

- Aggregates AI news from curated RSS sources
- Summarizes article content with OpenAI, Anthropic, or Ollama
- Stores articles and subscribers in PostgreSQL
- Sends email digests to subscribed users
- Exposes a FastAPI UI and JSON API
- Includes a scheduled daily pipeline
- Supports local Docker-based development

## How It Works

The pipeline is split into three stages:

1. Ingestion: fetches articles from configured RSS feeds
2. Processing: summarizes unsummarized articles with the selected AI provider
3. Delivery: sends the latest summarized articles to subscribers by email

Main flow:

- [`app/services/ingestion_service.py`](/Users/rahulchauhan/PythonProjects/ai-news-aggregator/app/services/ingestion_service.py)
- [`app/services/processing_service.py`](/Users/rahulchauhan/PythonProjects/ai-news-aggregator/app/services/processing_service.py)
- [`app/services/email_service.py`](/Users/rahulchauhan/PythonProjects/ai-news-aggregator/app/services/email_service.py)
- [`app/jobs/daily_pipeline.py`](/Users/rahulchauhan/PythonProjects/ai-news-aggregator/app/jobs/daily_pipeline.py)

## Tech Stack

- Python 3.12
- FastAPI
- SQLAlchemy
- PostgreSQL
- APScheduler
- `uv` for dependency management
- OpenAI, Anthropic, or Ollama for summarization

## Project Structure

```text
app/
  agents/      Agent wrappers around AI provider behavior
  ai/          Provider implementations and factory
  config/      Settings and source feed lists
  database/    DB connection, models, repository helpers
  jobs/        Scheduled and batch pipeline jobs
  scrapers/    Feed/content ingestion logic
  services/    Ingestion, processing, and email delivery
  templates/   FastAPI HTML templates
  web.py       FastAPI application
run.py         Simple pipeline entrypoint
Dockerfile     Container image build
docker-compose.yaml
```

## Prerequisites

- Python 3.12+
- PostgreSQL
- `uv` installed locally, or Docker + Docker Compose
- At least one AI provider configured
- Gmail account with an app password if you want email delivery

## Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/newsdb

AI_PROVIDER=openai

OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
OLLAMA_URL=http://localhost:11434

EMAIL=your_email@gmail.com
EMAIL_APP_PASSWORD=your_gmail_app_password
```

Notes:

- `AI_PROVIDER` supports `openai`, `anthropic`, or `ollama`
- The current settings module expects all listed variables to exist, even if you only use one provider
- The default OpenAI model is `gpt-4o-mini`
- The default Anthropic model is `claude-3-haiku-20240307`
- The default Ollama model is `llama3:8b`

## Local Setup

Install dependencies:

```bash
uv sync
```

Run the web app:

```bash
uv run uvicorn app.web:app --reload
```

The app will be available at `http://127.0.0.1:8000`.

Run the full pipeline once:

```bash
uv run python run.py
```

Run the scheduler:

```bash
uv run python -m app.jobs.scheduler
```

## Docker Setup

Start the application and PostgreSQL:

```bash
docker compose up --build
```

Services:

- App: `http://localhost:8000`
- PostgreSQL: `localhost:5432`
- pgAdmin: `http://localhost:8081`

The container starts the FastAPI app with:

```bash
uv run uvicorn app.web:app --host 0.0.0.0 --port 8000
```

## Web Endpoints

- `GET /` renders the latest summarized news
- `GET /subscribe` renders the subscription form
- `POST /subscribe` subscribes an email address
- `POST /unsubscribe` unsubscribes an email address
- `GET /admin/subscribers` lists active subscribers
- `POST /admin/send-newsletter` sends the latest digest to all subscribers
- `GET /api/news` returns summarized articles as JSON

## Data Sources

Configured feeds live in [`app/config/sources.py`](/Users/rahulchauhan/PythonProjects/ai-news-aggregator/app/config/sources.py) and currently include:

- OpenAI
- Anthropic
- Google AI
- DeepMind
- arXiv `cs.AI`
- MIT Technology Review
- TechCrunch AI
- VentureBeat AI
- The Verge

## AI Provider Selection

Provider resolution happens in [`app/ai/factory.py`](/Users/rahulchauhan/PythonProjects/ai-news-aggregator/app/ai/factory.py).

Set:

```env
AI_PROVIDER=openai
```

Valid values:

- `openai`
- `anthropic`
- `ollama`

## Development

Install dev dependencies:

```bash
uv sync --dev
```

Run tests:

```bash
uv run pytest
```

Format code:

```bash
uv run black .
```

Lint code:

```bash
uv run ruff check .
```

## Current Caveats

- The settings loader reads all environment variables eagerly, so missing unused provider keys can still raise startup errors
- Email delivery is hardcoded to Gmail SMTP
- The scheduler is configured for `hour=9` and uses the host/container timezone
- The web app runs ingestion and processing on startup, which can make startup slower

## License

Add a license section here if you plan to open-source or distribute the project.
