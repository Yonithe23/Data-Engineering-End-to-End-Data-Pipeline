from pathlib import Path

import requests
from sqlalchemy import create_engine, inspect


class SourceValidator:

    @staticmethod
    def validate_csv(file_path: str) -> bool:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"CSV file not found: {file_path}")

        if path.suffix != ".csv":
            raise ValueError("File must be a CSV file.")

        print("CSV source validation passed.")
        return True

    @staticmethod
    def validate_api(url: str) -> bool:
        response = requests.get(url, timeout=30)

        if response.status_code != 200:
            raise ValueError(f"API failed. Status code: {response.status_code}")

        try:
            response.json()
        except ValueError:
            raise ValueError("API response is not valid JSON.")

        print("API source validation passed.")
        return True

    @staticmethod
    def validate_database(db_url: str, table_name: str) -> bool:
        engine = create_engine(db_url)
        inspector = inspect(engine)

        if table_name not in inspector.get_table_names():
            raise ValueError(f"Table not found: {table_name}")

        print("Database source validation passed.")
        return True