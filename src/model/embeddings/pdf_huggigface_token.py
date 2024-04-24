from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PDFMinerLoader
from langchain_community.vectorstores import FAISS
from transformers import AutoModelForCausalLM, AutoTokenizer

import streamlit as st
import os as os

# import local class file
from model.vector import vector_db
from model.upload_file import upload_file

class pdf_huggigface_token_embeddings:   
    __directory = os.environ["upload_file_directory"]
    __embedding_model_name = os.environ["upload_file_directory"]
    
    # Instance attribute 
    def __init__(self, name): 
        self.name = name 
    
    # function to generate pdf embeddings using hugging face        
    def generate_pdf_huggingface_embeddings(self, pdfs):
        # if file is selected
        if pdfs is not None:
            # instance of the class
            upload_file = upload_file("file")
            # loop all PDF files
            for pdf in pdfs:
                # uploaded files
                if upload_file.upload_file(self.__directory, pdf):
                    # vector store name
                    store_name = f"{pdf.name[:-4]}.faiss"
                    # get chunks from uploaded file
                    chunks = self.read_and_textify_pdf(pdf)
                    # generate embeddings
                    faiss_vector_db = vector_db("faiss") 
                    faiss_vector_db.save_vector_db(store_name, chunks)     

    # function to read and textify pdf   
    def read_and_textify_pdf(self, pdf):
        # concate pdf path
        pdf_path = os.path.join(self.__directory, pdf.name)
        # read file file and get file text
        file_reader = PDFMinerLoader(pdf_path)
        file_text = file_reader.load()
        
        text_splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
            AutoTokenizer.from_pretrained(self.__embedding_model_name),
            chunk_size = int(os.environ['chunk_size']),
            chunk_overlap = int(os.environ['chunk_overlap'])
        )
        
        chunks = text_splitter.split_text(text = file_text[0].page_content)
        return chunks
