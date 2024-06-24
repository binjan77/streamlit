# Import necessary modules for the chat model, document chain creation, message handling, and prompts
from langchain_openai.chat_models import ChatOpenAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.callbacks import get_openai_callback

# Import utility function for getting the vector database and prompts
from util_langchain.prompt.prompt import DOCUMENT_CHAIN_PROMT, HISTORY_AWARE_RETRIEVER_CHAIN_PROMPT

# Import operating system functionality and Streamlit for web applications
import os
import streamlit as st

# Initialize chat history as an empty list
chat_history = []

# Get the directory for the Chroma vector store and the embedding model from environment variables
__chroma_vector_store_directory = os.environ.get('chroma_vector_store_directory')
__embedding_model = os.environ.get("OPENAI_API_EMBEDDING_MODEL")

# Define a function to search for similarities based on the user's query
def search_similarities(question, vector_db_retriever):
    """
    Search for similarities based on the user's query and generate a response.

    Parameters:
    prompt (str): The user's query or input.
    vector_db_retriever: The retriever for the vector database.

    Returns:
    str: The generated response based on the retrieved similar documents.
    """
    try:
        # Initialize the language model with the OpenAI API key and model name from environment variables
        llm = ChatOpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
            model_name=os.environ.get("OPENAI_API_GPT_MODEL"),
            temperature=os.environ.get("chain_temerature")
        )

        # Create the document chain prompt template from messages
        document_chain_prompt = ChatPromptTemplate.from_messages(DOCUMENT_CHAIN_PROMT)
        
        # Create the document chain using the language model and the prompt template
        document_chain = create_stuff_documents_chain(
            llm,
            document_chain_prompt
        )

        # Define the prompt template for generating a search query based on the chat history
        history_aware_retriever_chain_prompt = ChatPromptTemplate.from_messages(HISTORY_AWARE_RETRIEVER_CHAIN_PROMPT)
      
        # Create a history-aware retriever chain using the language model, retriever, and the prompt template
        history_aware_retriever_chain = create_history_aware_retriever(
            llm,
            vector_db_retriever,
            history_aware_retriever_chain_prompt
        )
            
        # Create a retrieval chain combining the history-aware retriever chain and the document chain
        retrieval_chain = create_retrieval_chain(history_aware_retriever_chain, document_chain)
        
        # Execute the chain with input documents and query
        with get_openai_callback() as cb:
            # Invoke the retrieval chain with the chat history and user input
            response = retrieval_chain.invoke({
                "chat_history": chat_history,
                "input": question,  # Required for HISTORY_AWARE_RETRIEVER_CHAIN_PROMPT
            })
            print(cb)  # Printing callback information
        
        # Update the chat history with the new human message
        chat_history.append(HumanMessage(content=question))
        
        # Update the chat history with the new AI message
        chat_history.append(AIMessage(content=response["answer"]))
        
        # Return the generated response
        return response["answer"]
    except Exception as e:
        # Handle exceptions and display an error message in the Streamlit app
        st.write(f"Error occurred while finding query similarities: {str(e)}")
        return False