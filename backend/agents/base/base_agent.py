from abc import ABC, abstractmethod

class BaseAgent(ABC):
    name: str
    role: str

    @abstractmethod
    def run(self, context: dict) -> dict:
        pass
