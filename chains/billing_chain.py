from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from chains.llm_declaration import llm
from chains.history import format_history

def run_billing_chain(query: str, history: list) -> str:
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a billing support specialist.
    Give a clear, direct response to the customer's billing query.
    - Be professional and reassuring
    - Give specific actionable steps
    - Remember the conversation history and refer back to it if relevant
    - End with an offer to help further"""),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{query}")
    ])
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"query": query, "history": format_history(history)})