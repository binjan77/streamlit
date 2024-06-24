import streamlit as st  # Importing the Streamlit library and aliasing it as 'st'

def sidebar():
    # Function to create the sidebar content

    # Setting the page configuration for the Streamlit app
    with st.sidebar:
        st.set_page_config(
            page_title="Software AG internal Chat Assistant"  # Setting the page title
        )

        # Adding links to different pages in the sidebar
        st.sidebar.page_link("app.py", label="App")  # Link to the 'App' page
        st.sidebar.page_link("pages/embeddings_page.py", label="Generate and Save Embeddings")  # Link to the 'Generate and Save Embeddings' page
        # st.sidebar.page_link("pages/chat_page.py", label="Chat Assistant")  # Link to the 'Chat Assistant' page
        st.sidebar.page_link("pages/chat_page_langgraph.py", label="Chat Assistant")  # Link to the 'Chat Assistant' page
        # st.sidebar.page_link("pages/chat_page_flashRank.py", label="Chat Assistant")  # Link to the 'Chat Assistant' page
        