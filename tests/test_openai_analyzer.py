import pytest
from core.openai_analyzer import OpenAIAnalyzer

class MockOpenAIAnalyzer(OpenAIAnalyzer):
    """
    Mocked version of OpenAIAnalyzer for unit testing.
    Overrides _chat_complete to avoid real API calls.
    """
    def __init__(self, api_key="mock-key", model="gpt-4"):
        super().__init__(api_key=api_key, model=model)
    def _chat_complete(self, prompt_template, variables):
        formatted = prompt_template.template.format(**variables)
        if "sentiment" in formatted.lower():
            return "Positive"
        elif "classify" in formatted.lower():
            return "Feature Request"
        elif "summarize" in formatted.lower():
            return "Users want dark mode and faster load times."
        return "Unknown"


@pytest.fixture
def analyzer():
    return MockOpenAIAnalyzer(api_key="mock-key", model="gpt-4")


def test_analyze_sentiment(analyzer):
    result = analyzer.analyze_sentiment("I love the new UI!")
    assert result == "Positive"


def test_classify_category(analyzer):
    result = analyzer.classify_category("It would be great to have offline mode.")
    assert result == "Feature Request"


def test_summarize_feedback(analyzer):
    feedback = [
        "Add dark mode please.",
        "App feels slow.",
        "Can we have a dashboard view?"
    ]
    result = analyzer.summarize_feedback(feedback)
    assert "dark mode" in result.lower()

def test_model_required():
    with pytest.raises(ValueError):
        OpenAIAnalyzer(api_key="mock-key")

def test_missing_api_key(monkeypatch):
    # Unset the OPENAI_API_KEY environment variable if set
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(ValueError):
        OpenAIAnalyzer()
        
def test_chat_complete_runtime_error():
    class FailingAnalyzer(OpenAIAnalyzer):
        def __init__(self):
            super().__init__(api_key="fake-key", model="gpt-3.5-turbo")
        def _chat_complete(self, messages, temperature=0.0):
            raise RuntimeError("Simulated OpenAI failure.")

    analyzer = FailingAnalyzer()
    with pytest.raises(RuntimeError, match="Simulated OpenAI failure."):
        analyzer.analyze_sentiment("This is a test.")