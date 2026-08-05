import streamlit as st
from utils.helpers import generate_pdf_bytes

def render_actions_bar(title: str, content: str, on_regenerate_callback=None):
    """
    Render quick actions bar: Copy Markdown, Download .md, Download .pdf, Regenerate.
    """
    st.markdown("### ⚡ Quick Actions")
    col1, col2, col3, col4 = st.columns(4)

    full_markdown = f"# {title}\n\n{content}"

    with col1:
        # Markdown File Download
        st.download_button(
            label="📥 Download Markdown",
            data=full_markdown,
            file_name=f"{title.lower().replace(' ', '_')[:30]}.md",
            mime="text/markdown",
            use_container_width=True
        )

    with col2:
        # PDF File Download
        pdf_bytes = generate_pdf_bytes(title, content)
        st.download_button(
            label="📄 Download PDF",
            data=pdf_bytes,
            file_name=f"{title.lower().replace(' ', '_')[:30]}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    with col3:
        # Copy to Clipboard (using Streamlit code block copy or button)
        if st.button("📋 Copy Markdown", use_container_width=True):
            st.toast("✅ Markdown copied to clipboard!", icon="📋")
            st.session_state.show_copy_code = True

    with col4:
        # Regenerate Button
        if st.button("🔄 Regenerate Blog", use_container_width=True):
            if on_regenerate_callback:
                on_regenerate_callback()

    # Optional code container if user clicks Copy
    if st.session_state.get("show_copy_code", False):
        with st.expander("📄 Raw Markdown (Click top-right icon to copy)", expanded=True):
            st.code(full_markdown, language="markdown")
