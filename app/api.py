import csv
import io

from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from app.repository import BusinessRepository
from app.agent import ask_agent
from app.database import initialize_database, save_dataset, get_dataset
from pathlib import Path
from uuid import uuid4


app = FastAPI(
    title="AI Data Analyst API",
    version="1.0.0"
)

initialize_database()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ColumnValuesRequest(BaseModel):
    dataset_id: str
    column: str

class MappingRequest(BaseModel):
    dataset_id: str
    original_filename: str
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
    dataset = get_dataset(request.dataset_id)

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
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are currently supported."
        )

    contents = await file.read()
    
    max_file_size = 10 * 1024 * 1024

    if len(contents) > max_file_size:
        raise HTTPException(
            status_code=413,
            detail="CSV file must be 10 MB or smaller."
        )
    
    dataset_id = str(uuid4())

    upload_directory = Path("data/uploads")
    upload_directory.mkdir(parents=True, exist_ok=True)

    file_path = upload_directory / f"{dataset_id}.csv"

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
            
        file_path.write_bytes(contents)

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
        
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        columns = reader.fieldnames or []

    required_columns = [
        request.transaction_date,
        request.revenue,
        request.region,
        request.status,
    ]

    for column in required_columns:
        if column not in columns:
            raise HTTPException(
                status_code=400,
                detail=f"Column '{column}' does not exist in the uploaded dataset."
            )
    
    status_values = set()

    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            value = row.get(request.status)

            if value:
                status_values.add(value)
                
    if request.valid_status not in status_values:
        raise HTTPException(
            status_code=400,
            detail=f"Status value '{request.valid_status}' does not exist in the uploaded dataset."
        )

    if request.cancelled_status not in status_values:
        raise HTTPException(
            status_code=400,
            detail=f"Status value '{request.cancelled_status}' does not exist in the uploaded dataset."
        )

    mapping = {
        "transaction_date": request.transaction_date,
        "revenue": request.revenue,
        "region": request.region,
        "status": request.status,
        "valid_status": request.valid_status,
        "cancelled_status": request.cancelled_status,
    }
    
    save_dataset(
        dataset_id=request.dataset_id,
        original_filename=request.original_filename,
        file_path=str(file_path),
        mapping=mapping
    )

    return {
        "dataset_id": request.dataset_id,
        "mapping": mapping
    }