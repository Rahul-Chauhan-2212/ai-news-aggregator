from abc import ABC, abstractmethod

class AIProvider(ABC):

    @abstractmethod
    def summarize(self, text: str) -> str:
        pass

    @abstractmethod
    def classify(self, text: str) -> str:
        pass