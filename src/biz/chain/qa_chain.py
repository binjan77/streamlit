# Import necessary modules
from langchain_openai.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain_community.callbacks import get_openai_callback

from biz.vector_store_util.util import get_vector_db
import os 
import streamlit as st
import json 

__qna = []

# Search for similarities based on the user's query
def search_similarities(prompt):
    """
    Search for similarities based on the user's query and generate a response.
    
    Args:
    search (str): The user's query.
    
    Returns:
    str or bool: Response string if successful, False if an error occurs.
    """
    try:
        # Fetch the vector database
        vector_db = get_vector_db()
        
        # Check if search query and vector database are available
        if prompt and vector_db:
            # Convert search query to JSON format
            chat_history = json.dumps(__qna, separators=(',', ':'))   
            
            # Perform similarity search based on the chat history
            docs = vector_db.similarity_search(query=chat_history, k=3)
            
            # Initialize OpenAI language model
            llm = ChatOpenAI(
                api_key=os.environ["OPENAI_API_KEY"]
                # , model=os.environ["OPENAI_API_GPT_MODEL"]  # Accessing environment variables
                , temperature=0.2 
            )
            
            # Load question-answering chain
            chain = load_qa_chain(
                llm=llm, 
                chain_type="stuff",
                verbose=True
            )
            
            # Execute the chain with input documents and query
            with get_openai_callback() as cb:
                response = chain.invoke(input_documents=docs, question=prompt)
                print(cb)  # Printing callback information
                
                # Update the chat history with the new human and AI messages
                __qna.append({"question": prompt, "answer": response})
                
            return response  # Return response if successful
        
    except Exception as e:
        # Handle exception if an error occurs
        st.write(f"Error occurred while finding query similarities: {str(e)}")
        return False  # Return False if an error occurs
