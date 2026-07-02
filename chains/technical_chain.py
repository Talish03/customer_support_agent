from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from chains.llm_declaration import llm
from chains.history import format_history

def run_technical_chain(query: str, history: list) -> str:
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a technical support specialist.
        Give a clear, helpful response to the customer's technical issue.
        - Use step-by-step instructions where appropriate
        - Explain technical terms simply
        - Be concise but thorough
        - Remember the conversation history and refer back to it if relevant
        - End with an offer to help further"""),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{query}")
    ])
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"query": query, "history": format_history(history)})
