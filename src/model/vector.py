from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

import os as os

class vector_db:        
    # Instance attribute 
    def __init__(self, name): 
        self.name = name 
        
    # check if FAISS index / database exists
    def store_exists(self, store_name):
        if os.path.exists(os.path.join(os.environ['vector_store_directory'], store_name)):
            return True
        else:
            return False
    
    # save FAISS index
    def save_vector_db(self, store_name, chunks):
        try:
            if (chunks):
                # file __name__
                store_path = os.path.join(os.environ['vector_store_directory'], store_name)
                # embeddings
                if not os.path.exists(store_path):
                    embedding = OpenAIEmbeddings(model = os.environ['OPENAI_API_MODEL'])
                    # create vector db
                    vector_db = FAISS.from_texts(chunks, embedding = embedding)
                    # save vector db
                    vector_db.save_local(store_path)
        except Exception as e:
            # Handle other exceptions
            print(f"An unexpected error occurred: {e}")