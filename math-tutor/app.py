import os
import streamlit as st
from utils.styles import inject_global_css
from utils.data_loader import PARENT_PIN

# Expose DATABASE_URL from st.secrets to os.environ so progress_store can read it
if "DATABASE_URL" not in os.environ:
    try:
        os.environ["DATABASE_URL"] = st.secrets["DATABASE_URL"]
    except Exception:
        pass

st.set_page_config(
    page_title="Math Stars",
    page_icon="⭐",
    layout="centered",
    initial_sidebar_state="collapsed",
)
inject_global_css()

# ── Routing guards ────────────────────────────────────────────────────────────
if st.session_state.get("child_active"):
    st.switch_page("pages/1_Child_Home.py")
if st.session_state.get("parent_active"):
    st.switch_page("pages/4_Parent_Dashboard.py")

# ── Landing page ──────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="text-align:center; padding: 2rem 0 1rem 0;">
        <div style="font-size:4rem;">⭐</div>
        <h1 style="margin:0.25rem 0 0.5rem 0;">Math Stars</h1>
        <p style="color:#718096; font-size:1.05rem; max-width:400px; margin:0 auto;">
            Practice math the way your teacher teaches it — and earn stars along the way!
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<br>", unsafe_allow_html=True)

col_l, col_c, col_r = st.columns([1, 2, 1])
with col_c:
    if st.button("⭐  I'm Ready to Practice!", use_container_width=True):
        st.session_state.child_active = True
        st.switch_page("pages/1_Child_Home.py")

st.markdown("<br>", unsafe_allow_html=True)

# ── Parent login (collapsible) ────────────────────────────────────────────────
with st.expander("🔒 Parent Login"):
    pin = st.text_input("Enter your 4-digit PIN", type="password", max_chars=4, key="pin_input")
    if st.button("Log In", use_container_width=True):
        # Check st.secrets first (Streamlit Cloud), fall back to data_loader constant
        try:
            expected = st.secrets.get("PARENT_PIN", PARENT_PIN)
        except Exception:
            expected = PARENT_PIN

        if pin == expected:
            st.session_state.parent_active = True
            st.switch_page("pages/4_Parent_Dashboard.py")
        else:
            st.error("Incorrect PIN. Please try again.")
