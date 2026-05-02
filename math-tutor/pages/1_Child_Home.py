import streamlit as st
from utils.styles import inject_global_css, require_child_auth, star_display, section_break
from utils.data_loader import APP_NAME, LANES, TOPICS, get_topics_by_lane
from utils.progress_store import get_star_count, get_topic_stats, get_focus_topic

st.set_page_config(
    page_title=f"{APP_NAME} — Pick a Topic",
    page_icon="⭐",
    layout="centered",
    initial_sidebar_state="collapsed",
)
inject_global_css()
require_child_auth()

focus_topic = get_focus_topic()
total_stars = get_star_count()

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(star_display(total_stars), unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("## Pick your lane for today")
st.markdown(
    '<p style="color:#718096; margin-top:-0.25rem;">'
    'Choose a <strong>Grade 3 Review</strong> topic to strengthen foundations or a '
    '<strong>Grade 4 Preview</strong> topic to get a head start.'
    "</p>",
    unsafe_allow_html=True,
)

def _start_topic(topic_key: str):
    st.session_state.selected_topic = topic_key
    st.session_state.selected_subtopic = None
    st.session_state.practice_state = "loading"
    st.session_state.session_problems = 0
    st.session_state.session_correct = 0
    st.session_state.session_stars = 0
    st.session_state.hint_count = 0
    st.session_state.wrong_attempts_count = 0
    st.switch_page("pages/2_Child_Practice.py")

for lane_key, lane_info in LANES.items():
    lane_topics = list(get_topics_by_lane(lane_key).keys())
    st.markdown(f"### {lane_info['emoji']} {lane_info['label']}")
    st.markdown(
        f'<p style="color:#718096; margin-top:-0.25rem;">{lane_info["description"]}</p>',
        unsafe_allow_html=True,
    )

    for i in range(0, len(lane_topics), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            idx = i + j
            if idx >= len(lane_topics):
                break
            key = lane_topics[idx]
            info = TOPICS[key]
            stats = get_topic_stats(key)
            is_focus = key == focus_topic

            with col:
                if stats["attempted"] > 0:
                    pct = int(stats["correct"] / stats["attempted"] * 100)
                    accuracy_str = f"{pct}% accuracy · {stats['stars']} ⭐"
                else:
                    accuracy_str = "Not started yet"

                focus_badge = " ⭐ Practice this!" if is_focus else ""

                st.markdown(
                    f"""
                    <div class="topic-card">
                        <div class="topic-emoji">{info['emoji']}</div>
                        <div class="topic-label">{info['label']}{focus_badge}</div>
                        <div class="topic-sub">{info['standard']} · {accuracy_str}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if st.button(f"Practice {info['label']}", key=f"btn_{key}", use_container_width=True):
                    _start_topic(key)

    section_break()

# ── Mix it up ─────────────────────────────────────────────────────────────────
import random
mix_a, mix_b = st.columns(2)
with mix_a:
    if st.button("🎲 Random Grade 3 Review", use_container_width=True):
        _start_topic(random.choice(list(get_topics_by_lane("grade3_review").keys())))
with mix_b:
    if st.button("🎲 Random Grade 4 Preview", use_container_width=True):
        _start_topic(random.choice(list(get_topics_by_lane("grade4_preview").keys())))

section_break()

# ── Sign out ──────────────────────────────────────────────────────────────────
if st.button("👋  Done for now", use_container_width=False):
    for key in [
        "child_active", "selected_topic", "selected_subtopic",
        "practice_state", "current_problem", "current_answer_choices",
        "hint_count", "current_hint", "wrong_attempts_count",
        "session_problems", "session_correct", "session_stars",
    ]:
        st.session_state.pop(key, None)
    st.switch_page("app.py")
