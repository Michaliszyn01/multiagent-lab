from abc import ABC, abstractmethod


class BaseLLM(ABC):
    @abstractmethod
    def generate(self, system_prompt: str, user_message: str) -> str:
        """Generate a text response for an agent."""
