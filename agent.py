from chains import (
    run_billing_chain,
    run_general_chain,
    run_technical_chain,
    categorization_chain,
    escalation_response,
    sentiment_chain
)
from models import CustomerQuery, SupportResponse , ChatMessage

session_store: dict[str, list[ChatMessage]] = {}

def get_history(session_id : str) -> list[ChatMessage] :
    if session_id not in session_store:
        session_store[session_id] = []
    return session_store[session_id]

def save_to_history(session_id: str, query: str, response: str):
    session_store[session_id].append(ChatMessage(role="customer", content=query))
    session_store[session_id].append(ChatMessage(role="agent", content=response))

def run_support_agent(customer_query: CustomerQuery) -> SupportResponse:
    query = customer_query.query
    session_id = customer_query.session_id
    
    history = get_history(session_id)

    
    category = categorization_chain.invoke({"query": query}).strip()

    sentiment = sentiment_chain.invoke({"query": query}).strip()

    if sentiment == "Negative":
        response = escalation_response(query)
    elif category == "Technical":
        response = run_technical_chain(query, history)
    elif category == "Billing":
        response = run_billing_chain(query, history)
    else:
        response = run_general_chain(query, history)

    save_to_history(session_id, query, response)

    return SupportResponse(
        session_id=session_id,
        query=query,
        category=category,
        sentiment=sentiment,
        response=response,
        history=get_history(session_id)
    )