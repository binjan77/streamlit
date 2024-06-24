from langchain import hub
from langchain_core.prompts import MessagesPlaceholder
from langchain.prompts.prompt import PromptTemplate

# Import necessary modules from langchain package

# Define the prompt for document chaining
# Prompt structure for document chaining, containing system and user input messages
DOCUMENT_CHAIN_PROMT=[
    ("system", "You are an assistant for question-answering tasks. \
        Use the following pieces of retrieved context to answer the question. \
        If you don't know the answer as per the provided context, just say that you don't know. \
            :\n\n{context}"),
    ("user", "{input}"),
] 

# Define the prompt for history-aware retriever chaining
# Prompt structure for history-aware retriever chaining, including chat history message placeholder and user inputs
HISTORY_AWARE_RETRIEVER_CHAIN_PROMPT=[
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    ("user", "Given the above conversation, generate a search query to look up to get information relevant to the conversation")
]


# Define the prompt for document chaining
# Prompt structure for document chaining, containing system and user input messages        
ConversationalRetrievalChain_PROMPT = PromptTemplate(
    input_variables=["context", "input"], 
    template="[ \
        ('system', 'You are an assistant for question-answering tasks. \
        Use the following pieces of retrieved context to answer the question. \
        If you don''t know the answer as per the provided context, just say that you don''t know. \
        :\n\n{context}''), \
        ('user', '{question}'), \
    ]"
)