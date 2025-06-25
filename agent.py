from typing import TypedDict, Annotated, Sequence
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent, ToolNode
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from tools.tools import buy_tickets, look_session
from utils.chat_stream import chat_loop

from langgraph.graph.message import add_messages

class TicketState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]



tools = [buy_tickets, look_session]
tool_node = ToolNode(tools) 

prompt = """You are a helpful assistant that helps users to book cinema sessions.
You can use the tools look_session and buy_tickets to help you with that.
You can ask the user for more information if needed.
You can also use the tool look_session to get a list of available cinema sessions.
Once you have all the information you can use the tool buy_tickets to book the tickets."""

agent = create_react_agent(ChatOllama(model="llama3.2") ,prompt=prompt, tools = tools)

#def user_input_node(state: TicketState):
#    # Extract user input from state
#    user_data = state["messages"][-1].content if state["messages"] else ""
    
#    return {"messages": [HumanMessage(content=user_data)]}
    

def should_continue(state: TicketState):
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return END


def call_agent(state: TicketState):
    # Get recent messages (last 6 for context)
    messages = state["messages"][-6:]
    
    # Convert messages to a format the agent expects
    agent_input = []
    for msg in messages:
        if isinstance(msg, HumanMessage):
            agent_input.append({"role": "user", "content": msg.content})
        elif isinstance(msg, AIMessage):
            agent_input.append({"role": "assistant", "content": msg.content})
        elif isinstance(msg, ToolMessage):
            agent_input.append({
                "role": "tool",
                "content": msg.content,
                "tool_call_id": msg.tool_call_id,
                "name": msg.name
            })
    
    # Invoke agent
    response = agent.invoke({"messages": agent_input})
    
    # Handle different response types
    if isinstance(response, dict) and "output" in response:
        content = response["output"]
    elif hasattr(response, "content"):
        content = response.content
    else:
        content = str(response)
    
    # Create proper AIMessage with tool calls if needed
    tool_calls = []
    if hasattr(response, "tool_calls"):
        tool_calls = response.tool_calls
    
    return {"messages": [AIMessage(content=content, tool_calls=tool_calls)]}


workflow = StateGraph(TicketState)

# Define the two nodes we will cycle between

#workflow.add_node("user_data", user_input_node)
workflow.add_node("agent", call_agent)
workflow.add_node("tools", tool_node)
workflow.set_entry_point("agent")

workflow.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
workflow.add_edge("tools", "agent")


app = workflow.compile()

chat_loop(TicketState, app)
