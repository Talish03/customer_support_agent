from fastapi import FastAPI , Request
from agent import run_support_agent
from models import CustomerQuery , SupportResponse
from logger import logger
import time
from exceptions import LLMError, SessionError
from fastapi.responses import JSONResponse
from exceptions import LLMError, SessionError, ValidationError
from database import create_tables

app=FastAPI(title="Customer Support Agent")


@app.on_event("startup")
def startup():
    logger.info("Starting up — creating database tables")
    create_tables()


@app.exception_handler(LLMError)
async def llm_error_handler(request: Request, exc: LLMError):
    logger.error(f"LLMError on {request.url.path} | {exc}")
    return JSONResponse(
        status_code=503,
        content={"error": "AI service unavailable", "detail": str(exc)}
    )

@app.exception_handler(SessionError)
async def session_error_handler(request: Request, exc: SessionError):
    logger.error(f"SessionError on {request.url.path} | {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Session error", "detail": str(exc)}
    )

@app.exception_handler(ValidationError)
async def validation_error_handler(request: Request, exc: ValidationError):
    logger.warning(f"ValidationError on {request.url.path} | {exc}")
    return JSONResponse(
        status_code=400,
        content={
            "error": "Validation error",
            "detail": str(exc)
        }
    )

@app.exception_handler(Exception)
async def generic_error_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error on {request.url.path} | {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Something went wrong", "detail": "Please try again."}
    )


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = round((time.time() - start) * 1000, 2)
    logger.info(f"HTTP {request.method} {request.url.path} | status={response.status_code} | {duration}ms")
    return response
@app.get("/")


def health_check():
    return {"status": "running"}


@app.post("/support", response_model=SupportResponse)
def support_endpoint(customer_query: CustomerQuery):
    result = run_support_agent(customer_query)
    return result