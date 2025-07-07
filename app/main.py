import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from core import OpenAIAnalyzer
from core.validator import validate_csv


def analyze_feedback_df(df, analyzer, column_name="feedback"):
    """
    Applies sentiment analysis, categorization, and summarization to the feedback DataFrame.
    Returns the updated DataFrame and the summary string.
    """
    df = df.copy()
    df["Sentiment"] = df[column_name].apply(analyzer.analyze_sentiment)
    df["Category"] = df[column_name].apply(analyzer.classify_category)
    summary = analyzer.summarize_feedback(df[column_name].tolist())
    return df, summary

# Set up page
st.set_page_config(page_title="Customer Feedback Analyzer", layout="wide")
st.title("🧠 AI-Powered Customer Feedback Analyzer")

# Upload file
uploaded_file = st.file_uploader("Upload a CSV file with a 'Feedback' column", type=["csv"])
column_name = "feedback"

if uploaded_file:
    df = validate_csv(uploaded_file)
    if df is not None:
        st.success(f"✅ Successfully loaded {len(df)} valid feedback entries.")
        st.write(df.head())

        if st.button("Analyze Feedback"):
            with st.spinner("Analyzing with OpenAI..."):
                analyzer = OpenAIAnalyzer()
                df, summary = analyze_feedback_df(df, analyzer, column_name)

            # Display summary
            st.subheader("📊 Summary of Common Feedback")
            st.write(summary)

            # Sentiment chart
            st.subheader("📈 Sentiment Distribution")
            st.bar_chart(df["Sentiment"].value_counts(), width=700, height=400, use_container_width=False)

            # Category chart
            st.subheader("📂 Category Breakdown")
            st.bar_chart(df["Category"].value_counts(), width=700, height=400, use_container_width=False)

            # Full table
            st.subheader("📋 Detailed Feedback Table")
            st.dataframe(df)