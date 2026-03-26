import requests
from app.ai.base import AIProvider

class OllamaProvider(AIProvider):

    def __init__(self, model="llama3"):
        self.model = model

    def summarize(self, text: str) -> str:
        res = requests.post("http://localhost:11434/api/generate", json={
            "model": self.model,
            "prompt": f"Summarize:\n{text}"
        })
        return res.json()["response"]

    def classify(self, text: str) -> str:
        res = requests.post("http://localhost:11434/api/generate", json={
            "model": self.model,
            "prompt": f"Classify:\n{text}"
        })
        return res.json()["response"]