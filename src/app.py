from dotenv import load_dotenv  # Importing the load_dotenv function from the dotenv module

import streamlit as st  # Importing the Streamlit library

from widget.st_sidebar import sidebar  # Importing the sidebar function from the st_sidebar module in the widget package

###################################################################
load_dotenv()  # Load environment variables from the local .env file
###################################################################

def main():
    sidebar()  # Setting up the Streamlit sidebar
    # Displaying a markdown message introducing the internal chatbot app for Software AG employees
    st.markdown("**Introducing our internal chatbot app designed specifically for Software AG employees! This smart assistant is your go-to for quick answers, IT support, and company information. Powered by AI, it streamlines communication, boosts productivity, and enhances employee experience within the organization.**")

if __name__ == '__main__':
    main()  # Calling the main function if the script is executed as the main program