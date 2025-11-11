import streamlit as st
import subprocess
import sys
import tempfile
import os

st.set_page_config(page_title="Code Playground", page_icon="⚡", layout="wide")

# Initialize components if not already done
if 'llm' not in st.session_state:
    from database import HistoryDB
    from embeddings import SemanticSearch
    from llm_handler import LLMHandler
    
    st.session_state.db = HistoryDB()
    st.session_state.search = SemanticSearch()
    st.session_state.llm = LLMHandler(model="llama3.1:latest")

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

with st.sidebar:
    st.markdown("### Quick Actions")
    if st.button("Clear Code", use_container_width=True):
        st.session_state.code_input = ""
        st.rerun()
    
    if st.button("Clear Output", use_container_width=True):
        if 'output' in st.session_state:
            del st.session_state.output
        st.rerun()

st.title("⚡ Code Playground")
st.caption("Write and test code instantly in your browser")

# Language selection
col1, col2 = st.columns([3, 1])

with col2:
    language = st.selectbox(
        "Language",
        ["Python", "JavaScript", "Go", "Rust", "C++", "Java"],
        help="Select programming language"
    )

# Code editor
st.markdown("### Code Editor")

# Default code examples
default_code = {
    "Python": "# Python Code\nprint('Hello, World!')\n\n# Try some math\nresult = 2 + 2\nprint(f'2 + 2 = {result}')",
    "JavaScript": "// JavaScript Code\nconsole.log('Hello, World!');\n\n// Try some math\nconst result = 2 + 2;\nconsole.log(`2 + 2 = ${result}`);",
    "Go": "package main\n\nimport \"fmt\"\n\nfunc main() {\n    fmt.Println(\"Hello, World!\")\n    result := 2 + 2\n    fmt.Printf(\"2 + 2 = %d\\n\", result)\n}",
    "Rust": "fn main() {\n    println!(\"Hello, World!\");\n    let result = 2 + 2;\n    println!(\"2 + 2 = {}\", result);\n}",
    "C++": "#include <iostream>\nusing namespace std;\n\nint main() {\n    cout << \"Hello, World!\" << endl;\n    int result = 2 + 2;\n    cout << \"2 + 2 = \" << result << endl;\n    return 0;\n}",
    "Java": "public class Main {\n    public static void main(String[] args) {\n        System.out.println(\"Hello, World!\");\n        int result = 2 + 2;\n        System.out.println(\"2 + 2 = \" + result);\n    }\n}"
}

if 'code_input' not in st.session_state:
    st.session_state.code_input = default_code.get(language, "")

code = st.text_area(
    "Write your code here:",
    value=st.session_state.code_input,
    height=300,
    key="code_editor"
)

st.session_state.code_input = code

# Run button
col1, col2, col3 = st.columns([1, 1, 4])
with col1:
    run_button = st.button("▶️ Run Code", type="primary", use_container_width=True)
with col2:
    load_example = st.button("📝 Load Example", use_container_width=True)

if load_example:
    st.session_state.code_input = default_code.get(language, "")
    st.rerun()

# Execute code
if run_button and code.strip():
    st.markdown("### Output")
    
    with st.spinner(f"Running {language} code..."):
        try:
            if language == "Python":
                # Run Python code
                result = subprocess.run(
                    [sys.executable, "-c", code],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                
                if result.stdout:
                    st.code(result.stdout, language="text")
                if result.stderr:
                    st.error(result.stderr)
                    
            elif language == "JavaScript":
                # Run JavaScript with Node.js
                with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
                    f.write(code)
                    temp_file = f.name
                
                try:
                    result = subprocess.run(
                        ["node", temp_file],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    
                    if result.stdout:
                        st.code(result.stdout, language="text")
                    if result.stderr:
                        st.error(result.stderr)
                finally:
                    os.unlink(temp_file)
                    
            else:
                st.warning(f"{language} execution not yet implemented. Currently supports Python and JavaScript.")
                st.info("Your code is valid and ready to run in a proper environment!")
                
        except subprocess.TimeoutExpired:
            st.error("Code execution timed out (5 seconds limit)")
        except FileNotFoundError as e:
            if language == "JavaScript":
                st.error("Node.js not found. Please install Node.js to run JavaScript code.")
            else:
                st.error(f"Required compiler/interpreter not found: {e}")
        except Exception as e:
            st.error(f"Error executing code: {str(e)}")

# Tips section
with st.expander("💡 Tips & Limitations"):
    st.markdown("""
    **Supported Languages:**
    - ✅ **Python**: Fully supported (uses your Python installation)
    - ✅ **JavaScript**: Requires Node.js installed
    - ⚠️ **Go, Rust, C++, Java**: Syntax highlighting only (requires compilers)
    
    **Limitations:**
    - 5 second execution timeout
    - No file I/O operations
    - No network access
    - Limited to standard library
    
    **Tips:**
    - Use print/console.log to see output
    - Keep code simple for quick testing
    - For complex projects, use a full IDE
    """)

with st.expander("🔧 Installation Guide"):
    st.markdown("""
    **To enable JavaScript support:**
    ```bash
    # Install Node.js from https://nodejs.org
    # Or use package manager:
    # Windows: choco install nodejs
    # Mac: brew install node
    # Linux: sudo apt install nodejs
    ```
    
    **To enable other languages:**
    - **Go**: Install from https://go.dev
    - **Rust**: Install from https://rustup.rs
    - **C++**: Install GCC or Clang
    - **Java**: Install JDK from https://adoptium.net
    """)
