import streamlit as st

from model.faiss.pdf import pdf_embeddings
from model.faiss.sitemap import sitemap_embeddings  
from model.faiss.html import html_embeddings       

from widget.st_sidebar import sidebar
   
def generate_embeddings():
    # get file_uploader widget
    pdfs = st.session_state.file_upload_widget
    # if file is selected
    if pdfs is not None:
        # # generate embedding for PDFs
        obj_pdf_embeddings = pdf_embeddings('pdf')
        success = obj_pdf_embeddings.generate_pdf_embeddings(pdfs)
        # embeddings are generated
        if success:
            st.write('FAISS index is generated for PDFs.')
        
    # get text_input widget
    input_sitemap = st.session_state.sitemap_widget
    # if sitemap url is entered
    if input_sitemap !=  "":
        # generate embedding for sitemap
        obj_sitemap_embeddings = sitemap_embeddings('sitemap')
        success = obj_sitemap_embeddings.generate_sitemap_embeddings(input_sitemap)
        # embeddings are generated
        if success:
            st.write('FAISS index is generated for Sitemap.')
       
    # input_url = st.session_state.url_widget
    # # if url is entered 
    # if input_url !=  "":    
    #     # generate embedding for HTML (NOT DONE)
    #     obj_html_embeddings = html_embeddings('html')
    #     obj_html_embeddings.generate_html_embeddings(input_url)

def main():
    sidebar()
    st.markdown("**Upload a PDF or a website URL to generate embeddings for the content. These embeddings will be used for retrieving relevant information when chatting with the chatbot.**")
    
    with st.form("sag-rag-form", clear_on_submit = True, border = False):
        # upload a PDF file
        st.file_uploader("Upload your PDF", type = 'pdf', key = 'file_upload_widget', accept_multiple_files = True)
        # sitemap
        st.text_input("Enter Sitemap Url", key = 'sitemap_widget')
        # # HTML Url
        # st.text_input("Enter Url", key = 'url_widget')
        # submit button
        st.form_submit_button("Generate Embeddings", on_click = generate_embeddings)
       
if __name__ ==  '__main__':
    main()