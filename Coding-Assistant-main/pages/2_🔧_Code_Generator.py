import streamlit as st

st.set_page_config(page_title="Code Generator", page_icon="🔧", layout="wide")

# Initialize components if not already done
if 'db' not in st.session_state:
    from database import HistoryDB
    from embeddings import SemanticSearch
    st.session_state.db = HistoryDB()
    st.session_state.search = SemanticSearch()

# Always reinitialize LLM based on current settings
from llm_handler import LLMHandler
llm = LLMHandler(
    model="llama3.1:latest",
    use_gemini=st.session_state.get('use_gemini', True),
    api_key=st.session_state.get('gemini_api_key', '')
)

db = st.session_state.db

# Load custom CSS
def load_css():
    try:
        with open("style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except:
        pass

load_css()

# Sidebar
from sidebar_config import render_sidebar
render_sidebar()

st.title("🔧 Code Generator")
st.caption("Generate production-ready code from natural language descriptions")

col1, col2 = st.columns([2, 1])

with col1:
    description = st.text_area(
        "Describe what you want to build:",
        height=200,
        placeholder="Example: Create a Python function to sort a list of dictionaries by a specific key, with options for ascending/descending order"
    )

with col2:
    st.markdown("### Options")
    language = st.selectbox(
        "Language",
        ["Python", "JavaScript", "TypeScript", "Java", "C++", "Go", "Rust", "C#", "PHP", "Ruby", "Swift", "Kotlin"]
    )
    
    include_tests = st.checkbox("Include unit tests")
    include_docs = st.checkbox("Include documentation")
    include_examples = st.checkbox("Include usage examples")

if st.button("✨ Generate Code", type="primary", use_container_width=True):
    if description:
        with st.spinner(f"Generating {language} code..."):
            prompt = f"Generate {language} code for: {description}"
            
            if include_tests:
                prompt += "\nInclude comprehensive unit tests."
            if include_docs:
                prompt += "\nInclude detailed documentation and comments."
            if include_examples:
                prompt += "\nInclude usage examples."
            
            response = llm.generate_code(prompt, language)
            
            st.markdown("### Generated Code")
            st.code(response, language=language.lower())
            
            # Save to history
            if db:
                db.add_conversation(description, response, response, language)
            
            # Copy button
            st.download_button(
                "📋 Download Code",
                response,
                f"generated_code.{language.lower()}",
                use_container_width=True
            )
    else:
        st.warning("Please provide a description of what you want to build.")

# Examples
with st.expander("💡 Example Prompts"):
    st.markdown("""
    **Python:**
    - Create a decorator that measures function execution time
    - Build a REST API client with retry logic and exponential backoff
    - Implement a binary search tree with insert, delete, and search operations
    
    **JavaScript:**
    - Create a debounce function for search input
    - Build a promise-based HTTP client with interceptors
    - Implement a virtual scrolling component for large lists
    
    **Go:**
    - Create a concurrent worker pool with graceful shutdown
    - Build a middleware chain for HTTP handlers
    - Implement a rate limiter using token bucket algorithm
    """)
