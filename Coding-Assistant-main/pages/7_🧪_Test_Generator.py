import streamlit as st

st.set_page_config(page_title="Test Generator", page_icon="🧪", layout="wide")

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

st.title("🧪 Unit Test Generator")
st.caption("Generate comprehensive unit tests for your code")

code_to_test = st.text_area(
    "Paste code to generate tests for:",
    height=300,
    placeholder="Paste the code you want to test..."
)

col1, col2, col3 = st.columns(3)

with col1:
    test_language = st.selectbox(
        "Language",
        ["Python", "JavaScript", "TypeScript", "Java", "Go", "C#", "Ruby"]
    )

with col2:
    test_framework = st.selectbox(
        "Test framework:",
        ["pytest", "unittest", "Jest", "Mocha", "JUnit", "Go testing", "NUnit", "RSpec"]
    )

with col3:
    coverage = st.slider("Coverage goal:", 50, 100, 80, 5)

include_edge_cases = st.checkbox("Include edge cases", value=True)
include_mocks = st.checkbox("Include mocks/stubs", value=False)

if st.button("🧪 Generate Tests", type="primary", use_container_width=True):
    if code_to_test:
        with st.spinner("Generating unit tests..."):
            prompt = f"Generate {test_framework} unit tests for this {test_language} code with {coverage}% coverage:\n\n{code_to_test}"
            
            if include_edge_cases:
                prompt += "\n\nInclude tests for edge cases and error conditions."
            
            if include_mocks:
                prompt += "\n\nInclude mocks and stubs for external dependencies."
            
            response = llm.generate_tests(prompt, test_language)
            
            st.markdown("### 🧪 Generated Tests")
            st.code(response, language=test_language.lower())
            
            # Save to history
            if db:
                db.add_conversation(f"Generate tests for {test_language}", response, response, test_language)
            
            # Download
            st.download_button(
                "📥 Download Tests",
                response,
                f"test_code.{test_language.lower()}",
                use_container_width=True
            )
    else:
        st.warning("Please paste code to generate tests for.")

# Testing tips
with st.expander("✅ Testing Best Practices"):
    st.markdown("""
    **Good Tests Should:**
    - Test one thing at a time (single responsibility)
    - Be independent and isolated
    - Have clear, descriptive names
    - Cover happy paths and edge cases
    - Be fast and deterministic
    - Use arrange-act-assert pattern
    
    **Test Coverage Should Include:**
    - Normal/expected inputs
    - Boundary conditions
    - Invalid inputs
    - Error handling
    - Edge cases and corner cases
    """)

with st.expander("🎯 Common Test Patterns"):
    st.markdown("""
    **Unit Tests**: Test individual functions/methods in isolation
    
    **Integration Tests**: Test how components work together
    
    **Mocking**: Replace external dependencies with controlled test doubles
    
    **Parameterized Tests**: Run same test with different inputs
    
    **Fixtures**: Set up and tear down test data/environment
    """)
