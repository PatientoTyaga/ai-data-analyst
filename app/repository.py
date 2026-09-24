import csv
from datetime import date


class BusinessRepository:

    def __init__(self, file_path: str):
        self.file_path = file_path

    def get_revenue(self, revenue_date: date):
        total_revenue = 0.0
        date_found = False

        with open(self.file_path, mode="r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                transaction_date = date.fromisoformat(row["transaction_date"])

                if transaction_date == revenue_date:
                    date_found = True

                    if row["status"] == "completed":
                        total_revenue += float(row["amount"])

        if not date_found:
            return None

        return total_revenue
