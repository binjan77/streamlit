import streamlit as st
import os as os

from model.doc_type.pdf import pdf_doc
from model.doc_type.sitemap import sitemap_doc  
from model.doc_type.html import html_doc

from widget.st_sidebar import sidebar
from enumerate.store_type import store_type

__options = ["FAISS Index", "CHROMA database"]
   
def generate_store():        
    # get file_uploader widget
    pdfs = st.session_state.file_upload_widget
    # if file is selected
    if pdfs is not None:
        # # generate embedding for PDFs
        obj_pdf = pdf_doc('pdf')
        success = obj_pdf.generate_store_from_pdfs(pdfs)
        # embeddings are generated
        if success:
            st.write('Vector store is generated for PDFs.')
        
    # get text_input widget
    input_sitemap = st.session_state.sitemap_widget
    # if sitemap url is entered
    if input_sitemap !=  "":
        # generate embedding for sitemap
        obj_sitemap = sitemap_doc('sitemap')
        success = obj_sitemap.generate_store_from_sitemap(input_sitemap)
        # embeddings are generated
        if success:
            st.write('Vector store is generated for Sitemap.')
    
    # input_url = st.session_state.url_widget
    # # if url is entered 
    # if input_url !=  "":    
    #     # generate embedding for HTML (NOT DONE)
    #     obj_html = html_doc('html')
    #     obj_html.generate_html(input_url)
        
def main():
    sidebar()
    st.markdown("**Upload a PDF or a website URL to generate embeddings for the content. These embeddings will be used for retrieving relevant information when chatting with the chatbot.**")
    
    with st.form("sag-rag-form", clear_on_submit=True, border=False):
        # upload a PDF file
        st.file_uploader("Upload your PDF", type='pdf', key='file_upload_widget', accept_multiple_files=True)
        # sitemap
        st.text_input("Enter Sitemap Url", key='sitemap_widget')
        # # HTML Url
        # st.text_input("Enter Url", key='url_widget')
        # submit button
        st.form_submit_button("Generate Embeddings", on_click=generate_store)
       
if __name__ ==  '__main__':
    main()