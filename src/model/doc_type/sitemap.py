from langchain_community.document_loaders.sitemap import SitemapLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from bs4 import BeautifulSoup

import streamlit as st
import os as os

# import local class file
from model.vector import save_faiss_vector_db, save_chroma_vector_db, store_exists
from enumerate.store_type import store_type

class sitemap_doc:    
    # Instance attribute 
    def __init__(self, name): 
        self.name = name 
                                
    # function to generate sitemap embeddings
    def generate_store_from_sitemap(self, input_sitemap: str):            
        # store selection 
        selected_store_type = int(os.environ["vector_store"])
        
        if input_sitemap !=  "":
            # vector store name       
            store_name = self.get_store_name(input_sitemap, selected_store_type)  
            # check vector store exits
            if not store_exists(store_name, selected_store_type):              
                sitemap_loader = SitemapLoader(web_path=input_sitemap)
                sitemap_loader.requests_per_second = 50
                # load sitemap
                docs = sitemap_loader.load() 
                
                match selected_store_type:
                    case store_type.FAISS.value:     
                        # get chunks from sitemap url
                        chunks = self.read_and_textify_docs(docs)
                        save_faiss_vector_db(store_name, chunks)
                    case store_type.CHROMA.value:                     
                        save_chroma_vector_db(store_name, docs)
                        
                # return true as all the process is completed successfully
                return True
            else:
                st.write(f"Sitemap: {input_sitemap}, FAISS Index OR Chroma database is exists.")  
                # return true as all the process is completed successfully
                return False      
        else:    
            return False
    
    # function to generate store name based on given sitemap url         
    def get_store_name(self, input_sitemap: str, selected_store_type: int):                        
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
            
        match selected_store_type:
            case store_type.FAISS.value:
                return  f"{input_sitemap[-(len_url-(double_forward_slash_pos_char + 2)):].replace("/", ".")}"              
            case store_type.CHROMA.value:
                return f"{input_sitemap[-(len_url-(double_forward_slash_pos_char + 2)):].replace("/", ".")[:63]}"
    
    # function to read and textify sitemap docs
    def read_and_textify_docs(self, docs):
        try:
            chunks = []
            # define text splitter
            text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
                chunk_size=int(os.environ['chunk_size']),
                chunk_overlap=int(os.environ['chunk_overlap'])
            )
                    
            # loop each document
            for doc in docs:           
                #st.write(doc.page_content) 
                chunks += text_splitter.split_text(text=self.remove_html_tags(doc.page_content))
                
            return chunks
        except Exception as e:
            # Handle other exceptions
            print(f">>> sitemap.py > read_and_textify_docs: An unexpected error occurred: {e}")
            return False

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