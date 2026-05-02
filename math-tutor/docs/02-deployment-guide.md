# 02 — Deployment Guide

How to run locally and how to deploy while keeping the current persistence options.

## Option A: Run Locally

Recommended if you want the simplest setup with persistent file-based progress.

### Requirements

- Python 3.9+
- `pip`
- an OpenAI API key

### Setup

```bash
git clone https://github.com/JEFFCROOZ/3rd-Grade-Math-Tutor.git
cd 3rd-Grade-Math-Tutor/math-tutor
pip install -r requirements.txt
```

### Set your API key

macOS:

```bash
export OPENAI_API_KEY=your-key-here
```

Optional:

```bash
export OPENAI_MODEL=gpt-5-mini
```

### Run

```bash
streamlit run app.py
```

### iPad access on the same WiFi

When Streamlit starts, copy the `Network URL` into Safari on the iPad.

## Option B: Streamlit Community Cloud

The app can be deployed to Streamlit Cloud.

### Important storage note

If you do **not** set `DATABASE_URL`, then hosted progress may reset because Streamlit Cloud does not guarantee durable local file storage between restarts.

If you **do** set `DATABASE_URL`, the app will use Postgres for persistent progress.

### Secrets

At minimum:

```toml
OPENAI_API_KEY = "your-key-here"
OPENAI_MODEL = "gpt-5-mini"
PARENT_PIN = "your-pin"
```

Optional persistent storage:

```toml
DATABASE_URL = "postgres://..."
```

## Local `.streamlit/secrets.toml`

You can also create local secrets instead of exporting env vars:

```toml
OPENAI_API_KEY = "your-key-here"
OPENAI_MODEL = "gpt-5-mini"
PARENT_PIN = "your-pin"
DATABASE_URL = "postgres://..."
```

`DATABASE_URL` is optional.

## Current Model Layer

The app uses the OpenAI Responses API through `utils/openai_client.py`.

Default model:

- `gpt-5-mini`

Override options:

- `OPENAI_MODEL` environment variable
- `OPENAI_MODEL` in Streamlit secrets

## Persistence Behavior Summary

### No `DATABASE_URL`

- local runs: file-based persistence in `data/progress.json`
- hosted runs: works, but progress may not survive restarts

### With `DATABASE_URL`

- local runs: database-backed persistence
- hosted runs: database-backed persistence

This preserves the current dual-path behavior rather than forcing one storage method.
