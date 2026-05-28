from pathlib import Path


def create_data_lake_structure() -> None:
    folders = [
        "data_lake/raw/csv",
        "data_lake/raw/api",
        "data_lake/raw/database",
        "data_lake/processed/csv",
        "data_lake/processed/api",
        "data_lake/processed/database",
        "data_lake/curated/final",
    ]

    for folder in folders:
        Path(folder).mkdir(parents=True, exist_ok=True)

    print("Data lake structure created successfully.")