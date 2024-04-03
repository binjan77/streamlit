import streamlit as st
      
# Sidebar contents
with st.sidebar:
    st.sidebar.page_link("app.py", label = "App")
    st.sidebar.page_link("pages/generate_embeddings_page.py", label = "Generate Embeddings")
    st.sidebar.page_link("pages/chat_page.py", label = "Chat")

def main():
    st.header("App 💬")

if __name__ ==  '__main__':
    main()