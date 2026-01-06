import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from utils.analysis import (
    load_csv,
    detect_column_types,
    compute_descriptive_stats,
    missing_value_summary,
    revenue_by_category,
    top_categories_by_metric,
    bottom_categories_by_metric,
    outlier_summary,
)

# NOTE: We are not using AI right now (quota/billing). Keep this import commented until the end.
# from utils.llm_summary import generate_summary


# Page title
st.title("AI-Powered Data Insight Tool")

# Short description
st.write(
    "Upload a CSV file and get automatic statistics, visualizations, "
    "and plain-English insights."
)

# File uploader
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Read CSV into DataFrame
    df = load_csv(uploaded_file)

    st.success("File uploaded and read successfully!")

    # Show first 5 rows
    st.subheader("Preview of the data")
    st.dataframe(df.head())

    # Detect column types
    numeric_cols, categorical_cols = detect_column_types(df)

    st.subheader("Detected column types")
    st.write("Numeric columns:", numeric_cols)
    st.write("Categorical columns:", categorical_cols)

    # Descriptive stats
    st.subheader("Descriptive statistics")
    if len(numeric_cols) == 0:
        st.info("No numeric columns found, so descriptive statistics cannot be computed.")
    else:
        stats_df = compute_descriptive_stats(df, numeric_cols)
        st.dataframe(stats_df)

    # Missing values
    st.subheader("Missing values summary")
    missing_df = missing_value_summary(df)
    if missing_df.empty:
        st.success("No missing values found 🎉")
    else:
        st.dataframe(missing_df)

    st.subheader("Visualizations")

    chart_type = st.selectbox(
        "Choose a chart to view",
        [
            "Histogram",
            "Box Plot",
            "Scatter Plot",
            "Correlation Heatmap",
        ],
        key="chart_type",
    )

    # 1) Histogram
    if chart_type == "Histogram":
        if len(numeric_cols) == 0:
            st.info("No numeric columns found to plot a histogram.")
        else:
            col = st.selectbox("Choose a numeric column", numeric_cols, key="hist_col")
            fig, ax = plt.subplots()
            ax.hist(df[col].dropna(), bins=20)
            ax.set_xlabel(col)
            ax.set_ylabel("Count")
            ax.set_title(f"Distribution of {col}")
            st.pyplot(fig)

    # 2) Box Plot
    elif chart_type == "Box Plot":
        if len(numeric_cols) == 0:
            st.info("No numeric columns found to plot a box plot.")
        else:
            col = st.selectbox("Choose a numeric column", numeric_cols, key="box_col")
            fig, ax = plt.subplots()
            ax.boxplot(df[col].dropna(), vert=False)
            ax.set_xlabel(col)
            ax.set_title(f"Box Plot of {col}")
            st.pyplot(fig)

    # 3) Scatter Plot
    elif chart_type == "Scatter Plot":
        if len(numeric_cols) < 2:
            st.info("Need at least two numeric columns for a scatter plot.")
        else:
            x_col = st.selectbox("X-axis", numeric_cols, key="scatter_x")
            y_col = st.selectbox("Y-axis", numeric_cols, key="scatter_y")
            fig, ax = plt.subplots()
            ax.scatter(df[x_col], df[y_col])
            ax.set_xlabel(x_col)
            ax.set_ylabel(y_col)
            ax.set_title(f"{y_col} vs {x_col}")
            st.pyplot(fig)

    # 4) Correlation Heatmap
    elif chart_type == "Correlation Heatmap":
        if len(numeric_cols) < 2:
            st.info("Need at least two numeric columns for correlation heatmap.")
        else:
            corr = df[numeric_cols].corr()
            fig, ax = plt.subplots()
            sns.heatmap(corr, annot=True, ax=ax)
            ax.set_title("Correlation Heatmap")
            st.pyplot(fig)

    st.subheader("Insights")

    insight_type = st.selectbox(
        "Choose an insight",
        [
            "Missing Values",
            "Top Categories (by metric)",
            "Bottom Categories (by metric)",
            "Outlier Summary",
        ],
        key="insight_type",
    )

    # Missing Values
    if insight_type == "Missing Values":
        if missing_df.empty:
            st.success("No missing values found 🎉")
        else:
            st.dataframe(missing_df)

    # Top Categories
    elif insight_type == "Top Categories (by metric)":
        if len(categorical_cols) == 0 or len(numeric_cols) == 0:
            st.info("Need at least one categorical and one numeric column.")
        else:
            cat = st.selectbox("Category column", categorical_cols, key="top_cat")
            metric = st.selectbox("Metric column", numeric_cols, key="top_metric")
            n = st.slider("How many?", min_value=3, max_value=15, value=5, key="top_n")
            top_df = top_categories_by_metric(df, cat, metric, top_n=n)
            st.dataframe(top_df)

    # Bottom Categories
    elif insight_type == "Bottom Categories (by metric)":
        if len(categorical_cols) == 0 or len(numeric_cols) == 0:
            st.info("Need at least one categorical and one numeric column.")
        else:
            cat = st.selectbox("Category column", categorical_cols, key="bottom_cat")
            metric = st.selectbox("Metric column", numeric_cols, key="bottom_metric")
            n = st.slider("How many?", min_value=3, max_value=15, value=5, key="bottom_n")
            bottom_df = bottom_categories_by_metric(df, cat, metric, bottom_n=n)
            st.dataframe(bottom_df)

    # Outlier Summary
    elif insight_type == "Outlier Summary":
        if len(numeric_cols) == 0:
            st.info("No numeric columns available for outlier detection.")
        else:
            out_df = outlier_summary(df, numeric_cols)
            st.dataframe(out_df)
