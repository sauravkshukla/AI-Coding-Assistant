import streamlit as st

st.set_page_config(page_title="Code Explainer", page_icon="🔍", layout="wide")

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

st.title("🔍 Code Explainer")
st.caption("Understand code with detailed, structured explanations")

code_to_explain = st.text_area(
    "Paste code to explain:",
    height=300,
    placeholder="Paste the code you want to understand..."
)

col1, col2 = st.columns(2)

with col1:
    explain_language = st.selectbox(
        "Language",
        ["Python", "JavaScript", "TypeScript", "Java", "C++", "Go", "Rust", "C#", "SQL", "Bash"]
    )

with col2:
    detail_level = st.select_slider(
        "Explanation detail:",
        options=["Beginner-friendly", "Intermediate", "Advanced"],
        value="Intermediate"
    )

explain_options = st.multiselect(
    "Focus on:",
    ["Algorithm logic", "Data structures", "Design patterns", "Performance", "Best practices"],
    default=["Algorithm logic"]
)

if st.button("🔍 Explain Code", type="primary", use_container_width=True):
    if code_to_explain:
        with st.spinner("Analyzing code..."):
            prompt = f"Explain this {explain_language} code at a {detail_level} level:\n\n{code_to_explain}"
            
            if explain_options:
                prompt += f"\n\nFocus on: {', '.join(explain_options)}"
            
            response = llm.explain_code(prompt)
            
            # Display code and explanation side by side
            col_a, col_b = st.columns([1, 1])
            
            with col_a:
                st.markdown("### 📝 Code")
                st.code(code_to_explain, language=explain_language.lower())
            
            with col_b:
                st.markdown("### 💡 Explanation")
                st.markdown(response)
            
            # Save to history
            if db:
                db.add_conversation(f"Explain {explain_language} code", response)
            
            # Download
            st.download_button(
                "📥 Download Explanation",
                response,
                "code_explanation.md",
                "text/markdown",
                use_container_width=True
            )
    else:
        st.warning("Please paste code to explain.")

# Learning resources
with st.expander("📚 How to Get Better Explanations"):
    st.markdown("""
    **For Beginners:**
    - Start with small code snippets
    - Ask for step-by-step breakdowns
    - Request analogies and real-world examples
    
    **For Intermediate:**
    - Focus on design patterns and architecture
    - Ask about trade-offs and alternatives
    - Explore performance implications
    
    **For Advanced:**
    - Deep dive into algorithms and complexity
    - Understand low-level implementation details
    - Analyze optimization opportunities
    """)
