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

def revenue_by_category(df: pd.DataFrame, category_col: str, value_col: str) -> pd.DataFrame:
    """
    Aggregate revenue by a categorical column.
    Returns a DataFrame sorted by total revenue.
    """
    grouped = (
        df.groupby(category_col)[value_col]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )
    return grouped

def missing_value_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return a DataFrame summarizing missing values per column,
    including count and percentage.
    """
    missing_count = df.isna().sum()
    missing_percent = (missing_count / len(df) * 100).round(2)

    summary = pd.DataFrame(
        {
            "missing_count": missing_count,
            "missing_percent": missing_percent,
        }
    )

    summary = summary[summary["missing_count"] > 0]
    summary = summary.sort_values("missing_count", ascending=False)

    return summary
