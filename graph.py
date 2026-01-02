from langgraph.graph import StateGraph, END
from state import ComplaintState

from agents.categorizer import categorize
from agents.sentiment import analyze_sentiment
from agents.priority import assign_priority
from agents.response import draft_response
from agents.suggestion import suggest_actions


def category_node(state: ComplaintState):
    state["category"] = categorize(state["complaint_text"]).category
    return state


def sentiment_node(state: ComplaintState):
    state["sentiment"] = analyze_sentiment(state["complaint_text"]).sentiment
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


def response_node(state: ComplaintState):
    result = draft_response(
        state["complaint_text"],
        state["category"],
        state["sentiment"],
        state["priority"]
    )
    state["response_email"] = result.body
    return state


def suggestion_node(state: ComplaintState):
    result = suggest_actions(
        state["complaint_text"],
        state["category"],
        state["priority"]
    )
    state["suggestions"] = result.actions
    return state


def build_graph():
    graph = StateGraph(ComplaintState)

    graph.add_node("categorize", category_node)
    graph.add_node("sentiment", sentiment_node)
    graph.add_node("priority", priority_node)
    graph.add_node("response", response_node)
    graph.add_node("suggestion", suggestion_node)

    graph.set_entry_point("categorize")
    graph.add_edge("categorize", "sentiment")
    graph.add_edge("sentiment", "priority")
    graph.add_edge("priority", "response")
    graph.add_edge("response", "suggestion")
    graph.add_edge("suggestion", END)

    return graph.compile()
