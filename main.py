from src.utils.create_data_lake import create_data_lake_structure

from src.validation.source_validator import SourceValidator

from src.ingestion.csv_ingestion import CSVIngestion
from src.ingestion.api_ingestion import APIIngestion
from src.ingestion.database_ingestion import DatabaseIngestion

from src.standardization.standardizer import DataStandardizer


def main() -> None:
    create_data_lake_structure()

    # -------------------------
    # 1. CSV source validation + ingestion
    # -------------------------
    csv_file = "data/sales.csv"

    SourceValidator.validate_csv(csv_file)

    csv_ingestion = CSVIngestion(
        source_file=csv_file,
        destination_dir="data_lake/raw/csv",
    )
    csv_raw_file = csv_ingestion.ingest()

    DataStandardizer.standardize_file(
        input_file=csv_raw_file,
        output_file="data_lake/processed/csv/standardized_sales.csv",
    )

    # -------------------------
    # 2. API source validation + ingestion
    # -------------------------
    api_url = "https://jsonplaceholder.typicode.com/posts"

    SourceValidator.validate_api(api_url)

    api_ingestion = APIIngestion(
        url=api_url,
        destination_dir="data_lake/raw/api",
        file_name="posts",
    )
    api_raw_file = api_ingestion.ingest()

    DataStandardizer.standardize_file(
        input_file=api_raw_file,
        output_file="data_lake/processed/api/standardized_posts.csv",
    )

    # -------------------------
    # 3. Database source validation + ingestion
    # -------------------------
    db_url = "postgresql+psycopg2://username:password@localhost:5432/mydb"
    table_name = "customers"

    SourceValidator.validate_database(
        db_url=db_url,
        table_name=table_name,
    )

    db_ingestion = DatabaseIngestion(
        db_url=db_url,
        table_name=table_name,
        destination_dir="data_lake/raw/database",
    )
    db_raw_file = db_ingestion.ingest()

    DataStandardizer.standardize_file(
        input_file=db_raw_file,
        output_file="data_lake/processed/database/standardized_customers.csv",
    )

    print("Full local data pipeline completed successfully.")


if __name__ == "__main__":
    main()