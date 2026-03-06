# Math Tutor App — Implementation Plan

## Context
Parent (age 39) is comfortable with math but unfamiliar with Common Core methods (arrays, area models, number bonds). His 8-year-old daughter is preparing for NYC standardized tests (NYS Math Assessment, 3rd grade). Goal: a Streamlit app that lives on the iPad (Safari), has a child-facing practice mode and a parent-facing dashboard/learning mode, and uses Claude API for both tutoring and problem generation.

Follows the patterns established in `/Users/jcmbair2021/Claude- MLOps/mlops-part2/` exactly.

---

## Directory Structure

```
math-tutor/
├── app.py                          # Entry: mode selector (Child vs Parent PIN)
├── requirements.txt                # streamlit>=1.32.0, anthropic>=0.25.0
├── .env                            # ANTHROPIC_API_KEY (local dev)
├── .streamlit/
│   └── config.toml                 # Light/warm theme (replaces dark)
├── data/
│   └── progress.json               # File-based persistence (auto-created)
├── pages/
│   ├── 1_Child_Home.py             # Topic picker, star count, focus badge
│   ├── 2_Child_Practice.py         # Active problem loop + hint system
│   ├── 3_Child_Results.py          # Session summary, stars earned
│   ├── 4_Parent_Dashboard.py       # Progress charts, weak topics, focus setter
│   ├── 5_Parent_Concepts.py        # Common Core explainer (streaming)
│   └── 6_Parent_Review.py          # Browse wrong answers, on-demand explanation
└── utils/
    ├── __init__.py
    ├── styles.py                   # inject_global_css() + all component helpers
    ├── data_loader.py              # Topics dict, encouragement messages, fallback problems
    ├── claude_client.py            # All Anthropic API calls
    └── progress_store.py           # Atomic JSON read/write
```

---

## Page Breakdown

### `app.py` — Entry / Mode Gate
- `set_page_config` + `inject_global_css()` + session state routing guards
- Two big buttons: "I'm Ready to Practice!" → sets `child_active=True`, `switch_page(1_Child_Home)`
- "Parent Login" → PIN input (4-digit), on success sets `parent_active=True`, `switch_page(4_Parent_Dashboard)`
- PIN stored in `data_loader.py` as `PARENT_PIN`, overridden by `st.secrets` for cloud deploy

### `pages/1_Child_Home.py` — Child Topic Picker
- `require_child_auth()` guard
- Large star count display at top
- 2-column grid of topic cards (3.OA, 3.NBT, 3.NF, 3.MD, 3.G) with emoji + mini progress bar
- Parent-set focus topic shows a badge: "Your parent wants you to practice this one!"
- "Mix It Up!" for random topic
- On card click: sets `selected_topic` in session state → `switch_page(2_Child_Practice)`

### `pages/2_Child_Practice.py` — Active Practice Loop (core page)
State machine via `st.session_state.practice_state`:
- `loading` → spinner ("Thinking of a good one...") → call `generate_problem()` → `answering`
- `answering` → show problem + visual + 4 answer buttons (2x2 grid) + Hint button
- `hint_shown` → show hint card, answers still available
- `answered_correct` → gold celebration card, record attempt, "Next Problem" button
- `answered_wrong` → gentle amber card + child explanation, record attempt, "Try Again" / "Next Problem"

**Critical:** Only trigger `generate_problem()` when `practice_state == "loading"`. Never on rerun.

### `pages/3_Child_Results.py` — Session Summary
- Stars earned this session as large emoji row (`"⭐" * n`)
- Problems tried, accuracy, encouraging message from `get_encouragement(pct)`
- "Keep Going!" → `1_Child_Home` | "See You Later!" → clears session → `app.py`

### `pages/4_Parent_Dashboard.py` — Parent Progress View
- `require_parent_auth()` guard
- 3 metrics: Total Stars, Problems Attempted, Overall Accuracy
- Topic breakdown: accuracy % per domain, flag weak topics (<60%) in amber
- Topic focus setter: `st.selectbox()` → writes to `progress.json` via `set_focus_topic()`
- Recent sessions list (last 5)
- Nav to `5_Parent_Concepts` and `6_Parent_Review`

### `pages/5_Parent_Concepts.py` — Common Core Explainer
- Topic + subtopic selectors
- "Explain This To Me" button → `st.write_stream(explain_concept_for_parent(topic))`
- Two sections in streamed response: "What This Method Is" + "How to Practice at Home"
- Adult language, no condescension, explains the *why* behind the method

### `pages/6_Parent_Review.py` — Wrong Answer Review
- Filter by topic, list wrong attempts with problem + what she answered + correct answer
- "Explain this problem" per item → on-demand Claude call (parent-level detail)

---

## Utils Modules

### `utils/styles.py`
Mirrors MLOps pattern exactly. Key additions:
- `inject_global_css()` — warm light theme, Nunito font (child), Inter (parent)
- `require_child_auth()` / `require_parent_auth()` — redirect guards
- `topic_card(key, title, emoji, attempted, stars)` → HTML string
- `star_display(count)` → HTML emoji row
- `problem_card(text, visual_html)` → styled problem box
- `feedback_correct(msg)` → green card | `feedback_wrong(msg)` → amber card (not red)
- `hint_card(text)` → blue hint bubble
- `render_array(rows, cols, emoji)` → emoji grid HTML — rendering in Python, not from Claude
- `render_fraction_rectangle(numerator, denominator)` → HTML fraction visual

### `utils/data_loader.py`
No Streamlit imports. Pure data:
- `PARENT_PIN = "1234"` (change before use)
- `TOPICS` dict — keys: 3OA, 3NBT, 3NF, 3MD, 3G; values: label, emoji, subtopics, standard
- `ENCOURAGEMENT_MESSAGES` list (10 entries)
- `get_fallback_problem(topic_key)` — 2-3 hardcoded problems per topic (API failure path)
- `get_encouragement(accuracy_pct)` → string

### `utils/claude_client.py`
```python
CLIENT = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env
API_AVAILABLE = True  # set False if key missing — all functions return fallbacks
```
Functions:
- `generate_problem(topic_key, subtopic, difficulty)` → dict (JSON schema enforced via system prompt)
- `get_hint(problem_dict, attempt_count)` → str (Socratic, never reveals answer)
- `explain_concept_for_parent(topic_key, subtopic)` → generator (for `st.write_stream`)
- `explain_wrong_answer_for_parent(problem_dict, wrong_answer)` → str

**Problem JSON schema** (Claude must return ONLY this):
```json
{
  "problem_text": "...",
  "answer": "...",
  "distractors": ["...", "...", "..."],
  "visual_type": "array|fraction|number_line|shape|none",
  "visual_data": {},
  "hint_1": "...",
  "explanation_child": "...",
  "explanation_parent": "..."
}
```
Validate response: all 7 keys present, 3 distractors, answer not in distractors. Retry once on failure, then fallback.

All API calls wrapped in try/except. Never let an API failure crash the child's session.

### `utils/progress_store.py`
- `load_progress()` → dict (returns default schema if file missing)
- `save_progress(data)` — atomic write via `os.replace(tmp, PROGRESS_FILE)`
- `record_attempt(topic_key, subtopic, problem_dict, user_answer, is_correct, hint_used)`
- `get_all_stats()`, `get_topic_stats(topic_key)`, `get_recent_sessions(n=5)`
- `get_wrong_attempts(topic_key=None)` — for parent review
- `get_star_count()`, `set_focus_topic(topic_key)`, `get_focus_topic()`
- `sessions` capped at 30, `wrong_attempts` capped at 100

---

## Session State Schema
```python
# Entry
child_active: bool
parent_active: bool

# Child navigation
selected_topic: str        # e.g. "3OA"
selected_subtopic: str

# Practice loop
practice_state: str        # "loading"|"answering"|"hint_shown"|"answered_correct"|"answered_wrong"
current_problem: dict
current_answer_choices: list   # shuffled [answer + distractors]
hint_count: int
current_hint: str
wrong_attempts: int
session_problems: int
session_correct: int
session_stars: int
```

Sign-out: `st.session_state.pop(key, None)` for each key in list (MLOps pattern).

---

## Progress JSON Schema
```json
{
  "meta": { "created": "...", "last_updated": "...", "schema_version": "1.0", "focus_topic": null },
  "totals": { "stars": 0, "problems_attempted": 0, "problems_correct": 0 },
  "topics": {
    "3OA": { "attempted": 0, "correct": 0, "stars": 0, "last_practiced": null }
  },
  "sessions": [],
  "wrong_attempts": []
}
```

---

## Theme (`.streamlit/config.toml`)
```toml
[theme]
base = "light"
backgroundColor = "#FFFBF0"
secondaryBackgroundColor = "#FFF3DC"
primaryColor = "#FF6B35"
textColor = "#2D2D2D"
font = "sans serif"

[server]
headless = true

[browser]
gatherUsageStats = false
```

Key CSS colors: success gold `#FFD700`, success bg `#F0FFF4`, wrong amber `#F6AD55`, hint blue `#4299E1`, parent accent purple `#553C9A`.

---

## NYC 3rd Grade Content (NYS Math Assessment Aligned)
- **3.OA** — Arrays, multiplication/division, word problems, commutative/distributive properties
- **3.NBT** — Rounding to 10/100, add/subtract within 1000, multiply by multiples of 10
- **3.NF** — Fractions as parts of a whole, fractions on number lines, comparing fractions
- **3.MD** — Time to nearest minute, area & perimeter, bar graphs & picture graphs
- **3.G** — Shape attributes, partitioning shapes into equal areas

---

## Critical Files to Reference During Build
| File | Why |
|---|---|
| `/Users/jcmbair2021/Claude- MLOps/mlops-part2/utils/styles.py` | CSS injection pattern, auth guard, helper components |
| `/Users/jcmbair2021/Claude- MLOps/mlops-part2/app.py` | Entry point structure, session routing |
| `/Users/jcmbair2021/Claude- MLOps/mlops-part2/pages/1_Home.py` | Card navigation, `st.switch_page` pattern |
| `/Users/jcmbair2021/Claude- MLOps/mlops-part2/.streamlit/config.toml` | Theme file to replace |

---

## Verification
1. `streamlit run app.py` — landing page shows two mode buttons
2. Child flow: Practice → generate problem → answer wrong → see hint → answer correct → star awarded → Results page shows star count
3. Parent flow: PIN entry → Dashboard shows stats → Concepts page streams explanation → Review shows wrong attempts
4. Kill and restart app → progress persists (file-based JSON)
5. Unset `ANTHROPIC_API_KEY` → app falls back to static problems, no crash
6. Open on iPad Safari → layout usable, buttons large enough to tap
