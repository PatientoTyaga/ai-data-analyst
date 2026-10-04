import csv
import io

from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from app.repository import BusinessRepository
from app.agent import ask_agent
from pathlib import Path
from uuid import uuid4


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

dataset_registry = {}

class ColumnValuesRequest(BaseModel):
    dataset_id: str
    column: str

class MappingRequest(BaseModel):
    dataset_id: str
    transaction_date: str
    revenue: str
    region: str
    status: str
    valid_status: str
    cancelled_status: str

class AskRequest(BaseModel):
    dataset_id: str
    question: str


class AskResponse(BaseModel):
    answer: str
    
@app.post("/column-values")
def get_column_values(request: ColumnValuesRequest):
    file_path = Path("data/uploads") / f"{request.dataset_id}.csv"

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Uploaded dataset was not found."
        )

    values = set()

    with open(file_path, mode="r") as file:
        reader = csv.DictReader(file)

        if request.column not in (reader.fieldnames or []):
            raise HTTPException(
                status_code=400,
                detail="Column does not exist."
            )

        for row in reader:
            value = row.get(request.column)

            if value:
                values.add(value)

    return {
        "values": sorted(values)
    }
    
@app.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest):
    dataset = dataset_registry.get(request.dataset_id)

    if not dataset:
        raise HTTPException(
            status_code=404,
            detail="Dataset configuration was not found."
        )

    repository = BusinessRepository(
        file_path=dataset["file_path"],
        mapping=dataset["mapping"]
    )

    try:
        answer = ask_agent(
            company_id=request.dataset_id,
            question=request.question,
            repository=repository
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
    
    dataset_id = str(uuid4())

    upload_directory = Path("data/uploads")
    upload_directory.mkdir(parents=True, exist_ok=True)

    file_path = upload_directory / f"{dataset_id}.csv"

    file_path.write_bytes(contents)

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
            "dataset_id": dataset_id,
            "filename": file.filename,
            "columns": columns,
            "sample_rows": sample_rows
        }

    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="Unable to read the CSV file."
        )
    
@app.post("/mapping")
def save_mapping(request: MappingRequest):
    file_path = Path("data/uploads") / f"{request.dataset_id}.csv"

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Uploaded dataset was not found."
        )

    mapping = {
        "transaction_date": request.transaction_date,
        "revenue": request.revenue,
        "region": request.region,
        "status": request.status,
        "valid_status": request.valid_status,
        "cancelled_status": request.cancelled_status,
    }
    
    dataset_registry[request.dataset_id] = {
        "file_path": str(file_path),
        "mapping": mapping
    }

    return {
        "dataset_id": request.dataset_id,
        "mapping": mapping
    }