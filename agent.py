from chains.billing_chain import run_billing_chain
from chains.categorization_chain import categorization_chain
from chains.sentiment_chain import sentiment_chain
from chains.general_chain import run_general_chain
from chains.technical_chain import run_technical_chain
from chains.escalation import escalation_response
from chains.history import format_history
from models import CustomerQuery, SupportResponse , ChatMessage
from logger import logger
from exceptions import LLMError , ValidationError , SessionError
from gaurdrails import run_guardrails
from database import SessionLocal, ConversationMessage


VALID_CATEGORIES = {"Technical", "Billing", "General"}
VALID_SENTIMENTS = {"Positive", "Neutral", "Negative"}

session_store: dict[str, list[ChatMessage]] = {}

def get_history(session_id: str) -> list[ChatMessage]:
    """Load conversation history from database"""
    try:
        db = SessionLocal()
        messages = db.query(ConversationMessage)\
            .filter(ConversationMessage.session_id == session_id)\
            .order_by(ConversationMessage.created_at)\
            .all()
        db.close()

        return [
            ChatMessage(role=msg.role, content=msg.content)
            for msg in messages
        ]
    except Exception as e:
        logger.error(f"Failed to get history | session={session_id} | error={e}")
        raise SessionError(f"Could not load session: {session_id}")

def save_to_history(session_id: str, query: str, response: str,
                    category: str, sentiment: str):
    """Save customer message and agent response to database"""
    try:
        db = SessionLocal()

        
        customer_msg = ConversationMessage(
            session_id=session_id,
            role="customer",
            content=query,
            category=category,
            sentiment=sentiment
        )

        
        agent_msg = ConversationMessage(
            session_id=session_id,
            role="agent",
            content=response
        )

        db.add(customer_msg)
        db.add(agent_msg)
        db.commit()
        db.close()

        logger.debug(f"Saved to database | session={session_id}")
    except Exception as e:
        logger.error(f"Failed to save to database | session={session_id} | error={e}")
        raise SessionError(f"Could not save session: {session_id}")
    


def run_support_agent(customer_query: CustomerQuery) -> SupportResponse:
    query = customer_query.query
    session_id = customer_query.session_id

    logger.info(f"New request | session={session_id} | query='{query}'")
    run_guardrails(query) 
    
    history = get_history(session_id)
    logger.debug(f"Loaded history | session={session_id} | turns={len(history)}")

    
    try:
        category = categorization_chain.invoke({"query": query}).strip()
        logger.info(f"Categorized | session={session_id} | category={category}")
    except Exception as e:
        logger.error(f"Categorization failed | session={session_id} | error={e}")
        raise LLMError("Categorization service unavailable. Please try again.")

    
    if category not in VALID_CATEGORIES:
        logger.warning(f"Invalid category returned | session={session_id} | value='{category}'")
        category = "General"  # safe fallback

    
    try:
        sentiment = sentiment_chain.invoke({"query": query}).strip()
        logger.info(f"Sentiment | session={session_id} | sentiment={sentiment}")
    except Exception as e:
        logger.error(f"Sentiment analysis failed | session={session_id} | error={e}")
        raise LLMError("Sentiment service unavailable. Please try again.")

    
    if sentiment not in VALID_SENTIMENTS:
        logger.warning(f"Invalid sentiment returned | session={session_id} | value='{sentiment}'")
        sentiment = "Neutral"  # safe fallback

    
    try:
        if sentiment == "Negative":
            logger.warning(f"Escalating | session={session_id} | reason=Negative sentiment")
            response = escalation_response(query)
        elif category == "Technical":
            logger.debug(f"Routing to technical handler | session={session_id}")
            response = run_technical_chain(query, history)
        elif category == "Billing":
            logger.debug(f"Routing to billing handler | session={session_id}")
            response = run_billing_chain(query, history)
        else:
            logger.debug(f"Routing to general handler | session={session_id}")
            response = run_general_chain(query, history)
    except LLMError:
        raise
    except Exception as e:
        logger.error(f"Response generation failed | session={session_id} | error={e}")
        raise LLMError("Response generation failed. Please try again.")

   
    save_to_history(session_id, query, response, category, sentiment)
    logger.info(f"Response sent | session={session_id} | history_length={len(get_history(session_id))}")

    updated_history = get_history(session_id)


    return SupportResponse(
        session_id=session_id,
        query=query,
        category=category,
        sentiment=sentiment,
        response=response,
        history=updated_history
    )