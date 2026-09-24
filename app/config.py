company_a_mapping = {
    "transaction_date": "transaction_date",
    "revenue": "amount",
    "region": "region",
    "status": "status",
    "valid_status": "completed"
}

company_b_mapping = {
    "transaction_date": "created_at",
    "revenue": "total_price",
    "region": "location",
    "status": "order_state",
    "valid_status": "paid"
}

companies = {
    "company_a": {
        "file_path": "data/company_a_sales.csv",
        "mapping": company_a_mapping
    },
    "company_b": {
        "file_path": "data/company_b_orders.csv",
        "mapping": company_b_mapping
    }
}