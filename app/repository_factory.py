from app.repository import BusinessRepository
from app.config import companies


def get_repository(company_id: str) -> BusinessRepository:
    if company_id not in companies:
        raise ValueError(f"Unknown company: {company_id}")

    company_config = companies[company_id]

    return BusinessRepository(
        company_config["file_path"],
        company_config["mapping"]
    )