import json

from config import OLLAMA_MODEL, OLLAMA_URL
from llm.base import BaseLLM


class OllamaLLM(BaseLLM):
    def __init__(self, model: str = OLLAMA_MODEL, url: str = OLLAMA_URL, timeout: int = 45):
        self.model = model
        self.url = url
        self.timeout = timeout

    def _import_requests(self):
        try:
            import requests

            return requests, None
        except ImportError:
            return None, (
                "Biblioteca requests nao encontrada. "
                "Instale com: python -m pip install requests"
            )

    def healthcheck(self):
        requests, error = self._import_requests()
        if error:
            return False, error

        payload = {
            "model": self.model,
            "prompt": "Responda apenas OK.",
            "stream": False,
            "options": {"num_predict": 4},
        }

        try:
            response = requests.post(self.url, json=payload, timeout=8)
            response.raise_for_status()
            return True, "Ollama disponivel."
        except Exception as exc:
            return False, f"Ollama nao respondeu em {self.url}: {exc}"

    def generate(self, system_prompt: str, user_message: str) -> str:
        requests, error = self._import_requests()
        if error:
            raise RuntimeError(error)

        prompt = (
            f"SYSTEM:\n{system_prompt}\n\n"
            f"USER:\n{user_message}\n\n"
            "Responda em portugues do Brasil, com objetividade e clareza."
        )

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }

        try:
            response = requests.post(self.url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "").strip() or "[WARN] Ollama retornou resposta vazia."
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"Resposta invalida do Ollama: {exc}") from exc
        except Exception as exc:
            raise RuntimeError(f"Falha ao chamar Ollama: {exc}") from exc
