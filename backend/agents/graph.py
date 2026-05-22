from langgraph.graph import StateGraph
from typing import TypedDict


class GraphState(TypedDict):
    review: str
    sentiment: str
    category: str
    context: str
    response: str


workflow = StateGraph(GraphState)

print("LangGraph initialized")