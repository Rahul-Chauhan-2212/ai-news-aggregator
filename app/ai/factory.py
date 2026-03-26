import os

from app.ai.anthropic_provider import AnthropicProvider
from app.ai.ollama_provider import OllamaProvider
from app.ai.openai_provider import OpenAIProvider
from app.config.settings import ANTHROPIC_API_KEY, OLLAMA_URL, OPENAI_API_KEY


def get_ai_provider():

    provider = os.getenv("AI_PROVIDER", "openai").lower()
    
    print(f"Using AI provider: {provider}")

    if provider == "openai":
        return OpenAIProvider(OPENAI_API_KEY)

    elif provider == "anthropic":
        return AnthropicProvider(ANTHROPIC_API_KEY)

    elif provider == "ollama":
        return OllamaProvider(OLLAMA_URL)

    else:
        raise ValueError("Unsupported provider")
