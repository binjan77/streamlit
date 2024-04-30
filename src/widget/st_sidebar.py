import streamlit as st

def sidebar():
    # Sidebar contents
    with st.sidebar:
        st.set_page_config(
            page_title = "Software AG internal Chat Assistant"
        )
        st.sidebar.page_link("app.py", label = "App")
        st.sidebar.page_link("pages/embeddings_page.py", label = "Generate Embeddings (FAISS)")
        st.sidebar.page_link("pages/chat_page.py", label = "Chat Assistant (FAISS)")
        st.sidebar.page_link("pages/embeddings_chroma_page.py", label = "Generate Embeddings (Chroma)")
        st.sidebar.page_link("pages/chat_chroma_page.py", label = "Chat Assistant (Chroma)")