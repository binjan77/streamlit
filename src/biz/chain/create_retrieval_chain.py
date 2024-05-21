# Import necessary modules for the chat model, document chain creation, message handling, and prompts
from langchain_openai.chat_models import ChatOpenAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate

# Import utility function for getting the vector database
from biz.vector_store_util.chroma import get_chroma_vector_db
from biz.prompt.prompt import DOCUMENT_CHAIN_PROMT, HISTORY_AWARE_RETRIEVER_CHAIN_PROMPT

# Import operating system functionality and Streamlit for web applications
import os
import streamlit as st

# Initialize chat history as an empty list
chat_history = []

__chroma_vector_store_directory = os.environ.get('chroma_vector_store_directory')
__embedding_model = os.environ["OPENAI_API_EMBEGGING_MODEL"]

# Define a special method to allow getting an element by index
def __getitem__(self, key):
    return self._vet[key]

# Define a function to search for similarities based on the user's query
def search_similarities(prompt):
    """
    Search for similarities based on the user's query and generate a response.
    """
    try:       
        
        # Initialize the language model with the OpenAI API key and model name from environment variables
        llm = ChatOpenAI(
                api_key=os.environ["OPENAI_API_KEY"]
                , model_name=os.environ["OPENAI_API_GPT_MODEL"]
                , temperature=0.2
            )
        
        # Define the prompt template for the document chain
        # document_chain_prompt = ChatPromptTemplate.from_messages(DOCUMENT_CHAIN_PROMT)
                
        # Create the document chain using the language model and the prompt template
        document_chain = create_stuff_documents_chain(
            llm
            , DOCUMENT_CHAIN_PROMT
        )    
        
        # Fetch the vector database
        vector_db = get_chroma_vector_db()
        # docs = vector_db.similarity_search(query=prompt, k=int(os.environ["related_doc_count"]))
        # print(len(docs))
        
        # Configure the retriever to search for similar documents with a similarity score threshold
        vector_db_retriever = vector_db.as_retriever(
            search_type="similarity"
            , search_kwargs={ "k": int(os.environ["related_doc_count"]) }
        )
        # vector_db_retriever = vector_db.as_retriever(
        #     search_type="similarity_score_threshold"
        #     , search_kwargs={
        #             "score_threshold": 0.2
        #             , "k": int(os.environ["related_doc_count"])
        #         }
        # )
        
        # Define the prompt template for generating a search query based on the chat history
        history_aware_retriever_chain_prompt = ChatPromptTemplate.from_messages(HISTORY_AWARE_RETRIEVER_CHAIN_PROMPT)
                
        # Create a history-aware retriever chain using the language model, retriever, and the prompt template
        history_aware_retriever_chain = create_history_aware_retriever(
            llm
            , vector_db_retriever
            , history_aware_retriever_chain_prompt
        )
            
        # Create a retrieval chain combining the history-aware retriever chain and the document chain
        retrieval_chain = create_retrieval_chain(history_aware_retriever_chain, document_chain)
        
        # Invoke the retrieval chain with the chat history and user input
        response = retrieval_chain.invoke({
            "chat_history": chat_history,
            "input": prompt, # require for HISTORY_AWARE_RETRIEVER_CHAIN_PROMPT
            "question": prompt # require for DOCUMENT_CHAIN_PROMT
        })
        
        # Update the chat history with the new human messages
        chat_history.append(HumanMessage(content=prompt))
        
        # Update the chat history with the new AI messages
        chat_history.append(AIMessage(content=response["answer"]))
        
        return response["answer"]
    except Exception as e:
        # Handle exceptions and display an error message in the Streamlit app
        st.write(f"Error occurred while finding query similarities: {str(e)}")
        return False