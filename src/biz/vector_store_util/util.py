from biz.vector_store_util.chroma import get_chroma_vector_db

import os

# Fetch directory paths from environment variables
__chroma_vector_store_directory = os.environ.get('chroma_vector_store_directory')

# Check if a store exists at the specified path
def vector_store_dir_exists():
    """
    Check if a store exists at the specified path.

    Returns:
    - True if store exists, False otherwise.
    """
    return os.path.exists(__chroma_vector_store_directory) and len(os.listdir(__chroma_vector_store_directory)) > 0

# Check if a store exists at the specified path
def vector_store_exists(store_name: str):
    """
    Check if a store exists at the specified path.

    Args:
    - store_name (str): Name of the store.

    Returns:
    - True if store exists, False otherwise.
    """
    return os.path.exists(os.path.join(__chroma_vector_store_directory, store_name))