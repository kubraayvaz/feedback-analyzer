import io
import pandas as pd
from core.validator import validate_csv
from app.main import analyze_feedback_df

def test_analyze_feedback_df():
    class DummyAnalyzer:
        def analyze_sentiment(self, x): return "Positive"
        def classify_category(self, x): return "Feature Request"
        def summarize_feedback(self, x): return "Summary"
    df = pd.DataFrame({"feedback": ["Great!", "Needs work"]})
    result_df, summary = analyze_feedback_df(df, DummyAnalyzer())
    assert all(result_df["Sentiment"] == "Positive")
    assert all(result_df["Category"] == "Feature Request")
    assert summary == "Summary"

def test_validate_csv_integration():
    csv = io.StringIO("feedback\nA\nB\n")
    df = validate_csv(csv)
    assert df is not None
    assert list(df["feedback"]) == ["A", "B"]

def test_validate_csv_missing_column():
    csv = io.StringIO("comment\nGood\nBad\n")
    df = validate_csv(csv)
    assert df is None


def test_csv_export_format():
    class DummyAnalyzer:
        def analyze_sentiment(self, x): return "Neutral"
        def classify_category(self, x): return "Other"
        def summarize_feedback(self, x): return "Some summary"
    df = pd.DataFrame({"feedback": ["This is fine", "Could be better"]})
    result_df, _ = analyze_feedback_df(df, DummyAnalyzer())
    csv_data = result_df.to_csv(index=False)
    assert "Sentiment" in csv_data
    assert "Category" in csv_data
    assert "Neutral" in csv_data
    assert "Other" in csv_data
