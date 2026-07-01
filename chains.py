from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage
import os

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

categorization_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a customer support classifier.
Classify the customer query into exactly one of these categories:
- Technical
- Billing
- General

Rules:
- Technical: issues with products, software, connectivity, errors, how-to questions
- Billing: payments, invoices, receipts, refunds, charges, subscriptions
- General: business hours, policies, contact info, anything else

Respond with ONLY the category name. No explanation, no punctuation."""),
    ("human", "{query}")
])
categorization_chain = categorization_prompt | llm | StrOutputParser()

sentiment_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a customer sentiment analyser.
Analyse the emotional tone of the customer and classify into exactly one of:
- Positive
- Neutral
- Negative

Rules:
- Positive: happy, satisfied, complimentary, excited
- Neutral: factual, informational, no strong emotion
- Negative: frustrated, angry, upset, disappointed, threatening to cancel

Respond with ONLY the sentiment label. No explanation, no punctuation."""),
    ("human", "{query}")
])
sentiment_chain = sentiment_prompt | llm | StrOutputParser()

def format_history(history):
    messages = []
    for msg in history:
        if msg.role == "customer":
            messages.append(HumanMessage(content=msg.content))
        else:
            messages.append(AIMessage(content=msg.content))
    return messages

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

def run_general_chain(query: str, history: list) -> str:
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a friendly customer support agent.
    Give a warm, helpful response to the customer's general query.
    - Be friendly and approachable
    - Be concise
    - Remember the conversation history and refer back to it if relevant
    - End with an offer to help further"""),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{query}")
    ])
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"query": query, "history": format_history(history)})

def escalation_response(query: str) -> str:
    return (
        "I sincerely apologize for the experience you're having. "
        "I completely understand your frustration and I want to make this right. "
        "I'm escalating your case to a senior support specialist who will reach out "
        "to you within 30 minutes to personally resolve this issue. Thank you for your patience."
    )