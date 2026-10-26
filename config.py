from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent
WORKSPACE_DIR = BASE_DIR / "workspace"
LOGS_DIR = BASE_DIR / "logs"

SESSION_LOG_FILE = LOGS_DIR / "session_log.txt"

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:4b")

OPENAI_URL = os.getenv("OPENAI_URL", "https://api.openai.com/v1/responses")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.5")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Options: auto, fake, ollama, openai. In auto mode the app tries Ollama and
# falls back to FakeLLM if requests is unavailable or Ollama is offline.
DEFAULT_LLM_MODE = os.getenv("MULTIAGENT_LLM_MODE", "auto").strip().lower()
