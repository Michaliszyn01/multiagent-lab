from agents.supervisor import Supervisor
from config import DEFAULT_LLM_MODE, LOGS_DIR, SESSION_LOG_FILE, WORKSPACE_DIR
from llm.fake_llm import FakeLLM
from llm.ollama_llm import OllamaLLM
from llm.openai_llm import OpenAILLM


def ensure_directories() -> None:
    WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)


def log_message(message: str) -> None:
    with SESSION_LOG_FILE.open("a", encoding="utf-8") as file:
        file.write(message.rstrip() + "\n")


def choose_llm(mode: str):
    mode = (mode or DEFAULT_LLM_MODE or "auto").strip().lower()

    if mode == "fake":
        print("[INFO] Usando FakeLLM.")
        return FakeLLM(), "fake"

    if mode in {"openai", "chatgpt", "api"}:
        openai = OpenAILLM()
        ok, reason = openai.healthcheck()

        if ok:
            print(f"[INFO] Usando OpenAI API com modelo '{openai.model}'.")
            return openai, "openai"

        print("[WARN] OpenAI API indisponivel. Caindo automaticamente para FakeLLM.")
        print(f"[INFO] Motivo: {reason}")
        if "requests" in reason.lower():
            print("[INFO] Para instalar requests: python -m pip install requests")
        if "openai_api_key" in reason.lower():
            print("[INFO] PowerShell: $env:OPENAI_API_KEY='sua-chave-aqui'")
        return FakeLLM(), "fake"

    if mode not in {"auto", "ollama"}:
        print(f"[WARN] Modo '{mode}' desconhecido. Usando modo auto.")
        mode = "auto"

    ollama = OllamaLLM()
    ok, reason = ollama.healthcheck()

    if ok:
        print(f"[INFO] Usando Ollama com modelo '{ollama.model}'.")
        return ollama, "ollama"

    if mode == "ollama":
        print("[WARN] Ollama indisponivel. Caindo automaticamente para FakeLLM.")
    else:
        print("[INFO] Ollama nao disponivel. Usando FakeLLM.")

    print(f"[INFO] Motivo: {reason}")
    if "requests" in reason.lower():
        print("[INFO] Para instalar requests: python -m pip install requests")

    return FakeLLM(), "fake"


def main() -> None:
    ensure_directories()

    print("=== Multiagent Lab ===")
    print("Modos disponiveis: auto, fake, ollama, openai")
    mode = input(f"Modo LLM [{DEFAULT_LLM_MODE}]: ").strip() or DEFAULT_LLM_MODE
    task = input("Digite a tarefa para os agentes: ").strip()

    if not task:
        print("[ERRO] Nenhuma tarefa informada. Encerrando.")
        return

    try:
        llm, active_mode = choose_llm(mode)
        supervisor = Supervisor(llm=llm, log_callback=log_message)

        log_message("\n" + "=" * 80)
        log_message(f"Nova sessao | modo={active_mode} | tarefa={task}")

        result = supervisor.run(task)

        print("\n=== Resultado Final ===")
        print(result)
        print(f"\n[INFO] Log salvo em: {SESSION_LOG_FILE}")
        print(f"[INFO] Artefatos salvos em: {WORKSPACE_DIR}")
    except KeyboardInterrupt:
        print("\n[INFO] Execucao interrompida pelo usuario.")
    except Exception as exc:
        print(f"[ERRO] Falha inesperada: {exc}")
        log_message(f"[ERRO] Falha inesperada: {exc}")


if __name__ == "__main__":
    main()
