import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """
    Configuration settings loaded from environment or defaults.
    """
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")

    @classmethod
    def validate(cls):
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not set in environment or .env file")

Settings.validate()