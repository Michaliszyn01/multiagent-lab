from datetime import datetime

from agents.coder import Coder
from agents.planner import Planner
from agents.reviewer import Reviewer
from agents.tester import Tester
from tools.workspace import WorkspaceTool


class Supervisor:
    def __init__(self, llm, log_callback=None):
        self.name = "Supervisor"
        self.role = "Coordena agentes especializados e consolida resultados."
        self.llm = llm
        self.log_callback = log_callback or (lambda message: None)
        self.workspace = WorkspaceTool()
        self.planner = Planner(llm)
        self.coder = Coder(llm)
        self.tester = Tester(llm)
        self.reviewer = Reviewer(llm)

    def _log_section(self, title: str, content: str) -> None:
        self.log_callback(f"\n[{title}]\n{content}")

    def run(self, task: str) -> str:
        if not task.strip():
            raise ValueError("Supervisor recebeu uma tarefa vazia.")

        print("\n[Supervisor] Recebi a tarefa. Iniciando coordenacao...")

        print("[Planner] Quebrando a tarefa em passos...")
        plan = self.planner.run(task)
        self._log_section("Planner", plan)

        print("[Coder] Propondo arquivos e codigo...")
        coder_input = f"Tarefa original:\n{task}\n\nPlano:\n{plan}"
        code_proposal = self.coder.run(coder_input)
        self._log_section("Coder", code_proposal)

        print("[Tester] Avaliando erros e testes...")
        tester_input = (
            f"Tarefa original:\n{task}\n\nPlano:\n{plan}\n\nProposta do Coder:\n{code_proposal}"
        )
        test_report = self.tester.run(tester_input)
        self._log_section("Tester", test_report)

        print("[Reviewer] Revisando arquitetura e riscos...")
        reviewer_input = (
            f"Tarefa original:\n{task}\n\nPlano:\n{plan}\n\n"
            f"Proposta do Coder:\n{code_proposal}\n\nRelatorio do Tester:\n{test_report}"
        )
        review = self.reviewer.run(reviewer_input)
        self._log_section("Reviewer", review)

        artifact = self._build_artifact(task, plan, code_proposal, test_report, review)
        artifact_name = self.workspace.write_text("generated_proposal.md", artifact)

        final_summary = self._build_final_summary(
            task=task,
            plan=plan,
            artifact_name=artifact_name,
            test_report=test_report,
            review=review,
        )
        self._log_section("Supervisor", final_summary)
        return final_summary

    def _build_artifact(
        self,
        task: str,
        plan: str,
        code_proposal: str,
        test_report: str,
        review: str,
    ) -> str:
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return (
            f"# Generated Proposal\n\n"
            f"Created at: {created_at}\n\n"
            f"## Original Task\n\n{task}\n\n"
            f"## Planner\n\n{plan}\n\n"
            f"## Coder\n\n{code_proposal}\n\n"
            f"## Tester\n\n{test_report}\n\n"
            f"## Reviewer\n\n{review}\n"
        )

    def _build_final_summary(
        self,
        task: str,
        plan: str,
        artifact_name: str,
        test_report: str,
        review: str,
    ) -> str:
        return (
            "Tarefa processada pelo fluxo multiagente.\n\n"
            f"Tarefa: {task}\n\n"
            "Ordem executada:\n"
            "1. Supervisor recebeu a tarefa\n"
            "2. Planner quebrou a tarefa em passos\n"
            "3. Coder propos arquivos e codigo\n"
            "4. Tester analisou erros e testes\n"
            "5. Reviewer revisou arquitetura, qualidade e riscos\n\n"
            f"Artefato criado em workspace/{artifact_name}\n\n"
            "Resumo do plano:\n"
            f"{plan}\n\n"
            "Pontos de teste:\n"
            f"{test_report}\n\n"
            "Revisao:\n"
            f"{review}\n"
        )
