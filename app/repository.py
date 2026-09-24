import csv
from datetime import date


class BusinessRepository:

    def __init__(self, file_path: str, mapping: dict):
        self.file_path = file_path
        self.mapping = mapping

    def get_revenue(self, revenue_date: date):
        total_revenue = 0.0
        date_found = False

        with open(self.file_path, mode="r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                transaction_date = date.fromisoformat(
                    row[self.mapping["transaction_date"]]
                )

                if transaction_date == revenue_date:
                    date_found = True

                    if row[self.mapping["status"]] == self.mapping["valid_status"]:
                        total_revenue += float(row[self.mapping["revenue"]])

        if not date_found:
            return None

        return total_revenue
    
    def get_revenue_by_region(self, revenue_date: date):
        revenue_by_region = {}
        date_found = False

        with open(self.file_path, mode="r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                transaction_date = date.fromisoformat(
                    row[self.mapping["transaction_date"]]
                )

                if transaction_date == revenue_date:
                    date_found = True

                    if row[self.mapping["status"]] == self.mapping["valid_status"]:
                        region = row[self.mapping["region"]]
                        amount = float(row[self.mapping["revenue"]])

                        revenue_by_region[region] = (
                            revenue_by_region.get(region, 0.0) + amount
                        )

        if not date_found:
            return None

        return revenue_by_region
