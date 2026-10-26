from llm.base import BaseLLM


class FakeLLM(BaseLLM):
    """Deterministic LLM substitute for testing the multiagent flow."""

    def generate(self, system_prompt: str, user_message: str) -> str:
        prompt = system_prompt.lower()

        if "reviewer" in prompt:
            return self._reviewer_response(user_message)
        if "tester" in prompt:
            return self._tester_response(user_message)
        if "planner" in prompt:
            return self._planner_response(user_message)
        if "coder" in prompt:
            return self._coder_response(user_message)

        return "FakeLLM recebeu a tarefa e retornou uma resposta generica."

    def _planner_response(self, task: str) -> str:
        return (
            "1. Entender a tarefa e definir o escopo minimo.\n"
            "2. Separar dados, regras de negocio e interface de terminal.\n"
            "3. Criar uma primeira versao simples, sem dependencias externas.\n"
            "4. Validar entradas do usuario e mensagens de erro.\n"
            "5. Revisar riscos antes de evoluir para persistencia real."
        )

    def _coder_response(self, task: str) -> str:
        return (
            "Proposta de implementacao:\n"
            "- Criar `app.py` com o loop principal de terminal.\n"
            "- Criar funcoes pequenas para cadastrar, listar e buscar registros.\n"
            "- Manter dados em memoria no primeiro ciclo.\n"
            "- Adicionar mensagens claras para entradas invalidas.\n\n"
            "Exemplo de esqueleto:\n"
            "```python\n"
            "def main():\n"
            "    print('Aplicacao simples no terminal')\n"
            "    # implementar menu aqui\n\n"
            "if __name__ == '__main__':\n"
            "    main()\n"
            "```"
        )

    def _tester_response(self, task: str) -> str:
        return (
            "Testes sugeridos:\n"
            "- Rodar o programa e escolher cada opcao do menu.\n"
            "- Informar entradas vazias e valores inesperados.\n"
            "- Verificar se a listagem funciona antes e depois de cadastrar itens.\n"
            "- Confirmar que o programa encerra sem stack trace.\n\n"
            "Possiveis erros:\n"
            "- Falta de validacao de input.\n"
            "- Estados em memoria perdidos ao reiniciar, esperado nesta versao."
        )

    def _reviewer_response(self, task: str) -> str:
        return (
            "Revisao:\n"
            "- A arquitetura esta adequada para um prototipo didatico.\n"
            "- Separar funcoes por responsabilidade facilita evolucao.\n"
            "- Evitar persistencia e execucao automatica reduz risco inicial.\n"
            "- Proximo passo natural: testes unitarios e persistencia em arquivo seguro."
        )
