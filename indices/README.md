# Career Assistant (RAG + Tool Calling)

A minimal, rubric-aligned implementation for KIT719 **Option A: Career Assistant**.
- RAG over OSCA (Occupation Standard Classification Australia) PDF(s)
- Tool calling for salary lookup (mock by default; pluggable real API)
- Prompt-driven router (LLM or heuristic fallback)
- Gradio local UI

## 0) Project Fit (KIT719)
- Uses RAG + Tool + Routing; cites sources; tool results shown clearly. fileciteturn1file0L57-L71
- UI is Gradio and runs locally. fileciteturn1file0L81-L93
- Provide ground truth & evaluation; include baseline and difficult Qs. fileciteturn1file4L1-L23
- Include `prompts.py` and `config.yml`. fileciteturn1file4L127-L143

## 1) Setup
```bash
python -m venv .venv && source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
```

### (Optional) Choose your model provider
- **Ollama (default)**: install and run `ollama serve`, then `ollama pull llama3.1`
- **OpenAI**: set `models.provider: openai_chat` in `config.yml` and export `OPENAI_API_KEY`.

## 2) Get documents (OSCA)
Download a subset (≈20 pages) of OSCA from ABS: print to PDF and save into `./data/`.
Example link in spec. fileciteturn1file2L15-L22

## 3) Build the index
```bash
python ingest.py
```

This creates FAISS index under `./indices`.

## 4) Run the app
```bash
python app.py
# open http://127.0.0.1:7861
```

## 5) Tool calling (salary)
- Default is **mock mode** (no key needed), returning plausible AU ranges
- To use a real API, set in `config.yml`:
  ```yaml
  tools:
    salary_api:
      enabled: true
      base_url: "https://your-salary-api.example.com"
      api_key_env: "SALARY_API_KEY"
  ```
  and export your key: `export SALARY_API_KEY=...`

## 6) Evaluation (Ground Truth)
Create a small `eval/` folder with a CSV or Markdown like:
```markdown
# Baseline
- Q: What tasks should I expect in project management?
  Gold citations: <OSCA pdf #chunks>
  Gold answer: ...
- Q: If I want to be a software engineer, which skills should I start building?
  Gold citations: ...
  Gold answer: ...
- Q: What's the average salary for a software engineer in Australia?
  Tool call: salary(tool) with title=software engineer, region=Australia
  Gold result: range ...
# Difficult
- Q: ...
```
See the rubric for details. fileciteturn1file4L27-L49

## 7) Files
- `app.py`: Gradio UI + orchestration
- `ingest.py`: load PDFs from `./data/`, chunk & build FAISS
- `rag.py`: embed+retrieve
- `router.py`: LLM router (or heuristic fallback)
- `llm_backend.py`: talk to OpenAI or Ollama
- `tools.py`: salary lookup (mock / real)
- `prompts.py`: system/answer/router prompts
- `config.yml`: knobs for model, RAG, tools
- `requirements.txt`

## 8) Notes & Tips
- Keep your PDF subset focused on occupations you’ll demo (e.g., Software Engineer, PM).
- Tune `chunk_size`, `overlap`, and `top_k` in `config.yml`.
- In the demo, show BOTH types of questions to satisfy the assignment.

## 9) Limitations (be transparent in report)
- PDF extraction can be noisy; consider cleaning text.
- Router in heuristic mode may mis-route; switch to LLM mode if you have API access.
- Mock salary ranges are illustrative; use a real API for stronger evaluation.
