"""
The core practice loop. State machine via st.session_state.practice_state.

States:
  loading          → fetch problem from the live model layer, then → answering
  answering        → show problem + answer choices + hint button
  hint_shown       → show hint card, answers still live
  answered_correct → celebration, Next Problem button
  answered_wrong   → gentle feedback, Try Again / Next Problem
"""

import random
import datetime
import streamlit as st

from utils.styles import (
    inject_global_css,
    require_child_auth,
    problem_card,
    feedback_correct,
    feedback_wrong,
    hint_card,
    render_visual,
    section_break,
)
from utils.data_loader import APP_NAME, LANES, TOPICS, get_subtopics
from utils.openai_client import generate_problem, get_hint
from utils.progress_store import record_attempt

st.set_page_config(
    page_title=f"{APP_NAME} — Practice",
    page_icon="⭐",
    layout="centered",
    initial_sidebar_state="collapsed",
)
inject_global_css()
require_child_auth()

# ── Session state defaults ────────────────────────────────────────────────────
topic_key = st.session_state.get("selected_topic", "3OA")
topic_info = TOPICS.get(topic_key, {})
topic_label = topic_info.get("label", "Math")
lane_label = LANES.get(topic_info.get("lane", ""), {}).get("label", "Summer Bridge")

def _init_state():
    defaults = {
        "practice_state": "loading",
        "current_problem": None,
        "current_answer_choices": [],
        "hint_count": 0,
        "current_hint": "",
        "wrong_attempts_count": 0,
        "problem_recorded": False,
        "session_problems": 0,
        "session_correct": 0,
        "session_stars": 0,
        "session_start": datetime.datetime.now().isoformat(),
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init_state()

# ── Header ────────────────────────────────────────────────────────────────────
col_title, col_stats = st.columns([3, 1])
with col_title:
    st.markdown(f"### {topic_info.get('emoji', '⭐')} {topic_label}")
    st.markdown(
        f'<div style="color:#718096; font-size:0.85rem; margin-top:-0.4rem;">'
        f'{lane_label} · {topic_info.get("standard", topic_key)}'
        f"</div>",
        unsafe_allow_html=True,
    )
with col_stats:
    stars = st.session_state.session_stars
    st.markdown(
        f'<div style="text-align:right; font-size:1.3rem; font-weight:800; color:#FF6B35;">'
        f"{'⭐' * min(stars, 10)}{f' +{stars-10}' if stars > 10 else ''}"
        f'</div>',
        unsafe_allow_html=True,
    )

# ── LOADING state — generate problem ─────────────────────────────────────────
if st.session_state.practice_state == "loading":
    spinner_messages = [
        "Thinking of a good one... 🤔",
        "Almost ready! ✨",
        "Here comes a tricky one! 💪",
        "Cooking up a problem... 🍳",
        "Getting your next challenge! 🚀",
    ]
    msg = random.choice(spinner_messages)
    with st.spinner(msg):
        subtopics = get_subtopics(topic_key)
        subtopic = st.session_state.get("selected_subtopic") or (
            random.choice(subtopics) if subtopics else None
        )
        # Cycle difficulty: easy → medium → hard → easy
        problems_done = st.session_state.session_problems
        difficulty = ["easy", "medium", "hard"][problems_done % 3]

        problem = generate_problem(topic_key, subtopic, difficulty)
        choices = [problem["answer"]] + problem["distractors"]
        random.shuffle(choices)

        st.session_state.current_problem = problem
        st.session_state.current_answer_choices = choices
        st.session_state.practice_state = "answering"
        st.session_state.hint_count = 0
        st.session_state.current_hint = ""
        st.session_state.wrong_attempts_count = 0
        st.session_state.problem_recorded = False
    st.rerun()

# ── Helpers to transition states without re-rendering in the same pass ────────
def _go_next():
    # Record as wrong if we're leaving without a correct answer
    if not st.session_state.problem_recorded and st.session_state.current_problem:
        st.session_state.session_problems += 1
        record_attempt(
            topic_key=topic_key,
            subtopic=st.session_state.get("selected_subtopic", ""),
            problem_dict=st.session_state.current_problem,
            user_answer="skipped",
            is_correct=False,
            hint_used=st.session_state.hint_count > 0,
        )
        st.session_state.problem_recorded = True
    st.session_state.practice_state = "loading"
    st.session_state.current_problem = None

def _answer_correct():
    st.session_state.session_problems += 1
    st.session_state.session_correct += 1
    st.session_state.session_stars += 1
    st.session_state.problem_recorded = True
    record_attempt(
        topic_key=topic_key,
        subtopic=st.session_state.get("selected_subtopic", ""),
        problem_dict=st.session_state.current_problem,
        user_answer=st.session_state.current_problem["answer"],
        is_correct=True,
        hint_used=st.session_state.hint_count > 0,
    )
    st.session_state.practice_state = "answered_correct"

def _answer_wrong(chosen: str):
    # Store the last wrong answer for the reveal on attempt 3
    st.session_state.wrong_attempts_count += 1
    st.session_state.last_wrong_answer = chosen
    st.session_state.practice_state = "answered_wrong"

# ── ANSWERING / HINT_SHOWN states ─────────────────────────────────────────────
if st.session_state.practice_state in ("answering", "hint_shown"):
    problem = st.session_state.current_problem
    choices = st.session_state.current_answer_choices

    # Render problem card
    visual_html = render_visual(
        problem.get("visual_type", "none"),
        problem.get("visual_data", {}),
    )
    st.markdown(problem_card(problem["problem_text"], visual_html), unsafe_allow_html=True)

    # Hint card (if shown)
    if st.session_state.practice_state == "hint_shown" and st.session_state.current_hint:
        st.markdown(hint_card(st.session_state.current_hint), unsafe_allow_html=True)

    # Answer buttons — 2x2 grid
    col1, col2 = st.columns(2)
    for i, choice in enumerate(choices):
        col = col1 if i % 2 == 0 else col2
        with col:
            if st.button(choice, key=f"choice_{i}", use_container_width=True):
                if choice == problem["answer"]:
                    _answer_correct()
                else:
                    _answer_wrong(choice)
                st.rerun()

    section_break()

    # Hint button
    hint_col, stop_col = st.columns([2, 1])
    with hint_col:
        if st.button("💡 Give me a hint", use_container_width=True):
            with st.spinner("Getting you a hint..."):
                hint_text = get_hint(problem, st.session_state.hint_count)
            st.session_state.current_hint = hint_text
            st.session_state.hint_count += 1
            st.session_state.practice_state = "hint_shown"
            st.rerun()
    with stop_col:
        if st.button("🏁 Stop", use_container_width=True):
            st.switch_page("pages/3_Child_Results.py")

# ── ANSWERED_CORRECT state ────────────────────────────────────────────────────
elif st.session_state.practice_state == "answered_correct":
    problem = st.session_state.current_problem
    st.markdown(feedback_correct(), unsafe_allow_html=True)

    stars_this_session = st.session_state.session_stars
    st.markdown(
        f'<div style="text-align:center; font-size:2rem; margin:0.5rem 0;">{"⭐" * min(stars_this_session, 15)}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div style="text-align:center; color:#718096; font-size:0.9rem;">'
        f"{stars_this_session} star{'s' if stars_this_session != 1 else ''} this session!</div>",
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    col_next, col_stop = st.columns([2, 1])
    with col_next:
        if st.button("➡️  Next Problem", use_container_width=True):
            _go_next()
            st.rerun()
    with col_stop:
        if st.button("🏁 Stop", use_container_width=True):
            st.switch_page("pages/3_Child_Results.py")

# ── ANSWERED_WRONG state ──────────────────────────────────────────────────────
elif st.session_state.practice_state == "answered_wrong":
    problem = st.session_state.current_problem
    attempts = st.session_state.wrong_attempts_count
    explanation = problem.get("explanation_child", "Not quite — let's look at this one together!")

    if attempts >= 3:
        # Reveal the answer
        answer = problem.get("answer", "")
        reveal_msg = f"The answer is **{answer}**. {explanation}"
        st.markdown(feedback_wrong(reveal_msg), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col_next, col_stop = st.columns([2, 1])
        with col_next:
            if st.button("➡️ Next Problem", use_container_width=True):
                _go_next()
                st.rerun()
        with col_stop:
            if st.button("🏁 Stop", use_container_width=True):
                st.switch_page("pages/3_Child_Results.py")

    elif attempts == 2:
        # Show hint_1 (Socratic, no answer)
        hint_text = problem.get("hint_1", "Think about what you already know — what's the first step?")
        st.markdown(feedback_wrong("Not quite — here's a hint to help you think it through! 💪"), unsafe_allow_html=True)
        st.markdown(hint_card(hint_text), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col_retry, col_next, col_stop = st.columns([1, 1, 1])
        with col_retry:
            if st.button("🔄 Try Again", use_container_width=True):
                st.session_state.practice_state = "answering"
                st.rerun()
        with col_next:
            if st.button("➡️ Next Problem", use_container_width=True):
                _go_next()
                st.rerun()
        with col_stop:
            if st.button("🏁 Stop", use_container_width=True):
                st.switch_page("pages/3_Child_Results.py")

    else:
        # Attempt 1: show method explanation, no answer
        st.markdown(feedback_wrong(explanation), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col_retry, col_next, col_stop = st.columns([1, 1, 1])
        with col_retry:
            if st.button("🔄 Try Again", use_container_width=True):
                st.session_state.practice_state = "answering"
                st.rerun()
        with col_next:
            if st.button("➡️ Next Problem", use_container_width=True):
                _go_next()
                st.rerun()
        with col_stop:
            if st.button("🏁 Stop", use_container_width=True):
                st.switch_page("pages/3_Child_Results.py")
