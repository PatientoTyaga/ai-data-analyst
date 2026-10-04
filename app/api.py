from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from app.agent import ask_agent


app = FastAPI(
    title="AI Data Analyst API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str
    
    
@app.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest):
    company_id = "company_a"

    try:
        answer = ask_agent(
            company_id=company_id,
            question=request.question
        )

        return AskResponse(answer=answer)

    except Exception as error:
        print("AI request failed:", error)

        raise HTTPException(
            status_code=503,
            detail="AI service is temporarily unavailable."
        )
        
    