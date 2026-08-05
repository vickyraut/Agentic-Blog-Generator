import streamlit as st

def render_agent_status_tracker(current_states: dict):
    """
    Render live step-by-step progress cards for the Agentic pipeline.
    """
    st.markdown("#### 🔄 Agent Workflow Execution")
    
    steps = [
        ("title", "SEO Title Agent", "Formulating engaging SEO-friendly blog title..."),
        ("content", "Content Generation Agent", "Writing detailed Markdown blog content..."),
        ("translation", "Translation Agent", "Translating into target language..."),
        ("completed", "Completed", "Blog generation pipeline finished successfully!")
    ]

    cols = st.columns(4)

    for idx, (step_key, label, desc) in enumerate(steps):
        state = current_states.get(step_key, "pending")
        with cols[idx]:
            if state == "done":
                st.markdown(
                    f"""
                    <div class="status-pill done">
                        <span>✓</span> <strong>{label}</strong>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            elif state == "active" or state == "running":
                st.markdown(
                    f"""
                    <div class="status-pill active">
                        <span>⏳</span> <strong>{label}</strong>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"""
                    <div class="status-pill">
                        <span>⚪</span> <span style="color:#64748B;">{label}</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
