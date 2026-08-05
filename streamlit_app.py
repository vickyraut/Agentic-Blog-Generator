import streamlit as st
import time

# Page Configuration - Must be the first Streamlit command
st.set_page_config(
    page_title="Agentic Blog Generator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styles & Imports
from utils.styles import inject_custom_css
inject_custom_css()

from components.header import render_header
from components.sidebar import render_sidebar
from components.status import render_agent_status_tracker
from components.blog_display import render_blog_output
from components.actions import render_actions_bar
from utils.helpers import calculate_blog_stats
from services.api_service import BlogGeneratorService

def main():
    # 1. Render Header
    render_header()

    # 2. Render Sidebar & retrieve settings
    sidebar_settings = render_sidebar()
    selected_language = sidebar_settings["language"]
    blog_length = sidebar_settings["blog_length"]

    # Session State Initialization
    if "is_generating" not in st.session_state:
        st.session_state.is_generating = False
    if "generated_blog" not in st.session_state:
        st.session_state.generated_blog = None
    if "agent_steps" not in st.session_state:
        st.session_state.agent_steps = {
            "title": "pending",
            "content": "pending",
            "translation": "pending",
            "completed": "pending"
        }

    # 3. Main Topic Input Section
    st.markdown("### 💡 What topic would you like a blog post on?")
    
    topic_input = st.text_area(
        label="Blog Topic",
        placeholder="e.g. The Future of Quantum Computing and Artificial Intelligence in 2026",
        height=110,
        disabled=st.session_state.is_generating,
        help="Provide a clear topic, keyword, or summary of the blog post you want to generate."
    )

    col_btn, col_empty = st.columns([1, 3])
    with col_btn:
        generate_clicked = st.button(
            "⚡ Generate Blog",
            disabled=st.session_state.is_generating or not topic_input.strip(),
            use_container_width=True
        )

    # Trigger Generation Workflow
    if generate_clicked:
        if not topic_input.strip():
            st.warning("Please enter a blog topic before generating.")
            return

        st.session_state.is_generating = True
        st.session_state.show_copy_code = False
        st.session_state.agent_steps = {
            "title": "active",
            "content": "pending",
            "translation": "pending",
            "completed": "pending"
        }

        # Step Progress Placeholder
        status_placeholder = st.empty()
        with status_placeholder.container():
            render_agent_status_tracker(st.session_state.agent_steps)

        def update_step_status(step_name: str, state_value: str):
            st.session_state.agent_steps[step_name] = state_value
            with status_placeholder.container():
                render_agent_status_tracker(st.session_state.agent_steps)

        try:
            with st.spinner("🤖 Agents working in sequence..."):
                result = BlogGeneratorService.generate_blog_direct(
                    topic=topic_input.strip(),
                    language=selected_language,
                    blog_length=blog_length,
                    step_callback=update_step_status
                )

            st.session_state.generated_blog = result
            st.session_state.generated_topic = topic_input.strip()
            st.success("🎉 Blog generation completed successfully!")
            
        except Exception as e:
            st.error(f"❌ Error during blog generation: {str(e)}")
            st.session_state.agent_steps = {
                "title": "pending",
                "content": "pending",
                "translation": "pending",
                "completed": "pending"
            }
        finally:
            st.session_state.is_generating = False
            st.rerun()

    # 4. Display Results if available
    if st.session_state.generated_blog:
        blog_data = st.session_state.generated_blog
        title = blog_data.get("title", "Untitled Blog")
        content = blog_data.get("content", "")
        elapsed_time = blog_data.get("elapsed_time", 0.0)

        # Calculate statistics
        stats = calculate_blog_stats(
            text=content,
            generation_time_sec=elapsed_time,
            language=selected_language
        )

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Display Agent Status Completed State
        render_agent_status_tracker({
            "title": "done",
            "content": "done",
            "translation": "done",
            "completed": "done"
        })

        st.markdown("<br>", unsafe_allow_html=True)

        # Actions Bar (Copy, Download MD, Download PDF, Regenerate)
        def handle_regenerate():
            st.session_state.generated_blog = None
            st.rerun()

        render_actions_bar(
            title=title,
            content=content,
            on_regenerate_callback=handle_regenerate
        )

        # Output Display
        render_blog_output(title=title, content=content, stats=stats)


if __name__ == "__main__":
    main()
