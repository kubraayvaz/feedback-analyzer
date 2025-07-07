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
