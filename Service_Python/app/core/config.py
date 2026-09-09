import os
from pydantic import BaseModel
from typing import Dict, Any

env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")

def load_env_file():
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ[k.strip()] = v.strip().strip('"').strip("'")

load_env_file()

class Settings(BaseModel):
    HOST: str = "127.0.0.1"
    PORT: int = 8765
    OLLAMA_HOST: str = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
    
    # API Keys de proveedores Cloud
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    
    DEFAULT_PROVIDER: str = "ollama"
    DEFAULT_MODEL: str = "qwen3:1.7b"
    SERVICE_VERSION: str = "1.2.0"

    def reload(self):
        load_env_file()
        self.OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
        self.OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
        self.GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
        self.ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

    def save_env(self, new_values: Dict[str, str]):
        current_env = {}
        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        current_env[k.strip()] = v.strip()
        
        for k, v in new_values.items():
            if v is not None:
                current_env[k] = v
                os.environ[k] = v

        lines = [
            "# ==============================================================================",
            "# CONFIGURACIÓN DE PROVEEDORES DE IA (VB6 AI Assistant)",
            "# ==============================================================================",
            "",
            "# 1. Ollama (100% Local y Gratuito sin API Key)",
            f"OLLAMA_HOST={current_env.get('OLLAMA_HOST', 'http://127.0.0.1:11434')}",
            "",
            "# 2. OpenRouter (Modelos gratuitos como openrouter/free, nemotron-3.5-lightning:free)",
            f"OPENROUTER_API_KEY={current_env.get('OPENROUTER_API_KEY', '')}",
            "",
            "# 3. Groq (Ultra-rápido, tier gratuito)",
            f"GROQ_API_KEY={current_env.get('GROQ_API_KEY', '')}",
            "",
            "# 4. Google Gemini (Google AI Studio)",
            f"GEMINI_API_KEY={current_env.get('GEMINI_API_KEY', '')}",
            "",
            "# 5. OpenAI (Opcional)",
            f"OPENAI_API_KEY={current_env.get('OPENAI_API_KEY', '')}",
            "",
            "# 6. Anthropic Claude (Opcional)",
            f"ANTHROPIC_API_KEY={current_env.get('ANTHROPIC_API_KEY', '')}",
            ""
        ]
        with open(env_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        
        self.reload()

settings = Settings()
