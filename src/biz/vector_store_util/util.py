from biz.util.store_type import store_type  # Import store type enumeration for storing embeddings
from biz.vector_store_util.faiss import get_faiss_vector_db
from biz.vector_store_util.chroma import get_chroma_vector_db

import os

# Fetch directory paths from environment variables
__faiss_vector_store_directory = os.environ.get('faiss_vector_store_directory')
__chroma_vector_store_directory = os.environ.get('chroma_vector_store_directory')

# Check if a store exists at the specified path
def vector_store_dir_exists():
    """
    Check if a store exists at the specified path.

    Args:
    - store_name (str): Name of the store.
    - selected_store_type (int): Type of the store (FAISS or CHROMA).

    Returns:
    - True if store exists, False otherwise.
    """
    selected_store_type = int(os.environ["vector_store"])
    if selected_store_type == store_type.FAISS.value:
        return os.path.exists(__faiss_vector_store_directory) and len(os.listdir(__faiss_vector_store_directory)) > 0
    elif selected_store_type == store_type.CHROMA.value:
        return os.path.exists(__chroma_vector_store_directory) and len(os.listdir(__chroma_vector_store_directory)) > 0

# Check if a store exists at the specified path
def vector_store_exists(store_name: str, selected_store_type: int):
    """
    Check if a store exists at the specified path.

    Args:
    - store_name (str): Name of the store.
    - selected_store_type (int): Type of the store (FAISS or CHROMA).

    Returns:
    - True if store exists, False otherwise.
    """
    if selected_store_type == store_type.FAISS.value:
        return os.path.exists(os.path.join(__faiss_vector_store_directory, store_name))
    elif selected_store_type == store_type.CHROMA.value:
        return os.path.exists(os.path.join(__chroma_vector_store_directory, store_name))

# Load vector database based on the selected store type
def get_vector_db():
    """
    Load vector database based on the selected store type.

    Returns:
    - Vector database if successful, False otherwise.
    """
    selected_store_type = int(os.environ["vector_store"])
    try:
        if selected_store_type == store_type.FAISS.value:
            return get_faiss_vector_db()
        elif selected_store_type == store_type.CHROMA.value:
            return get_chroma_vector_db()
        else:
            print(f"Invalid store type: {selected_store_type}")
            return False
    except FileNotFoundError as e:
        # Handle specific exception when the file or directory does not exist
        print(f"Error loading vector database: {e}")
        return False
    except Exception as e:
        # Handle other unexpected exceptions
        print(f"An unexpected error occurred while loading vector database: {e}")
        return False
