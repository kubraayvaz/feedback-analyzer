
import pytest
from core.prompts import CategoryPrompts, SentimentPrompts, SummaryPrompts


def test_prompt_formatting_with_missing_variable():
    with pytest.raises(KeyError):
        SentimentPrompts.ANALYZE.template.format()  # Missing 'feedback'

    with pytest.raises(KeyError):
        SummaryPrompts.SUMMARIZE.template.format()  # Missing 'joined_feedback'



def test_prompt_formatting_and_content():
    prompts = [
        (SentimentPrompts.ANALYZE, {"feedback": "Great product!"}, ["Great product!", "sentiment"]),
        (CategoryPrompts.CLASSIFY, {"feedback": "Please add export option."}, ["Please add export option.", "classify"]),
        (SummaryPrompts.SUMMARIZE, {"joined_feedback": "App is slow.\nNeeds offline mode."}, ["offline mode", "summarize"])
    ]

    for prompt, data, expected_substrings in prompts:
        rendered = prompt.template.format(**data)
        assert isinstance(rendered, str)
        for substring in expected_substrings:
            assert substring.lower() in rendered.lower()


def test_prompt_metadata():
    assert SentimentPrompts.ANALYZE.temperature == 0.0
    assert CategoryPrompts.CLASSIFY.temperature == 0.0
    assert SummaryPrompts.SUMMARIZE.temperature == 0.5