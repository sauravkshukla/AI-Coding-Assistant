import streamlit as st

st.set_page_config(page_title="Refactor", page_icon="♻️", layout="wide")

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

st.title("♻️ Code Refactoring")
st.caption("Improve code structure, readability, and maintainability")

code_to_refactor = st.text_area(
    "Paste code to refactor:",
    height=300,
    placeholder="Paste the code you want to improve..."
)

col1, col2 = st.columns([2, 1])

with col1:
    refactor_goals = st.multiselect(
        "Refactoring goals:",
        [
            "Improve readability",
            "Optimize performance",
            "Reduce complexity",
            "Follow design patterns",
            "Make more modular",
            "Add type hints/annotations",
            "Remove code duplication",
            "Improve error handling"
        ],
        default=["Improve readability"]
    )

with col2:
    refactor_language = st.selectbox(
        "Language",
        ["Python", "JavaScript", "TypeScript", "Java", "C++", "Go", "Rust", "C#"]
    )
    
    preserve_behavior = st.checkbox("Preserve exact behavior", value=True)

if st.button("♻️ Refactor Code", type="primary", use_container_width=True):
    if code_to_refactor and refactor_goals:
        with st.spinner("Refactoring code..."):
            goals_str = ", ".join(refactor_goals)
            prompt = f"Refactor this {refactor_language} code to {goals_str}:\n\n{code_to_refactor}"
            
            if preserve_behavior:
                prompt += "\n\nIMPORTANT: Preserve the exact behavior and functionality."
            
            response = llm.refactor_code(prompt, refactor_language)
            
            # Display side by side
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.markdown("### 📝 Original Code")
                st.code(code_to_refactor, language=refactor_language.lower())
            
            with col_b:
                st.markdown("### ✨ Refactored Code")
                st.code(response, language=refactor_language.lower())
            
            # Save to history
            if db:
                db.add_conversation(f"Refactor {refactor_language}", response, response, refactor_language)
            
            # Download
            st.download_button(
                "📥 Download Refactored Code",
                response,
                f"refactored_code.{refactor_language.lower()}",
                use_container_width=True
            )
    else:
        st.warning("Please paste code and select at least one refactoring goal.")

# Refactoring patterns
with st.expander("🎯 Refactoring Patterns"):
    st.markdown("""
    **Extract Method**: Break down large functions into smaller, focused ones
    
    **Rename Variable**: Use descriptive names that reveal intent
    
    **Remove Duplication**: Consolidate repeated code into reusable functions
    
    **Simplify Conditionals**: Make complex if-else chains more readable
    
    **Introduce Design Patterns**: Apply appropriate patterns (Strategy, Factory, etc.)
    
    **Optimize Loops**: Reduce nested loops and improve iteration efficiency
    
    **Add Type Safety**: Include type hints and annotations for better code clarity
    """)
