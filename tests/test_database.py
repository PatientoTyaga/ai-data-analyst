from app.database import save_dataset, get_dataset


def test_save_and_get_dataset(tmp_path, monkeypatch):
    test_database = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.database.DATABASE_PATH",
        test_database
    )

    from app.database import initialize_database

    initialize_database()

    mapping = {
        "transaction_date": "created_at",
        "revenue": "total_price",
        "region": "location",
        "status": "order_state",
        "valid_status": "paid",
        "cancelled_status": "cancelled",
    }

    save_dataset(
        dataset_id="test-dataset-123",
        original_filename="test.csv",
        file_path="data/uploads/test.csv",
        mapping=mapping
    )

    result = get_dataset("test-dataset-123")

    assert result is not None
    assert result["dataset_id"] == "test-dataset-123"
    assert result["original_filename"] == "test.csv"
    assert result["file_path"] == "data/uploads/test.csv"
    assert result["mapping"] == mapping