from langchain.memory import ConversationBufferMemory
from langchain_openai.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain_core.messages import HumanMessage, AIMessage

from biz.eval.trulens_eval_util import TrulensEvalUtil
from biz.prompt.prompt import ConversationalRetrievalChain_PROMPT

import os  # for getting API token from env variable OPENAI_API_KEY
import streamlit as st

# Initialize chat history as an empty list
chat_history = []

# Define a function to search for similarities based on the user's query
def search_similarities(prompt, vector_db_retriever, generate_eval):
    try:
        # Retrieve necessary environment variables
        openai_api_key = os.environ.get('OPENAI_API_KEY')
        chain_max_token = os.environ.get('conversational_retrieval_chain_max_token')
        openai_api_gpt_model = os.environ.get('OPENAI_API_GPT_MODEL')
        truLens_app_id = os.environ.get('truLens_app_id')

        # Check if all required environment variables are set
        if not openai_api_key or not chain_max_token or not openai_api_gpt_model or not truLens_app_id:
            st.write("Missing required environment variables.")
            return False

        # Initialize memory for storing chat history
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        
        # Create a conversational retrieval chain with the specified LLM and vector database retriever
        conversational_retrieval_chain = ConversationalRetrievalChain.from_llm(
            ChatOpenAI(
                openai_api_key=openai_api_key, 
                max_tokens=int(chain_max_token), 
                temperature=float(os.environ.get("chain_temerature")), 
                model_name=openai_api_gpt_model
            ), 
            vector_db_retriever, 
            memory=memory,
            combine_docs_chain_kwargs={'prompt': ConversationalRetrievalChain_PROMPT}
        )
        
        # Get the response from the conversational retrieval chain
        conversational_retrieval_chain_response = conversational_retrieval_chain(
            {"question": prompt, "chat_history": chat_history}
        )
        
        if generate_eval:
            # Initialize evaluation utility if generate_eval is True
            trulens_eval_util = TrulensEvalUtil(
                app_id=truLens_app_id,
                rag_chain=conversational_retrieval_chain
            )
            # Perform evaluation of the prompt and chat history
            trulens_eval_util.do_evaluation(prompt, chat_history)
        
        # Update the chat history with the new human message
        chat_history.append(HumanMessage(content=prompt))
        
        # Update the chat history with the new AI message
        chat_history.append(AIMessage(content=conversational_retrieval_chain_response["answer"]))
        
        # Return the AI response
        return conversational_retrieval_chain_response["answer"]
    except Exception as e:
        # Handle exceptions and display an error message in the Streamlit app
        st.write(f"Error occurred while finding query similarities: {str(e)}")
        return False