from app.repository import BusinessRepository
from app.models import RevenueArgs
from datetime import date


repository = BusinessRepository()


def get_revenue(revenue_date: date) -> float | None:
    return repository.get_revenue(revenue_date)

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