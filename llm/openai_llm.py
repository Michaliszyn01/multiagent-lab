from config import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_URL
from llm.base import BaseLLM


class OpenAILLM(BaseLLM):
    def __init__(
        self,
        model: str = OPENAI_MODEL,
        url: str = OPENAI_URL,
        api_key: str = OPENAI_API_KEY,
        timeout: int = 60,
    ):
        self.model = model
        self.url = url
        self.api_key = api_key
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
        _, error = self._import_requests()
        if error:
            return False, error

        if not self.api_key:
            return False, (
                "OPENAI_API_KEY nao configurada. "
                "Defina a variavel de ambiente antes de usar o modo OpenAI."
            )

        return True, "OpenAI configurada."

    def generate(self, system_prompt: str, user_message: str) -> str:
        requests, error = self._import_requests()
        if error:
            raise RuntimeError(error)

        if not self.api_key:
            raise RuntimeError(
                "OPENAI_API_KEY nao configurada. "
                "Defina a variavel de ambiente antes de usar o modo OpenAI."
            )

        payload = {
            "model": self.model,
            "instructions": system_prompt,
            "input": user_message,
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        try:
            response = requests.post(
                self.url,
                json=payload,
                headers=headers,
                timeout=self.timeout,
            )
            response.raise_for_status()
            data = response.json()
            return self._extract_text(data)
        except Exception as exc:
            raise RuntimeError(f"Falha ao chamar OpenAI API: {exc}") from exc

    def _extract_text(self, data: dict) -> str:
        output_text = data.get("output_text")
        if output_text:
            return output_text.strip()

        chunks = []
        for item in data.get("output", []):
            for content in item.get("content", []):
                text = content.get("text")
                if text:
                    chunks.append(text)

        text = "\n".join(chunks).strip()
        return text or "[WARN] OpenAI API retornou resposta vazia."
