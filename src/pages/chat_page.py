from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_openai.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain_community.callbacks import get_openai_callback

from biz.vector_store_util.util import get_vector_db
from biz.util.store_type import store_type  # Import store type enumeration for storing embeddings

from widget.st_sidebar import sidebar

import streamlit as st
import os
import json 

# Initialize the chat history if it doesn't exist
if 'question_answer' not in st.session_state:
    st.session_state['question_answer'] = [{"role": "system", "content": "You are a helpful assistant, please get me related information to the query I have posted."}]

# Fetch the vector database
__vector_db = get_vector_db()

# Search for similarities based on the user's query
def search_similarities():
    """
    Search for similarities based on the user's query and generate a response.
    """
    search = st.session_state.question_answer
    if search and __vector_db:
        query = json.dumps(search, separators=(',', ':'))        
        docs = __vector_db.similarity_search(query=query, k=3)
        llm = OpenAI(
            temperature=0.2, 
            model=os.environ["OPENAI_API_MODEL"]
        )
        chain=load_qa_chain(
            llm=llm, 
            chain_type="stuff",
            verbose=True
        )
        with get_openai_callback() as cb:
            response=chain.run(input_documents=docs, question=search[:-1])
            print(cb)
        st.chat_message("assistant").markdown(response)
        st.session_state.question_answer.append({"role": "assistant", "content": response})

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
        st.chat_message("user").markdown(prompt)
        st.session_state.question_answer.append({"role": "user", "content": prompt})
        search_similarities()

def main():
    """
    Main function to setup UI and start the chatbot application.
    """
    sidebar()
    
    if __vector_db:
        st.markdown("**Welcome to our internal chatbot app, tailored for Software AG employees! Find answers to your questions here.**")
        question_answer()
    else:
        st.write("No vector store found.")   

if __name__ ==  '__main__':
    main()
