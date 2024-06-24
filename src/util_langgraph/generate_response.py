### Generate
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

import os

# Prompt
prompt = hub.pull("rlm/rag-prompt")

__openai_api_gpt_model = os.environ.get('OPENAI_API_GPT_MODEL')

# LLM
llm = ChatOpenAI(model_name=__openai_api_gpt_model, temperature=0)


# Post-processing
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


# Chain
rag_chain = prompt | llm | StrOutputParser()