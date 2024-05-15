from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PDFMinerLoader
from langchain_community.vectorstores import FAISS
from transformers import AutoModelForCausalLM, AutoTokenizer

import streamlit as st
import os as os

# import local class file
from model.vector import save_faiss_vector_db, save_chroma_vector_db, store_exists
from model.upload_file import upload_file
from enumerate.store_type import store_type

class pdf_doc:   
    # Instance attribute 
    def __init__(self, name: str): 
        self.name = name        
        # set upload directory path
        self.__directory = os.environ["upload_file_directory"]
      
    # function to generate pdf embeddings   
    def generate_store_from_pdfs(self, pdfs):         
        # store selection 
        selected_store_type = int(os.environ["vector_store"])
        
        # if file is selected
        if pdfs is not None:
            # check path exists, if not exists, create directory
            if not os.path.exists(self.__directory):
                os.mkdir(self.__directory)
            
            # loop all PDF files
            for pdf in pdfs:
                # vector store name
                store_name = self.get_store_name(pdf.name, selected_store_type)
                # check store exits
                if not store_exists(store_name, selected_store_type):                        
                    # uploaded files
                    if upload_file(self.__directory, pdf):                        
                        match selected_store_type:
                            case store_type.FAISS.value:       
                                # get chunks from uploaded file
                                chunks = self.read_and_textify_pdf(pdf)
                                save_faiss_vector_db(store_name, chunks)                                
                            case store_type.CHROMA.value:    
                                save_chroma_vector_db(store_name, pdf)
                                
                        # return true as all the process is completed successfully
                        return True
                    else:
                        st.write("File upload failed.")
                        return False 
                else:
                    st.write(f"PDF: {pdf.name}, FAISS index is exists.")
                    return False
        else:
            return False        
    
    # function to generate store name based on given pdf name         
    def get_store_name(self, pdf_name: str, selected_store_type: int):
        # length of the input string
        len_url = len(pdf_name)
        # check if url has extension
        dot_char = pdf_name.rfind(".")
        if dot_char > 0:
            # remove extension
            pdf_name = f"{pdf_name[:-(len_url-dot_char)]}"
            # recalculate length of the string
            len_url = len(pdf_name)       
            
        match selected_store_type:
            case store_type.FAISS.value:
                return  f"{pdf_name[-(len_url):].replace("/", ".")}"              
            case store_type.CHROMA.value:
                return f"{pdf_name[-(len_url):].replace("/", ".")[:63]}"
      
    # function to read and textify pdf   
    def read_and_textify_pdf(self, pdf):
        try:
            # concate pdf path
            pdf_path = os.path.join(self.__directory, pdf.name)
            # read file file and get file text
            file_reader = PDFMinerLoader(pdf_path)
            file_text = file_reader.load()
            return file_text
            
            # text_splitter=RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            #     chunk_size=int(os.environ['chunk_size']),
            #     chunk_overlap=int(os.environ['chunk_overlap'])
            # )
            # chunks = text_splitter.split_text(text=file_text[0].page_content)
            # return chunks
        except Exception as e:
            # Handle other exceptions
            print(f">>> pdf.py > read_and_textify_pdf: An unexpected error occurred: {e}")
            return False
