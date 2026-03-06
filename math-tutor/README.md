# 3rd Grade Math Tutor ⭐

A Streamlit app for NYC 3rd grade Common Core math practice — built for an 8-year-old preparing for the NYS Math Assessment, with a parent dashboard on the side.

## What It Does

**Child Mode** — Your daughter picks a topic, gets AI-generated practice problems, asks for hints (Socratic — never just gives the answer), earns stars for correct answers, and sees a session summary when she stops.

**Parent Mode** — PIN-protected. You see her progress by topic, set a focus area, learn Common Core methods in plain adult language, and review every wrong answer with on-demand explanations.

## NYC 3rd Grade Topics Covered

| Standard | Topic |
|---|---|
| 3.OA | Multiplication & Division (arrays, word problems, properties) |
| 3.NBT | Numbers to 1,000 (rounding, add/subtract, multiply by 10s) |
| 3.NF | Fractions (parts of a whole, number lines, comparing) |
| 3.MD | Measurement & Data (time, area & perimeter, graphs) |
| 3.G | Shapes (attributes, partitioning into equal areas) |

## Tech Stack

- Python 3.9+
- Streamlit ≥ 1.32
- Anthropic Claude API (`claude-sonnet-4-6`)
- File-based progress persistence (`data/progress.json`)

## Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/JEFFCROOZ/3rd-Grade-Math-Tutor.git
cd 3rd-Grade-Math-Tutor

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your API key
export ANTHROPIC_API_KEY=sk-ant-your-key-here

# 4. Run
streamlit run app.py
```

Open `http://localhost:8501` in any browser — including iPad Safari on your local network.

## Streamlit Cloud Deployment

1. Push this repo to GitHub (already done)
2. Go to [share.streamlit.io](https://share.streamlit.io) → New app
3. Select this repo, branch `main`, entry file `app.py`
4. Under **Advanced settings → Secrets**, add:

```toml
ANTHROPIC_API_KEY = "sk-ant-your-key-here"
PARENT_PIN = "your-pin-here"
```

> ⚠️ **Important:** Streamlit Community Cloud has ephemeral storage — `data/progress.json` resets when the app restarts or redeploys. For persistent progress tracking, run the app locally instead.

## Configuration

| Setting | Where | Default |
|---|---|---|
| Parent PIN | `utils/data_loader.py` → `PARENT_PIN` or Streamlit secrets | `1234` |
| Claude model | `utils/claude_client.py` → `MODEL` | `claude-sonnet-4-6` |
| Progress file | `data/progress.json` | Auto-created on first run |

## Project Structure

```
├── app.py                    # Entry point — mode selector
├── pages/
│   ├── 1_Child_Home.py       # Topic picker
│   ├── 2_Child_Practice.py   # Practice loop + hints
│   ├── 3_Child_Results.py    # Session summary
│   ├── 4_Parent_Dashboard.py # Progress overview
│   ├── 5_Parent_Concepts.py  # Common Core explainer
│   └── 6_Parent_Review.py    # Wrong answer review
├── utils/
│   ├── styles.py             # CSS + component helpers
│   ├── data_loader.py        # Topics, fallback problems
│   ├── claude_client.py      # Anthropic API calls
│   └── progress_store.py     # File-based persistence
└── data/
    └── progress.json         # Auto-created, gitignored
```
