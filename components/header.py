import streamlit as st
from config.constants import APP_TITLE, APP_SUBTITLE

def render_header():
    """
    Render top application header and description subtitle.
    """
    st.markdown(
        f"""
        <div class="app-header">
            <h1>🤖 {APP_TITLE}</h1>
            <p>{APP_SUBTITLE}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
