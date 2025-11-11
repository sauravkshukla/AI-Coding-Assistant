import streamlit as st

st.set_page_config(page_title="Code Quality", page_icon="📊", layout="wide")

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

st.title("📊 Code Quality Analyzer")
st.caption("Comprehensive code review for performance, security, and best practices")

code_to_analyze = st.text_area(
    "Paste your code for quality analysis:",
    height=300,
    placeholder="Paste the code you want to analyze..."
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    analysis_language = st.selectbox(
        "Language",
        ["Python", "JavaScript", "TypeScript", "Java", "C++", "Go", "Rust", "C#"]
    )

with col2:
    check_performance = st.checkbox("⚡ Performance", value=True)

with col3:
    check_security = st.checkbox("🔒 Security", value=True)

with col4:
    check_style = st.checkbox("✨ Style", value=True)

if st.button("🔍 Analyze Code", type="primary", use_container_width=True):
    if code_to_analyze:
        with st.spinner("Analyzing code quality..."):
            checks = []
            if check_performance:
                checks.append("performance and efficiency")
            if check_security:
                checks.append("security vulnerabilities")
            if check_style:
                checks.append("style and best practices")
            
            prompt = f"Analyze this {analysis_language} code for {', '.join(checks)}:\n\n{code_to_analyze}"
            prompt += "\n\nProvide a detailed analysis with severity levels (Critical/High/Medium/Low) and specific recommendations."
            
            response = llm.analyze_quality(prompt)
            
            st.markdown("### 📋 Analysis Results")
            st.markdown(response)
            
            # Save to history
            if db:
                db.add_conversation(f"Quality analysis: {analysis_language}", response)
            
            # Export report
            st.download_button(
                "📥 Download Report",
                response,
                "code_quality_report.md",
                "text/markdown",
                use_container_width=True
            )
    else:
        st.warning("Please paste code to analyze.")

# Analysis categories
with st.expander("📚 What We Analyze"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **⚡ Performance**
        - Algorithm complexity
        - Memory usage
        - Unnecessary computations
        - Caching opportunities
        - Database query optimization
        """)
    
    with col2:
        st.markdown("""
        **🔒 Security**
        - SQL injection risks
        - XSS vulnerabilities
        - Authentication issues
        - Data validation
        - Sensitive data exposure
        """)
    
    with col3:
        st.markdown("""
        **✨ Style & Best Practices**
        - Code readability
        - Naming conventions
        - Code duplication
        - Error handling
        - Documentation
        """)
