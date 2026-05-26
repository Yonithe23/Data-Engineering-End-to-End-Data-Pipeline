from src.ingestion.csv_ingestion import CSVIngestion
from src.ingestion.database_ingestion import DatabaseIngestion
from src.ingestion.api_ingestion import APIIngestion


def main():

    # CSV Ingestion
    csv_ingestion = CSVIngestion(
        source_file="data/sales.csv",
        destination_dir="data_lake/raw/csv"
    )

    csv_ingestion.ingest()

    # Database Ingestion
    db_ingestion = DatabaseIngestion(
        db_url="postgresql+psycopg2://username:password@localhost:5432/mydb",
        table_name="customers",
        destination_dir="data_lake/raw/database"
    )

    db_ingestion.ingest()

    api_ingestion = APIIngestion(
        url="https://jsonplaceholder.typicode.com/posts",
        destination_dir="data_lake/raw/api",
        file_name="posts"
    )

    api_ingestion.ingest()


if __name__ == "__main__":
    main()