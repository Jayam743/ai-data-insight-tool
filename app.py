import streamlit as st

# Page title
st.title("AI-Powered Data Insight Tool")

# Short description
st.write(
    "Upload a CSV file and get automatic statistics, visualizations, "
    "and plain-English insights."
)

# File uploader
uploaded_file = st.file_uploader(
    "Upload your CSV file",
    type=["csv"]
)

if uploaded_file is not None:
    import pandas as pd

    # Read CSV into DataFrame
    df = pd.read_csv(uploaded_file)

    st.success("File uploaded and read successfully!")

    # Show first 5 rows
    st.subheader("Preview of the data")
    st.dataframe(df.head())
