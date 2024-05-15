from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_openai.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain_community.callbacks import get_openai_callback

import streamlit as st
import os as os
import json 

from model.vector import get_vector_db

from widget.st_sidebar import sidebar
from enumerate.store_type import store_type

if 'question_answer' not in st.session_state:
    st.session_state['question_answer'] = [{"role": "system", "content": "You are a helpful assistant, please get me related information to the query I have posted."}]
            
###################################################################
__vector_db = get_vector_db()
 ##################################################################
   
# search answer for the query 
def search_similarities():
    search = st.session_state.question_answer
    # if query has value and 
    if search and __vector_db:
        query = json.dumps(search, separators=(',', ':'))        
        # st.write(query)        
        # run similarity search        
        docs = __vector_db.similarity_search(query=query, k=3)
        # create llm object
        llm = OpenAI(temperature=0.2)
        # Q&A model
        chain=load_qa_chain(
            llm=llm, 
            chain_type="stuff",
            verbose=True
        )
        # cost of the requests
        with get_openai_callback() as cb:
            response=chain.run(input_documents=docs, question=search[:-1])
            print(cb)
            
        # Display user message in chat message container
        st.chat_message("assistant").markdown(response)
        # Add assistant response to chat history
        st.session_state.question_answer.append({"role": "assistant", "content": response})
   
# function to display question answer from session state
def display_qna():    
    # Display chat messages from history on app rerun
    for qna in st.session_state.question_answer:
        if (qna["role"] == "user" or qna["role"] == "assistant"):
            with st.chat_message(qna["role"]):
                st.markdown(qna["content"])
   
# function to display input field for ask question
def question_answer():    
    # display qna
    display_qna()
    
    # React to user input
    if prompt :=  st.chat_input("Enter text here"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.question_answer.append({"role": "user", "content": prompt})
        # search for similarities
        search_similarities()
        
def main():
    sidebar()
    
    if __vector_db:
        st.markdown("**Welcome to our internal chatbot app, tailored for Software AG employees! Find answers to your questions here.**")
        # show UI for ask questions
        question_answer()
    else:
        st.write("No vector store found.")   
        
if __name__ ==  '__main__':
    main()