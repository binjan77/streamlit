from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_openai.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain_community.callbacks import get_openai_callback

import streamlit as st
import os as os
import json 

__vector_directory = r"./vector_store/"

###################################################################
load_dotenv() # read local .env file
###################################################################

if 'question_answer' not in st.session_state:
    st.session_state['question_answer'] = [ {"role": "system", "content": "You are a helpful assistant, please get me related information to the query I have posted."}]

# load all vector database
def load_vector_database():
    dir_files = os.listdir(__vector_directory) 
    # store name found 
    if len(dir_files) > 0:        
        count = 0
        for dir_file in dir_files:
            # file __name__
            store_file_path = os.path.join(__vector_directory, dir_file)
            # embeddings
            if os.path.exists(store_file_path):
                # first file
                if count ==  0:
                    vector_db = FAISS.load_local(store_file_path, OpenAIEmbeddings(model = os.environ['OPENAI_API_MODEL']))
                # 2nd, 3rd, 4th, so on...
                elif count > 0:
                    # load vector db
                    load_vector_db = FAISS.load_local(store_file_path, OpenAIEmbeddings(model = os.environ['OPENAI_API_MODEL']))
                    # merge 2 dbs
                    vector_db.merge_from(load_vector_db)
                else:
                    print("failed to load FAISS database.")
                    
                # increment counter
                count +=  1
            else:
                print(f"Store '{store_file_path}' not found.")
    else:
        print("No Store found.")
        
    return vector_db
     
###################################################################
__vector_db = load_vector_database()
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
        
# Sidebar contents
with st.sidebar:
    st.sidebar.page_link("app.py", label = "App")
    st.sidebar.page_link("pages/generate_embeddings_page.py", label = "Generate Embeddings")
    st.sidebar.page_link("pages/chat_page.py", label = "Chat")

def main():
    st.header("Chat 💬")
    # show UI for ask questions
    question_answer()   
    
if __name__ ==  '__main__':
    main()