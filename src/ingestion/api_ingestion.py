from pathlib import Path
from datetime import datetime
import json

import requests


class APIIngestion:
    def __init__(self, url: str, destination_dir: str, file_name: str):
        self.url = url
        self.destination_dir = Path(destination_dir)
        self.file_name = file_name

    def ingest(self):
        self.destination_dir.mkdir(parents=True, exist_ok=True)

        response = requests.get(self.url, timeout=30)
        response.raise_for_status()

        data = response.json()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.destination_dir / f"{self.file_name}_{timestamp}.json"

        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        print(f"API data ingested successfully: {output_file}")
        return output_file