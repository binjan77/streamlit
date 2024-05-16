from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

# Import local class file
from biz.vector_store_util.util import store_exists  # Check if a store exists at the specified path
from biz.util.store_type import store_type # Enumeration checking for different types of vector stores

import os  # For interacting with the file system
import streamlit as st  # For displaying messages in Streamlit

# Directory for storing Chroma vector data
__chroma_vector_store_directory = os.environ.get('chroma_vector_store_directory')

def save_chroma_vector_db(store_name: str, docs):
    """
    Save documents into a Chroma vector database.

    Args:
    - store_name (str): Name of the store/database.
    - docs (list): List of documents to store.

    Returns:
    - None
    """
    try:
        if docs:
            # Construct the path for storing the vector database
            store_path = os.path.join(__chroma_vector_store_directory, store_name)
            
            # Check if the vector store already exists
            if not store_exists(store_path, store_type.CHROMA.value):
                # Initialize OpenAIEmbeddings
                embeddings = OpenAIEmbeddings()
                
                # Store documents into the Chroma vector database
                Chroma.from_documents(
                    docs,
                    embeddings,
                    collection_name=store_name,
                    persist_directory=store_path
                )
    except FileNotFoundError:
        # Handle the case where the directory doesn't exist
        print(f">>> vector.py > save_chroma_vector_db: Directory '{__chroma_vector_store_directory}' not found.")
    except Exception as e:
        # Handle other unexpected exceptions
        print(f">>> vector.py > save_chroma_vector_db: An unexpected error occurred: {e}")

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
                vector_db = load_chroma_database_as_vector_database(dir_files)
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

def load_chroma_database_as_vector_database(dir_files):
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
        
        # Loop through each file in the directory
        for dir_file in dir_files:
            # Check if the file is a Chroma vector database
            if store_exists(dir_file, store_type.CHROMA.value):
                # Construct the full path to the file
                store_file_path = os.path.join(__chroma_vector_store_directory, dir_file)
                
                # Load the vector database
                if vector_db is None:
                    vector_db = Chroma.from_documents(
                        store_file_path, 
                        OpenAIEmbeddings()
                    )
                else:
                    # Merge the current vector database with the loaded one
                    loaded_vector_db = Chroma.from_documents(
                        store_file_path, 
                        OpenAIEmbeddings()
                    )
                    vector_db.merge_from(loaded_vector_db)
            else:
                print(f">>> Store '{os.path.join(__chroma_vector_store_directory, dir_file)}' not found.")
        
        return vector_db
    except Exception as e:
        # Handle unexpected exceptions
        print(f">>> vector.py > load_chroma_database_as_vector_database: An unexpected error occurred: {e}")
        return None
