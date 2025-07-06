import pandas as pd
import streamlit as st


def validate_csv(file) -> pd.DataFrame | None:
    try:
        df = pd.read_csv(file)
    except Exception as e:
        st.error(f"❌ Failed to read the uploaded file: {e}")
        return None

    # Convert all column names to lowercase for matching
    lower_cols = [col.lower() for col in df.columns]
    if "feedback" not in lower_cols:
        st.error("❌ The CSV file must contain a column named **'feedback'** (case-insensitive).")
        return None

    # Get the actual column name matching 'feedback'
    feedback_col = df.columns[lower_cols.index("feedback")]

    df = df.dropna(subset=[feedback_col])
    df[feedback_col] = df[feedback_col].astype(str).str.strip()

    if df[feedback_col].eq("").all():
        st.warning("⚠️ All 'feedback' entries are empty. Please upload a valid dataset.")
        return None

    # Optionally rename for consistency in downstream usage
    df = df.rename(columns={feedback_col: "feedback"})

    return df