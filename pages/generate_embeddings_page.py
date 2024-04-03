import streamlit as st

from model.embeddings.pdf import pdf_embeddings
from model.embeddings.html import html_embeddings
from model.embeddings.sitemap import sitemap_embeddings         
   
def generate_embeddings(pdfs, input_url, input_sitemap):
    # # generate embedding for PDFs
    obj_pdf_embeddings = pdf_embeddings('pdf')
    obj_pdf_embeddings.generate_pdf_embeddings(pdfs)
    # generate embedding for HTML (NOT DONE)
    # obj_html_embeddings = html_embeddings('html')
    # obj_html_embeddings.generate_html_embeddings(input_url)
    # generate embedding for sitemap
    obj_sitemap_embeddings = sitemap_embeddings('sitemap')
    obj_sitemap_embeddings.generate_sitemap_embeddings(input_sitemap)

# Sidebar contents
with st.sidebar:
    st.sidebar.page_link("app.py", label = "App")
    st.sidebar.page_link("pages/generate_embeddings_page.py", label = "Generate Embeddings")
    st.sidebar.page_link("pages/chat_page.py", label = "Chat")

def main():
    st.header("Embeddings </>")
    # upload a PDF file
    pdfs = st.file_uploader("Upload your PDF", type = 'pdf', accept_multiple_files = True)
    
    # input_url = st.text_input("Enter Url")
    input_url = ""
    
    input_sitemap = st.text_input("Enter Sitemap Url")
    
    st.button("Generate Embeddings", on_click = generate_embeddings, args = (pdfs, input_url, input_sitemap))
        
if __name__ ==  '__main__':
    main()