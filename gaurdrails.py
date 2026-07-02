from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from chains.llm_declaration import llm
from logger import logger
from exceptions import ValidationError



INJECTION_PHRASES = [
    "ignore previous instructions",
    "ignore all instructions",
    "disregard your instructions",
    "you are now",
    "pretend you are",
    "act as if",
    "forget everything",
    "new persona",
    "jailbreak",
    "do anything now",
    "dan mode",
]

OFFENSIVE_WORDS = [
    "fuck", "shit", "bitch", "asshole", "bastard",
    "idiot", "stupid", "moron", "dumbass", "crap"
]

def check_length(query: str):
    """Block empty or too-short queries"""
    if not query or not query.strip():
        raise ValidationError("Query cannot be empty.")
    if len(query.strip()) < 3:
        raise ValidationError("Query is too short. Please describe your issue.")
    if len(query.strip()) > 2000:
        raise ValidationError("Query is too long. Please keep it under 2000 characters.")

def check_injection(query: str):
    """Block prompt injection attempts"""
    lower = query.lower()
    for phrase in INJECTION_PHRASES:
        if phrase in lower:
            logger.warning(f"Prompt injection attempt detected | query='{query[:50]}'")
            raise ValidationError("Invalid input detected. Please describe your support issue.")

def check_offensive(query: str):
    """Flag and block highly offensive language"""
    lower = query.lower()
    for word in OFFENSIVE_WORDS:
        if word in lower:
            logger.warning(f"Offensive language detected | query='{query[:50]}'")
            raise ValidationError(
                "We understand you may be frustrated. "
                "Please describe your issue without offensive language and we'll be happy to help."
            )



relevance_prompt = ChatPromptTemplate.from_messages([
    (
        "system", """You are a relevance checker for a customer support system.
        Determine if the query is related to customer support topics such as:
        - Technical issues, software problems, connectivity
        - Billing, payments, invoices, refunds
        - General questions about services, policies, business hours

        Reply with ONLY 'relevant' or 'irrelevant'. Nothing else."""),
    ("human", "{query}")
])
relevance_chain = relevance_prompt | llm | StrOutputParser()


def check_relevance(query: str):
    """Block completely off-topic queries using LLM"""
    try:
        result = relevance_chain.invoke({"query": query}).strip().lower()
        logger.debug(f"Relevance check | result={result} | query='{query[:50]}'")
        if result == "irrelevant":
            raise ValidationError(
                "I can only help with customer support topics like technical issues, "
                "billing, or general service questions. How can I assist you?"
            )
    except ValidationError:
        raise
    except Exception as e:
        logger.error(f"Relevance check failed | error={e}")
        pass



def run_guardrails(query: str):
    """Run all checks in order. Raises ValidationError if any fail."""
    check_length(query)
    check_injection(query)
    check_offensive(query)
    check_relevance(query)
    logger.debug(f"Guardrails passed | query='{query[:50]}'")