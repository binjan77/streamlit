from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

template = """

The following is a friendly conversation between a human and an AI. 
The AI is talkative and provides lots of specific details from its context. 
If the AI does not know the answer to a question, it truthfully says it does
not know.

Current conversation:
Human: {input}
AI Assistant:"""

system_message_prompt = SystemMessagePromptTemplate.from_template(template)

example_human_history = HumanMessagePromptTemplate.from_template("Hi")
example_ai_history = AIMessagePromptTemplate.from_template("hello, how are you today?")

human_template="{input}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, example_human_history, example_ai_history, human_message_prompt])

chat = ChatOpenAI(model_name="gpt-4o", temperature=0.5)

chain = LLMChain(llm=chat, prompt=chat_prompt)

print(chain.run("What is the future of generative AI ? Explain in two sentences ?"))