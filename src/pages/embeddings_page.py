from biz.supported_doc_type.pdf import pdf_doc
from biz.supported_doc_type.sitemap import sitemap_doc
from biz.util.store_type import store_type  # Import store type enumeration for storing embeddings

from widget.st_sidebar import sidebar

import streamlit as st
import os

def generate_store():        
    """
    Function to generate embeddings for uploaded PDF files or entered sitemap URLs.
    """
    # Get the uploaded PDF files
    pdfs = st.session_state.file_upload_widget
    # If PDF files are uploaded
    if pdfs is not None:
        # Generate embeddings for PDFs
        obj_pdf = pdf_doc('pdf')
        success = obj_pdf.generate_store_from_pdfs(pdfs)
        # Check if embeddings are generated successfully
        if success:
            st.write('Vector store is generated for PDFs.')
        
    # Get the entered sitemap URL
    input_sitemap = st.session_state.sitemap_widget
    # If a sitemap URL is entered
    if input_sitemap !=  "":
        # Generate embeddings for the sitemap
        obj_sitemap = sitemap_doc('sitemap')
        success = obj_sitemap.generate_store_from_sitemap(input_sitemap)
        # Check if embeddings are generated successfully
        if success:
            st.write('Vector store is generated for Sitemap.')
        
def main():
    """
    Main function to set up the Streamlit UI and handle user inputs.
    """
    sidebar()
    st.markdown("**Upload a PDF or a website URL to generate embeddings for the content. These embeddings will be used for retrieving relevant information when chatting with the chatbot.**")
    
    with st.form("sag-rag-form", clear_on_submit=True, border=False):
        # Upload a PDF file
        st.file_uploader("Upload your PDF", type='pdf', key='file_upload_widget', accept_multiple_files=True)
        # Enter a sitemap URL
        st.text_input("Enter Sitemap Url", key='sitemap_widget')
        # Submit button to generate embeddings
        st.form_submit_button("Generate Embeddings", on_click=generate_store)
       
if __name__ ==  '__main__':
    main()
