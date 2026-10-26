from llm.base import BaseLLM


class BaseAgent:
    def __init__(self, name: str, role: str, system_prompt: str, llm: BaseLLM):
        self.name = name
        self.role = role
        self.system_prompt = system_prompt
        self.llm = llm

    def run(self, task: str) -> str:
        if not task.strip():
            raise ValueError(f"{self.name} recebeu uma tarefa vazia.")

        return self.llm.generate(
            system_prompt=self.system_prompt,
            user_message=task,
        )
