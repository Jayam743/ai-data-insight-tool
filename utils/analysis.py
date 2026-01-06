import pandas as pd


def load_csv(file) -> pd.DataFrame:
    """
    Read an uploaded CSV file (Streamlit uploader object) into a DataFrame.
    """
    return pd.read_csv(file)


def detect_column_types(df: pd.DataFrame) -> tuple[list[str], list[str]]:
    """
    Return (numeric_cols, categorical_cols) based on pandas dtypes.
    """
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    categorical_cols = df.select_dtypes(exclude="number").columns.tolist()
    return numeric_cols, categorical_cols

def compute_descriptive_stats(df: pd.DataFrame, numeric_cols: list[str]) -> pd.DataFrame:
    """
    Compute basic descriptive statistics for numeric columns.
    Returns a DataFrame with mean, min, and max.
    """
    stats = df[numeric_cols].agg(["mean", "min", "max"])
    return stats
