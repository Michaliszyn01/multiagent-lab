from agents.base import BaseAgent


class Tester(BaseAgent):
    def __init__(self, llm):
        super().__init__(
            name="Tester",
            role="Analisa possiveis erros, testes manuais e casos de borda.",
            system_prompt=(
                "Voce e o Tester de um sistema multiagente local. "
                "Analise a proposta do Coder, aponte riscos de erro e sugira testes manuais. "
                "Nao execute codigo."
            ),
            llm=llm,
        )
