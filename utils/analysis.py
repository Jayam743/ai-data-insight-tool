import pandas as pd
from typing import List, Tuple


# -----------------------------
# Layer 1: Data loading
# -----------------------------

def load_csv(uploaded_file) -> pd.DataFrame:
    """
    Load an uploaded CSV file into a pandas DataFrame.
    """
    return pd.read_csv(uploaded_file)


def detect_column_types(df: pd.DataFrame) -> Tuple[List[str], List[str]]:
    """
    Detect numeric and categorical columns.
    """
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    categorical_cols = df.select_dtypes(exclude=["number"]).columns.tolist()
    return numeric_cols, categorical_cols


# -----------------------------
# Layer 2: Statistics & quality
# -----------------------------

def compute_descriptive_stats(
    df: pd.DataFrame,
    numeric_cols: List[str]
) -> pd.DataFrame:
    """
    Compute descriptive statistics for numeric columns.
    """
    if not numeric_cols:
        return pd.DataFrame()
    return df[numeric_cols].describe().T


def missing_value_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return a summary of missing values per column.
    """
    missing = df.isnull().sum()
    missing = missing[missing > 0].reset_index()
    missing.columns = ["column", "missing_values"]
    return missing


# -----------------------------
# Layer 3: Aggregations
# -----------------------------

def revenue_by_category(
    df: pd.DataFrame,
    category_col: str,
    value_col: str
) -> pd.DataFrame:
    """
    Aggregate total values by category.
    """
    return (
        df.groupby(category_col)[value_col]
        .sum()
        .reset_index()
        .sort_values(by=value_col, ascending=False)
    )


# -----------------------------
# Layer 4: Business insights
# -----------------------------

def top_categories_by_metric(
    df: pd.DataFrame,
    category_col: str,
    metric_col: str,
    top_n: int = 5
) -> pd.DataFrame:
    """
    Return top N categories ranked by total metric value.
    """
    return (
        df.groupby(category_col)[metric_col]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )


def bottom_categories_by_metric(
    df: pd.DataFrame,
    category_col: str,
    metric_col: str,
    bottom_n: int = 5
) -> pd.DataFrame:
    """
    Return bottom N categories ranked by total metric value.
    """
    return (
        df.groupby(category_col)[metric_col]
        .sum()
        .sort_values(ascending=True)
        .head(bottom_n)
        .reset_index()
    )


def outlier_summary(
    df: pd.DataFrame,
    numeric_cols: List[str]
) -> pd.DataFrame:
    """
    Identify potential outliers using IQR method.
    """
    outlier_data = []

    for col in numeric_cols:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        count = ((df[col] < lower) | (df[col] > upper)).sum()

        outlier_data.append({
            "column": col,
            "outlier_count": count
        })

    return pd.DataFrame(outlier_data)
