import io
import pandas as pd
from core import validator
class DummyStreamlit:
    def __init__(self):
        self.errors = []
        self.warnings = []
    def error(self, msg):
        self.errors.append(msg)
    def warning(self, msg):
        self.warnings.append(msg)

def test_valid_csv(monkeypatch):
    csv = io.StringIO("feedback\nGreat app!\nNeeds work\n")
    monkeypatch.setattr(validator, "st", DummyStreamlit())
    df = validator.validate_csv(csv)
    assert df is not None
    assert list(df.columns) == ["feedback"]
    assert len(df) == 2

def test_missing_feedback_column(monkeypatch):
    csv = io.StringIO("comment\nHello\nWorld\n")
    dummy_st = DummyStreamlit()
    monkeypatch.setattr(validator, "st", dummy_st)
    df = validator.validate_csv(csv)
    assert df is None
    assert any("feedback" in e.lower() for e in dummy_st.errors)

def test_all_feedback_empty(monkeypatch):
    csv = io.StringIO("feedback\n \n\t\n")
    dummy_st = DummyStreamlit()
    monkeypatch.setattr(validator, "st", dummy_st)
    df = validator.validate_csv(csv)
    assert df is None
    assert any("empty" in w.lower() for w in dummy_st.warnings)

def test_feedback_column_case_insensitive(monkeypatch):
    csv = io.StringIO("FeedBack\nA\nB\n")
    monkeypatch.setattr(validator, "st", DummyStreamlit())
    df = validator.validate_csv(csv)
    assert df is not None
    assert list(df.columns) == ["feedback"]
    assert set(df["feedback"]) == {"A", "B"}
