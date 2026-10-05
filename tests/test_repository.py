from datetime import date

from app.repository import BusinessRepository
from app.config import company_a_mapping, company_b_mapping


def test_company_a_revenue():
    repository = BusinessRepository(
        "data/company_a_sales.csv",
        company_a_mapping
    )

    result = repository.get_revenue(date(2026, 9, 20))

    assert result == 5975.25


def test_company_b_revenue():
    repository = BusinessRepository(
        "data/company_b_orders.csv",
        company_b_mapping
    )

    result = repository.get_revenue(date(2026, 9, 20))

    assert result == 3750.75


def test_revenue_by_region():
    repository = BusinessRepository(
        "data/company_a_sales.csv",
        company_a_mapping
    )

    result = repository.get_revenue_by_region(date(2026, 9, 20))

    assert result == {
        "East": 3300.00,
        "Central": 950.25,
        "West": 1725.00
    }


def test_average_revenue():
    repository = BusinessRepository(
        "data/company_a_sales.csv",
        company_a_mapping
    )

    result = repository.get_average_revenue(
        date(2026, 9, 19),
        2
    )

    assert result == 6601.0


def test_cancellations():
    repository = BusinessRepository(
        "data/company_a_sales.csv",
        company_a_mapping
    )

    result = repository.get_cancellations(date(2026, 9, 20))

    assert result == 1


def test_cancellations_by_region():
    repository = BusinessRepository(
        "data/company_a_sales.csv",
        company_a_mapping
    )

    result = repository.get_cancellations_by_region(
        date(2026, 9, 20)
    )

    assert result == {
        "West": 1
    }


def test_missing_date_returns_none():
    repository = BusinessRepository(
        "data/company_a_sales.csv",
        company_a_mapping
    )

    result = repository.get_revenue(date(2026, 1, 1))

    assert result is None