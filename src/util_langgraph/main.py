from dotenv import load_dotenv 
from pprint import pprint
from util_langgraph.graph_app import graph_app
from langchain_core.messages import HumanMessage

import os

###################################################################
load_dotenv()  # Load environment variables from the local .env file
###################################################################

def get_response(inputs):
    # Run
    # inputs = {"question": "What permission level for CEP management permission type do I need to use Analytics Builder?"}
    pid = os.getpid["pid"]
    config = {"configurable": {"thread_id": "{pid}"}}
    
    for output in graph_app.stream(inputs, config):
        for key, value in output.items():
            # Node
            pprint(f"Node '{key}':")
            # Optional: print full state at each node
            # pprint.pprint(value["keys"], indent=2, width=80, depth=None)
        pprint("\n---\n")

    # Final generation
    pprint(value["generation"])
    return value["generation"]