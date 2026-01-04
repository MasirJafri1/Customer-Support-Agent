from langgraph.graph import StateGraph, END
from .state import ComplaintState

from .agents.categorizer import categorize
from .agents.sentiment import analyze_sentiment
from .agents.priority import assign_priority
from .agents.response import generate_email_response
from .agents.suggestion import suggest_actions
from .agents.reevaluate import reevaluate_priority
from .agents.escalation import decide_escalation

from .utils.memory_store import store_high_priority


def categorize_node(state):
    state["category"] = categorize(state["complaint_text"]).category
    return state


def sentiment_node(state):
    state["sentiment"] = analyze_sentiment(state["complaint_text"]).sentiment
    return state


def priority_node(state):
    result = assign_priority(
        state["complaint_text"],
        state["category"],
        state["sentiment"]
    )
    state["priority"] = result.priority
    state["priority_reason"] = result.reason
    return state


def response_node(state):
    state["response_email"] = generate_email_response(
        complaint_text=state["complaint_text"],
        category=state["category"],
        priority=state["priority"]
    )
    return state

def suggestion_node(state):
    result = suggest_actions(
        state["complaint_text"],
        state["category"],
        state["priority"]
    )
    state["suggestions"] = result.actions
    return state


def reevaluate_node(state):
    result = reevaluate_priority(
        state["complaint_text"],
        state["priority"],
        state["response_email"],
        state["suggestions"]
    )
    state["reevaluated_priority"] = result.updated_priority
    state["escalation_reason"] = result.reason
    return state


def escalation_node(state):
    result = decide_escalation(
        state["complaint_text"],
        state["reevaluated_priority"],
        state["escalation_reason"]
    )
    state["escalation_required"] = result.escalate

    if result.escalate:
        try:
            store_high_priority(state)
        except Exception:
            pass  

    return state


def route_after_escalation(state):
    if state["escalation_required"]:
        return "human"
    return END


def human_node(state):
    print("\n🚨 HUMAN ESCALATION REQUIRED 🚨\n")
    print(state)
    return state


def build_graph():
    graph = StateGraph(ComplaintState)

    graph.add_node("categorize", categorize_node)
    graph.add_node("sentiment", sentiment_node)
    graph.add_node("priority", priority_node)
    graph.add_node("response", response_node)
    graph.add_node("suggestion", suggestion_node)
    graph.add_node("reevaluate", reevaluate_node)
    graph.add_node("escalation", escalation_node)
    graph.add_node("human", human_node)

    graph.set_entry_point("categorize")
    graph.add_edge("categorize", "sentiment")
    graph.add_edge("sentiment", "priority")
    graph.add_edge("priority", "response")
    graph.add_edge("response", "suggestion")
    graph.add_edge("suggestion", "reevaluate")
    graph.add_edge("reevaluate", "escalation")
    graph.add_conditional_edges("escalation", route_after_escalation)

    return graph.compile()
