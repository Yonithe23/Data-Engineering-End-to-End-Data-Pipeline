from pathlib import Path
from datetime import datetime
import shutil


class CSVIngestion:
    def __init__(self, source_file: str, destination_dir: str):
        self.source_file = Path(source_file)
        self.destination_dir = Path(destination_dir)

    def ingest(self):
        if not self.source_file.exists():
            raise FileNotFoundError(f"File not found: {self.source_file}")

        self.destination_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        destination_file = self.destination_dir / f"{self.source_file.stem}_{timestamp}.csv"

        shutil.copy2(self.source_file, destination_file)

        print(f"CSV ingested successfully: {destination_file}")
        return destination_file