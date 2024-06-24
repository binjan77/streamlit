# from util_langchain.create_retrieval_chain import search_similarities as create_retrieval_chain_search_similarities
from util_langchain.conversational_retrieval_chain import search_similarities as conversational_retrieval_chain_search_similarities
from biz.util.util import vector_store_dir_exists
from biz.util_vector_store.chroma import get_chroma_db_as_retriever

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
    
    if question :=  st.chat_input("Enter text here"):
        try:
            st.chat_message("user").markdown(question)
            st.session_state.question_answer.append({"role": "user", "content": question})
            
            # set value based on environment variable
            generate_eval =  True if os.environ.get("generate_eval")=="True" else False
            rerank_doc =  True if os.environ.get("rerank_doc")=="True" else False
            
            # # find similarities (create_retrieval_chain)
            # response = create_retrieval_chain_search_similarities(
            #     prompt, 
            #     get_chroma_db_as_retriever(rerank_doc)
            # ) 
            
            # find similarities (conversational retrieval chain)
            response = conversational_retrieval_chain_search_similarities(
                question=question, 
                vector_db_retriever=get_chroma_db_as_retriever(rerank_doc),
                generate_eval=generate_eval
            )           
             
            st.chat_message("assistant").markdown(response)
            st.session_state.question_answer.append({"role": "assistant", "content": response})           
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
        # vector store retriever
        question_answer()
    else:
        st.write("No vector store found.")   

if __name__ ==  '__main__':
    main()