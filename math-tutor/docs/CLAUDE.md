# Math Tutor Project — Session Context

**Owner:** Jeff (jeff@cruzdigitalconsulting.com)
**Last updated:** March 2026
**Purpose:** Preserve key decisions, architecture, and state for future Claude sessions

---

## About Jeff

- Age 39, husband, two kids: daughter (8, 3rd grade) and son (3)
- Lives in NYC
- Experienced with Streamlit app development (has two prior MLOps apps on GitHub)
- First Anthropic API key created for this project
- Has GitHub account: **JEFFCROOZ**

---

## Project: 3rd Grade Math Tutor (Math Stars)

### What It Is
A Streamlit app that tutors Jeff's 8-year-old daughter in Common Core 3rd grade math, preparing her for NYC standardized tests (NYS Math Assessment). Has both a child mode and a parent mode.

### Live Deployment
- **GitHub:** https://github.com/JEFFCROOZ/3rd-Grade-Math-Tutor
- **Streamlit Cloud:** https://3rd-grade-math-tutor-hwjkbvudfjpc6hydtwrosj.streamlit.app
- **Local path:** `/Users/jcmbair2021/Claude- Math Tutor/math-tutor/`

### Launch Command (local)
```bash
export ANTHROPIC_API_KEY=sk-ant-your-key-here
cd "/Users/jcmbair2021/Claude- Math Tutor"
/Users/jcmbair2021/opt/anaconda3/bin/streamlit run math-tutor/app.py
```

---

## Technical Stack

| Layer | Choice |
|---|---|
| Framework | Streamlit multi-page app |
| AI | Anthropic Claude API (`claude-sonnet-4-6`) |
| Language | Python 3.9 (Anaconda) |
| Persistence | File-based (`data/progress.json`) |
| Hosting | Streamlit Community Cloud (free tier) |

**Critical Python 3.9 constraint:** No `str | None` union type syntax — use bare return types or `Optional`. This bit us once already.

---

## App Structure

```
math-tutor/
├── app.py                      ← landing page + routing
├── pages/
│   ├── 1_Child_Home.py         ← topic grid for child
│   ├── 2_Child_Practice.py     ← practice state machine (most complex)
│   ├── 3_Child_Results.py      ← session summary + stars
│   ├── 4_Parent_Dashboard.py   ← progress overview
│   ├── 5_Parent_Review.py      ← problem-level review
│   └── 6_Parent_Concepts.py    ← Common Core explanations
├── utils/
│   ├── claude_client.py        ← API calls, problem generation prompt
│   ├── data_loader.py          ← fallback problems, topic config
│   ├── progress_store.py       ← read/write progress.json
│   └── styles.py               ← CSS injection, visual renderers
├── data/
│   └── progress.json           ← persistent progress (ephemeral on Streamlit Cloud)
└── docs/
    ├── 00-app-overview.md
    ├── 01-common-core-topics.md
    └── 02-deployment-guide.md
```

---

## Key Design Decisions

### 3-Attempt Wrong Answer System
Agreed and implemented. The progression per problem:

| Attempt | What the child sees | Buttons |
|---|---|---|
| 1st wrong | `explanation_child` — method only, **no answer** | Try Again · Next Problem · Stop |
| 2nd wrong | `hint_1` — Socratic pre-generated hint, no answer | Try Again · Next Problem · Stop |
| 3rd wrong | Answer revealed: "The answer is X." + explanation | Next Problem · Stop **only** |

- Try Again returns to answering state without resetting `wrong_attempts_count`
- One record per problem regardless of retries (`problem_recorded` flag pattern)
- `hint_1` is used on attempt 2 (pre-generated in same API call, zero extra cost)

### Scoring
- One attempt record per problem (not per wrong tap)
- `session_problems` only increments when problem is closed (correct or skipped)
- Stars = correct answers in session
- `record_attempt()` fires on: correct answer, or "Next Problem" clicked from wrong state

### Visual Rendering
All visuals are pure HTML/SVG — no chart libraries, no extra API calls. Rendered by `styles.py`.

| `visual_type` | Renderer | Used for |
|---|---|---|
| `array` | `render_array()` | 3.OA multiplication/division |
| `fraction` | `render_fraction_shape()` | 3.NF fractions |
| `number_line` | inline HTML | 3.NF, 3.NBT |
| `bar_graph` | `render_bar_graph()` | 3.MD data/graphing |
| `clock` | `render_clock()` SVG | 3.MD time problems |

**Important prompt constraint added:** Bar graph values in `visual_data.bars` must exactly match the numbers stated in `problem_text`. Never 0, never placeholders.

### File Path Fix
`progress.json` path is anchored to `__file__` in `progress_store.py`, not CWD. This makes the app work regardless of where `streamlit run` is executed from.

### API Cost
- Model: `claude-sonnet-4-6`
- ~500 tokens per problem call
- ~$0.0015 per problem (~$0.03 per 20-problem session)
- Fallback problems exist in `data_loader.py` — app never crashes if API is unavailable
- Jeff's monthly spend cap: $5 (set in Anthropic console)

---

## Streamlit Cloud Config

Secrets (set in Advanced Settings → Secrets):
```toml
ANTHROPIC_API_KEY = "sk-ant-..."
PARENT_PIN = "<jeff's chosen pin>"
```

**Note:** Streamlit Cloud free tier has ephemeral storage — `progress.json` resets on restart. Discussed but deferred: swap to Supabase free tier for persistent storage. This is a 30-minute change when Jeff is ready.

---

## Common Core Domain Reference

| Code | Domain | Key 3rd Grade Content |
|---|---|---|
| 3.OA | Operations & Algebraic Thinking | Multiplication, division, arrays, equal groups, word problems |
| 3.NBT | Number & Operations in Base Ten | Rounding to 10/100, add/subtract within 1000, multiply by multiples of 10 |
| 3.NF | Number & Operations — Fractions | Fractions as numbers on a number line, unit fractions, comparing fractions |
| 3.MD | Measurement & Data | Time to nearest minute, area, perimeter, bar graphs, picture graphs |
| 3.G | Geometry | Shape attributes (square is a rectangle), partitioning shapes into equal parts |

The domains are connected: Arrays (3.OA) → Area (3.MD) → Shape partitioning (3.G) → Fractions (3.NF) is one continuous thread.

---

## Bugs Fixed (for reference)

1. **Wrong answers revealing the answer** — Fixed `explanation_child` prompt instruction + all 9 fallback problem strings in `data_loader.py`
2. **Bar graph values showing 0** — Added explicit prompt constraint requiring bar values to match problem text
3. **No clock renderer** — Added SVG analog clock renderer in `styles.py`, added `clock` to allowed `visual_type` values
4. **No bar graph renderer** — Added HTML bar chart renderer in `styles.py`
5. **Python 3.9 type hints** — Removed `str | None` union syntax throughout
6. **CWD path mismatch** — Fixed `progress_store.py` to use `__file__`-anchored path

---

## Prior Projects (for pattern reference)

Jeff has two other Streamlit apps on GitHub (JEFFCROOZ):
- **ML-Model-Flow-App** — Movie recommendation engine, SVD + cosine similarity, CSV-based, no API calls
- **ML-MLOps-Part2** — MLOps educational dashboard, hardcoded content, no API calls

Both are "closed systems" — no external API calls, no ongoing cost. The Math Tutor is the first "open system" app using a live AI API.

---

## Open Questions / Future Decisions

- **Persistent storage:** Replace file-based `progress.json` with Supabase for survival across Streamlit Cloud restarts (deferred)
- **Model swap option:** Switch to `claude-haiku-4-5-20251001` in `claude_client.py` for ~10x cost reduction if needed
- **iPad native app:** Discussed but deferred — Streamlit via Safari on iPad is the current approach
- **Agent / MCP expansion:** Jeff is interested in building a personal life agent (school email triage, health memory, grocery tracking, gift tracking) — to be explored in future sessions
