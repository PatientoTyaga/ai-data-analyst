from datetime import date

class BusinessRepository:

    def __init__(self):
        self.revenue_data = {
            date(2026, 9, 18): 18452.73,
            date(2026, 9, 19): 21340.50,
            date(2026, 9, 20): 19780.25
        }

    def get_revenue(self, revenue_date: date) -> float | None:
        return self.revenue_data.get(revenue_date)