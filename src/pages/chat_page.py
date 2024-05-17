from biz.chain.qa_chain import search_similarities as qa_search_similarities 
from biz.chain.create_retrieval_chain import search_similarities as create_retrieval_chain_search_similarities
from biz.util.chain_type import chain_type  # Import store type enumeration for storing embeddings
from biz.vector_store_util.util import vector_store_dir_exists

from widget.st_sidebar import sidebar

import streamlit as st
import os

# Initialize the chat history if it doesn't exist
if 'question_answer' not in st.session_state:
    st.session_state['question_answer'] = [{"role": "system", "content": "You are a helpful assistant, please get me related information to the query I have posted."}]


# Display the chat history
def display_qna():    
    """
    Display the chat history.
    """ 
    for qna in st.session_state.question_answer:
        if (qna["role"] == "user" or qna["role"] == "assistant"):
            with st.chat_message(qna["role"]):
                st.markdown(qna["content"])

# Allow users to input questions and get answers
def question_answer():    
    """
    Allow users to input questions and get answers.
    """
    display_qna()
    
    if prompt :=  st.chat_input("Enter text here"):
        try:
            st.chat_message("user").markdown(prompt)
            st.session_state.question_answer.append({"role": "user", "content": prompt})
            # Get chain name from enviroment
            selected_chain = int(os.environ["chain_type"]) 
            if (selected_chain == chain_type.qa_chain.value):
                print('>>> QA chain.')
                # find similarities (qa_chain)
                response = qa_search_similarities(prompt)
                st.chat_message("assistant").markdown(response)
                st.session_state.question_answer.append({"role": "assistant", "content": response})
            elif (selected_chain == chain_type.create_retrieval_chain.value):
                print('>>> create_retrieval_chain.')
                # find similarities (conversational retrieval chain)
                response = create_retrieval_chain_search_similarities(prompt)
                st.chat_message("assistant").markdown(response)
                st.session_state.question_answer.append({"role": "assistant", "content": response})
            else:
                st.write(">>> No Chain type is found in environment.")
        except Exception as e:
            # Handle exception if sitemap loading fails
            st.write(f"Error occurred while question prompt: {str(e)}")
            return False  
        
def main():
    """
    Main function to setup UI and start the chatbot application.
    """
    sidebar()
    
    if vector_store_dir_exists():
        st.markdown("**Welcome to our internal chatbot app, tailored for Software AG employees! Find answers to your questions here.**")
        question_answer()
    else:
        st.write("No vector store found.")   

if __name__ ==  '__main__':
    main()