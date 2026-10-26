from agents.base import BaseAgent


class Planner(BaseAgent):
    def __init__(self, llm):
        super().__init__(
            name="Planner",
            role="Quebra tarefas em passos pequenos e objetivos.",
            system_prompt=(
                "Voce e o Planner de um sistema multiagente local. "
                "Quebre a tarefa do usuario em passos claros, pequenos e executaveis. "
                "Nao escreva codigo completo; foque em planejamento."
            ),
            llm=llm,
        )
