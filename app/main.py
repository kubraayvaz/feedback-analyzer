import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from core import OpenAIAnalyzer
from core.validator import validate_csv
from core.models import MODEL_OPTIONS

def analyze_feedback_df(
    df: pd.DataFrame, 
    analyzer: OpenAIAnalyzer, 
    column_name: str = "feedback"
) -> tuple[pd.DataFrame, str]:
    """
    Applies sentiment analysis, categorization, and summarization to the feedback DataFrame.
    Returns the updated DataFrame and the summary string.
    """
    df = df.copy()
    df["Sentiment"] = df[column_name].apply(analyzer.analyze_sentiment)
    df["Category"] = df[column_name].apply(analyzer.classify_category)
    summary = analyzer.summarize_feedback(df[column_name].tolist())
    return df, summary

def render_dashboard(df: pd.DataFrame, summary: str) -> None:
    """
    Renders the Streamlit dashboard with summary, charts, and the feedback table.
    """
    st.subheader("📊 Summary of Common Feedback")
    st.write(summary)

    st.subheader("📈 Sentiment Distribution")
    st.bar_chart(df["Sentiment"].value_counts(), width=700, height=400, use_container_width=False)

    st.subheader("📂 Category Breakdown")
    st.bar_chart(df["Category"].value_counts(), width=700, height=400, use_container_width=False)

    st.subheader("📋 Detailed Feedback Table")
    st.dataframe(df)

def main() -> None:
    st.set_page_config(page_title="Customer Feedback Analyzer", layout="wide")
    st.title("🧠 AI-Powered Customer Feedback Analyzer")

    model_choice = st.selectbox("Select GPT Model", MODEL_OPTIONS, index=2)
    uploaded_file = st.file_uploader("Upload a CSV file with a 'Feedback' column", type=["csv"])
    column_name = "feedback"

    try:
        if uploaded_file:
            df = validate_csv(uploaded_file)
            if df is not None:
                st.success(f"✅ Successfully loaded {len(df)} valid feedback entries.")
                st.write(df.head())

                if st.button("Analyze Feedback"):
                    try:
                        with st.spinner("Analyzing with OpenAI..."):
                            analyzer = OpenAIAnalyzer(model=model_choice)
                            analyzed_df, summary = analyze_feedback_df(df, analyzer, column_name)
                        render_dashboard(analyzed_df, summary)
                    except Exception as analysis_error:
                        st.error(f"❌ An error occurred during feedback analysis: {analysis_error}")
    except Exception as e:
        st.error(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()