import streamlit as st  # Import Streamlit for creating interactive web apps
import os as os  # Import os module for file and directory operations

def upload_file(path: str, file):  
    """
    Function to upload a file.

    Args:
    - path (str): The directory path where the file will be saved.
    - file: The file object to upload.

    Returns:
    - True if file is successfully uploaded, False otherwise.
    """
    try:      
        # Construct file path
        file_path = os.path.join(path, file.name)
        # Check if file already exists
        if not os.path.exists(file_path): 
            # Write file to disk
            with open(file_path, "wb") as f:
                f.write(file.getbuffer())
            return True
        else:
            st.error("File already exists.")
            return False
    except FileNotFoundError:
        st.error("Specified directory does not exist.")
        return False
    except IsADirectoryError:
        st.error("Specified path is a directory, not a file.")
        return False
    except Exception as e:
        # Handle other exceptions
        st.error(f"An unexpected error occurred: {e}")
        return False