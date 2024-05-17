from enum import Enum

class store_type(Enum):
    """
    Enumeration defining different types of vector stores.
    """
    FAISS = 0  # Type of vector store using FAISS indexing
    CHROMA = 1  # Type of vector store using CHROMA database
