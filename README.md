# news-agent

A small AI agent that follows news on a topic you choose: it reads RSS feeds, opens the relevant articles and writes a short digest. It runs locally with [Ollama](https://ollama.com).

> **Educational project.** Built for learning purposes: to practice building an AI agent from scratch (tool calling, an agent loop, persistent memory).

The digest is written in Bulgarian, so the project is designed and tuned to work in Bulgarian.
## How it works

The agent runs a loop: the model decides which tool to call (`fetch_feed`, `read_article`), the code executes it and returns the result, and this repeats until the model produces the final digest.

A SQLite database remembers which articles were already processed, so the same news is not reported twice, and stores the generated digests.

## Requirements

- Python 3.13
- [uv](https://docs.astral.sh/uv/)
- Ollama running locally with a tool-calling model (default: `qwen3:8b`)
- SQLite (`sqlite3` CLI, preinstalled on macOS)

## Setup

```bash
uv sync
ollama pull qwen3:8b
```

Create the database once. The application does not create it; it only reads from and writes to it.

```bash
mkdir -p data
sqlite3 data/news.db < schema.sql
sqlite3 data/news.db ".tables"   # should list: digests  seen_articles
```

## Run

```bash
uv run python -m news_agent.agent
```

Topic and sources are currently constants in `src/news_agent/agent.py`.

## Structure

```
schema.sql          # database schema, run once during setup
data/               # news.db lives here (git-ignored)
src/news_agent/
├── llm.py          # the only place that talks to Ollama
├── agent.py        # the agent loop and system prompt
├── db.py           # SQLite memory: seen articles and saved digests
└── tools/
    ├── __init__.py # tool registry and runner
    ├── feeds.py    # fetch_feed: latest articles from an RSS feed
    └── reader.py   # read_article: clean text of an article
```
