import streamlit as st

def inject_custom_css():
    """
    Inject sleek Black & White modern minimalist CSS styles.
    """
    custom_css = """
    <style>
    /* Global Reset & Base Styling */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Dark / Black & White Background Override */
    .stApp {
        background-color: #0B0F17;
        color: #F3F4F6;
    }
    
    /* Header Container Styling */
    .app-header {
        padding: 1.8rem 2rem;
        background: linear-gradient(180deg, #111827 0%, #0F172A 100%);
        border: 1px solid #1E293B;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }
    
    .app-header h1 {
        font-weight: 700;
        font-size: 2.2rem;
        color: #FFFFFF;
        margin-bottom: 0.4rem;
        letter-spacing: -0.02em;
    }
    
    .app-header p {
        color: #94A3B8;
        font-size: 1.05rem;
        font-weight: 400;
        margin: 0;
    }
    
    /* Sidebar Modern Container */
    [data-testid="stSidebar"] {
        background-color: #0F172A !important;
        border-right: 1px solid #1E293B;
    }

    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #F8FAFC !important;
    }

    /* Cards & Containers */
    .bw-card {
        background-color: #111827;
        border: 1px solid #1E293B;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.2rem;
        transition: border-color 0.2s ease-in-out;
    }
    
    .bw-card:hover {
        border-color: #334155;
    }

    /* Statistics Metrics Container */
    .stat-box {
        background: #111827;
        border: 1px solid #1E293B;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        text-align: center;
    }
    
    .stat-label {
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748B;
        margin-bottom: 0.3rem;
        font-weight: 600;
    }
    
    .stat-value {
        font-size: 1.35rem;
        font-weight: 700;
        color: #F8FAFC;
    }

    /* Agent Status Pill */
    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 500;
        margin-bottom: 8px;
        width: 100%;
        background-color: #111827;
        border: 1px solid #1E293B;
        color: #E2E8F0;
    }

    .status-pill.active {
        border-color: #38BDF8;
        color: #38BDF8;
        background-color: #0C4A6E22;
    }

    .status-pill.done {
        border-color: #22C55E;
        color: #4ADE80;
        background-color: #14532D22;
    }

    /* Primary Buttons Styling (B&W Sleek) */
    .stButton > button {
        background-color: #F8FAFC !important;
        color: #090D16 !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        padding: 0.6rem 1.4rem !important;
        border: none !important;
        transition: all 0.2s ease !important;
        width: 100%;
    }
    
    .stButton > button:hover {
        background-color: #E2E8F0 !important;
        box-shadow: 0 4px 12px rgba(255, 255, 255, 0.15) !important;
        transform: translateY(-1px);
    }
    
    .stDownloadButton > button {
        background-color: #1E293B !important;
        color: #F8FAFC !important;
        border: 1px solid #334155 !important;
        font-weight: 500 !important;
        border-radius: 10px !important;
        padding: 0.5rem 1rem !important;
        width: 100%;
    }

    .stDownloadButton > button:hover {
        background-color: #334155 !important;
        border-color: #475569 !important;
    }

    /* Text Inputs & Text Area */
    .stTextArea textarea, .stSelectbox select {
        background-color: #111827 !important;
        color: #F8FAFC !important;
        border: 1px solid #1E293B !important;
        border-radius: 10px !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #475569 !important;
        box-shadow: none !important;
    }

    /* Markdown Styling in Output */
    .blog-output-container {
        background-color: #111827;
        border: 1px solid #1E293B;
        border-radius: 16px;
        padding: 2.2rem;
        margin-top: 1.5rem;
        line-height: 1.7;
    }
    
    .blog-output-container h1, .blog-output-container h2, .blog-output-container h3 {
        color: #F8FAFC;
        margin-top: 1.5rem;
        margin-bottom: 0.8rem;
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
