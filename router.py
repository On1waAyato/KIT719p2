import yaml
from llm_backend import LLM
from prompts import ROUTER_PROMPT

class Router:
    def __init__(self, config_path="config.yml"):
        with open(config_path, "r") as f:
            self.cfg = yaml.safe_load(f)
        self.mode = self.cfg["router"]["mode"]
        self.llm = LLM(config_path)

    def route(self, question: str) -> str:
        """Simple heuristic router without LLM fallback or double check."""
        q = (question or "").lower()

        salary_kw = (
            "salary", "salaries", "pay", "wage", "compensation",
            "remuneration", "income", "per year", "per annum", "aud",
            "average salary", "median salary", "range"
        )
        skill_kw = (
            "skill", "skills", "competenc", "qualification", "certif",
            "duty", "duties", "responsib", "responsibility",
            "task", "tasks", "requirements", "what do they do",
            "what should i learn"
        )

        has_salary = any(k in q for k in salary_kw)
        has_skill = any(k in q for k in skill_kw)

        # --- routing logic ---
        if has_salary and has_skill:
            return "BOTH"
        elif has_salary:
            return "TOOL"
        elif has_skill:
            return "RAG"
        else:
            return "RAG"