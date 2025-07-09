from openai import OpenAI
from typing import List, Optional
from openai.types.chat import ChatCompletionMessageParam
import os

from config import Settings
from core.prompts import SentimentPrompts, CategoryPrompts, SummaryPrompts, PromptTemplate


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

    def _chat_complete(self, prompt_template: PromptTemplate, variables: dict) -> str:
        try:
            formatted_prompt = prompt_template.template.format(**variables)
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": formatted_prompt}],
                temperature=prompt_template.temperature,
                max_tokens=prompt_template.max_tokens
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise RuntimeError(f"❌ OpenAI API call failed: {e}")

    def analyze_sentiment(self, feedback: str) -> str:
        return self._chat_complete(SentimentPrompts.ANALYZE, {"feedback": feedback})

    def classify_category(self, feedback: str) -> str:
        return self._chat_complete(CategoryPrompts.CLASSIFY, {"feedback": feedback})

    def summarize_feedback(self, feedback_list: List[str]) -> str:
        joined_feedback = "\n".join(feedback_list[:20])
        return self._chat_complete(SummaryPrompts.SUMMARIZE, {"joined_feedback": joined_feedback})