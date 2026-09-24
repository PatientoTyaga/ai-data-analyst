from app.repository import BusinessRepository
from app.models import RevenueArgs
from datetime import date


repository = BusinessRepository("data/company_a_sales.csv")


def get_revenue(revenue_date: date) -> dict:
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

#-----------------------------------------
# function registry
#-----------------------------------------

tool_functions = {
    "get_revenue": get_revenue
}


#-----------------------------------------
# Validation registry
#-----------------------------------------

tool_validators = {
    "get_revenue": RevenueArgs
}

#-----------------------------------------
# tools registry
#-----------------------------------------

tools = [
    get_revenue_tool
]