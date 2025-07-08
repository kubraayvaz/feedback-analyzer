from openai import OpenAI
from typing import List, Optional
from openai.types.chat import ChatCompletionMessageParam
import os

from config import Settings


class OpenAIAnalyzer:
    """
    Handles sentiment analysis, categorization, and summarization using OpenAI's GPT model.
    """

    def __init__(self, api_key: Optional[str] = None, model: str = None):
        if not model:
            raise ValueError("You must specify a GPT model name.")
        self.model = model
        # Prefer runtime environment variable, fallback to config
        self._api_key = api_key or os.environ.get("OPENAI_API_KEY") or Settings.OPENAI_API_KEY
        if not self._api_key:
            raise ValueError("OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable or .env file.")
        self.client = OpenAI(api_key=self._api_key)

    def _chat_complete(self, messages: List[ChatCompletionMessageParam], temperature: float = 0.0) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature
        )
        return response.choices[0].message.content.strip()

    def analyze_sentiment(self, feedback: str) -> str:
        prompt = f"What is the sentiment of this feedback: \"{feedback}\"? Reply with Positive, Neutral, or Negative."
        return self._chat_complete([{"role": "user", "content": prompt}])

    def classify_category(self, feedback: str) -> str:
        prompt = (
            "Classify this feedback into one of the following categories:\n"
            "- Bug\n- Feature Request\n- UX Issue\n- Other\n\n"
            f"Feedback: \"{feedback}\"\n\n"
            "Reply with only one category name."
        )
        return self._chat_complete([{"role": "user", "content": prompt}])

    def summarize_feedback(self, feedback_list: List[str]) -> str:
        joined_feedback = "\n".join(feedback_list[:20])
        prompt = (
            "Summarize the main recurring issues in the following customer feedback:\n"
            f"{joined_feedback}"
        )
        return self._chat_complete([{"role": "user", "content": prompt}], temperature=0.5)