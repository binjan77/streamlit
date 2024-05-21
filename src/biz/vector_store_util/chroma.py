from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

import os  # For interacting with the file system
import streamlit as st  # For displaying messages in Streamlit

# Directory for storing Chroma vector data
__chroma_vector_store_directory = os.environ.get('chroma_vector_store_directory')
__embedding_model = os.environ["OPENAI_API_EMBEGGING_MODEL"]

def save_chroma_vector_db(store_name: str, docs) -> bool:
    """
    Save documents into a Chroma vector database.

    Args:
    - store_name (str): Name of the store/database.
    - docs (list): List of documents to store.

    Returns:
    - None
    """
    result = False
    try:
        if docs:
            # Construct the path for storing the vector database
            store_path = os.path.join(__chroma_vector_store_directory, store_name)
            
            # Check if the vector store already exists
            if not os.path.exists(store_path):
                # Initialize OpenAIEmbeddings
                embedding = OpenAIEmbeddings(model=__embedding_model)
                
                # Store documents into the Chroma vector database
                vector_db = Chroma.from_documents(
                    docs,
                    embedding,
                    collection_name=store_name,
                    persist_directory=store_path
                )      
                print(f'>>>>> Vector DB Collection count: {vector_db._collection.count()}')          
                result = True
    except FileNotFoundError:
        # Handle the case where the directory doesn't exist
        print(f">>> vector.py > save_chroma_vector_db: Directory '{__chroma_vector_store_directory}' not found.")
    except Exception as e:
        # Handle other unexpected exceptions
        print(f">>> vector.py > save_chroma_vector_db: An unexpected error occurred: {e}")
        
    return result 

def get_chroma_vector_db():
    """
    Load the Chroma vector database.

    Returns:
    - Chroma vector database if successful, False otherwise.
    """
    try:
        # Check if the vector directory exists
        if os.path.exists(__chroma_vector_store_directory):
            # Get a list of files in the vector directory
            dir_files = os.listdir(__chroma_vector_store_directory)
            
            # Note: Currently supported only for 1 data store
            # if more files found then only it takes the 1st item from the list
            # create context from the given collection
            if dir_files and len(dir_files) >= 1:  
                print(">>> Move vector store files found.")
                # Load the Chroma vector database
                # instantiate embedding object
                openai_embeddings = OpenAIEmbeddings(model=__embedding_model)
                vector_db = Chroma(
                    embedding_function=openai_embeddings
                    , persist_directory=os.path.join(__chroma_vector_store_directory, dir_files[0])
                    , collection_name=dir_files[0]
                )
                return vector_db
            else:
                print(">>> No files found.")
        else:
            st.write("Vector store path does not exist.")
    except FileNotFoundError:
        # Handle the case where the directory doesn't exist
        print(f">>> vector.py > get_chroma_vector_db: Directory '{__chroma_vector_store_directory}' not found.")
    except Exception as e:
        # Handle other unexpected exceptions
        print(f">>> vector.py > get_chroma_vector_db: An unexpected error occurred: {e}")
        return False