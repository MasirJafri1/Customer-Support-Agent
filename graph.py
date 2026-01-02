from langgraph.graph import StateGraph, END
from state import ComplaintState
from agents.categorizer import categorize
from agents.sentiment import analyze_sentiment
from agents.priority import assign_priority

def category_node(state: ComplaintState):
    result = categorize(state["complaint_text"])
    state["category"] = result.category
    return state

def sentiment_node(state: ComplaintState):
    result = analyze_sentiment(state["complaint_text"])
    state["sentiment"] = result.sentiment
    return state

def priority_node(state: ComplaintState):
    result = assign_priority(
        state["complaint_text"],
        state["category"],
        state["sentiment"]
    )
    state["priority"] = result.priority
    state["priority_reason"] = result.reason
    return state

def build_graph():
    graph = StateGraph(ComplaintState)

    graph.add_node("categorize", category_node)
    graph.add_node("sentiment", sentiment_node)
    graph.add_node("priority", priority_node)

    graph.set_entry_point("categorize")
    graph.add_edge("categorize", "sentiment")
    graph.add_edge("sentiment", "priority")
    graph.add_edge("priority", END)

    return graph.compile()
