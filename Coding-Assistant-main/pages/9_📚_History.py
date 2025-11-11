import streamlit as st

st.set_page_config(page_title="History", page_icon="📚", layout="wide")

# Initialize components if not already done
if 'db' not in st.session_state:
    from database import HistoryDB
    from embeddings import SemanticSearch
    st.session_state.db = HistoryDB()
    st.session_state.search = SemanticSearch()

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

st.title("📚 Conversation History")
st.caption("Search and manage your past conversations")

# Get stats
if db:
    stats = db.get_stats()
    
    # Display stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Conversations", stats["total"])
    with col2:
        st.metric("Languages Used", len(stats["by_language"]))
    with col3:
        if stats["by_language"]:
            most_used = max(stats["by_language"].items(), key=lambda x: x[1])
            st.metric("Most Used Language", most_used[0])
        else:
            st.metric("Most Used Language", "N/A")
    
    st.markdown("---")

# Sidebar controls
with st.sidebar:
    st.markdown("### 🔧 Actions")
    
    if st.button("🔄 Rebuild Search Index", use_container_width=True):
        if db:
            conversations = db.get_all_conversations()
            if search:
                search.build_index(conversations)
                st.success(f"✅ Index rebuilt with {len(conversations)} conversations")
            else:
                st.error("Search component not available")
    
    st.markdown("---")
    
    # Clear history with confirmation
    st.markdown("### ⚠️ Danger Zone")
    if st.button("🗑️ Clear All History", use_container_width=True, type="secondary"):
        st.session_state.show_confirm = True
    
    if st.session_state.get('show_confirm', False):
        st.warning("⚠️ This will delete ALL conversation history!")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Confirm", use_container_width=True):
                if db:
                    db.clear_all()
                    st.success("All history cleared!")
                    st.session_state.show_confirm = False
                    st.rerun()
        with col2:
            if st.button("❌ Cancel", use_container_width=True):
                st.session_state.show_confirm = False
                st.rerun()
    
    st.markdown("---")
    
    # Export all history
    if st.button("📥 Export All History", use_container_width=True):
        if db:
            conversations = db.get_all_conversations()
            if conversations:
                export_text = "# Conversation History\n\n"
                for r in conversations:
                    export_text += f"## {r[1]}\n\n"
                    export_text += f"**Query:** {r[2]}\n\n"
                    export_text += f"**Response:** {r[3]}\n\n"
                    if r[4]:
                        export_text += f"```{r[5] if r[5] else ''}\n{r[4]}\n```\n\n"
                    export_text += "---\n\n"
                
                st.download_button(
                    "📥 Download",
                    export_text,
                    "history_export.md",
                    "text/markdown",
                    use_container_width=True
                )

# Search section
st.markdown("### 🔍 Search History")
col1, col2 = st.columns([3, 1])

with col1:
    keyword = st.text_input("Search by keyword:", placeholder="Enter search term...", label_visibility="collapsed")

with col2:
    search_button = st.button("🔍 Search", use_container_width=True)

if (keyword and search_button) or keyword:
    if db:
        results = db.search_by_keyword(keyword)
        
        if results:
            st.success(f"Found {len(results)} results")
            
            for r in results:
                with st.expander(f"📅 {r[1][:19]} | {r[2][:80]}..."):
                    col_a, col_b = st.columns([3, 1])
                    
                    with col_a:
                        st.markdown(f"**🔹 Query:**")
                        st.info(r[2])
                        
                        st.markdown(f"**💬 Response:**")
                        st.markdown(r[3])
                        
                        if r[4]:  # code snippet
                            st.markdown(f"**💻 Code:**")
                            st.code(r[4], language=r[5].lower() if r[5] else "")
                    
                    with col_b:
                        st.markdown(f"**ID:** {r[0]}")
                        st.markdown(f"**Time:** {r[1][11:19]}")
                        if r[5]:
                            st.markdown(f"**Language:** {r[5]}")
                        
                        if st.button("🗑️ Delete", key=f"del_{r[0]}", use_container_width=True):
                            db.delete_conversation(r[0])
                            st.success("Deleted!")
                            st.rerun()
        else:
            st.warning(f"No results found for '{keyword}'")
else:
    # Show recent conversations
    st.markdown("### 📝 Recent Conversations")
    
    if db:
        conversations = db.get_all_conversations()
        
        if conversations:
            # Pagination
            items_per_page = 10
            total_pages = (len(conversations) + items_per_page - 1) // items_per_page
            
            if 'history_page' not in st.session_state:
                st.session_state.history_page = 0
            
            # Page navigation
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                if st.button("⬅️ Previous", disabled=st.session_state.history_page == 0):
                    st.session_state.history_page -= 1
                    st.rerun()
            with col2:
                st.markdown(f"<center>Page {st.session_state.history_page + 1} of {total_pages}</center>", unsafe_allow_html=True)
            with col3:
                if st.button("Next ➡️", disabled=st.session_state.history_page >= total_pages - 1):
                    st.session_state.history_page += 1
                    st.rerun()
            
            st.markdown("---")
            
            # Display conversations for current page
            start_idx = st.session_state.history_page * items_per_page
            end_idx = start_idx + items_per_page
            page_conversations = conversations[start_idx:end_idx]
            
            for r in page_conversations:
                with st.expander(f"📅 {r[1][:19]} | {r[2][:80]}..."):
                    col_a, col_b = st.columns([3, 1])
                    
                    with col_a:
                        st.markdown(f"**🔹 Query:**")
                        st.info(r[2])
                        
                        st.markdown(f"**💬 Response:**")
                        response_preview = r[3][:500] + "..." if len(r[3]) > 500 else r[3]
                        st.markdown(response_preview)
                        
                        if r[4]:  # code snippet
                            st.markdown(f"**💻 Code:**")
                            code_preview = r[4][:300] + "..." if len(r[4]) > 300 else r[4]
                            st.code(code_preview, language=r[5].lower() if r[5] else "")
                    
                    with col_b:
                        st.markdown(f"**ID:** {r[0]}")
                        st.markdown(f"**Time:** {r[1][11:19]}")
                        if r[5]:
                            st.markdown(f"**Language:** {r[5]}")
                        
                        if st.button("🗑️ Delete", key=f"del_{r[0]}", use_container_width=True):
                            db.delete_conversation(r[0])
                            st.success("Deleted!")
                            st.rerun()
        else:
            st.info("📭 No conversations yet. Start chatting to build your history!")
            
            # Quick links to get started
            st.markdown("### 🚀 Get Started")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("💬 Start Chat", use_container_width=True):
                    st.switch_page("pages/1_💬_Chat.py")
            
            with col2:
                if st.button("🔧 Generate Code", use_container_width=True):
                    st.switch_page("pages/2_🔧_Code_Generator.py")
            
            with col3:
                if st.button("🐛 Fix Bugs", use_container_width=True):
                    st.switch_page("pages/3_🐛_Bug_Fixer.py")
