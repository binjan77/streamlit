from langgraph.graph import END, StateGraph
from langgraph.checkpoint.sqlite import SqliteSaver

from util_langgraph.graph_state import GraphState
from util_langgraph.nodes import retrieve, grade_documents, decide_to_generate, transform_query, generate, grade_generation_v_documents_and_question

workflow = StateGraph(GraphState)

# Define the nodes
workflow.add_node("retrieve", retrieve)  # retrieve
workflow.add_node("grade_documents", grade_documents)  # grade documents
workflow.add_node("generate", generate)  # generatae
workflow.add_node("transform_query", transform_query)  # transform_query

# Build graph
workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "grade_documents")
workflow.add_conditional_edges(
    "grade_documents",
    decide_to_generate,
    {
        "transform_query": "transform_query",
        "generate": "generate",
    },
)
workflow.add_edge("transform_query", "retrieve")
workflow.add_conditional_edges(
    "generate",
    grade_generation_v_documents_and_question,
    {
        "not supported": "generate",
        "useful": END,
        "not useful": "transform_query",
    },
)

# memory = SqliteSaver.from_conn_string(":memory:")
memory = SqliteSaver.from_conn_string(".\chat_history\chat.sqlite")

# Compile
graph_app = workflow.compile(checkpointer=memory)
