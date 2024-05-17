from enum import Enum

class chain_type(Enum):
    """
    Enumeration defining different chain for llm.
    """
    qa_chain = 0
    create_retrieval_chain = 1               
