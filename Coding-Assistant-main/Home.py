import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page config MUST be first
st.set_page_config(
    page_title="AI Coding Assistant",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

from database import HistoryDB
from embeddings import SemanticSearch
from llm_handler import LLMHandler

# Load custom CSS
def load_css():
    try:
        with open("style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except:
        pass

load_css()

# Initialize session state for model selection
if 'use_gemini' not in st.session_state:
    st.session_state.use_gemini = True  # Default to Gemini
if 'gemini_api_key' not in st.session_state:
    # Load from environment variable
    st.session_state.gemini_api_key = os.getenv('GEMINI_API_KEY', '')

# Initialize components
@st.cache_resource
def init_components(use_gemini=False, api_key=None):
    db = HistoryDB()
    search = SemanticSearch()
    llm = LLMHandler(model="llama3.1:latest", use_gemini=use_gemini, api_key=api_key)
    return db, search, llm

# Clear cache on first load
if 'initialized' not in st.session_state:
    st.cache_resource.clear()
    st.session_state.initialized = True

db, search, llm = init_components(st.session_state.use_gemini, st.session_state.gemini_api_key)

# Store in session state for access across pages
st.session_state.db = db
st.session_state.search = search
st.session_state.llm = llm

# Hero section
st.title("💻 AI Coding Assistant")
st.markdown("### Your Intelligent Coding Companion")

st.markdown("")

# Stats dashboard
conversations = db.get_all_conversations()
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("💬 Conversations", len(conversations))
with col2:
    model_name = "Gemini 2.0" if st.session_state.use_gemini else "Llama 3.1"
    st.metric("🤖 Active Model", model_name)
with col3:
    privacy = "Cloud" if st.session_state.use_gemini else "100% Local"
    st.metric("🔒 Privacy", privacy)
with col4:
    st.metric("📡 Status", "🟢 Online")

st.markdown("---")

# Feature highlights
st.markdown("## ✨ All Features")

# Create feature cards
features = [
    {"icon": "💬", "title": "Chat", "desc": "AI-powered coding conversations", "page": "pages/1_💬_Chat.py"},
    {"icon": "🔧", "title": "Generator", "desc": "Create code from descriptions", "page": "pages/2_🔧_Code_Generator.py"},
    {"icon": "🐛", "title": "Bug Fixer", "desc": "Debug and repair code", "page": "pages/3_🐛_Bug_Fixer.py"},
    {"icon": "📊", "title": "Quality", "desc": "Analyze code quality", "page": "pages/4_📊_Code_Quality.py"},
    {"icon": "♻️", "title": "Refactor", "desc": "Improve code structure", "page": "pages/5_♻️_Refactor.py"},
    {"icon": "📝", "title": "Docs", "desc": "Generate documentation", "page": "pages/6_📝_Documentation.py"},
    {"icon": "🧪", "title": "Tests", "desc": "Create unit tests", "page": "pages/7_🧪_Test_Generator.py"},
    {"icon": "🔍", "title": "Explainer", "desc": "Understand code easily", "page": "pages/8_🔍_Code_Explainer.py"},
    {"icon": "⚡", "title": "Playground", "desc": "Test code in browser", "page": "pages/10_⚡_Code_Playground.py"},
    {"icon": "📚", "title": "History", "desc": "Search past chats", "page": "pages/9_📚_History.py"}
]

# Display in 5 columns
cols = st.columns(5)
for i, feature in enumerate(features):
    with cols[i % 5]:
        st.markdown(f"### {feature['icon']}")
        st.markdown(f"**{feature['title']}**")
        st.caption(feature['desc'])
        if st.button("Open", key=f"btn_{i}", use_container_width=True):
            st.switch_page(feature['page'])

st.markdown("---")

# Supported languages
st.markdown("## 🌐 Supported Languages")
st.markdown("""
<div style='text-align: center; font-size: 1.1em; padding: 10px;'>
Python • JavaScript • TypeScript • Java • C++ • Go • Rust • C# • PHP • Ruby • Swift • Kotlin • SQL • Bash
</div>
""", unsafe_allow_html=True)

# Quick info
st.markdown("---")
st.markdown("### 📊 Quick Stats")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**🎯 Features**")
    st.markdown("- 10 AI-powered tools")
    st.markdown("- Multi-language support")
    st.markdown("- Code playground")
    st.markdown("- Conversation history")

with col2:
    st.markdown("**🔧 Capabilities**")
    st.markdown("- Code generation")
    st.markdown("- Bug fixing & debugging")
    st.markdown("- Quality analysis")
    st.markdown("- Test generation")

with col3:
    st.markdown("**🌟 Languages**")
    st.markdown("- Python, JavaScript, TypeScript")
    st.markdown("- Java, C++, Go, Rust")
    st.markdown("- C#, PHP, Ruby, Swift")
    st.markdown("- SQL, Kotlin, and more")
