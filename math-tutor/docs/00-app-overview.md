# 00 — App Overview & Design Notes

> **Internal reference document.** Explains why this app exists, who it's for, and the key design decisions made during development.

---

## Why This Exists

Common Core math is genuinely different from how most parents in their 30s and 40s learned math. The methods — arrays as multiplication models, area models for multi-digit multiplication, fraction bars, number bonds — weren't standardized until after most of today's parents graduated high school.

The result: an 8-year-old comes home with homework her dad can actually solve, but not the way her teacher taught it. That disconnect undermines confidence on both sides.

This app solves two problems simultaneously:
1. **The child gets consistent practice** aligned to how her teacher actually teaches it
2. **The parent learns the method** so they can reinforce it at home

---

## Who This Is For

**Primary user (child, age 8):** She should be able to use this mostly independently. The UI is intentionally simple — large buttons, warm colors, encouraging language, no reading required for navigation. Stars as feedback because stars are universally understood.

**Secondary user (parent, age 39):** Mathematically capable but new to Common Core framing. The parent dashboard speaks to an adult — direct, no condescension, explains the pedagogical *why*, not just the *what*.

---

## Key Design Decisions

### Streamlit over Native iPad
A native SwiftUI app would be better UX in theory. In practice: Streamlit opened in Safari on iPad delivers 80% of the experience at 20% of the build time. The content and pedagogy matter more than the platform at this stage. Native can come later.

### Claude API for Problem Generation
Pre-written problem banks go stale and require constant curation. Claude generates problems on demand, which means:
- Variety every session (no "I've seen this one")
- Difficulty can adjust (easy → medium → hard cycling)
- Explanations are tailored to the specific problem

Fallback static problems exist for every topic so the app never breaks without an API key.

### Three-Attempt Wrong-Answer System
When a child gets a problem wrong, the app gives her up to three chances before revealing the answer. The progression is deliberate:

1. **Attempt 1 wrong:** Shows `explanation_child` — explains the *method* to use, never the answer. Try Again available.
2. **Attempt 2 wrong:** Shows `hint_1` — a Socratic question to guide her thinking, still no answer. Try Again available.
3. **Attempt 3 wrong:** Reveals the answer explicitly ("The answer is X") plus the method explanation. Try Again is removed — at this point seeing it and moving on is the right move.

One attempt record is written per problem regardless of how many wrong taps. Scoring stays clean.

The first two steps use pre-generated fields from the same Claude API call — no extra cost for the hint on attempt 2.

### Socratic Hints — Never Give the Answer
The hint system is deliberately constrained. Claude is instructed to give guiding questions, not answers. `hint_1` is generated alongside the problem (no extra API call) and surfaces on the second wrong attempt. This is intentional pedagogy — productive struggle matters for learning.

### Gentle Wrong-Answer Feedback
The feedback for wrong answers uses amber (not red) and "Not quite... 💪" (not "Wrong!"). This is deliberate. An 8-year-old's relationship with mistakes during practice shapes their math identity. The goal is to normalize trying again, not avoid being wrong.

### File-Based Persistence
No database, no backend service. Progress lives in `data/progress.json` using atomic writes. This is the right level of complexity for a family app running locally or on a single Streamlit Cloud instance. Upgrade path to a database exists but isn't needed yet.

### Parent PIN, Not Password
A 4-digit PIN keeps the parent section separate without creating friction. It's not a security system — it's just enough to prevent an 8-year-old from accidentally landing in the parent view.

---

## What the AI Does (and Doesn't Do)

**Does:**
- Generate varied, standards-aligned problems on demand
- Adapt problem context to make it engaging (real-world scenarios)
- Explain Common Core methods in adult language to the parent
- Give Socratic hints that guide without solving
- Pre-generate wrong-answer explanations at two levels (child / parent)
- Return structured visual data (arrays, fractions, number lines, bar graphs) for Python to render

**Doesn't:**
- Control the app or make navigation decisions (Claude is a tool, not an agent here)
- Store any user data or conversation history
- Replace the parent — the "How to practice at home" section is designed to pull the parent into the learning, not out of it

---

## NYC Standardized Test Context

The NYS Math Assessment for 3rd grade tests:
- **Conceptual understanding** — do they understand *why* the method works
- **Procedural fluency** — can they execute the method accurately
- **Application** — can they apply it to word problems

The problem generation prompts specifically target all three, which is why array problems always include visual representations and word problems are included alongside computation.

## Visual Rendering

Claude returns a `visual_type` and `visual_data` payload alongside every problem. Python renders the visual — Claude never outputs raw HTML. Supported types:

| `visual_type` | Used for | Renderer |
|---|---|---|
| `array` | Multiplication, area (3.OA, 3.MD) | Emoji grid (`render_array`) |
| `fraction` | Fraction problems (3.NF) | Colored rectangle or circle blocks (`render_fraction_shape`) |
| `number_line` | Fraction placement, rounding (3.NF, 3.NBT) | ASCII-style line |
| `bar_graph` | Data/graph problems (3.MD) | Pure HTML/CSS vertical bars (`render_bar_graph`) |
| `clock` | Time-telling problems (3.MD) | SVG analog clock face (`render_clock`) |
| `none` | Word problems, computation | No visual |

All visuals are rendered in Python — Claude returns only data parameters, never HTML. No chart library required; no extra API call per visual. The visual data travels inside the same JSON response as the problem itself.

**Bar graph integrity rule:** The prompt explicitly requires that every bar `value` matches the exact integer in `problem_text`. This prevents Claude from populating the visual with placeholder zeros while describing real numbers in the question text.
