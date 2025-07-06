import pytest
from core.openai_analyzer import OpenAIAnalyzer

class MockOpenAIAnalyzer(OpenAIAnalyzer):
    """
    Mocked version of OpenAIAnalyzer for unit testing.
    Overrides _chat_complete to avoid real API calls.
    """
    def _chat_complete(self, messages, temperature=0.0):
        prompt = messages[0]["content"]
        if "sentiment" in prompt.lower():
            return "Positive"
        elif "classify" in prompt.lower():
            return "Feature Request"
        elif "summarize" in prompt.lower():
            return "Users want dark mode and faster load times."
        return "Unknown"


@pytest.fixture
def analyzer():
    return MockOpenAIAnalyzer(api_key="mock-key")


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