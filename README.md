# AI Assistant (Telegram + Local RAG)

This project pulls recent Telegram messages, stores them in SQLite, builds a FAISS vector store, and answers user queries with a local Mistral GGUF model.

## Features

- Fetches Telegram DMs from the last 24 hours
- Stores messages in local SQLite tables per user
- Builds semantic embeddings with SentenceTransformers
- Retrieves relevant chunks via FAISS similarity search
- Generates final answers using local `llama-cpp-python`

## Project Structure

- `main.py`: End-to-end entry point
- `api_telegram/telegram_listener.py`: Telegram data ingestion
- `database/database.py`: SQLite table operations
- `vec_dbs/vec_db.py`: Vector store build logic
- `vec_dbs/query.py`: Semantic retrieval
- `llm/mistral_runner.py`: Local LLM response generation

## Requirements

- Python 3.10+
- Telegram API credentials (from https://my.telegram.org)
- Local model file at `models/mistral-7b-instruct-v0.1.Q4_K_M.gguf`

## Model Download

1. Create a `models` folder in the project root if it does not exist.
2. Download a GGUF model file (for example, Mistral 7B Instruct GGUF) from a trusted source such as Hugging Face.
3. Place the downloaded file in the `models` folder.
4. If you use the current default setup, keep this filename:
	- `models/mistral-7b-instruct-v0.1.Q4_K_M.gguf`

### Change Model Later

You can switch models at any time:

1. Download a different GGUF model.
2. Put it inside the `models` folder.
3. Update `model_path` in `llm/mistral_runner.py` to point to the new file.

Example:

```python
model_path="models\\your-new-model.gguf"
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Setup

1. Copy `.env.example` to `.env`.
2. Fill in your real credentials:

```env
TELEGRAM_API_ID=your_telegram_api_id
TELEGRAM_API_HASH=your_telegram_api_hash
TELEGRAM_SESSION_NAME=session_default
```

## Run

```bash
python main.py
```

## Security Notes

- Do not commit `.env`.
- Do not commit `*.session`, `*.db`, or model binaries.
- Rotate Telegram credentials if they were ever committed publicly.

