from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage
import os

def escalation_response(query: str) -> str:
    return (
        "I sincerely apologize for the experience you're having. "
        "I completely understand your frustration and I want to make this right. "
        "I'm escalating your case to a senior support specialist who will reach out "
        "to you within 30 minutes to personally resolve this issue. Thank you for your patience."
    )