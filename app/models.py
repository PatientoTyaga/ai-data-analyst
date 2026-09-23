from datetime import date
from pydantic import BaseModel


class RevenueArgs(BaseModel):
    revenue_date: date