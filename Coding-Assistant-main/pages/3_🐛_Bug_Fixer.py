import streamlit as st

st.set_page_config(page_title="Bug Fixer", page_icon="🐛", layout="wide")

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

st.title("🐛 Bug Fixer & Debugger")
st.caption("Analyze, debug, and repair your code")

col1, col2 = st.columns([3, 1])

with col1:
    buggy_code = st.text_area(
        "Paste your buggy code:",
        height=300,
        placeholder="Paste the code that's causing issues..."
    )

with col2:
    st.markdown("### Options")
    code_language = st.selectbox(
        "Language",
        ["Python", "JavaScript", "TypeScript", "Java", "C++", "Go", "Rust", "C#"]
    )
    
    error_msg = st.text_area(
        "Error message (optional):",
        height=100,
        placeholder="Paste any error messages here..."
    )
    
    explain_fix = st.checkbox("Explain the fix", value=True)

if st.button("🔧 Fix Bug", type="primary", use_container_width=True):
    if buggy_code:
        with st.spinner("Analyzing and fixing bugs..."):
            # First, get the fixed code
            fix_prompt = f"Fix the bugs in this {code_language} code:\n\n{buggy_code}"
            if error_msg:
                fix_prompt += f"\n\nError message: {error_msg}"
            
            fixed_code = llm.fix_bug(fix_prompt, code_language)
            
            # Then, get explanation if requested
            explanation = ""
            if explain_fix:
                explain_prompt = f"""Analyze the bugs that were fixed in this {code_language} code.

Original Code:
{buggy_code}

Fixed Code:
{fixed_code}

Provide a detailed analysis in this format:
## 🐛 Bugs Found

1. **Bug Name**: Brief description
   - **Severity**: Critical/High/Medium/Low
   - **Issue**: What was wrong
   - **Fix**: How it was fixed

2. (Continue for each bug found)

## ✅ Summary
Brief summary of all fixes applied."""
                
                explanation = llm.generate_response(explain_prompt)
            
            # Display side by side
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.markdown("### 🔴 Original Code")
                st.code(buggy_code, language=code_language.lower())
            
            with col_b:
                st.markdown("### ✅ Fixed Code")
                st.code(fixed_code, language=code_language.lower())
            
            # Show explanation below
            if explanation:
                st.markdown("---")
                st.markdown("### 📋 Bug Analysis & Fixes")
                st.markdown(explanation)
            
            # Save to history
            if db:
                db.add_conversation(f"Fix bug in {code_language}", fixed_code, fixed_code, code_language)
            
            # Download buttons
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    "📥 Download Fixed Code",
                    fixed_code,
                    f"fixed_code.{code_language.lower()}",
                    use_container_width=True
                )
            with col2:
                if explanation:
                    st.download_button(
                        "📄 Download Report",
                        explanation,
                        "bug_fix_report.md",
                        "text/markdown",
                        use_container_width=True
                    )
    else:
        st.warning("Please paste the code you want to fix.")

# Common issues
with st.expander("🔍 Common Issues We Can Fix"):
    st.markdown("""
    **Syntax Errors:**
    - Missing brackets, parentheses, or semicolons
    - Incorrect indentation
    - Invalid syntax for the language
    
    **Logic Errors:**
    - Off-by-one errors in loops
    - Incorrect conditional statements
    - Wrong operator usage
    
    **Runtime Errors:**
    - Null pointer/undefined references
    - Index out of bounds
    - Type mismatches
    
    **Performance Issues:**
    - Inefficient algorithms
    - Memory leaks
    - Unnecessary computations
    """)
