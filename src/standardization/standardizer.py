from pathlib import Path
import json
import pandas as pd


class DataStandardizer:

    @staticmethod
    def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
            .str.replace("-", "_")
            .str.replace(".", "_")
        )
        return df

    @staticmethod
    def standardize_file(input_file: str, output_file: str) -> None:
        input_path = Path(input_file)
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if input_path.suffix == ".json":
            with open(input_path, "r", encoding="utf-8") as file:
                data = json.load(file)
            df = pd.json_normalize(data)
        else:
            df = pd.read_csv(input_path)

        df = DataStandardizer.standardize_columns(df)
        df.to_csv(output_path, index=False)

        print(f"Standardized file saved: {output_path}")