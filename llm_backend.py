# llm_backend.py
import os

import yaml

class LLM:
    def __init__(self, config_path="config.yml"):
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
        self.cfg = cfg
        self.provider = cfg["models"]["provider"]

    def chat(self, system_prompt: str, user_prompt: str, temperature: float = None) -> str:
        if self.provider == "openai_chat":
            return self._openai_chat(system_prompt, user_prompt, temperature)
        elif self.provider == "ollama":
            return self._ollama(system_prompt, user_prompt, temperature)
        elif self.provider == "google_genai":
            return self._google_genai(system_prompt, user_prompt, temperature)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    # -------- Google Generative AI (Gemini) --------
    def _google_genai(self, system_prompt, user_prompt, temperature=None):
        import google.generativeai as genai
        from google.generativeai import types

        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise RuntimeError("GOOGLE_API_KEY is not set in environment.")

        client = genai.Client(api_key=api_key)
        model = self.cfg["models"]["google"].get("model", "models/gemini-2.0-flash")
        temp = temperature or self.cfg["models"]["google"].get("temperature", 0.2)

        cfg = types.GenerateContentConfig(temperature=float(temp))

        merged_prompt = f"System instructions:\n{system_prompt}\n\nUser question:\n{user_prompt}"

        resp = client.models.generate_content(
            model=model,
            contents=[types.Part(text=merged_prompt)],
            config=cfg,
        )

        return (resp.text or "").strip()
