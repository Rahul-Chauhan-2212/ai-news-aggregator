import anthropic
from app.ai.base import AIProvider

class AnthropicProvider(AIProvider):

    def __init__(self, api_key: str, model="claude-3-haiku-20240307"):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    def summarize(self, text: str) -> str:
        res = self.client.messages.create(
            model=self.model,
            max_tokens=200,
            messages=[{"role": "user", "content": f"Summarize:\n{text}"}]
        )
        return res.content[0].text

    def classify(self, text: str) -> str:
        res = self.client.messages.create(
            model=self.model,
            max_tokens=100,
            messages=[{"role": "user", "content": f"Classify:\n{text}"}]
        )
        return res.content[0].text