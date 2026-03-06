import streamlit as st
from utils.styles import inject_global_css, require_child_auth, star_display, section_break
from utils.data_loader import TOPICS
from utils.progress_store import get_star_count, get_topic_stats, get_focus_topic

st.set_page_config(
    page_title="Math Stars — Pick a Topic",
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
st.markdown("## What do you want to practice today?")

# ── Topic Grid ────────────────────────────────────────────────────────────────
topic_keys = list(TOPICS.keys())

for i in range(0, len(topic_keys), 2):
    cols = st.columns(2)
    for j, col in enumerate(cols):
        idx = i + j
        if idx >= len(topic_keys):
            break
        key = topic_keys[idx]
        info = TOPICS[key]
        stats = get_topic_stats(key)
        is_focus = key == focus_topic

        with col:
            accuracy_str = ""
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
                    <div class="topic-sub">{accuracy_str}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(f"Practice {info['label']}", key=f"btn_{key}", use_container_width=True):
                st.session_state.selected_topic = key
                st.session_state.selected_subtopic = None
                st.session_state.practice_state = "loading"
                st.session_state.session_problems = 0
                st.session_state.session_correct = 0
                st.session_state.session_stars = 0
                st.session_state.hint_count = 0
                st.session_state.wrong_attempts_count = 0
                st.switch_page("pages/2_Child_Practice.py")

section_break()

# ── Mix it up ─────────────────────────────────────────────────────────────────
import random
if st.button("🎲  Mix It Up! (Random Topic)", use_container_width=True):
    st.session_state.selected_topic = random.choice(topic_keys)
    st.session_state.selected_subtopic = None
    st.session_state.practice_state = "loading"
    st.session_state.session_problems = 0
    st.session_state.session_correct = 0
    st.session_state.session_stars = 0
    st.session_state.hint_count = 0
    st.session_state.wrong_attempts_count = 0
    st.switch_page("pages/2_Child_Practice.py")

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
