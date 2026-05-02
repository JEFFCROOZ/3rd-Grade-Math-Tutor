"""
CSS and component helpers — mirrors the MLOps utils/styles.py pattern.
All UI primitives live here. Pages stay clean.
"""

import math
import streamlit as st

# ── Theme Colors ──────────────────────────────────────────────────────────────
ORANGE = "#FF6B35"
ORANGE_DARK = "#E55A25"
GOLD = "#FFD700"
SUCCESS_BG = "#F0FFF4"
SUCCESS_BORDER = "#48BB78"
WRONG_BG = "#FFFAF0"
WRONG_BORDER = "#F6AD55"
HINT_BG = "#EBF8FF"
HINT_BORDER = "#4299E1"
PARENT_PURPLE = "#553C9A"
PARENT_PURPLE_LIGHT = "#7C5CB9"
CREAM = "#FFFBF0"
CREAM_DARK = "#FFF3DC"
TEXT_DARK = "#2D2D2D"
TEXT_MED = "#4A4A4A"
TEXT_MUTED = "#718096"
CARD_BORDER = "#E2D9C8"


def inject_global_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&family=Inter:wght@400;500;600&display=swap');

        /* ── Base ── */
        html, body, [data-testid="stApp"] {
            background-color: #FFFBF0;
            color: #2D2D2D;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 820px;
        }

        /* ── Typography ── */
        body, p, span, div, label {
            font-family: 'Nunito', sans-serif;
            font-size: 1.05rem;
            line-height: 1.6;
        }
        h1 { font-family: 'Nunito', sans-serif; font-weight: 800; color: #2D2D2D; font-size: 2.2rem; }
        h2 { font-family: 'Nunito', sans-serif; font-weight: 700; color: #2D2D2D; font-size: 1.6rem; }
        h3 { font-family: 'Nunito', sans-serif; font-weight: 700; color: #4A4A4A; font-size: 1.25rem; }

        /* Parent pages override to Inter */
        .parent-container, .parent-container * {
            font-family: 'Inter', sans-serif !important;
        }
        .parent-header {
            background: linear-gradient(135deg, #553C9A 0%, #7C5CB9 100%);
            color: white;
            padding: 0.4rem 1rem;
            border-radius: 8px;
            font-family: 'Inter', sans-serif;
            font-size: 0.85rem;
            font-weight: 500;
            margin-bottom: 1.5rem;
            display: inline-block;
        }

        /* ── Streamlit Buttons ── */
        .stButton > button {
            font-family: 'Nunito', sans-serif;
            font-weight: 700;
            font-size: 1.05rem;
            padding: 0.7rem 1.5rem;
            border-radius: 12px;
            border: 2px solid transparent;
            background-color: #FF6B35;
            color: white;
            transition: all 0.15s ease;
            width: 100%;
        }
        .stButton > button:hover {
            background-color: #E55A25;
            border-color: #E55A25;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(255,107,53,0.3);
        }
        .stButton > button:active { transform: translateY(0); }

        /* ── Inputs ── */
        .stTextInput > div > input, .stNumberInput > div > input {
            font-family: 'Nunito', sans-serif;
            font-size: 1.1rem;
            border-radius: 10px;
            border: 2px solid #E2D9C8;
            padding: 0.5rem 0.75rem;
        }
        .stTextInput > div > input:focus {
            border-color: #FF6B35;
            box-shadow: 0 0 0 3px rgba(255,107,53,0.15);
        }

        /* ── Selectbox ── */
        .stSelectbox > div > div {
            font-family: 'Nunito', sans-serif;
            border-radius: 10px;
        }

        /* ── Sidebar hidden ── */
        [data-testid="stSidebar"] { display: none; }

        /* ── Cards ── */
        .math-card {
            background: white;
            border: 2px solid #E2D9C8;
            border-radius: 16px;
            padding: 1.25rem 1.5rem;
            margin-bottom: 1rem;
        }
        .topic-card {
            background: white;
            border: 2px solid #E2D9C8;
            border-radius: 16px;
            padding: 1.2rem;
            text-align: center;
            cursor: pointer;
            transition: border-color 0.15s, box-shadow 0.15s;
            margin-bottom: 0.75rem;
        }
        .topic-card:hover {
            border-color: #FF6B35;
            box-shadow: 0 4px 16px rgba(255,107,53,0.15);
        }
        .topic-emoji { font-size: 2.2rem; margin-bottom: 0.3rem; }
        .topic-label { font-weight: 700; font-size: 1rem; color: #2D2D2D; }
        .topic-sub   { font-size: 0.8rem; color: #718096; margin-top: 0.2rem; }
        .focus-badge {
            background: #FFD700;
            color: #2D2D2D;
            font-size: 0.7rem;
            font-weight: 800;
            padding: 0.15rem 0.5rem;
            border-radius: 20px;
            margin-left: 0.4rem;
        }

        /* ── Problem Card ── */
        .problem-card {
            background: white;
            border: 2px solid #E2D9C8;
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 1.25rem;
        }
        .problem-text {
            font-size: 1.2rem;
            font-weight: 700;
            color: #2D2D2D;
            line-height: 1.5;
            margin-bottom: 1rem;
        }
        .visual-box {
            background: #FFF3DC;
            border-radius: 12px;
            padding: 1rem;
            text-align: center;
            margin-bottom: 1rem;
        }

        /* ── Feedback Cards ── */
        .feedback-correct {
            background: #F0FFF4;
            border: 2px solid #48BB78;
            border-radius: 16px;
            padding: 1.25rem 1.5rem;
            margin: 1rem 0;
        }
        .feedback-wrong {
            background: #FFFAF0;
            border: 2px solid #F6AD55;
            border-radius: 16px;
            padding: 1.25rem 1.5rem;
            margin: 1rem 0;
        }
        .feedback-title {
            font-size: 1.3rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
        }

        /* ── Hint Card ── */
        .hint-card {
            background: #EBF8FF;
            border: 2px solid #4299E1;
            border-radius: 14px;
            padding: 1rem 1.25rem;
            margin: 0.75rem 0;
        }
        .hint-label {
            font-size: 0.8rem;
            font-weight: 700;
            color: #4299E1;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.3rem;
        }

        /* ── Star Display ── */
        .star-hero {
            text-align: center;
            font-size: 3rem;
            line-height: 1.2;
            margin: 0.5rem 0 1rem 0;
        }
        .star-count-label {
            text-align: center;
            font-weight: 800;
            font-size: 1.1rem;
            color: #FF6B35;
        }

        /* ── Parent Metric Card ── */
        .p-metric {
            background: white;
            border: 2px solid #E2D9C8;
            border-radius: 12px;
            padding: 1rem;
            text-align: center;
        }
        .p-metric-value {
            font-size: 2rem;
            font-weight: 800;
            color: #553C9A;
        }
        .p-metric-label {
            font-size: 0.85rem;
            color: #718096;
            font-weight: 600;
            margin-top: 0.2rem;
        }

        /* ── Progress Bar override ── */
        .stProgress > div > div > div { background-color: #FF6B35; border-radius: 4px; }

        /* ── Section break ── */
        .section-break {
            border: none;
            border-top: 2px solid #E2D9C8;
            margin: 1.5rem 0;
        }

        /* ── Weak topic alert ── */
        .weak-alert {
            background: #FFFAF0;
            border: 2px solid #F6AD55;
            border-radius: 12px;
            padding: 0.8rem 1.1rem;
            margin: 0.5rem 0;
            font-size: 0.95rem;
        }

        /* ── Wrong attempt row ── */
        .wrong-row {
            background: white;
            border: 1px solid #E2D9C8;
            border-radius: 10px;
            padding: 0.9rem 1.1rem;
            margin: 0.5rem 0;
        }

        /* ── Spinner text ── */
        .stSpinner > div { color: #FF6B35 !important; }

        /* ── Hide default st header ── */
        header[data-testid="stHeader"] { display: none; }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ── Auth Guards ───────────────────────────────────────────────────────────────

def require_child_auth():
    if not st.session_state.get("child_active"):
        st.switch_page("app.py")


def require_parent_auth():
    if not st.session_state.get("parent_active"):
        st.switch_page("app.py")


# ── Visual Renderers (Python-controlled — the model only provides parameters) ──

def render_array(rows: int, cols: int, emoji: str) -> str:
    if rows > 10 or cols > 10:
        return ""
    row_html = "  ".join([emoji] * cols)
    rows_html = "".join([f"<div style='line-height:2rem;'>{row_html}</div>"] * rows)
    return (
        f'<div style="font-size:1.8rem; text-align:center; padding: 0.5rem 0;">'
        f"{rows_html}"
        f"</div>"
    )


def render_fraction_shape(numerator: int, denominator: int, shape: str = "rectangle") -> str:
    if denominator < 1 or denominator > 12 or numerator < 0 or numerator > denominator:
        return ""
    if shape == "circle":
        # Use emoji-based fallback for circle
        filled = "🟠" * numerator
        empty = "⚪" * (denominator - numerator)
        return (
            f'<div style="font-size:1.6rem; text-align:center; padding:0.5rem;">'
            f"{filled}{empty}"
            f'<div style="font-size:0.75rem; color:#718096; margin-top:0.4rem;">'
            f"{numerator} out of {denominator} equal parts</div>"
            f"</div>"
        )
    # Rectangle using colored blocks
    block_w = max(30, min(60, int(300 / denominator)))
    blocks = ""
    for i in range(denominator):
        color = "#FF6B35" if i < numerator else "#E2D9C8"
        blocks += (
            f'<div style="display:inline-block; width:{block_w}px; height:40px; '
            f'background:{color}; border:2px solid #aaa; margin:1px;"></div>'
        )
    return (
        f'<div style="text-align:center; padding:0.5rem;">{blocks}'
        f'<div style="font-size:0.75rem; color:#718096; margin-top:0.4rem;">'
        f"{numerator} out of {denominator} equal parts</div>"
        f"</div>"
    )


def render_bar_graph(title: str, bars: list, y_label: str = "") -> str:
    if not bars:
        return ""
    max_val = max(b.get("value", 0) for b in bars)
    if max_val == 0:
        return ""

    bar_htmls = []
    for bar in bars:
        val = bar.get("value", 0)
        label = bar.get("label", "")
        pct = int(val / max_val * 100)
        bar_htmls.append(
            f'<div style="display:flex;flex-direction:column;align-items:center;flex:1;min-width:0;">'
            f'<div style="font-size:0.75rem;font-weight:700;color:#2D2D2D;margin-bottom:3px;">{val}</div>'
            f'<div style="background:#FF6B35;width:80%;height:{pct}%;border-radius:4px 4px 0 0;min-height:4px;"></div>'
            f'<div style="font-size:0.7rem;color:#4A5568;margin-top:5px;text-align:center;word-break:break-word;">{label}</div>'
            f'</div>'
        )

    title_html = (
        f'<div style="text-align:center;font-weight:700;font-size:0.85rem;color:#2D2D2D;margin-bottom:6px;">{title}</div>'
        if title else ""
    )
    y_html = (
        f'<div style="font-size:0.7rem;color:#718096;margin-bottom:4px;">{y_label}</div>'
        if y_label else ""
    )

    return (
        f'<div style="background:#FFF3DC;border-radius:12px;padding:12px 16px;margin:8px 0;">'
        f'{title_html}'
        f'{y_html}'
        f'<div style="display:flex;align-items:flex-end;gap:6px;height:130px;">'
        + "".join(bar_htmls)
        + f'</div>'
        f'</div>'
    )


def render_clock(hour: int, minute: int) -> str:
    cx, cy, r = 60, 60, 50

    # Hour hand
    h_angle = math.radians((hour % 12 + minute / 60) * 30 - 90)
    hx = cx + 28 * math.cos(h_angle)
    hy = cy + 28 * math.sin(h_angle)

    # Minute hand
    m_angle = math.radians(minute * 6 - 90)
    mx = cx + 38 * math.cos(m_angle)
    my = cy + 38 * math.sin(m_angle)

    # 12 tick marks around the face
    ticks = ""
    for i in range(12):
        a = math.radians(i * 30 - 90)
        x1 = cx + (r - 7) * math.cos(a)
        y1 = cy + (r - 7) * math.sin(a)
        x2 = cx + r * math.cos(a)
        y2 = cy + r * math.sin(a)
        ticks += f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#2D2D2D" stroke-width="2"/>'

    # Numbers at 12, 3, 6, 9
    nums = {12: (60, 16), 3: (104, 62), 6: (60, 108), 9: (16, 62)}
    num_html = "".join(
        f'<text x="{nx}" y="{ny}" text-anchor="middle" dominant-baseline="middle" '
        f'font-size="11" font-weight="bold" fill="#2D2D2D">{n}</text>'
        for n, (nx, ny) in nums.items()
    )

    display_min = f"{minute:02d}"
    svg = (
        f'<div style="text-align:center;padding:0.5rem;">'
        f'<svg viewBox="0 0 120 120" width="140" height="140">'
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="white" stroke="#2D2D2D" stroke-width="2.5"/>'
        + ticks
        + num_html
        + f'<line x1="{cx}" y1="{cy}" x2="{hx:.1f}" y2="{hy:.1f}" stroke="#2D2D2D" stroke-width="4" stroke-linecap="round"/>'
        + f'<line x1="{cx}" y1="{cy}" x2="{mx:.1f}" y2="{my:.1f}" stroke="#FF6B35" stroke-width="2.5" stroke-linecap="round"/>'
        + f'<circle cx="{cx}" cy="{cy}" r="3" fill="#2D2D2D"/>'
        f'</svg>'
        f'<div style="font-size:0.85rem;color:#718096;margin-top:2px;">{hour}:{display_min}</div>'
        f'</div>'
    )
    return svg


def render_visual(visual_type: str, visual_data: dict) -> str:
    if visual_type == "array":
        return render_array(
            visual_data.get("rows", 3),
            visual_data.get("cols", 4),
            visual_data.get("emoji", "🔵"),
        )
    elif visual_type == "fraction":
        return render_fraction_shape(
            visual_data.get("numerator", 1),
            visual_data.get("denominator", 4),
            visual_data.get("shape", "rectangle"),
        )
    elif visual_type == "number_line":
        start = visual_data.get("start", 0)
        end = visual_data.get("end", 10)
        mark = visual_data.get("mark", 5)
        label = visual_data.get("label", "")
        return (
            f'<div style="text-align:center; padding:0.5rem;">'
            f'<div style="font-size:0.8rem; color:#718096;">{label}</div>'
            f'<div style="font-size:1.2rem; margin:0.4rem 0;">|—{start}———————{mark}◀———{end}—|</div>'
            f"</div>"
        )
    elif visual_type == "bar_graph":
        return render_bar_graph(
            visual_data.get("title", ""),
            visual_data.get("bars", []),
            visual_data.get("y_label", ""),
        )
    elif visual_type == "clock":
        return render_clock(
            visual_data.get("hour", 12),
            visual_data.get("minute", 0),
        )
    return ""


# ── Component HTML Builders ───────────────────────────────────────────────────

def star_display(count: int) -> str:
    stars = "⭐" * min(count, 20)
    overflow = f" +{count - 20} more" if count > 20 else ""
    return (
        f'<div class="star-hero">{stars}</div>'
        f'<div class="star-count-label">{count} star{"s" if count != 1 else ""} earned{overflow}</div>'
    )


def topic_card(key: str, title: str, emoji: str, attempted: int, stars: int, is_focus: bool = False) -> str:
    focus_badge = '<span class="focus-badge">⭐ Practice this!</span>' if is_focus else ""
    accuracy = f"{int(stars/attempted*100)}% accuracy" if attempted > 0 else "Not started yet"
    return (
        f'<div class="topic-card">'
        f'<div class="topic-emoji">{emoji}</div>'
        f'<div class="topic-label">{title}{focus_badge}</div>'
        f'<div class="topic-sub">{accuracy}</div>'
        f"</div>"
    )


def problem_card(text: str, visual_html: str = "") -> str:
    visual_section = f'<div class="visual-box">{visual_html}</div>' if visual_html else ""
    return (
        f'<div class="problem-card">'
        f'<div class="problem-text">{text}</div>'
        f"{visual_section}"
        f"</div>"
    )


def feedback_correct(message: str = "") -> str:
    msg = message or "That's right! Great work! 🎉"
    return (
        f'<div class="feedback-correct">'
        f'<div class="feedback-title">⭐ Correct!</div>'
        f'<div>{msg}</div>'
        f"</div>"
    )


def feedback_wrong(explanation: str = "") -> str:
    exp = explanation or "Not quite — give it another look!"
    return (
        f'<div class="feedback-wrong">'
        f'<div class="feedback-title">Not quite... 💪</div>'
        f'<div>{exp}</div>'
        f"</div>"
    )


def hint_card(hint_text: str) -> str:
    return (
        f'<div class="hint-card">'
        f'<div class="hint-label">💡 Hint</div>'
        f'<div>{hint_text}</div>'
        f"</div>"
    )


def parent_metric_card(label: str, value: str, sub: str = "") -> str:
    sub_html = f'<div style="font-size:0.75rem;color:#718096;">{sub}</div>' if sub else ""
    return (
        f'<div class="p-metric">'
        f'<div class="p-metric-value">{value}</div>'
        f'<div class="p-metric-label">{label}</div>'
        f"{sub_html}"
        f"</div>"
    )


def section_break() -> None:
    st.markdown('<hr class="section-break">', unsafe_allow_html=True)


def parent_banner() -> None:
    st.markdown('<span class="parent-header">🔒 Parent View</span>', unsafe_allow_html=True)
