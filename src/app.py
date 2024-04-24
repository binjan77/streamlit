import streamlit as st
      
from widget.st_sidebar import sidebar

def main():
    sidebar()
    st.markdown("**Introducing our internal chatbot app designed specifically for Software AG employees! This smart assistant is your go-to for quick answers, IT support, and company information. Powered by AI, it streamlines communication, boosts productivity, and enhances employee experience within the organization.**")

if __name__ ==  '__main__':
    main()