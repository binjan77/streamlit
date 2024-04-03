from dotenv import load_dotenv
from langchain_community.document_loaders.sitemap import SitemapLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

import streamlit as st
import os as os

# import local class file
from model.vector import vector_db

class sitemap_embeddings:    
    # Instance attribute 
    def __init__(self, name): 
        self.name = name 
        load_dotenv() # read local .env file
          
    def generate_sitemap_embeddings(self, input_sitemap):
        if input_sitemap !=  "":
            # vector store name       
            store_name = self.get_store_name(input_sitemap)     
            # generate embeddings
            obj_faiss_vector_db = vector_db("faiss") 
            # check vector store exits
            if not obj_faiss_vector_db.store_exists(store_name):              
                sitemap_loader = SitemapLoader(web_path = input_sitemap)
                sitemap_loader.requests_per_second = 50
                
                docs = sitemap_loader.load()      
                # get chunks from sitemap url
                chunks = self.read_and_textify_docs(docs)
                obj_faiss_vector_db.save_vector_db(store_name, chunks)
            else:
                st.write("Sitemap: FAISS index is exists.")
               
    def get_store_name(self, input_sitemap):                        
        # length of the input string
        len_url = len(input_sitemap)
        # find last position of character "//"
        double_forward_slash_pos_char = input_sitemap.find("//")        
        # check if url has extension
        dot_char = input_sitemap.rfind(".")
        if dot_char > 0:
            # remove extension
            input_sitemap = f"{input_sitemap[:-(len_url-dot_char)]}"
            # recalculate length of the string
            len_url = len(input_sitemap)       
            
        return  f"{input_sitemap[-(len_url-(double_forward_slash_pos_char + 2)):].replace("/", ".")}.faiss"              
            
    def read_and_textify_docs(self, docs):
        chunks = []
        # define text splitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = int(os.environ['chunk_size']),
            chunk_overlap = int(os.environ['chunk_overlap']),
            length_function = len
        )
        # loop each document
        for doc in docs:            
            chunks += text_splitter.split_text(text = doc.page_content)
            
        return chunks