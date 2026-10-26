from pathlib import Path

from config import WORKSPACE_DIR


class WorkspaceTool:
    """Safe file helper restricted to the local workspace directory."""

    def __init__(self, root: Path = WORKSPACE_DIR):
        self.root = root.resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def _safe_path(self, relative_path: str) -> Path:
        if not relative_path or not relative_path.strip():
            raise ValueError("Caminho vazio nao e permitido.")

        candidate = (self.root / relative_path).resolve()

        if candidate == self.root:
            raise ValueError("Informe um arquivo dentro do workspace.")

        if self.root not in candidate.parents:
            raise ValueError(f"Acesso bloqueado fora do workspace: {relative_path}")

        return candidate

    def write_text(self, relative_path: str, content: str) -> str:
        path = self._safe_path(relative_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return str(path.relative_to(self.root))

    def read_text(self, relative_path: str) -> str:
        path = self._safe_path(relative_path)
        if not path.exists():
            raise FileNotFoundError(f"Arquivo nao encontrado no workspace: {relative_path}")
        if not path.is_file():
            raise ValueError(f"O caminho nao e um arquivo: {relative_path}")
        return path.read_text(encoding="utf-8")
