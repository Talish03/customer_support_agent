from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from chains.llm_declaration import llm

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