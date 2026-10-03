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
    
    
    def get_average_revenue(self, end_date: date, days: int):
        daily_revenues = {}

        with open(self.file_path, mode="r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                transaction_date = date.fromisoformat(
                    row[self.mapping["transaction_date"]]
                )

                if transaction_date <= end_date:
                    if row[self.mapping["status"]] == self.mapping["valid_status"]:
                        amount = float(row[self.mapping["revenue"]])

                        daily_revenues[transaction_date] = (
                            daily_revenues.get(transaction_date, 0.0) + amount
                        )
                        
        if not daily_revenues:
            return None

        sorted_dates = sorted(daily_revenues.keys(), reverse=True)

        selected_dates = sorted_dates[:days]

        total_revenue = sum(
            daily_revenues[revenue_date]
            for revenue_date in selected_dates
        )

        average_revenue = total_revenue / len(selected_dates)

        return average_revenue
    
    
    def get_cancellations(self, cancellation_date: date):
        cancellation_count = 0
        date_found = False

        with open(self.file_path, mode="r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                transaction_date = date.fromisoformat(
                    row[self.mapping["transaction_date"]]
                )

                if transaction_date == cancellation_date:
                    date_found = True

                    if (
                        row[self.mapping["status"]]
                        == self.mapping["cancelled_status"]
                    ):
                        cancellation_count += 1

        if not date_found:
            return None

        return cancellation_count
    

    def get_cancellations_by_region(self, cancellation_date: date):
        cancellations_by_region = {}
        date_found = False

        with open(self.file_path, mode="r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                transaction_date = date.fromisoformat(
                    row[self.mapping["transaction_date"]]
                )

                if transaction_date == cancellation_date:
                    date_found = True

                    if (
                        row[self.mapping["status"]]
                        == self.mapping["cancelled_status"]
                    ):
                        region = row[self.mapping["region"]]

                        cancellations_by_region[region] = (
                            cancellations_by_region.get(region, 0) + 1
                        )

        if not date_found:
            return None

        return cancellations_by_region
