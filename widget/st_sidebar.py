import streamlit as st

def sidebar():
    # Sidebar contents
    with st.sidebar:
        st.set_page_config(
            page_title = "Software AG internal Chat Assistant"
        )
        st.sidebar.page_link("app.py", label = "App")
        st.sidebar.page_link("pages/generate_embeddings_page.py", label = "Generate Embeddings")
        st.sidebar.page_link("pages/chat_page.py", label = "Chat Assistant")