# 02 — Deployment Guide

> How to run locally (for persistent progress) and how to deploy to Streamlit Community Cloud.

---

## Option A: Run Locally (Recommended for Progress Tracking)

Running locally means progress persists in `data/progress.json` across sessions. This is the best option for regular use.

### Requirements
- Python 3.9+
- Anaconda or pip
- An Anthropic API key

### Setup

```bash
git clone https://github.com/JEFFCROOZ/3rd-Grade-Math-Tutor.git
cd 3rd-Grade-Math-Tutor
pip install -r requirements.txt
```

### Set your API key

**macOS (terminal):**
```bash
export ANTHROPIC_API_KEY=sk-ant-your-key-here
```

To make it permanent, add that line to `~/.zshrc` or `~/.bash_profile`.

### Run the app
```bash
streamlit run app.py
```

### Access on iPad (same WiFi network)
When the app starts, the terminal shows:
```
Network URL: http://192.168.1.x:8501
```
Open that URL in iPad Safari. Works on any device on the same WiFi network.

---

## Option B: Streamlit Community Cloud (Free Hosting)

> ⚠️ **Ephemeral storage warning:** Streamlit Community Cloud does not have persistent file storage. `data/progress.json` will reset whenever the app restarts, sleeps, or is redeployed. Progress will not survive between sessions. If tracking progress over time matters, use Option A (local) instead.

The app will still work correctly on Streamlit Cloud — problems generate, hints work, stars show during a session — but the history won't persist.

### Steps

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account (JEFFCROOZ)
3. Click **New app**
4. Select:
   - Repository: `JEFFCROOZ/3rd-Grade-Math-Tutor`
   - Branch: `main`
   - Main file path: `app.py`
5. Click **Advanced settings**
6. Under **Secrets**, add:

```toml
ANTHROPIC_API_KEY = "sk-ant-your-key-here"
PARENT_PIN = "your-chosen-pin"
```

7. Click **Deploy**

The app will build and be live at a public URL like `https://your-app-name.streamlit.app`.

---

## Secrets Reference

| Secret | Required | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | Yes (for live problems) | Your Anthropic API key. Without it, the app falls back to static practice problems. |
| `PARENT_PIN` | No | Overrides the default PIN (`1234`). Set this before sharing the app URL. |

### Local secrets (alternative to environment variable)

You can also create `.streamlit/secrets.toml` for local development:

```toml
ANTHROPIC_API_KEY = "sk-ant-your-key-here"
PARENT_PIN = "your-pin"
```

This file is gitignored and will not be committed.

---

## Changing the Parent PIN

Three ways, in order of preference:

1. **Streamlit Cloud:** Set `PARENT_PIN` in the app secrets (see above)
2. **Local with secrets.toml:** Add `PARENT_PIN = "your-pin"` to `.streamlit/secrets.toml`
3. **Direct edit:** Change `PARENT_PIN = "1234"` in `utils/data_loader.py`

---

## Upgrading to Persistent Cloud Storage

If persistent progress tracking on the cloud becomes a priority, the upgrade path is:

1. Add `supabase-py` or `pymongo` to `requirements.txt`
2. Replace `utils/progress_store.py` read/write functions with database calls
3. Add database connection string to Streamlit secrets

The rest of the app doesn't need to change — all database interaction is isolated in `progress_store.py`.
