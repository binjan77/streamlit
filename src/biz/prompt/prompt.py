from langchain import hub
from langchain_core.prompts import MessagesPlaceholder

# https://smith.langchain.com/hub/rlm/rag-prompt
DOCUMENT_CHAIN_PROMT=hub.pull("rlm/rag-prompt")

# DOCUMENT_CHAIN_PROMT=[
#     ("system", "Answer the user's questions based on the below context:\n\n{context}"),
#     MessagesPlaceholder(variable_name="chat_history"),
#     ("user", "{question}"),
# ] 

HISTORY_AWARE_RETRIEVER_CHAIN_PROMPT=[
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    ("user", "Given the above conversation, generate a search query to look up to get information relevant to the conversation")
]