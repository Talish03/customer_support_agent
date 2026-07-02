from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from chains.llm_declaration import llm

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