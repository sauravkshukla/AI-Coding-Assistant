import streamlit as st

st.set_page_config(page_title="Documentation", page_icon="📝", layout="wide")

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

st.title("📝 Documentation Generator")
st.caption("Generate comprehensive documentation for your code")

code_to_document = st.text_area(
    "Paste code to document:",
    height=300,
    placeholder="Paste the code you want to document..."
)

col1, col2 = st.columns(2)

with col1:
    doc_language = st.selectbox(
        "Language",
        ["Python", "JavaScript", "TypeScript", "Java", "C++", "Go", "Rust", "C#", "PHP"]
    )

with col2:
    doc_style = st.selectbox(
        "Documentation style:",
        [
            "Inline comments",
            "Docstrings/JSDoc",
            "README format",
            "API documentation",
            "Tutorial format"
        ]
    )

include_examples = st.checkbox("Include usage examples", value=True)

if st.button("📝 Generate Documentation", type="primary", use_container_width=True):
    if code_to_document:
        with st.spinner("Generating documentation..."):
            prompt = f"Generate {doc_style} for this {doc_language} code:\n\n{code_to_document}"
            
            if include_examples:
                prompt += "\n\nInclude practical usage examples."
            
            response = llm.generate_docs(prompt, doc_language)
            
            st.markdown("### 📄 Generated Documentation")
            st.markdown(response)
            
            # Save to history
            if db:
                db.add_conversation(f"Document {doc_language} code", response)
            
            # Download
            st.download_button(
                "📥 Download Documentation",
                response,
                "documentation.md",
                "text/markdown",
                use_container_width=True
            )
    else:
        st.warning("Please paste code to document.")

# Documentation tips
with st.expander("💡 Documentation Best Practices"):
    st.markdown("""
    **Good Documentation Should:**
    - Explain WHAT the code does (high-level overview)
    - Explain WHY certain decisions were made
    - Describe parameters and return values
    - Include usage examples
    - Note any edge cases or limitations
    - Mention dependencies and requirements
    
    **Avoid:**
    - Stating the obvious (e.g., "this function adds two numbers" for `add(a, b)`)
    - Outdated comments that don't match the code
    - Over-commenting simple, self-explanatory code
    """)
