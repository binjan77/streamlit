# from biz.chain.create_retrieval_chain import search_similarities as create_retrieval_chain_search_similarities
from biz.chain.conversational_retrieval_chain import search_similarities as conversational_retrieval_chain_search_similarities
from biz.vector_store_util.util import vector_store_dir_exists
from biz.vector_store_util.chroma import get_chroma_db_as_retriever

from widget.st_sidebar import sidebar

import streamlit as st
import os

# Initialize the chat history if it doesn't exist
if 'question_answer' not in st.session_state:
    st.session_state['question_answer'] = [{"role": "system", "content": "You are a helpful assistant, please get me related information to the query I have posted."}]


# Display the chat history
def display_qna():    
    """
    Display the chat history.
    """ 
    for qna in st.session_state.question_answer:
        if (qna["role"] == "user" or qna["role"] == "assistant"):
            with st.chat_message(qna["role"]):
                st.markdown(qna["content"])

# Allow users to input questions and get answers
def question_answer():    
    """
    Allow users to input questions and get answers.
    """
    display_qna()
    
    # set value based on environment variable
    generate_eval =  True if os.environ.get("generate_eval")=="True" else False
    rerank_doc =  True if os.environ.get("rerank_doc")=="True" else False
    
    questions = ["What is a sensor app?",
                "What permission level for CEP management permission type do I need to use Analytics Builder?",
                "Is createBulk operation available for managedObjects endpoint in SmartREST?",
                "Explain the status ""Waiting for connection"" in the device registration process in Cumulocity IoT and describe what action should be taken when a device is in this status?",
                "What are managed objects in Cumulocity IoT?",
                "How many types of Cumulocity IoT events are there?",
                "What do Measurements consist of?",
                "What programming language should I use when developing a Cumulocity IoT microservice?",
                "How should I extend the device registration flow?",
                "Using the Apama Event Processing Language can you write me a statement that listens for new temperature sensor readings greater than a particular temperature?",
                "I do not have a physical device. Can I still use Cumulocity IoT Sensor App with Bluetooth?",
                "What should I do if I receive a “Device type error” a message when using LoRa device?",
                "On which port should the Cumulocity IoT devices connected?",
                "What does the c8y_Firmware fragment do?",
                "What does thec8y_Position fragment do?",
                "Can you please give me a payload example for creating multiple events in the Cumulocity IoT MQTT implementation?",
                "Does the Cloud Remote Access support Telnet protocol?",
                "Why can't I change the interval between measurements sent to Cumulocity IoT in the sensor properties?",
                "From where can I access the Cumulocity IoT application for my tenant?",
                "What kind of access to the Cumulocity IoT application does the Devicemanagement User have?",
                "Why can't I edit a device that I didn't create?",
                "What are Inventory roles?",
                "Which endpoint can I use to monitor the health of active offloading configurations in Cumulocity IoT DataHub microservices?",
                "Is magnetometer a supported smartphone sensor in the sensor app?"
            ]
    
    for question in questions:
        try:
            st.chat_message("user").markdown(question)
            st.session_state.question_answer.append({"role": "user", "content": question}) 
        
            # find similarities (conversational retrieval chain)
            response = conversational_retrieval_chain_search_similarities(
                question=question, 
                vector_db_retriever=get_chroma_db_as_retriever(rerank_doc),
                generate_eval=generate_eval
            )           
                
            st.chat_message("assistant").markdown(response)
            st.session_state.question_answer.append({"role": "assistant", "content": response})    
        except Exception as e:
            # Handle exception if sitemap loading fails
            st.write(f"Error occurred while question prompt: {str(e)}")
            return False 
    
    # if prompt :=  st.chat_input("Enter text here"):
    #     try:
    #         st.chat_message("user").markdown(prompt)
    #         st.session_state.question_answer.append({"role": "user", "content": prompt})
            
    #         # # find similarities (create_retrieval_chain)
    #         # response = create_retrieval_chain_search_similarities(
    #         #     prompt, 
    #         #     get_chroma_db_as_retriever(rerank_doc)
    #         # ) 
            
    #         # find similarities (conversational retrieval chain)
    #         generate_eval =  True if os.environ.get("generate_eval")=="True" else False
    #         response = conversational_retrieval_chain_search_similarities(
    #             prompt=prompt, 
    #             vector_db_retriever=get_chroma_db_as_retriever(rerank_doc),
    #             generate_eval=generate_eval
    #         )           
             
    #         st.chat_message("assistant").markdown(response)
    #         st.session_state.question_answer.append({"role": "assistant", "content": response})           
    #     except Exception as e:
    #         # Handle exception if sitemap loading fails
    #         st.write(f"Error occurred while question prompt: {str(e)}")
    #         return False  
        
def main():
    """
    Main function to setup UI and start the chatbot application.
    """
    sidebar()
    
    if vector_store_dir_exists():
        st.markdown("**Welcome to our internal chatbot app, tailored for Software AG employees! Find answers to your questions here.**")
        # vector store retriever
        question_answer()
    else:
        st.write("No vector store found.")   

if __name__ ==  '__main__':
    main()