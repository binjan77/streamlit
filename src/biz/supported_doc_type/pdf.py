# Import necessary modules and packages
from langchain.text_splitter import RecursiveCharacterTextSplitter  # Import text splitter module for text extraction
from langchain_community.document_loaders import PDFMinerLoader  # Import PDF loader module for PDF processing

# Import local class file
from biz.vector_store_util.faiss import save_faiss_vector_db  # Import function to save embeddings to FAISS vector database
from biz.vector_store_util.chroma import save_chroma_vector_db  # Import function to save embeddings to Chroma vector database
from biz.vector_store_util.util import store_exists  # Import function to check whether the vector store exists
from biz.util.upload_file import upload_file  # Import function to upload files
from biz.util.store_type import store_type  # Import store type enumeration for storing embeddings

import streamlit as st  # Import Streamlit for creating interactive web apps
import os as os  # Import os module for file and directory operations

# Define a class for handling PDF documents
class pdf_doc:
    # Constructor to initialize instance attributes
    def __init__(self, name: str):
        self.name = name  # Initialize PDF document name
        # Set upload directory path
        self.__directory = os.environ["upload_file_directory"]

    # Method to generate embeddings and store them from PDFs
    def generate_store_from_pdfs(self, pdfs):
        # Retrieve selected store type from environment variables
        selected_store_type = int(os.environ["vector_store"])

        # Check if PDFs are provided
        if pdfs is not None:
            # Check if the upload directory exists, if not, create it
            if not os.path.exists(self.__directory):
                os.mkdir(self.__directory)
            
            # Loop through each PDF file
            for pdf in pdfs:
                # Generate store name based on PDF name and selected store type
                store_name = self.get_store_name(pdf.name, selected_store_type)
                
                # Check if the store already exists
                if not store_exists(store_name, selected_store_type):
                    # Upload the PDF file to the specified directory
                    if upload_file(self.__directory, pdf):
                        # Generate text from the uploaded PDF file
                        pdf_doc = self.read_and_textify_pdf(pdf)
                        # Check if provided PDF is converted into doc
                        if pdf_doc:
                            # Perform actions based on the selected store type
                            match selected_store_type:
                                case store_type.FAISS.value:
                                    # Save embeddings to the FAISS vector database
                                    save_faiss_vector_db(store_name, pdf_doc)
                                    return True                               
                                case store_type.CHROMA.value:
                                    # Save embeddings to the Chroma vector database
                                    save_chroma_vector_db(store_name, pdf_doc)
                                    return True 
                        else:
                            # Return False if text extraction fails
                            st.write("Text extraction failed for PDF:", pdf.name)
                            return False
                        # Return True if the process completes successfully
                        return True
                    else:
                        # Return False if file upload fails
                        st.write("File upload failed for PDF:", pdf.name)
                        return False 
                else:
                    # Return False if the PDF's FAISS index already exists
                    st.write(f"PDF: {pdf.name}, FAISS index already exists.")
                    return False
        else:
            # Return False if no PDFs are provided
            return False

    # Method to generate store name based on PDF name and selected store type
    def get_store_name(self, pdf_name: str, selected_store_type: int):
        # Get the length of the PDF name
        len_url = len(pdf_name)
        # Check if the PDF name has an extension
        dot_char = pdf_name.rfind(".")
        if dot_char > 0:
            # Remove the extension
            pdf_name = f"{pdf_name[:-(len_url-dot_char)]}"
            # Recalculate the length of the string
            len_url = len(pdf_name)       
            
        # Generate store name based on the selected store type
        match selected_store_type:
            case store_type.FAISS.value:
                return f"{pdf_name[-(len_url):].replace('/', '.')}"
            case store_type.CHROMA.value:
                return f"{pdf_name[-(len_url):].replace('/', '.')[:63]}"

    # Method to read and extract text from PDF
    def read_and_textify_pdf(self, pdf):
        try:
            # Concatenate PDF path
            pdf_path = os.path.join(self.__directory, pdf.name)
            # Read the file and extract text
            file_reader = PDFMinerLoader(pdf_path)
            file_text = file_reader.load()
            return file_text
        except FileNotFoundError as e:
            # Handle file not found error
            st.write("PDF file not found:", pdf.name)
            return False
        except Exception as e:
            # Handle other exceptions
            print(f">>> pdf.py > read_and_textify_pdf: An unexpected error occurred: {e}")
            st.write("An unexpected error occurred while processing PDF:", pdf.name)
            return False