import pandas as pd


class DataTransformer:

    @staticmethod
    def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
        return df.drop_duplicates()

    @staticmethod
    def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
        return df.fillna("unknown")

    @staticmethod
    def convert_column_types(
        df: pd.DataFrame,
        column_types: dict
    ) -> pd.DataFrame:

        for column, dtype in column_types.items():
            if column in df.columns:
                df[column] = df[column].astype(dtype)

        return df

    @staticmethod
    def transform(
        df: pd.DataFrame,
        column_types: dict | None = None
    ) -> pd.DataFrame:

        df = DataTransformer.remove_duplicates(df)

        df = DataTransformer.handle_missing_values(df)

        if column_types:
            df = DataTransformer.convert_column_types(
                df,
                column_types
            )

        return df