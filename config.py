import os
from pathlib import Path
from dotenv import load_dotenv

# Base Directory
BASE_DIR = Path(__file__).resolve().parent

# Load .env file
env_path = BASE_DIR / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv(dotenv_path=BASE_DIR / ".env.example")

class Config:
    DEFAULT_PROVIDER = os.getenv("DEFAULT_LLM_PROVIDER", "google").lower()

    # Gemini Settings
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    # OpenAI Settings
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    # Anthropic Settings
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")

    # Ollama / Local Settings
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

    # Lab Server Config
    LAB_HTTP_HOST = os.getenv("LAB_HTTP_HOST", "0.0.0.0")
    LAB_HTTP_PORT = int(os.getenv("LAB_HTTP_PORT", 8080))
    LAB_FTP_HOST = os.getenv("LAB_FTP_HOST", "0.0.0.0")
    LAB_FTP_PORT = int(os.getenv("LAB_FTP_PORT", 2121))
    LAB_FTP_USER = os.getenv("LAB_FTP_USER", "labuser")
    LAB_FTP_PASS = os.getenv("LAB_FTP_PASS", "labpass123")
