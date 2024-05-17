from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

import os  # For interacting with the file system
import streamlit as st  # For displaying messages in Streamlit
import chromadb

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
                embeddings = OpenAIEmbeddings(model=__embedding_model)
                
                # Store documents into the Chroma vector database
                Chroma.from_documents(
                    docs,
                    embeddings,
                    collection_name=store_name,
                    persist_directory=store_path
                )
                
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
            
            if dir_files:
                # Load the Chroma vector database
                vector_db = load_chroma_database(dir_files)
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

def load_chroma_database(dir_files):
    """
    Load Chroma vector database from files.

    Args:
    - dir_files (list): List of files in the vector directory.

    Returns:
    - Chroma vector database if successful, None otherwise.
    """
    try:
        # Initialize an empty vector database
        vector_db = None
        
        # instantiate embedding object
        openai_embeddings = OpenAIEmbeddings(model=__embedding_model)
        client_settings = chromadb.config.Settings(
            is_persistent=True,
            persist_directory=__chroma_vector_store_directory,
            anonymized_telemetry=False
        )
        vector_db = Chroma(
            collection_name="project_store_all",
            persist_directory=__chroma_vector_store_directory,
            client_settings=client_settings,
            embedding_function=openai_embeddings
        )
        return vector_db
    except Exception as e:
        # Handle unexpected exceptions
        print(f">>> vector.py > load_chroma_database_as_faiss_index: An unexpected error occurred: {e}")
        return None
