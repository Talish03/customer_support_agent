from langchain_core.messages import HumanMessage, AIMessage

def format_history(history):
    messages = []
    for msg in history:
        if msg.role == "customer":
            messages.append(HumanMessage(content=msg.content))
        else:
            messages.append(AIMessage(content=msg.content))
    return messages