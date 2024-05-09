from langchain_community.vectorstores import FAISS
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from pathlib import Path

import chromadb.utils.embedding_functions as embedding_functions

import os as os
import streamlit as st

from enumerate.store_type import store_type

__faiss_vector_store_directory = os.environ['faiss_vector_store_directory']     
__chroma_vector_store_directory = os.environ['chroma_vector_store_directory']              
# OpenAI model
__model = os.environ['OPENAI_API_MODEL']
    
# check if FAISS index / database OR CHROMA database exists
def store_exists(store_name: str, selected_store_type: int):
    match selected_store_type:
        case store_type.FAISS.value:
            return os.path.exists(os.path.join(__faiss_vector_store_directory, store_name))
        case store_type.CHROMA.value:
            return os.path.exists(os.path.join(__chroma_vector_store_directory, store_name))   

# save FAISS index
def save_vector_db(store_name: str, selected_store_type: int, chunks):            
    try:
        if (chunks):
            # embeddings
            if not store_exists(store_name, selected_store_type):
                embedding = OpenAIEmbeddings(model=__model)
                 
                match selected_store_type:
                    case store_type.FAISS.value:
                        # file __name__
                        store_path = os.path.join(__faiss_vector_store_directory, store_name)
                        # create vector db
                        vector_db = FAISS.from_texts(chunks, embedding=embedding)
                        # save vector db
                        vector_db.save_local(store_path)
                    case store_type.CHROMA.value:
                        # file __name__
                        store_path = os.path.join(__chroma_vector_store_directory, store_name)
                        print(store_path)
                        # create the open-source embedding function
                        openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                            api_key=os.environ['OPENAI_API_KEY'] ,
                            model_name=__model
                        )
                        # create vector db
                        vector_db = Chroma(
                            chunks,
                            embedding_function=openai_ef, 
                            persist_directory=store_path
                        )
    
    except Exception as e:
        # Handle other exceptions
        print(f">>> save_vector_db: An unexpected error occurred: {e}")         

# load vector database
def get_vector_db(selected_store_type: int):
    try:
        match selected_store_type:
            case store_type.FAISS.value:
                return get_faiss_vector_db()
            case store_type.CHROMA.value:
                return
    except Exception as e:
        # Handle other exceptions
        print(f">>> get_vector_db: An unexpected error occurred: {e}")
        return False

# load faiss databases
def get_faiss_vector_db():
    try:
        # check if vector directory is present 
        if os.path.exists(__faiss_vector_store_directory):
            # get faiss files
            dir_files = os.listdir(__faiss_vector_store_directory) 
            # faiss indexes are found 
            if len(dir_files) > 0:
                # load vector database
                vector_db = load_faiss_vector_database(dir_files)
                return vector_db
            else:
                print(">>> No files found.")
        else:
            st.write("Vector store path does not exists.")
    except Exception as e:
        # Handle other exceptions
        print(f">>> get_faiss_vector_db: An unexpected error occurred: {e}")
        return False

def load_faiss_vector_database(dir_files):
    # counter to load first database index and later merge in database indexes
    count = 0
    # loop through each file
    for dir_file in dir_files:
        # embeddings
        if store_exists(dir_file, store_type.FAISS.value):
            # file_name
            store_file_path = os.path.join(__faiss_vector_store_directory, dir_file)
            # first file
            if count ==  0:
                vector_db = FAISS.load_local(
                    store_file_path, 
                    OpenAIEmbeddings(model=__model),
                    allow_dangerous_deserialization=True)
            # 2nd, 3rd, 4th, so on...
            elif count > 0:
                # load vector db
                load_vector_db = FAISS.load_local(
                    store_file_path, 
                    OpenAIEmbeddings(model=__model),
                    allow_dangerous_deserialization=True)
                # merge 2 dbs
                vector_db.merge_from(load_vector_db)
            else:
                print(">>> failed to load FAISS database.")
                
            # increment counter
            count +=  1
        else:
            print(f">>> Store '{os.path.join(__faiss_vector_store_directory, dir_file)}' not found.")
    
    return vector_db