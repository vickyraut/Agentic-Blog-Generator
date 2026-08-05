import streamlit as st
from utils.helpers import calculate_blog_stats

def render_blog_statistics(stats: dict):
    """
    Render key metrics in sleek rounded cards.
    """
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(
            f"""
            <div class="stat-box">
                <div class="stat-label">Word Count</div>
                <div class="stat-value">{stats['word_count']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            f"""
            <div class="stat-box">
                <div class="stat-label">Char Count</div>
                <div class="stat-value">{stats['char_count']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            f"""
            <div class="stat-box">
                <div class="stat-label">Reading Time</div>
                <div class="stat-value">{stats['reading_time']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col4:
        st.markdown(
            f"""
            <div class="stat-box">
                <div class="stat-label">Target Language</div>
                <div class="stat-value" style="font-size: 1.1rem; padding-top: 2px;">{stats['language']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col5:
        st.markdown(
            f"""
            <div class="stat-box">
                <div class="stat-label">Gen Time</div>
                <div class="stat-value">{stats['generation_time']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


def render_blog_output(title: str, content: str, stats: dict):
    """
    Render formatted blog Markdown and statistics.
    """
    st.markdown("### 📊 Generation Overview")
    render_blog_statistics(stats)
    st.markdown("---")

    # Render main blog card
    st.markdown("### 📝 Generated Blog Post")
    
    with st.container():
        st.markdown(f"# {title}")
        st.markdown("---")
        st.markdown(content)
