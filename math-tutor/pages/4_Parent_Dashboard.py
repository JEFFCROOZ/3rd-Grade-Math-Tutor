import streamlit as st
from utils.styles import inject_global_css, require_parent_auth, parent_banner, parent_metric_card, section_break
from utils.data_loader import APP_NAME, LANES, TOPICS, get_topics_by_lane
from utils.progress_store import get_all_stats, get_recent_sessions, set_focus_topic, get_focus_topic

st.set_page_config(
    page_title=f"{APP_NAME} — Parent Dashboard",
    page_icon="🔒",
    layout="centered",
    initial_sidebar_state="collapsed",
)
inject_global_css()
require_parent_auth()

parent_banner()
st.markdown("## Dashboard")

# ── Load data ─────────────────────────────────────────────────────────────────
stats = get_all_stats()
totals = stats["totals"]
topics = stats["topics"]
sessions = get_recent_sessions(5)
current_focus = get_focus_topic()

# ── Summary metrics ───────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)
accuracy_pct = (
    f"{int(totals['problems_correct'] / totals['problems_attempted'] * 100)}%"
    if totals["problems_attempted"] > 0
    else "—"
)
with col1:
    st.markdown(parent_metric_card("Total Stars", str(totals["stars"]), "⭐"), unsafe_allow_html=True)
with col2:
    st.markdown(parent_metric_card("Problems Tried", str(totals["problems_attempted"])), unsafe_allow_html=True)
with col3:
    st.markdown(parent_metric_card("Overall Accuracy", accuracy_pct), unsafe_allow_html=True)

section_break()

# ── Topic breakdown ───────────────────────────────────────────────────────────
st.markdown("### Topic Breakdown")

weak_topics = []

for lane_key, lane_info in LANES.items():
    st.markdown(f"#### {lane_info['emoji']} {lane_info['label']}")
    st.markdown(
        f'<p style="color:#718096; margin-top:-0.25rem;">{lane_info["description"]}</p>',
        unsafe_allow_html=True,
    )

    for key, info in get_topics_by_lane(lane_key).items():
        t = topics.get(key, {"attempted": 0, "correct": 0, "stars": 0, "last_practiced": None})
        if t["attempted"] == 0:
            acc_str = "Not started"
            acc_pct = None
        else:
            pct = int(t["correct"] / t["attempted"] * 100)
            acc_str = f"{pct}%"
            acc_pct = pct
            if pct < 60:
                weak_topics.append((key, info["label"], pct))

        last = t["last_practiced"] or "Never"
        focus_badge = " ⭐" if key == current_focus else ""

        st.markdown(
            f'<div class="math-card" style="margin-bottom:0.6rem;">'
            f'<strong>{info["emoji"]} {info["label"]}{focus_badge}</strong> '
            f'&nbsp;·&nbsp; {info["standard"]} '
            f'&nbsp;·&nbsp; Accuracy: <strong>{acc_str}</strong> '
            f'&nbsp;·&nbsp; {t["attempted"]} problems '
            f'&nbsp;·&nbsp; Last: {last}'
            f"</div>",
            unsafe_allow_html=True,
        )
        if acc_pct is not None:
            st.progress(acc_pct / 100)

    st.markdown("<br>", unsafe_allow_html=True)

# Weak topic alerts
if weak_topics:
    section_break()
    st.markdown("### ⚠️ Topics to Focus On")
    for key, label, pct in weak_topics:
        st.markdown(
            f'<div class="weak-alert">📉 <strong>{label}</strong> is at {pct}% accuracy — consider setting this as the focus topic below.</div>',
            unsafe_allow_html=True,
        )

section_break()

# ── Focus topic setter ────────────────────────────────────────────────────────
st.markdown("### Set a Focus Topic")
st.markdown(
    '<p style="color:#718096; font-size:0.9rem;">The child home screen will show a badge on this topic to encourage her to practice it.</p>',
    unsafe_allow_html=True,
)

topic_options = {
    f"{info['emoji']} {info['label']} ({info['standard']})": key for key, info in TOPICS.items()
}
topic_options_with_none = {"No specific focus": None, **topic_options}
current_label = next(
    (lbl for lbl, k in topic_options_with_none.items() if k == current_focus),
    "No specific focus",
)

selected_label = st.selectbox("Focus topic", list(topic_options_with_none.keys()), index=list(topic_options_with_none.keys()).index(current_label))
if st.button("Save Focus Topic", use_container_width=False):
    new_focus = topic_options_with_none[selected_label]
    set_focus_topic(new_focus)
    st.success("Focus topic saved!")

section_break()

# ── Recent sessions ───────────────────────────────────────────────────────────
st.markdown("### Recent Sessions")
if not sessions:
    st.markdown('<p style="color:#718096;">No sessions recorded yet.</p>', unsafe_allow_html=True)
else:
    for s in sessions:
        topic_label = TOPICS.get(s["topic"], {}).get("label", s["topic"])
        acc = f"{int(s['problems_correct']/s['problems_attempted']*100)}%" if s["problems_attempted"] > 0 else "—"
        mins = int(s.get("duration_seconds", 0) / 60)
        st.markdown(
            f'<div class="wrong-row">'
            f'📅 <strong>{s["date"]}</strong> &nbsp;·&nbsp; {topic_label} &nbsp;·&nbsp; '
            f'{s["problems_correct"]}/{s["problems_attempted"]} correct ({acc}) &nbsp;·&nbsp; '
            f'{"⭐" * min(s["stars_earned"], 10)} ({s["stars_earned"]} stars) &nbsp;·&nbsp; {mins} min'
            f"</div>",
            unsafe_allow_html=True,
        )

section_break()

# ── Nav ───────────────────────────────────────────────────────────────────────
col_a, col_b, col_c = st.columns(3)
with col_a:
    if st.button("📚 Learn the Method", use_container_width=True):
        st.switch_page("pages/5_Parent_Concepts.py")
with col_b:
    if st.button("🔍 Review Wrong Answers", use_container_width=True):
        st.switch_page("pages/6_Parent_Review.py")
with col_c:
    if st.button("🔒 Sign Out", use_container_width=True):
        for key in ["parent_active", "parent_selected_topic"]:
            st.session_state.pop(key, None)
        st.switch_page("app.py")
