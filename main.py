# main.py
import streamlit as st
from scrape import (
    scrape_website,
    extract_body_content,
    clean_body_content,
    split_dom_content,
)
from parse import parse_with_ollama

# — Page Config —
st.set_page_config(
    page_title="AI Web Scraper Pro",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="🔍"
)

# — Custom CSS & Google Fonts —
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
      :root {
        --primary: #1f2833;
        --secondary: #66fcf1;
        --bg: #0b0c10;
        --card: #1f2833;
        --text-light: #c5c6c7;
        --text-dark: #e8e8e8;
      }
      * { font-family: 'Inter', sans-serif; }
      body, .reportview-container .main {
        background-color: var(--bg);
        color: var(--text-dark);
      }
      h1, h2, h3, .css-18e3th9 { color: var(--secondary); }
      .stSidebar { background-color: var(--bg); }
      .stButton>button {
        background: linear-gradient(90deg, var(--secondary), #45a29e);
        color: var(--primary);
        font-weight: 600;
        border: none;
        border-radius: 4px;
        padding: 0.6rem 1.2rem;
      }
      .stButton>button:hover {
        opacity: 0.9;
      }
      .stTextInput>div>div>input,
      .stTextArea>div>div>textarea {
        background: var(--card);
        color: var(--text-light);
        border: 1px solid #333;
        border-radius: 4px;
        padding: 0.6rem;
      }
      .streamlit-expanderHeader {
        background-color: var(--card) !important;
        border-radius: 4px;
        color: var(--secondary) !important;
      }
      .card {
        background-color: var(--card);
        padding: 1.2rem;
        border-radius: 8px;
        margin-bottom: 1rem;
      }
      .section {
        padding: 2rem 0;
      }
      .divider {
        height: 2px;
        background: var(--secondary);
        margin: 2rem 0;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# — Header —
st.markdown(
    """
    <div style="text-align:center; padding:2rem 0;">
      <h1>AI Web Scraper Pro</h1>
      <p style="color:var(--text-light); max-width:700px; margin:auto;">
        Effortlessly scrape, clean, and parse web content—powered by a local LLM, 
        packaged in a seamless, modern interface.
      </p>
    </div>
    <div class="divider"></div>
    """,
    unsafe_allow_html=True,
)

# — Two‑column Features Section —
col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("One‑Click Scraping")
    st.write("Fetch any public webpage with a single button—no browser plugins or API keys required.")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("AI‑Powered Parsing")
    st.write("Extract exactly the data you need using a local LLM—no noise, no filler, just results.")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# — Scrape & Parse Form —
with st.form("workflow", clear_on_submit=False):
    st.subheader("Enter URL & Extraction Details")
    url = st.text_input("Website URL", placeholder="https://example.com")
    parse_description = st.text_area(
        "Extraction Request",
        placeholder="E.g., List all headings or extract product names and prices"
    )
    run = st.form_submit_button("Run")

if run:
    if not url:
        st.error("Please provide a valid URL.")
    else:
        # Scraping
        with st.spinner("Scraping website…"):
            html = scrape_website(url)
            body = extract_body_content(html)
            cleaned = clean_body_content(body)
            st.session_state.cleaned = cleaned
        st.success("Website scraped")

        # Display cleaned content side‑by‑side with parsed output
        c1, c2 = st.columns([1, 1])
        with c1:
            st.subheader("Cleaned Content")
            st.text_area("", st.session_state.cleaned, height=300)
        with c2:
            st.subheader("Parsed Output")
            if parse_description:
                with st.spinner("Parsing with LLM…"):
                    chunks = split_dom_content(st.session_state.cleaned)
                    parsed = parse_with_ollama(chunks, parse_description)
                    st.session_state.parsed = parsed
                st.text_area("", st.session_state.parsed or "No matching data found.", height=300)
            else:
                st.info("Add a description to extract data.")

# — Footer —
st.markdown(
    """
    <div class="section" style="text-align:center; color:var(--text-light); font-size:0.9rem;">
      © 2025 AI Web Scraper Pro &middot; Built with Streamlit &middot; Designed for professionals
    </div>
    """,
    unsafe_allow_html=True,
)
