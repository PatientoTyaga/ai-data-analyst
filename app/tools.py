from app.models import RevenueArgs, AverageRevenueArgs
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
    
def get_average_revenue(company_id: str, end_date: date, days: int) -> dict:
    repository = get_repository(company_id)

    average_revenue = repository.get_average_revenue(
        end_date=end_date,
        days=days
    )

    if average_revenue is None:
        return {
            "success": False,
            "error_code": "DATA_NOT_FOUND",
            "message": f"No transaction data exists on or before {end_date}."
        }

    return {
        "success": True,
        "average_revenue": average_revenue,
        "days_requested": days
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

get_average_revenue_tool = {
    "type": "function",
    "name": "get_average_revenue",
    "description": "Gets the average daily revenue over a specified number of recent days ending on a specific date.",
    "parameters": {
        "type": "object",
        "properties": {
            "end_date": {
                "type": "string",
                "description": "The final date to include in the average, in YYYY-MM-DD format."
            },
            "days": {
                "type": "integer",
                "description": "The number of recent days with transaction data to include in the average."
            }
        },
        "required": ["end_date", "days"]
    }
}

#-----------------------------------------
# function registry
#-----------------------------------------

tool_functions = {
    "get_revenue": get_revenue,
    "get_revenue_by_region": get_revenue_by_region,
    "get_average_revenue": get_average_revenue
}


#-----------------------------------------
# Validation registry
#-----------------------------------------

tool_validators = {
    "get_revenue": RevenueArgs,
    "get_revenue_by_region": RevenueArgs,
    "get_average_revenue": AverageRevenueArgs
}

#-----------------------------------------
# tools registry
#-----------------------------------------

tools = [
    get_revenue_tool,
    get_revenue_by_region_tool,
    get_average_revenue_tool
]