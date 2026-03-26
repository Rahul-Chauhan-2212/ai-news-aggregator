import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

EMAIL = os.environ["EMAIL"]
EMAIL_APP_PASSWORD = os.environ["EMAIL_APP_PASSWORD"]

ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
OLLAMA_URL = os.environ["OLLAMA_URL"]
AI_PROVIDER = os.getenv("AI_PROVIDER", "openai").lower()
