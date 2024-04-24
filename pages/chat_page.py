from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_openai.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain_community.callbacks import get_openai_callback

import streamlit as st
import os as os
import json 

from widget.st_sidebar import sidebar

###################################################################
load_dotenv() # read local .env file
###################################################################

# variable for vector directory
__vector_directory = os.environ['vector_store_directory']
# OpenAI model
__model = os.environ['OPENAI_API_MODEL']

if 'question_answer' not in st.session_state:
    st.session_state['question_answer'] = [ {"role": "system", "content": "You are a helpful assistant, please get me related information to the query I have posted."}]

# load all vector database
def get_vector_database():    
    try:
        # check if vector directory is present 
        if os.path.exists(__vector_directory):
            # get faiss files
            dir_files = os.listdir(__vector_directory) 
            # faiss indexes are found 
            if len(dir_files) > 0:
                # load vector database
                vector_db = load_vector_database(dir_files)
                return vector_db
            else:
                print("No files found.")
        else:
            st.write("Vector store path does not exists.")
    except Exception as e:
        # Handle other exceptions
        print(f"An unexpected error occurred: {e}")
        return False

def load_vector_database(dir_files):
    # counter to load first database index and later merge in database indexes
    count = 0
    # loop through each file
    for dir_file in dir_files:
        # file_name
        store_file_path = os.path.join(__vector_directory, dir_file)
        # embeddings
        if os.path.exists(store_file_path):
            # first file
            if count ==  0:
                vector_db = FAISS.load_local(store_file_path, OpenAIEmbeddings(model = __model))
            # 2nd, 3rd, 4th, so on...
            elif count > 0:
                # load vector db
                load_vector_db = FAISS.load_local(store_file_path, OpenAIEmbeddings(model = __model))
                # merge 2 dbs
                vector_db.merge_from(load_vector_db)
            else:
                print("failed to load FAISS database.")
                
            # increment counter
            count +=  1
        else:
            print(f"Store '{store_file_path}' not found.")
     
    return vector_db
            
###################################################################
__vector_db = get_vector_database()
###################################################################
   
# search answer for the query 
def search_similarities(search):
    # if query has value and 
    if search and __vector_db:
        query = json.dumps(search, separators = (',', ':'))        
        # st.write(query)        
        # run similarity search        
        docs = __vector_db.similarity_search(query = query, k = 3)
        # create llm object
        llm = OpenAI(temperature = 0.2)
        # Q&A model
        chain = load_qa_chain(llm = llm, chain_type = "stuff")
        # cost of the requests
        with get_openai_callback() as cb:
            response = chain.run(input_documents = docs, question = search)
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
        search_similarities(st.session_state.question_answer)
        
def main():
    if __vector_db:
        sidebar()
        st.markdown("**Welcome to our internal chatbot app, tailored for Software AG employees! Find answers to your questions here.**")
        # show UI for ask questions
        question_answer()
    else:
        st.write("No vector store found.")   
        
if __name__ ==  '__main__':
    main()