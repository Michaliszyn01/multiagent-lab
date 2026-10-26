from agents.base import BaseAgent


class Reviewer(BaseAgent):
    def __init__(self, llm):
        super().__init__(
            name="Reviewer",
            role="Revisa qualidade, arquitetura, seguranca e riscos.",
            system_prompt=(
                "Voce e o Reviewer de um sistema multiagente local. "
                "Revise a arquitetura, clareza, seguranca e manutencao da solucao. "
                "Seja objetivo e destaque riscos relevantes."
            ),
            llm=llm,
        )
