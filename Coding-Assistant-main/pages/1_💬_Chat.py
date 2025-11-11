import streamlit as st

st.set_page_config(page_title="Chat", page_icon="💬", layout="wide")

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
search = st.session_state.search

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

st.title("💬 Chat Assistant")
st.caption("General coding conversations with context awareness")

# Sidebar settings
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    use_semantic_search = st.checkbox("Use Semantic Search", value=True, 
                                      help="Find and use relevant past conversations")
    
    st.markdown("---")
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    
    # Export
    if st.button("📥 Export Chat"):
        if 'messages' in st.session_state and st.session_state.messages:
            export_text = "\n\n".join([f"**{m['role'].upper()}:** {m['content']}" 
                                       for m in st.session_state.messages])
            st.download_button("Download Markdown", export_text, 
                             "chat_export.md", "text/markdown")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything about coding..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            context = ""
            
            # Semantic search for relevant history
            if use_semantic_search and db and search:
                conversations = db.get_all_conversations()
                if conversations:
                    search.build_index(conversations)
                    similar = search.search(prompt, k=3)
                    if similar:
                        context = "\n".join([f"Q: {s[2]}\nA: {s[3][:200]}" for s in similar])
            
            # Generate response
            response = llm.generate_response(prompt, context, st.session_state.messages[:-1])
            st.markdown(response)
    
    # Save to history
    st.session_state.messages.append({"role": "assistant", "content": response})
    if db:
        db.add_conversation(prompt, response)
