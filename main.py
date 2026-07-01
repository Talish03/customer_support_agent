from fastapi import FastAPI
from agent import run_support_agent
from models import CustomerQuery , SupportResponse

app=FastAPI(title="Customer Support Agent")

@app.get("/")
def health_check():
    return {"status": "running"}


@app.post("/support", response_model=SupportResponse)
def support_endpoint(customer_query: CustomerQuery):
    result = run_support_agent(customer_query)
    return result