from datetime import date
from pydantic import BaseModel, Field


class RevenueArgs(BaseModel):
    revenue_date: date
    
class AverageRevenueArgs(BaseModel):
    end_date: date
    days: int = Field(gt=0)