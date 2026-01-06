import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def generate_summary(
    *,
    dataset_shape,
    numeric_cols,
    categorical_cols,
    descriptive_stats,
    missing_summary,
) -> str:
    """
    Generate a plain-English summary from computed results only.
    """

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "OPENAI_API_KEY is missing. Add it to a .env file and restart Streamlit."

    client = OpenAI(api_key=api_key)

    prompt = f"""
You are a data analyst. Write a clear, non-technical summary.

Dataset:
- Rows, Columns: {dataset_shape}
- Numeric columns: {numeric_cols}
- Categorical columns: {categorical_cols}

Descriptive stats (mean/min/max):
{descriptive_stats}

Missing values summary:
{missing_summary}

Rules:
- Only describe what is supported by the provided stats.
- Do NOT invent numbers.
- If something cannot be determined, say so.
- Keep it concise (5–8 bullet points).
"""

    resp = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
    )

    return resp.output_text.strip()
