import streamlit as st
import os

def render_sidebar():
    """Render the global sidebar with model toggle"""
    
    # Initialize session state if not already done
    if 'use_gemini' not in st.session_state:
        st.session_state.use_gemini = True  # Default to Gemini
    if 'gemini_api_key' not in st.session_state:
        st.session_state.gemini_api_key = os.getenv('GEMINI_API_KEY', '')
    
    with st.sidebar:
        st.markdown("")  # Spacing
        
        # Model toggle at the top
        st.markdown("### 🤖 AI Model")
        
        use_gemini_toggle = st.toggle(
            "Use Gemini 2.0 Flash",
            value=st.session_state.use_gemini,
            help="Toggle between Local Llama 3.1 and Cloud Gemini 2.0"
        )
        
        # Handle toggle change
        if use_gemini_toggle != st.session_state.use_gemini:
            st.session_state.use_gemini = use_gemini_toggle
            st.cache_resource.clear()
            st.rerun()
        
        # Show current model status
        if st.session_state.use_gemini:
            st.success("✅ Gemini 2.0 Flash (Cloud)")
        else:
            st.info("🏠 Llama 3.1 (Local)")
        
        st.markdown("---")
