
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langgraph.graph.message import add_messages




def print_message(message: BaseMessage):

    if isinstance(message, HumanMessage):
        print(f"👤 User: {message.content}")

    elif isinstance(message, AIMessage):
        print(f"🤖 Assistant: {message.content}")

        if hasattr(message, 'tool_calls') and message.tool_calls:
            for tool_call in message.tool_calls:
                args = ", ".join([f"{k}={v}" for k,v in tool_call['args'].items()])
                print(f"🛠️  Tool Call: {tool_call['name']}({args})")


    elif isinstance(message, ToolMessage):
        print(f"⚙️  Tool Result (ID {message.tool_call_id}): {message.content}")

    print("─" * 50)  # Visual separator

# Chat loop with step visualization
def chat_loop(TicketState, app):
    print("\n🚀 Starting chat session (type 'exit' to end)\n")
    state = TicketState(messages=[])
    
    while True:
        user_input = input("👤 You: ")
        if user_input.lower() == 'exit':
            break
            
        # Add user message to state
        user_msg = HumanMessage(content=user_input)
        new_messages = add_messages(state["messages"], [user_msg])
        state = TicketState(messages=new_messages)
        print_message(user_msg)  # Print user message
        
        # Track current message count BEFORE processing
        current_count = len(state["messages"])
        
        # Process through the graph
        for step in app.stream(
            state,
            stream_mode="values"
        ):
            # Get all messages in the current state
            all_messages = step["messages"]
            
            # Print only new messages added since we started processing
            new_messages_in_step = all_messages[current_count:]
            for msg in new_messages_in_step:
                # Ensure we have a proper message object
                if not isinstance(msg, BaseMessage):
                    try:
                        # Try to convert to AIMessage if possible
                        if "content" in msg and "role" in msg:
                            if msg["role"] == "assistant":
                                msg = AIMessage.content
                            elif msg["role"] == "tool":
                                msg = "tool_msg"
                            else:
                                msg = HumanMessage.content
                        else:
                            msg = AIMessage(content=str(msg))
                    except Exception as e:
                        print(f"⚠️ Error converting message: {e}")
                        msg = AIMessage(content=str(msg))
                
                print_message(msg)
            
            # Update state and message count
            state = step
            current_count = len(state["messages"])
            
        # Add separation
        print("\n" + "="*80 + "\n")