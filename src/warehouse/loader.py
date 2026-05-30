from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine


class WarehouseLoader:
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.engine = create_engine(db_url)

    def load_csv_to_table(
        self,
        csv_file: str,
        table_name: str,
        if_exists: str = "replace",
    ) -> None:
        file_path = Path(csv_file)

        if not file_path.exists():
            raise FileNotFoundError(f"CSV file not found: {csv_file}")

        df = pd.read_csv(file_path)

        df.to_sql(
            name=table_name,
            con=self.engine,
            if_exists=if_exists,
            index=False,
        )

        print(f"Loaded {csv_file} into table: {table_name}")