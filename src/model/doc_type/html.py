import json
from pathlib import Path
from langchain.text_splitter import Language, RecursiveCharacterTextSplitter
from langchain_community.document_loaders import JSONLoader, UnstructuredURLLoader

import streamlit as st
import os as os
import urllib3

# import local class file
from model.vector import save_vector_db

class html_doc:    
    # Instance attribute 
    def __init__(self, name: str): 
        self.name = name 
       
    # function to generate html embeddings 
    def generate_html(self, input_url: str):
        if input_url !=  "":
            # vector store name
            # store_name = self.get_store_name(input_url)
            # get chunks from uploaded file
            chunks = self.read_and_textify_html_urllib3(input_url)
            st.write(chunks)
            # # generate embeddings
            # save_vector_db(store_name, chunks)     
     
    # function to generate store name based on given html url              
    def get_store_name(self, input_url: str):                        
        # length of the input string
        len_url = len(input_url)
        # find last position of character "/"
        pos_char = input_url.rfind("/")
        
        # check if url has extension
        dot_char = input_url.rfind(".")
        if dot_char > 0:
            # remove extension
            input_url = f"{input_url[:-(len_url-dot_char)]}"
            # recalculate length of the string
            len_url = len(input_url)            
                
        return f"{input_url[-(len_url-(pos_char + 1)):]}"  
    
    # function to read and textify html    
    def read_and_textify_html(self, input_url: str):        
        # load URL
        loader = UnstructuredURLLoader(urls=[input_url])
        data = loader.load()
        st.write(data)
        
        # html text splitter
        html_splitter = RecursiveCharacterTextSplitter.from_language(
            language=Language.HTML, 
            chunk_size=int(os.environ['chunk_size']),
            chunk_overlap=int(os.environ['chunk_overlap'])
        )
        # generate split doc
        html_docs = html_splitter.create_documents(data)
        return html_docs

    def read_and_textify_html_urllib3(self, input_url: str):
        # # solution 1
        # try:
        #     headers = {'User-Agent': 'Mozilla/5.0'}
        #     http = urllib3.PoolManager()
        #     resp = http.request(
        #         method="GET",
        #         url=input_url,
        #         headers=headers)
        #     print(f">>> An unexpected error occurred: {resp.data}")
        #     print(">>> Request was successful")
        # solution 2
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            resp = urllib3.request("GET", input_url, headers=headers)
            print(resp.data)
        except Exception as e:
            # Handle other exceptions
            print(f">>> read_and_textify_html_urllib3: An unexpected error occurred: {e}")
        # except HTTPSConnectionPool as e:
        #     # Handle HTTPConnectionPool exceptions
        #     print(f">>> An HTTPConnectionPool exception occurred: {e}")