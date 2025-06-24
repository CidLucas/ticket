from typing import List, TypedDict, Optional, Literal
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent, ToolNode
from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from tools.tools import buy_tickets, look_session
from IPython.display import Image, display



class TicketState(TypedDict):
    messages: List[BaseMessage]


tools = [buy_tickets, look_session]
tool_node = ToolNode(tools) 

agent = create_react_agent(ChatOllama(model="llama3.2") , tools = tools)




def should_continue(state: MessagesState):
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return END


def call_model(state: MessagesState):
    messages = state["messages"]
    response = agent.invoke(messages)
    return {"messages": [response]}


workflow = StateGraph(MessagesState)

# Define the two nodes we will cycle between
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", should_continue, ["tools", END])
workflow.add_edge("tools", "agent")

app = workflow.compile()



try:
    display(Image(app.get_graph().draw_mermaid_png()))
except Exception:
    # This requires some extra dependencies and is optional
    pass