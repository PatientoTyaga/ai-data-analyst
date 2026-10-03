from fastapi import FastAPI
from pydantic import BaseModel

from app.agent import ask_agent


app = FastAPI(
    title="AI Data Analyst API",
    version="1.0.0"
)


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str
    
@app.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest):
    company_id = "company_a"

    answer = ask_agent(
        company_id=company_id,
        question=request.question
    )

    return AskResponse(answer=answer)
        
    