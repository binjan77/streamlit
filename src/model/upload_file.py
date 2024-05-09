import streamlit as st
import os as os

# function to upload file
def upload_file(path: str, file):  
    try:      
        # file path
        file_path = os.path.join(path, file.name)
        # check file exist (already uploaded)
        if not os.path.exists(file_path): 
            # write file on disk
            with open(file_path,"wb") as f:
                f.write(file.getbuffer())
            return True
        else:
            return False
    except Exception as e:
        # Handle other exceptions
        print(f">>> upload_file: An unexpected error occurred: {e}")
        return False
        