import pandas as pd

from src.config.configuration import ConfigurationManager
from src.utils.create_data_lake import create_data_lake_structure
from src.validation.source_validator import SourceValidator
from src.ingestion.csv_ingestion import CSVIngestion
from src.ingestion.api_ingestion import APIIngestion
from src.ingestion.database_ingestion import DatabaseIngestion
from src.standardization.standardizer import DataStandardizer
from src.transformation.transformer import DataTransformer
from src.warehouse.loader import WarehouseLoader


def main() -> None:
    create_data_lake_structure()

    config_manager = ConfigurationManager()

    csv_config = config_manager.get_csv_config()
    api_config = config_manager.get_api_config()
    database_config = config_manager.get_database_config()
    warehouse_config = config_manager.get_warehouse_config()

    # CSV pipeline
    SourceValidator.validate_csv(csv_config.source_file)

    csv_raw_file = CSVIngestion(
        source_file=csv_config.source_file,
        destination_dir=csv_config.destination_dir,
    ).ingest()

    DataStandardizer.standardize_file(
        input_file=csv_raw_file,
        output_file="data_lake/processed/csv/standardized_sales.csv",
    )

    csv_df = pd.read_csv("data_lake/processed/csv/standardized_sales.csv")
    csv_transformed = DataTransformer.transform(csv_df)

    csv_transformed.to_csv(
        "data_lake/curated/final/transformed_sales.csv",
        index=False,
    )

    # API pipeline
    SourceValidator.validate_api(api_config.url)

    api_raw_file = APIIngestion(
        url=api_config.url,
        destination_dir=api_config.destination_dir,
        file_name=api_config.file_name,
    ).ingest()

    DataStandardizer.standardize_file(
        input_file=api_raw_file,
        output_file="data_lake/processed/api/standardized_posts.csv",
    )

    api_df = pd.read_csv("data_lake/processed/api/standardized_posts.csv")
    api_transformed = DataTransformer.transform(api_df)

    api_transformed.to_csv(
        "data_lake/curated/final/transformed_posts.csv",
        index=False,
    )

    # Database pipeline
    SourceValidator.validate_database(
        db_url=database_config.db_url,
        table_name=database_config.table_name,
    )

    db_raw_file = DatabaseIngestion(
        db_url=database_config.db_url,
        table_name=database_config.table_name,
        destination_dir=database_config.destination_dir,
    ).ingest()

    DataStandardizer.standardize_file(
        input_file=db_raw_file,
        output_file="data_lake/processed/database/standardized_customers.csv",
    )

    db_df = pd.read_csv("data_lake/processed/database/standardized_customers.csv")
    db_transformed = DataTransformer.transform(db_df)

    db_transformed.to_csv(
        "data_lake/curated/final/transformed_customers.csv",
        index=False,
    )

    # Warehouse loading
    warehouse = WarehouseLoader(db_url=warehouse_config.db_url)

    warehouse.load_csv_to_table(
        csv_file="data_lake/curated/final/transformed_sales.csv",
        table_name="sales",
    )

    warehouse.load_csv_to_table(
        csv_file="data_lake/curated/final/transformed_posts.csv",
        table_name="posts",
    )

    warehouse.load_csv_to_table(
        csv_file="data_lake/curated/final/transformed_customers.csv",
        table_name="customers",
    )

    print("End-to-end data pipeline completed successfully.")


if __name__ == "__main__":
    main()