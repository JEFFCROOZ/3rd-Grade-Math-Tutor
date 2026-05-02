import streamlit as st
from utils.styles import inject_global_css, require_child_auth, star_display, section_break
from utils.data_loader import APP_NAME, TOPICS, get_encouragement
from utils.progress_store import close_session, get_star_count

st.set_page_config(
    page_title=f"{APP_NAME} — Session Done!",
    page_icon="⭐",
    layout="centered",
    initial_sidebar_state="collapsed",
)
inject_global_css()
require_child_auth()

session_problems = st.session_state.get("session_problems", 0)
session_correct = st.session_state.get("session_correct", 0)
session_stars = st.session_state.get("session_stars", 0)
topic = st.session_state.get("selected_topic", "3OA")
session_start = st.session_state.get("session_start")
topic_label = TOPICS.get(topic, {}).get("label", topic)

# Close session in progress store
if session_start and session_problems > 0:
    close_session(
        session_start=session_start,
        topic_key=topic,
        problems_attempted=session_problems,
        problems_correct=session_correct,
        stars_earned=session_stars,
    )
    st.session_state.pop("session_start", None)

accuracy = session_correct / session_problems if session_problems > 0 else 0
message = get_encouragement(accuracy)

# ── Results display ───────────────────────────────────────────────────────────
st.markdown("## 🎉 Great session!")
st.markdown(
    f'<p style="text-align:center; color:#718096; margin-top:-0.25rem;">'
    f'You practiced <strong>{topic_label}</strong> today.'
    f"</p>",
    unsafe_allow_html=True,
)

st.markdown(star_display(session_stars), unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Problems Tried", session_problems)
with col2:
    st.metric("Correct", session_correct)
with col3:
    pct = f"{int(accuracy * 100)}%"
    st.metric("Accuracy", pct)

section_break()

st.markdown(
    f'<div class="math-card" style="text-align:center; font-size:1.1rem; font-weight:600;">'
    f"{message}"
    f"</div>",
    unsafe_allow_html=True,
)

total_stars = get_star_count()
st.markdown(
    f'<div style="text-align:center; color:#718096; font-size:0.9rem; margin-top:0.5rem;">'
    f"Total stars ever: {total_stars} ⭐"
    f"</div>",
    unsafe_allow_html=True,
)

st.markdown("<br>", unsafe_allow_html=True)

col_a, col_b = st.columns(2)
with col_a:
    if st.button("⭐  Keep Going!", use_container_width=True):
        st.session_state.session_problems = 0
        st.session_state.session_correct = 0
        st.session_state.session_stars = 0
        st.session_state.practice_state = "loading"
        import datetime
        st.session_state.session_start = datetime.datetime.now().isoformat()
        st.switch_page("pages/2_Child_Practice.py")
with col_b:
    if st.button("👋  See You Later!", use_container_width=True):
        for key in [
            "child_active", "selected_topic", "selected_subtopic",
            "practice_state", "current_problem", "current_answer_choices",
            "hint_count", "current_hint", "wrong_attempts_count",
            "session_problems", "session_correct", "session_stars", "session_start",
        ]:
            st.session_state.pop(key, None)
        st.switch_page("app.py")
