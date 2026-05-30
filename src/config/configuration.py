from pathlib import Path

import yaml
from box import ConfigBox

from src.entity.config_entity import (
    CSVConfig,
    APIConfig,
    DatabaseConfig,
    WarehouseConfig,
)


class ConfigurationManager:
    def __init__(self, config_filepath: str = "config/config.yaml"):
        self.config_filepath = Path(config_filepath)
        self.config = self._read_config()

    def _read_config(self) -> ConfigBox:
        with open(self.config_filepath, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)

        return ConfigBox(config)

    def get_csv_config(self) -> CSVConfig:
        return CSVConfig(
            source_file=self.config.csv.source_file,
            destination_dir=self.config.csv.destination_dir,
        )

    def get_api_config(self) -> APIConfig:
        return APIConfig(
            url=self.config.api.url,
            destination_dir=self.config.api.destination_dir,
            file_name=self.config.api.file_name,
        )

    def get_database_config(self) -> DatabaseConfig:
        return DatabaseConfig(
            db_url=self.config.database.db_url,
            table_name=self.config.database.table_name,
            destination_dir=self.config.database.destination_dir,
        )

    def get_warehouse_config(self) -> WarehouseConfig:
        return WarehouseConfig(
            db_url=self.config.warehouse.db_url,
        )