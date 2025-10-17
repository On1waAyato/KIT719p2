# Career Assistant (RAG + Google Gemini + Tool Calling)

A refined, rubric-aligned implementation for KIT719 **Option A: Career Assistant**.
- RAG over OSCA (Occupation Standard Classification Australia) PDF(s)
- Tool calling for salary lookup (Google Gemini API or mock fallback)
- Prompt-driven router (LLM or heuristic fallback)
- Gradio local UI

## 0) Project Fit (KIT719)
- Uses RAG + Tool + Routing; cites sources; tool results shown clearly.
- UI is Gradio and runs locally.
- Provide ground truth & evaluation; include baseline and difficult Qs.
- Include `prompts.py` and `config.yml`.

## 1) Environment Setup
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### (Optional) Choose Your Model Provider
- **Google Gemini (Recommended)**: install and configure `google-genai`
- **Ollama (Local)**: install and run `ollama serve`, then `ollama pull llama3.1`
- **OpenAI**: set `models.provider: openai_chat` in `config.yml` and export your `OPENAI_API_KEY`

Example configuration (`config.yml`):
```yaml
models:
  provider: google_genai
  google:
    model: gemini-2.5-flash
```

Set your API key:
```python
os.environ["GOOGLE_API_KEY"] = "your_key_here"
```

## 2) Get OSCA Document
Place your OSCA (≈20 pages) PDF under `./data/`, e.g.:
```
./data/OSCA_20pages.pdf
```
Then build the FAISS index:
```bash
python ingest.py
```
Creates `./indices` with embedded vectors.

## 3) Run the Career Assistant
```bash
python app.py
# open http://127.0.0.1:7861
```
Ask questions such as:
- “What skills do nurses need?”
- “What’s the average salary for a software engineer in Australia?”
- “What tasks do project managers perform?”

## 4) Salary Tool (Google Gemini API or Mock)
The salary lookup tool uses the Gemini API (real) or mock fallback:

```yaml
tools:
  salary_api:
    provider: google_genai
    default_region: Australia
```

Example tool output:
```json
{
  "title": "software engineer",
  "region": "Australia",
  "low": 80000,
  "mid": 120000,
  "high": 180000
}
```
If Gemini API is unavailable, the system defaults to **mock salary values**.

## 5) System Architecture
| File | Description |
|------|--------------|
| `app.py` | Main orchestration with Gradio UI (RAG + Tool integration) |
| `ingest.py` | PDF loading, text chunking, FAISS index creation |
| `rag.py` | Retrieve top-k context chunks from OSCA |
| `router.py` | Route query to RAG or tool |
| `llm_backend.py` | Interface for Google Gemini, OpenAI, or Ollama |
| `tools.py` | Salary lookup implementation (Gemini or mock) |
| `prompts.py` | Prompts for system, router, and answering |
| `config.yml` | Configuration for models, tools, and RAG |

## 6) Evaluation (Ground Truth)
Create an `eval/` folder and include a file like:
```markdown
# KIT719 Evaluation
- Q: What are the responsibilities of project managers?
  Gold citations: OSCA_20pages.pdf#chunk4
  Gold answer: Project Managers plan, organise, direct, control, and coordinate operations within organisations.
- Q: What’s the average salary for a nurse in Australia?
  Tool: salary (google-genai)
  Gold: $70,000–$120,000, median $85,000
- Q: What skills do ICT professionals need?
  Gold citations: OSCA_20pages.pdf#chunk5
```

## 7) Example Outputs
**Q:** “What’s the average salary for a software engineer in Australia?”  
**A:** “The average salary for a software engineer in Australia is $120,000, with a range from $80,000 to $180,000. [tool_result: google-genai]”

**Q:** “What skills do nurses need, and what’s their average salary?”  
**A:** “Nurses require strong clinical, communication, and teamwork skills. The average salary ranges from $70,000 to $120,000, with a median salary of $85,000. [tool_result: google-genai]”

## 8) Project Demonstration (for Submission Video)
Your demonstration video should show:
1. **RAG queries** (e.g., “What tasks do project managers perform?”)
2. **Tool queries** (e.g., “What’s the average salary for a software engineer in Australia?”)
3. **Hybrid queries** combining both (e.g., “What skills do nurses need, and what’s their average salary?”)
4. **Citation display** from both RAG and tool results in the output.

## 9) Notes & Recommendations
- Focus the OSCA subset on your chosen occupations (e.g., nurse, software engineer, project manager).
- Adjust `chunk_size`, `overlap`, and `top_k` in `config.yml` to optimize retrieval.
- Use latest Gemini model (e.g., `gemini-2.5-flash`) to avoid 404 errors.
- When Gemini API fails, automatic fallback to mock ensures continuity.
- Show examples of both RAG-only and Tool-only responses for clarity.

## 10) Limitations
- OSCA PDF text may require manual cleaning before embedding.
- Google Gemini API doesn’t support a “system” role; handled through prompt concatenation.
- Salary estimates are illustrative and may vary regionally.

## 11) Citation Format (for report)
Outputs include citations in the format:
```
[source: <filename>#chunkID]
[tool_result: google-genai]
```
Example:
```
Project Managers plan, organise, direct, control, and coordinate operations within organisations [source: OSCA_20pages.pdf#chunk1].
For ICT projects, they manage risks and quality assurance [source: OSCA_20pages.pdf#chunk4].
Tool result (Salary): Software engineer, Australia, AUD 80k–180k.
```
