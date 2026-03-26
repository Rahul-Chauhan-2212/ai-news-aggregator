import requests
from app.ai.base import AIProvider


class OllamaProvider(AIProvider):

    def __init__(self, url: str, model="llama3:8b"):
        self.model = model
        self.base_url = f"{url}/api/generate"

    def _call_ollama(self, prompt: str) -> str:
        try:
            res = requests.post(
                self.base_url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30
            )

            data = res.json()

            if "error" in data:
                raise Exception(data["error"])

            return data.get("response", "").strip()

        except Exception as e:
            print(f"Ollama error: {e}") 
            return None

    def summarize(self, text: str) -> str:
        return self._call_ollama(
            f"Summarize:\n{text}"
        )

    def classify(self, text: str) -> str:
        return self._call_ollama(
            f"Classify:\n{text}"
        )