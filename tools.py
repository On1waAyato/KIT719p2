# tools.py
import os, json, yaml
from google import genai
from google.genai import types

os.environ["GOOGLE_API_KEY"] = "AIzaSyDOLPZFapdO3hh2FFCasrbaYZqmWriUxWg"

class SalaryTool:
    """Call Google Generative AI to get real salary data"""

    def __init__(self, config_path="config.yml"):
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
        self.cfg = cfg["tools"]["salary_api"]
        self.google_cfg = self.cfg.get("google", {})
        self.region = self.cfg.get("default_region", "Australia")

    def lookup(self, title: str, region: str = None):
        region = region or self.region
        return self._lookup_google_genai(title, region)

    def _lookup_google_genai(self, title: str, region: str):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise RuntimeError("GOOGLE_API_KEY is not set in environment.")

        client = genai.Client(api_key=api_key)

        model = self.google_cfg.get("model", "models/gemini-2.0-flash")
        currency = self.google_cfg.get("currency", "AUD")

        prompt = f"""
    Return a JSON object with fields ONLY:
    - low: integer (annual, {currency})
    - mid: integer (annual, {currency})
    - high: integer (annual, {currency})

    Occupation: {title}
    Region: {region}

    Rules:
    - Output valid JSON ONLY (no code fences, no explanations).
    - Values must be integers.
    """

        cfg = types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "low": types.Schema(type=types.Type.NUMBER),
                    "mid": types.Schema(type=types.Type.NUMBER),
                    "high": types.Schema(type=types.Type.NUMBER),
                    "source_urls": types.Schema(
                        type=types.Type.ARRAY,
                        items=types.Schema(type=types.Type.STRING),
                    ),
                },
                required=["low", "mid", "high"],
            ),
        )

        resp = client.models.generate_content(
            model=model,
            contents=[types.Part(text=prompt)],
            config=cfg,
        )

        txt = (getattr(resp, "text", None) or "").strip()
        if not txt:
            for c in getattr(resp, "candidates", []) or []:
                parts = getattr(getattr(c, "content", None), "parts", []) or []
                for p in parts:
                    t = getattr(p, "text", None)
                    if t and t.strip():
                        txt = t.strip()
                        break
                if txt:
                    break

        if txt.startswith("```"):
            txt = txt.strip("`\n ")
            if txt.lower().startswith("json"):
                txt = txt[4:].lstrip() 

        data = None
        try:
            data = json.loads(txt)
        except Exception:
            nums = [int(n) for n in re.findall(r"\d{2,6}", txt)]
            if len(nums) >= 3:
                data = {"low": nums[0], "mid": nums[1], "high": nums[2]}
            else:
                raise RuntimeError(f"Tool returned non-JSON text: {txt[:200]}")

        out = {
            "title": title,
            "region": region,
            "source": "google-genai",
            "low": int(round(float(data["low"]))),
            "mid": int(round(float(data["mid"]))),
            "high": int(round(float(data["high"]))),
        }
        if isinstance(data.get("source_urls"), list):
            out["source_urls"] = data["source_urls"][:5]

        return out
