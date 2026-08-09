import os
import json
import urllib.request
from typing import Dict, Any, Optional
from config import Config

class LLMProvider:
    """Unified LLM Provider abstraction supporting Google Gemini, NVIDIA NIM, OpenCode, OpenAI, Anthropic, and Ollama."""
    
    def __init__(self, provider_type: Optional[str] = None):
        self.provider_type = (provider_type or Config.DEFAULT_PROVIDER).lower()

    def generate(self, system_prompt: str, user_prompt: str, temperature: float = 0.2) -> str:
        """Generates a text completion based on prompt."""
        # 1. Check for local/mock response if no API key or placeholder API key is provided
        placeholder_keys = [
            "your_gemini_api_key_here", "your_openai_api_key_here", 
            "your_anthropic_api_key_here", "your_nvidia_api_key_here", 
            "your_opencode_api_key_here", ""
        ]
        
        if self.provider_type == "google" and Config.GEMINI_API_KEY in placeholder_keys:
            return self._mock_response(system_prompt, user_prompt)
        elif self.provider_type == "nvidia" and Config.NVIDIA_API_KEY in placeholder_keys:
            return self._mock_response(system_prompt, user_prompt)
        elif self.provider_type == "opencode" and Config.OPENCODE_API_KEY in placeholder_keys:
            return self._mock_response(system_prompt, user_prompt)
        elif self.provider_type == "openai" and Config.OPENAI_API_KEY in placeholder_keys:
            return self._mock_response(system_prompt, user_prompt)
        elif self.provider_type == "anthropic" and Config.ANTHROPIC_API_KEY in placeholder_keys:
            return self._mock_response(system_prompt, user_prompt)

        # 2. Real LLM execution routes
        try:
            if self.provider_type == "google":
                return self._call_google(system_prompt, user_prompt, temperature)
            elif self.provider_type == "nvidia":
                return self._call_nvidia(system_prompt, user_prompt, temperature)
            elif self.provider_type == "opencode":
                return self._call_opencode(system_prompt, user_prompt, temperature)
            elif self.provider_type == "openai":
                return self._call_openai(system_prompt, user_prompt, temperature)
            elif self.provider_type == "anthropic":
                return self._call_anthropic(system_prompt, user_prompt, temperature)
            elif self.provider_type == "ollama":
                return self._call_ollama(system_prompt, user_prompt, temperature)
            else:
                return self._mock_response(system_prompt, user_prompt)
        except Exception as e:
            return f"[Provider Error ({self.provider_type})]: {str(e)}\n\n(Fallback output generated for lab testing environment)"

    def _call_google(self, system_prompt: str, user_prompt: str, temperature: float) -> str:
        try:
            from google import genai
            client = genai.Client(api_key=Config.GEMINI_API_KEY)
            response = client.models.generate_content(
                model=Config.GEMINI_MODEL,
                contents=f"{system_prompt}\n\nUser Request: {user_prompt}",
                config={"temperature": temperature}
            )
            return response.text
        except ImportError:
            return self._mock_response(system_prompt, user_prompt)

    def _call_nvidia(self, system_prompt: str, user_prompt: str, temperature: float) -> str:
        url = f"{Config.NVIDIA_BASE_URL.rstrip('/')}/chat/completions"
        return self._call_openai_compatible(
            url=url,
            api_key=Config.NVIDIA_API_KEY,
            model=Config.NVIDIA_MODEL,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=temperature
        )

    def _call_opencode(self, system_prompt: str, user_prompt: str, temperature: float) -> str:
        url = f"{Config.OPENCODE_BASE_URL.rstrip('/')}/chat/completions"
        return self._call_openai_compatible(
            url=url,
            api_key=Config.OPENCODE_API_KEY,
            model=Config.OPENCODE_MODEL,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=temperature
        )

    def _call_openai(self, system_prompt: str, user_prompt: str, temperature: float) -> str:
        url = "https://api.openai.com/v1/chat/completions"
        return self._call_openai_compatible(
            url=url,
            api_key=Config.OPENAI_API_KEY,
            model=Config.OPENAI_MODEL,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=temperature
        )

    def _call_openai_compatible(
        self, url: str, api_key: str, model: str, system_prompt: str, user_prompt: str, temperature: float
    ) -> str:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": temperature
        }
        req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), headers=headers)
        with urllib.request.urlopen(req) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            return res["choices"][0]["message"]["content"]

    def _call_anthropic(self, system_prompt: str, user_prompt: str, temperature: float) -> str:
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": Config.ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        }
        data = {
            "model": Config.ANTHROPIC_MODEL,
            "system": system_prompt,
            "messages": [{"role": "user", "content": user_prompt}],
            "max_tokens": 1024,
            "temperature": temperature
        }
        req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), headers=headers)
        with urllib.request.urlopen(req) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            return res["content"][0]["text"]

    def _call_ollama(self, system_prompt: str, user_prompt: str, temperature: float) -> str:
        url = f"{Config.OLLAMA_BASE_URL.rstrip('/')}/chat/completions"
        headers = {"Content-Type": "application/json"}
        data = {
            "model": Config.OLLAMA_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": temperature
        }
        req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), headers=headers)
        with urllib.request.urlopen(req) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            return res["choices"][0]["message"]["content"]

    def _mock_response(self, system_prompt: str, user_prompt: str) -> str:
        """Deterministic mock response for verification when API keys are unconfigured."""
        return (
            f"[LAB MOCK RESPONSE - Provider: {self.provider_type.upper()}]\n"
            f"System Persona Active: {system_prompt.splitlines()[0] if system_prompt else 'Standard Security Agent'}\n"
            f"Task Processed Successfully: '{user_prompt[:80]}...'\n"
            "Status: System fully functional and ready for configured API key execution."
        )

def get_llm_provider(provider_type: Optional[str] = None) -> LLMProvider:
    return LLMProvider(provider_type=provider_type)
