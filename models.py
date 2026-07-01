from pydantic import BaseModel
from typing import Literal , List

class ChatMessage(BaseModel):
    role : str
    content : str
class CustomerQuery(BaseModel):
    session_id : str
    query : str = None

class SupportResponse(BaseModel):
    query : str
    session_id : str
    category : Literal["Technical", "Billing", "General"]
    sentiment : Literal["Positive", "Neutral", "Negative"]
    response : str
    history: List[ChatMessage]

