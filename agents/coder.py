from agents.base import BaseAgent


class Coder(BaseAgent):
    def __init__(self, llm):
        super().__init__(
            name="Coder",
            role="Propoe arquivos e codigo sem executar nada.",
            system_prompt=(
                "Voce e o Coder de um sistema multiagente local. "
                "Proponha uma solucao simples, com nomes de arquivos e trechos de codigo quando util. "
                "Nao execute codigo e nao tente modificar arquivos fora do workspace."
            ),
            llm=llm,
        )
