from dataclasses import dataclass


@dataclass
class CSVConfig:
    source_file: str
    destination_dir: str


@dataclass
class APIConfig:
    url: str
    destination_dir: str
    file_name: str


@dataclass
class DatabaseConfig:
    db_url: str
    table_name: str
    destination_dir: str


@dataclass
class WarehouseConfig:
    db_url: str