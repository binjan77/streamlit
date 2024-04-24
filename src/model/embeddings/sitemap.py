from dotenv import load_dotenv
from langchain_community.document_loaders.sitemap import SitemapLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from bs4 import BeautifulSoup

import streamlit as st
import os as os

# import local class file
from model.vector import vector_db

class sitemap_embeddings:    
    # Instance attribute 
    def __init__(self, name): 
        self.name = name 
        load_dotenv() # read local .env file
        
    # function to generate sitemap embeddings
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
                # return true as all the process is completed successfully
                return True
            else:
                st.write(f"Sitemap: {input_sitemap}, FAISS index is exists.")  
                # return true as all the process is completed successfully
                return False      
        else:    
            return False
    
    # function to generate store name based on given sitemap url         
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
            
    # function to read and textify sitemap docs
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
            #st.write(doc.page_content) 
            chunks += text_splitter.split_text(text = self.remove_html_tags(doc.page_content))
            
        return chunks

    # function to remove all html tags
    def remove_html_tags(self, text):
        # Remove html tags from a string
        import re
        clean = re.compile('^<.*?>$')
        return re.sub(clean, '', text)
    
    # function to remove all nav and header component from the imported page content
    def remove_nav_and_header_elements(self, content: BeautifulSoup) -> str:
        # Find all 'nav' and 'header' elements in the BeautifulSoup object
        nav_elements = content.find_all("nav")
        header_elements = content.find_all("header")

        # Remove each 'nav' and 'header' element from the BeautifulSoup object
        for element in nav_elements + header_elements:
            element.decompose()

        return str(content.get_text())