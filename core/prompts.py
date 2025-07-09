from dataclasses import dataclass
from typing import Optional

@dataclass
class PromptTemplate:
    template: str
    temperature: float = 0.0
    max_tokens: Optional[int] = None

class SentimentPrompts:
    ANALYZE = PromptTemplate(
        template='What is the sentiment of this feedback: "{feedback}"? Reply with Positive, Neutral, or Negative.'
    )

class CategoryPrompts:
    CLASSIFY = PromptTemplate(
        template=(
            "Classify this feedback into one of the following categories:\n"
            "- Bug\n- Feature Request\n- UX Issue\n- Other\n\n"
            'Feedback: "{feedback}"\n\n'
            "Reply with only one category name."
        )
    )

class SummaryPrompts:
    SUMMARIZE = PromptTemplate(
        template=(
            "Summarize the main recurring issues in the following customer feedback:\n"
            "{joined_feedback}"
        ),
        temperature=0.5
    )