import streamlit as st
from utils.styles import inject_global_css, require_parent_auth, parent_banner, section_break
from utils.data_loader import TOPICS, get_subtopics
from utils.claude_client import explain_concept_for_parent

st.set_page_config(
    page_title="Math Stars — Learn Common Core",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="collapsed",
)
inject_global_css()
require_parent_auth()

parent_banner()
st.markdown("## Learn the Common Core Method")
st.markdown(
    '<p style="color:#718096;">Pick a topic and get a clear, adult explanation of how it\'s taught today — '
    "and what to do at home to reinforce it.</p>",
    unsafe_allow_html=True,
)

section_break()

# ── Selectors ─────────────────────────────────────────────────────────────────
topic_options = {f"{info['emoji']} {info['label']} ({info['standard']})": key for key, info in TOPICS.items()}
selected_topic_label = st.selectbox("Choose a topic", list(topic_options.keys()), key="concept_topic")
selected_topic_key = topic_options[selected_topic_label]

subtopics = get_subtopics(selected_topic_key)
selected_subtopic = st.selectbox("Choose a subtopic (optional)", ["— General overview —"] + subtopics, key="concept_subtopic")
subtopic_arg = None if selected_subtopic.startswith("—") else selected_subtopic

section_break()

# ── Explain button ────────────────────────────────────────────────────────────
if st.button("📖  Explain This To Me", use_container_width=True):
    with st.spinner("Writing your explanation..."):
        st.write_stream(explain_concept_for_parent(selected_topic_key, subtopic_arg))

section_break()

if st.button("← Back to Dashboard", use_container_width=False):
    st.switch_page("pages/4_Parent_Dashboard.py")
