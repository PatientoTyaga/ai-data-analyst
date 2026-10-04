import csv
import io

from fastapi import FastAPI, HTTPException, UploadFile, File
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
        
@app.post("/upload")
async def upload_data(file: UploadFile = File(...)):
    if not file.filename or not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are currently supported."
        )

    contents = await file.read()

    try:
        text = contents.decode("utf-8")
        reader = csv.DictReader(io.StringIO(text))

        columns = reader.fieldnames

        if not columns:
            raise HTTPException(
                status_code=400,
                detail="CSV file does not contain column headers."
            )

        sample_rows = []

        for index, row in enumerate(reader):
            if index >= 5:
                break

            sample_rows.append(row)

        return {
            "filename": file.filename,
            "columns": columns,
            "sample_rows": sample_rows
        }

    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="Unable to read the CSV file."
        )
        
    