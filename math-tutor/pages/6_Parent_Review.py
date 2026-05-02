import streamlit as st
from utils.styles import inject_global_css, require_parent_auth, parent_banner, section_break
from utils.data_loader import APP_NAME, TOPICS
from utils.progress_store import get_wrong_attempts
from utils.openai_client import explain_wrong_answer_for_parent

st.set_page_config(
    page_title=f"{APP_NAME} — Wrong Answer Review",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="collapsed",
)
inject_global_css()
require_parent_auth()

parent_banner()
st.markdown("## Wrong Answer Review")
st.markdown(
    '<p style="color:#718096;">Browse every incorrect answer and get a parent-level explanation on demand.</p>',
    unsafe_allow_html=True,
)

section_break()

# ── Topic filter ──────────────────────────────────────────────────────────────
filter_options = {"All Topics": None} | {
    f"{info['emoji']} {info['label']} ({info['standard']})": key for key, info in TOPICS.items()
}
selected_filter_label = st.selectbox("Filter by topic", list(filter_options.keys()))
filter_key = filter_options[selected_filter_label]

wrong = get_wrong_attempts(topic_key=filter_key)

section_break()

if not wrong:
    st.markdown(
        '<div class="math-card" style="text-align:center; color:#48BB78; font-weight:700;">'
        "🎉 No wrong answers recorded for this filter yet!"
        "</div>",
        unsafe_allow_html=True,
    )
else:
    st.markdown(f"**{len(wrong)} wrong attempt{'s' if len(wrong) != 1 else ''} found.**")
    st.markdown("<br>", unsafe_allow_html=True)

    for i, attempt in enumerate(wrong):
        topic_label = TOPICS.get(attempt["topic"], {}).get("label", attempt["topic"])
        hint_note = " (used a hint)" if attempt.get("hint_used") else ""

        st.markdown(
            f'<div class="wrong-row">'
            f'<div style="font-size:0.75rem; color:#718096;">'
            f'{attempt.get("timestamp","")[:10]} &nbsp;·&nbsp; {topic_label} — {attempt.get("subtopic","")}{hint_note}'
            f"</div>"
            f'<div style="font-weight:700; margin:0.4rem 0;">{attempt["problem_text"]}</div>'
            f'<div>She answered: <strong style="color:#E53E3E;">{attempt["user_answer"]}</strong> &nbsp;|&nbsp; '
            f'Correct: <strong style="color:#38A169;">{attempt["correct_answer"]}</strong></div>'
            f"</div>",
            unsafe_allow_html=True,
        )

        # Inline child explanation (pre-generated, no API call)
        if attempt.get("explanation_child"):
            st.markdown(
                f'<div style="font-size:0.85rem; color:#718096; margin:0.3rem 0 0.6rem 1rem;">'
                f'💬 Child explanation: {attempt["explanation_child"]}</div>',
                unsafe_allow_html=True,
            )

        # On-demand parent explanation
        explain_key = f"explain_{i}"
        if st.button(f"📖 Explain this problem in depth", key=f"btn_explain_{i}"):
            with st.spinner("Generating explanation..."):
                explanation = explain_wrong_answer_for_parent(
                    problem_dict={
                        "problem_text": attempt["problem_text"],
                        "answer": attempt["correct_answer"],
                        "explanation_parent": attempt.get("explanation_parent", ""),
                    },
                    wrong_answer=attempt["user_answer"],
                )
            st.session_state[explain_key] = explanation

        if st.session_state.get(explain_key):
            st.markdown(
                f'<div class="hint-card">{st.session_state[explain_key]}</div>',
                unsafe_allow_html=True,
            )

        if i < len(wrong) - 1:
            st.markdown("---")

section_break()

if st.button("← Back to Dashboard", use_container_width=False):
    st.switch_page("pages/4_Parent_Dashboard.py")
