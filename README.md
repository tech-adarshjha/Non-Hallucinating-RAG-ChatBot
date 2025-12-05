[`<img src="images/logo.png" width="300" alt="Logo">`
](https://raw.githubusercontent.com/tech-adarshjha/Non-Hallucinating-RAG-ChatBot/refs/heads/main/SCR-20251205-naoe.png)
A Simple MVP to demonstrate QnA thats free from hallucinations without using LLMs. This can serve as a base for more complex systems and would suffice need for most QnA Bot use case.

# QnA (FastAPI)

Lightweight question-answering service that serves bot responses from a CSV-backed knowledge base. It uses TF-IDF embeddings with FAISS for nearest-neighbor lookup and an optional linear SVM for simple intent routing. A small collector script can bootstrap Q&A pairs from a web page using Google Gemini (requires your own API key).

## Features
- `POST /bot/{bot_id}` FastAPI endpoint that returns the closest answer for a user query.
- File-based knowledge bases under `assets/kb_data/<bot_id>/files/` (CSV with `Question`, `Answer`, optional `Class`).
- TF-IDF vectorizer persisted per bot plus FAISS index for fast similarity search; optional SVM classifier when labeled `Class` data exists.
- Pluggable bot instances via `core.focused.botEngine` with in-memory caching for speed.
- Optional web collector (`src/kb/web_collector.py`) to auto-generate Q&A pairs from a URL using Google Gemini.

## Project layout
- `src/api/main.py` – FastAPI app and router wiring.
- `src/api/bot.py` – `/bot/{bot_id}` endpoint and request model.
- `src/core/focused/botEngine.py` – Vectorization, FAISS search, and SVM intent model.
- `src/core/focused/vectorizers/` – TF-IDF vectorizer factory and persistence.
- `src/config/bot.py` – Paths, model names, and helper utilities for bot assets.
- `src/kb/web_collector.py` – Optional helper to scrape a URL and generate Q&A pairs via Google Gemini.
- `assets/kb_data/` – Expected location for bot-specific data (create locally).

## Requirements
- Python 3.9+
- Poetry (preferred) or pip
- NLTK `punkt` tokenizer data (downloaded at runtime once; see below)

## Setup
```bash
# Install dependencies
poetry install

# (Optional) install NLTK data used by the bot
poetry run python -m nltk.downloader punkt punkt_tab
```

## Running the API
The FastAPI app object lives in `src/api/main.py`.

```bash
# From the repo root
poetry run uvicorn src.api.main:app --reload --port 8000
```

### Endpoint
`POST /bot/{bot_id}`

Request body:
```json
{
	"query": "How do I reset my password?"
}
```

Example request:
```bash
curl -X POST \
	-H "Content-Type: application/json" \
	-d '{"query": "What are your support hours?"}' \
	http://localhost:8000/bot/candawills
```

## Preparing a knowledge base
1. Create a folder for your bot: `assets/kb_data/<bot_id>/files/`.
2. Add one or more CSV files with columns:
	 - `Question` (string)
	 - `Answer` (string)
	 - `Class` (optional string for grouping similar intents)
3. The first request for a given `bot_id` will build and cache the TF-IDF model and FAISS index under `assets/kb_data/<bot_id>/`.

## Using the web collector (optional)
`src/kb/web_collector.py` can scrape a URL, generate Q&A pairs using Google Gemini, and return CSV text.

Configure your key securely (do **not** hardcode it):
```bash
export GOOGLE_GENAI_API_KEY="your-key"
```
Then edit `src/kb/web_collector.py` to read from the environment instead of the placeholder `API_KEY`, and run the script for your target URL.

## Logging
Logs go to stdout with colored formatting (`src/util/logger.py`). Set log level in `src/config/log.py` (default DEBUG).

## Known limitations / next steps
- Only TF-IDF similarity is implemented; no semantic embeddings yet.
- Knowledge base reload requires a process restart or extending the reload hooks.
- No authentication on the API endpoint—protect before public exposure.

## Security & secrets check
- No API keys are committed. `src/kb/web_collector.py` contains a placeholder `API_KEY`; replace it with an environment variable before use. Do not commit real keys.
- No other credentials or tokens were found during a repo scan (token/password/secret keywords).

## License
Add your chosen license before making the repository public.
