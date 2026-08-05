import streamlit as st
from utils.languages import LANGUAGE_CATEGORIES, get_languages_for_category, CATEGORY_GLOBAL
from config.constants import BLOG_LENGTH_OPTIONS, BLOG_LENGTH_DESCRIPTIONS

def render_sidebar():
    """
    Render application settings sidebar with dynamic language dropdown and blog length selection.
    """
    st.sidebar.markdown("### ⚙️ Application Settings")
    st.sidebar.markdown("---")

    # 1. Language Category Selection
    category = st.sidebar.radio(
        "Language Category",
        options=LANGUAGE_CATEGORIES,
        index=0,
        help="Choose between Global and Indian language packs."
    )

    # 2. Dynamic Language Dropdown based on Category Selection
    available_languages = get_languages_for_category(category)
    
    # Store or reset language selection in session state if switching categories
    if "selected_language" not in st.session_state or st.session_state.selected_language not in available_languages:
        st.session_state.selected_language = available_languages[0]

    selected_language = st.sidebar.selectbox(
        "Target Language",
        options=available_languages,
        index=available_languages.index(st.session_state.selected_language),
        help="Select the language for the final blog post output."
    )
    st.session_state.selected_language = selected_language

    st.sidebar.markdown("---")

    # 3. Blog Length Selection
    blog_length = st.sidebar.select_slider(
        "Blog Length",
        options=BLOG_LENGTH_OPTIONS,
        value="Medium",
        help="Controls the target length and depth of the generated blog."
    )
    
    # Show length guide badge
    length_desc = BLOG_LENGTH_DESCRIPTIONS.get(blog_length, "")
    st.sidebar.caption(f"📏 Target Depth: **{blog_length}** ({length_desc})")

    st.sidebar.markdown("---")
    st.sidebar.markdown(
        """
        <div style="font-size: 0.85rem; color: #94A3B8; text-align: center; line-height: 1.6;">
            Made with ❤️ by <a href="https://vickyraut.vercel.app/" target="_blank" style="color: #38BDF8; text-decoration: none; font-weight: 600;">Vicky V. Raut (CodeMonk)</a>
            <br>
            <span style="font-size: 0.75rem; color: #64748B;">Powered by <strong>LangGraph</strong> & <strong>Groq Llama 3.1</strong></span>
        </div>
        """,
        unsafe_allow_html=True
    )

    return {
        "category": category,
        "language": selected_language,
        "blog_length": blog_length
    }
