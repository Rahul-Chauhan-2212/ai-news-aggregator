from openai import OpenAI
from app.ai.base import AIProvider


class OpenAIProvider(AIProvider):

    def __init__(self, api_key: str, model="gpt-4o-mini"):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def summarize(self, text: str) -> str:
        res = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": f"Summarize:\n{text}"}],
        )
        return res.choices[0].message.content

    def classify(self, text: str) -> str:
        res = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": f"Classify:\n{text}"}],
        )
        return res.choices[0].message.content
