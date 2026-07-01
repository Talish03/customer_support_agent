# Customer Support Agent
A LangChain-powered customer support agent that categorizes queries, analyzes sentiment, and routes them to the appropriate response handler — built with FastAPI and Groq.

## Features
- Categorizes queries into Technical, Billing, or General
- Analyzes sentiment as Positive, Neutral, or Negative
- Routes negative sentiment queries to escalation, regardless of category
- Generates contextual responses for each category
- Maintains per-session conversation history for multi-turn conversations


## Setup
1. Clone the repo and navigate into the folder
2. Create a virtual environment:
    python -m venv venv
    venv\Scripts\activate
3. Install dependencies:
    pip install -r requirements.txt
4. Create a `.env` file with your Groq API key:
    GROQ_API_KEY=your_key_here

## Running the App
uvicorn main:app --reload
Visit `http://127.0.0.1:8000/docs` to test the API via Swagger UI.

## How It Works
1. Customer query comes in via POST /support
2. LLM classifies the query into Technical, Billing, or General
3. LLM analyzes the sentiment — Positive, Neutral, or Negative
4. Routing logic runs: Negative sentiment always escalates, regardless of category
5. The appropriate handler generates a contextual response
6. Result is returned as structured JSON validated by Pydantic

## Tech Stack
- LangChain — prompt chaining and LLM orchestration
- Groq (llama-3.1-8b-instant) — LLM provider
- FastAPI — REST API framework
- Pydantic — input/output validation
- Python-dotenv — environment config