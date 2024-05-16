# Import necessary modules and packages
from langchain_community.document_loaders.sitemap import SitemapLoader  # Import sitemap loader module for processing sitemaps
from langchain.text_splitter import RecursiveCharacterTextSplitter  # Import text splitter module for text extraction
from bs4 import BeautifulSoup  # Import BeautifulSoup for HTML parsing

# Import local class file
from biz.vector_store_util.faiss import save_faiss_vector_db  # Import function to save embeddings to FAISS vector database
from biz.vector_store_util.chroma import save_chroma_vector_db  # Import function to save embeddings to Chroma vector database
from biz.vector_store_util.util import store_exists  # Import function to check if store exists
from biz.util.store_type import store_type  # Import store type enumeration for storing embeddings

import streamlit as st  # Import Streamlit for creating interactive web apps
import os as os  # Import os module for file and directory operations

class sitemap_doc:    
    # Instance attribute 
    def __init__(self, name): 
        self.name = name  # Initialize sitemap document name 
                                
    # function to generate sitemap embeddings
    def generate_store_from_sitemap(self, input_sitemap: str):            
        # store selection 
        selected_store_type = int(os.environ.get("vector_store", 0))  # Retrieve selected store type from environment variables
        
        if input_sitemap != "":
            # vector store name       
            store_name = self.get_store_name(input_sitemap, selected_store_type)  # Generate vector store name
            
            try:
                if not store_exists(store_name, selected_store_type):  # Check if store already exists              
                    sitemap_loader = SitemapLoader(web_path=input_sitemap)  # Create sitemap loader object
                    sitemap_loader.requests_per_second = 50  # Set requests per second
                    
                    # Load documents from sitemap
                    docs = sitemap_loader.load()  
                    
                    # Perform actions based on selected store type
                    match selected_store_type:
                        case store_type.FAISS.value:     
                            # Get text chunks from sitemap url
                            chunks = self.read_and_textify_docs(docs)  # Extract text chunks from documents
                            save_faiss_vector_db(store_name, chunks)  # Save embeddings to FAISS vector database
                        case store_type.CHROMA.value:                     
                            save_chroma_vector_db(store_name, docs)  # Save embeddings to Chroma vector database

                    # Inform if store already exists
                    st.write(f"Sitemap: {input_sitemap}, FAISS Index OR Chroma database already exists.")  
                    return False
                else:
                    # Return False if store already exists
                    st.write(f"Sitemap: {input_sitemap}, FAISS Index OR Chroma database already exists.")  
                    return False
            except Exception as e:
                # Handle exception if sitemap loading fails
                st.write(f"Error occurred while processing sitemap: {str(e)}")
                return False      
        else:    
            # Return False if no sitemap provided
            st.write("No sitemap provided.")
            return False
    
    # function to generate store name based on given sitemap url         
    def get_store_name(self, input_sitemap: str, selected_store_type: int):                        
        try:
            # Length of the input string
            len_url = len(input_sitemap)
            # Find last position of character "//"
            double_forward_slash_pos_char = input_sitemap.find("//")        
            # Check if URL has extension
            dot_char = input_sitemap.rfind(".")
            if dot_char > 0:
                # Remove extension
                input_sitemap = f"{input_sitemap[:-(len_url-dot_char)]}"
                # Recalculate length of the string
                len_url = len(input_sitemap)       
                
            # Generate store name based on the selected store type
            match selected_store_type:
                case store_type.FAISS.value:
                    return  f"{input_sitemap[-(len_url-(double_forward_slash_pos_char + 2)):].replace('/', '.')}"              
                case store_type.CHROMA.value:
                    return f"{input_sitemap[-(len_url-(double_forward_slash_pos_char + 2)):].replace('/', '.')[:63]}"
        except Exception as e:
            # Handle exception if generating store name fails
            st.write(f"Error occurred while generating store name: {str(e)}")
            return None
    
    # function to read and textify sitemap docs
    def read_and_textify_docs(self, docs):
        try:
            chunks = []  # Initialize list to store text chunks
            # Define text splitter
            text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
                chunk_size=int(os.environ.get('chunk_size', 1000)),  # Get chunk size from environment variables
                chunk_overlap=int(os.environ.get('chunk_overlap', 100))  # Get chunk overlap from environment variables
            )
                    
            # Loop through each document
            for doc in docs:           
                chunks += text_splitter.split_text(text=self.remove_html_tags(doc.page_content))  # Split text into chunks and add to list
                
            return chunks  # Return text chunks
        except Exception as e:
            # Handle exception if text extraction fails
            st.write(f"Error occurred while extracting text: {str(e)}")
            return []
    
    # function to remove all HTML tags from text
    def remove_html_tags(self, text):
        try:
            # Remove HTML tags from a string
            import re
            clean = re.compile('^<.*?>$')
            return re.sub(clean, '', text)  # Return text with HTML tags removed
        except Exception as e:
            # Handle exception if HTML tag removal fails
            st.write(f"Error occurred while removing HTML tags: {str(e)}")
            return text
    
    # function to remove navigation and header elements from the imported page content
    def remove_nav_and_header_elements(self, content: BeautifulSoup) -> str:
        try:
            # Find all 'nav' and 'header' elements in the BeautifulSoup object
            nav_elements = content.find_all("nav")
            header_elements = content.find_all("header")

            # Remove each 'nav' and 'header' element from the BeautifulSoup object
            for element in nav_elements + header_elements:
                element.decompose()

            return str(content.get_text())  # Return cleaned text
        except Exception as e:
            # Handle exception if removal of navigation and header elements fails
            st.write(f"Error occurred while removing navigation and header elements: {str(e)}")
            return str(content.get_text())