from pathlib import Path
from datetime import datetime

import pandas as pd
from sqlalchemy import create_engine


class DatabaseIngestion:
    def __init__(
        self,
        db_url: str,
        table_name: str,
        destination_dir: str
    ):
        self.db_url = db_url
        self.table_name = table_name
        self.destination_dir = Path(destination_dir)

    def ingest(self):
        self.destination_dir.mkdir(parents=True, exist_ok=True)

        engine = create_engine(self.db_url)

        query = f"SELECT * FROM {self.table_name}"
        df = pd.read_sql(query, engine)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        output_file = (
            self.destination_dir /
            f"{self.table_name}_{timestamp}.csv"
        )

        df.to_csv(output_file, index=False)

        print(f"Ingested: {output_file}")

        return output_file