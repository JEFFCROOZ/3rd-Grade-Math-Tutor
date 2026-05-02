# Grade 3 to 4 Math Bridge ⭐

A Streamlit app for a summer math bridge between third and fourth grade in NYC-style elementary math instruction.

It keeps the original child-and-parent split:

- **Child mode**: pick a topic, solve practice problems, ask for hints, earn stars, and end each session with a simple summary.
- **Parent mode**: review progress, set a focus topic, learn the method in plain language, and inspect wrong answers.

## What Changed

This project now focuses on a **two-lane summer bridge**:

- **Grade 3 Review**: reinforce the third grade foundations that need to feel solid before school starts.
- **Grade 4 Preview**: preview the big ideas that will show up in fourth grade.

The live AI layer now uses the **OpenAI Responses API** instead of Anthropic. The default model is `gpt-5-mini`, chosen for fast, lower-cost structured problem generation. OpenAI recommends the Responses API for new projects. Sources: [Responses migration guide](https://developers.openai.com/api/docs/guides/migrate-to-responses), [Responses API reference](https://platform.openai.com/docs/api-reference/responses/list?lang=python), [GPT-5 mini model page](https://platform.openai.com/docs/models/gpt-5-mini/)

## Topic Coverage

### Grade 3 Review

| Standard | Topic |
|---|---|
| 3.OA | Multiplication & Division Review |
| 3.NBT | Place Value to 1,000 Review |
| 3.NF | Fractions Review |
| 3.MD | Measurement & Data Review |
| 3.G | Shapes Review |

### Grade 4 Preview

| Standard | Topic |
|---|---|
| 4.OA | Operations & Problem Solving |
| 4.NBT | Place Value & Big Numbers |
| 4.NF | Fractions & Decimals |
| 4.MD | Measurement, Data & Angles |
| 4.G | Geometry Preview |

## Tech Stack

- Python 3.9+
- Streamlit >= 1.32
- OpenAI Responses API
- Default model: `gpt-5-mini`
- Progress persistence:
  - local file storage in `data/progress.json`
  - optional Postgres storage when `DATABASE_URL` is set

## Run Locally

```bash
# Clone the repo
git clone https://github.com/JEFFCROOZ/3rd-Grade-Math-Tutor.git
cd 3rd-Grade-Math-Tutor/math-tutor

# Install dependencies
pip install -r requirements.txt

# Set your OpenAI API key
export OPENAI_API_KEY=your-key-here

# Optional: choose a different model
export OPENAI_MODEL=gpt-5-mini

# Run
streamlit run app.py
```

Open `http://localhost:8501` in a browser. On the same WiFi network, you can also use the local network URL on an iPad.

## Streamlit Cloud Deployment

Add these secrets in Streamlit Community Cloud:

```toml
OPENAI_API_KEY = "your-key-here"
OPENAI_MODEL = "gpt-5-mini"
PARENT_PIN = "your-pin-here"
```

Optional, for persistent cloud progress:

```toml
DATABASE_URL = "postgres://..."
```

Without `DATABASE_URL`, the app still works correctly, but file-based progress on Streamlit Cloud can reset because the filesystem is ephemeral.

## Configuration

| Setting | Where | Default |
|---|---|---|
| Parent PIN | `utils/data_loader.py` or Streamlit secrets | `1234` |
| OpenAI model | `OPENAI_MODEL` env/secrets or `utils/openai_client.py` | `gpt-5-mini` |
| Progress file | `data/progress.json` | auto-created on first run |
| Database backend | `DATABASE_URL` env/secrets | off by default |

## Project Structure

```text
├── app.py
├── pages/
│   ├── 1_Child_Home.py
│   ├── 2_Child_Practice.py
│   ├── 3_Child_Results.py
│   ├── 4_Parent_Dashboard.py
│   ├── 5_Parent_Concepts.py
│   └── 6_Parent_Review.py
├── utils/
│   ├── data_loader.py
│   ├── openai_client.py
│   ├── progress_store.py
│   └── styles.py
└── data/
    └── progress.json
```

## Repo Name Note

The GitHub repository is still named `3rd-Grade-Math-Tutor` for continuity, but the app itself is now the `Grade 3 to 4 Math Bridge`.
