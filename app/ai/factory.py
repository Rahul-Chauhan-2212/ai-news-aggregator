from app.ai.openai_provider import OpenAIProvider
from app.ai.anthropic_provider import AnthropicProvider
from app.ai.ollama_provider import OllamaProvider
from app.config.settings import *

def get_ai_provider():

    provider = "openai"  # load from env later

    if provider == "openai":
        return OpenAIProvider(OPENAI_API_KEY)

    elif provider == "anthropic":
        return AnthropicProvider(ANTHROPIC_API_KEY)

    elif provider == "ollama":
        return OllamaProvider()

    else:
        raise ValueError("Unsupported provider")