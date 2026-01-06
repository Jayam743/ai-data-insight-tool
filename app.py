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

    # =========================
    # LAYER 2: VISUALIZATIONS
    # =========================
    st.subheader("Distribution (Histogram)")

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

    st.subheader("Outlier Detection (Box Plot)")

    if len(numeric_cols) == 0:
        st.info("No numeric columns found.")
    else:
        box_col = st.selectbox(
            "Choose a numeric column for box plot",
            numeric_cols,
            key="box_col"
        )

        fig, ax = plt.subplots()
        ax.boxplot(df[box_col].dropna(), vert=False)
        ax.set_xlabel(box_col)
        ax.set_title(f"Box Plot of {box_col}")
        st.pyplot(fig)

    st.subheader("Relationship Between Numeric Columns (Scatter Plot)")

    if len(numeric_cols) < 2:
        st.info("Need at least two numeric columns.")
    else:
        x_col = st.selectbox("X-axis", numeric_cols, key="scatter_x")
        y_col = st.selectbox("Y-axis", numeric_cols, key="scatter_y")

        fig, ax = plt.subplots()
        ax.scatter(df[x_col], df[y_col])
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.set_title(f"{y_col} vs {x_col}")
        st.pyplot(fig)

    st.subheader("Correlation Heatmap")

    if len(numeric_cols) < 2:
        st.info("Need at least two numeric columns for correlation.")
    else:
        corr = df[numeric_cols].corr()

        fig, ax = plt.subplots()
        sns.heatmap(
            corr,
            annot=True,
            cmap="coolwarm",
            ax=ax
        )
        ax.set_title("Correlation Between Numeric Features")
        st.pyplot(fig)

    # -------------------------
    # AI SUMMARY (later)
    # -------------------------
    # st.subheader("AI Summary")
    # if st.button("Generate AI Summary"):
    #     with st.spinner("Generating summary..."):
    #         dataset_shape = (df.shape[0], df.shape[1])
    #         summary_text = generate_summary(
    #             dataset_shape=dataset_shape,
    #             numeric_cols=numeric_cols,
    #             categorical_cols=categorical_cols,
    #             descriptive_stats=stats_df.to_string() if len(numeric_cols) else "",
    #             missing_summary=missing_df.to_string() if not missing_df.empty else "",
    #         )
    #     st.write(summary_text)
