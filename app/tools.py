from app.models import RevenueArgs
from datetime import date
from app.repository_factory import get_repository

def get_revenue(company_id: str, revenue_date: date) -> dict:
    repository = get_repository(company_id)
    
    revenue = repository.get_revenue(revenue_date)

    if revenue is None:
        return {
            "success": False,
            "error_code": "DATA_NOT_FOUND",
            "message": f"No transaction data exists for {revenue_date}."
        }

    return {
        "success": True,
        "revenue": revenue
    }
    
def get_revenue_by_region(company_id: str, revenue_date: date) -> dict:
    repository = get_repository(company_id)

    revenue_by_region = repository.get_revenue_by_region(revenue_date)

    if revenue_by_region is None:
        return {
            "success": False,
            "error_code": "DATA_NOT_FOUND",
            "message": f"No transaction data exists for {revenue_date}."
        }

    return {
        "success": True,
        "revenue_by_region": revenue_by_region
    }
    
#-----------------------------------------
# Tools
#-----------------------------------------

get_revenue_tool = {
    "type": "function",
    "name": "get_revenue",
    "description": "Gets the total revenue for a specific date.",
    "parameters": {
        "type": "object",
        "properties": {
            "revenue_date": {
                "type": "string",
                "description": "The date to retrieve revenue for, in YYYY-MM-DD format."
            }
        },
        "required": ["revenue_date"]
    }
}

get_revenue_by_region_tool = {
    "type": "function",
    "name": "get_revenue_by_region",
    "description": "Gets the revenue breakdown by region for a specific date.",
    "parameters": {
        "type": "object",
        "properties": {
            "revenue_date": {
                "type": "string",
                "description": "The date to retrieve regional revenue for, in YYYY-MM-DD format."
            }
        },
        "required": ["revenue_date"]
    }
}

#-----------------------------------------
# function registry
#-----------------------------------------

tool_functions = {
    "get_revenue": get_revenue,
    "get_revenue_by_region": get_revenue_by_region
}


#-----------------------------------------
# Validation registry
#-----------------------------------------

tool_validators = {
    "get_revenue": RevenueArgs,
    "get_revenue_by_region": RevenueArgs
}

#-----------------------------------------
# tools registry
#-----------------------------------------

tools = [
    get_revenue_tool,
    get_revenue_by_region_tool
]