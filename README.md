# Career Assistant RAG + Tool System

## Scenario
We built the system as a **Career Assistant for Australian job seekers**. The brief required a helper that can answer OSCA-derived occupation questions and supplement them with live labour-market insights. We kept the scenario instead of inventing a new domain because the provided OSCA (Occupational Skills and Competencies Assessment) PDF already covers Australian roles, tasks, and skills; combining that corpus with a salary lookup tool gives students and professionals a single place to research duties and pay.

## Documents & Tools Used
- **Grounding documents (RAG knowledge base):**
  - `data/OSCA_20pages.pdf` → chunked and embedded via `ingest.py`, stored under `indices/`.【F:ingest.py†L1-L53】【F:rag.py†L1-L65】
- **External tools / APIs:**
  - **SalaryTool** → wraps Google Generative AI (Gemini) to obtain low/mid/high annual salary ranges in AUD.【F:tools.py†L10-L107】
  - No web search or math-specific APIs beyond the salary call.

## LLMs & Frameworks
- **LLM:** Google Gemini Flash (`models/gemini-2.0-flash`) accessed through the `google-genai` Python SDK.【F:llm_backend.py†L1-L46】【F:config.yml†L8-L30】
- **Embedding model:** `sentence-transformers/all-MiniLM-L6-v2` for document encoding, searched with **FAISS**.【F:rag.py†L1-L65】【F:config.yml†L14-L18】
- **Frameworks & libraries:** Gradio UI, PyYAML for config, SentenceTransformers + FAISS for retrieval, and google-genai for both chat and tool outputs.【F:app.py†L1-L85】【F:requirements.txt†L1-L9】

## Routing Logic
1. Every user query is lower-cased and checked for keyword groups inside `router.py`.
2. Salary-related keywords (e.g., "salary", "wage", "income") trigger the **TOOL** path; skill/task keywords trigger **RAG**; if both categories are present, the router returns **BOTH** so the system combines retrieval with the salary tool.【F:router.py†L1-L39】
3. The Gradio app reads the route and:
   - Calls `RAGIndexer.retrieve(...)` when **RAG** or **BOTH** is chosen.【F:app.py†L12-L47】
   - Calls `SalaryTool.lookup(...)` when **TOOL** or **BOTH** is chosen, mapping the query to a job title via `extract_title`.【F:app.py†L27-L67】
4. Retrieved context, tool JSON, and prompts in `prompts.py` are merged so the LLM produces a grounded answer with citations and an optional tool block.【F:app.py†L35-L67】【F:prompts.py†L1-L37】

## Run Instructions
1. **Install dependencies** (Python 3.10+):
   ```bash
   pip install -r requirements.txt
   ```
2. **Prepare the OSCA index** (only once per document set):
   ```bash
   python ingest.py
   ```
   This reads PDFs from `./data`, chunks them, and saves a FAISS index in `./indices`.【F:ingest.py†L1-L53】
3. **Set credentials:** export `GOOGLE_API_KEY` in your shell so both the LLM client and salary tool can call Gemini. If you skip this step, running `python app.py` will prompt you in the terminal to enter the key before the app launches.【F:app.py†L1-L30】【F:llm_backend.py†L24-L46】【F:tools.py†L24-L33】
4. **Launch the app:**
   ```bash
   python app.py
   ```
   The Gradio UI starts at `http://127.0.0.1:7861` by default. Ask career questions, inspect citations, and verify salary tool cards.【F:app.py†L53-L85】【F:config.yml†L1-L6】
5. **Test retrieval-only logic:** temporarily disable the tool or ask skill-based queries (see Examples) to confirm citation rendering.【F:router.py†L13-L39】【F:prompts.py†L1-L37】

## Examples
1. **Hybrid (BOTH):**
   - *Input:* "What does an enrolled nurse do, and what salary should I expect in Australia?"
   - *Expected output:* Answer summarises duties with `[source:OSCA_20pages.pdf#chunkX]` citations and appends a "Tool result (Salary)" card showing low/mid/high salary in AUD sourced from Google Gemini.【F:app.py†L35-L67】【F:prompts.py†L1-L37】
2. **RAG only:**
   - *Input:* "List the key responsibilities of a project manager in the OSCA guide."
   - *Expected output:* Paragraph grounded in OSCA chunks with citations; no salary block because routing selects RAG only.【F:router.py†L16-L37】【F:app.py†L35-L60】

## Limitations
- **Document scope:** Only the supplied ~20-page OSCA excerpt is indexed, so questions outside those occupations or requiring cross-document synthesis may fail.【F:ingest.py†L31-L53】【F:Evaluation_GroundTruth.md†L38-L42】
- **Keyword routing:** Acronyms or novel phrasing (e.g., "PMs" for project managers) might bypass the heuristic router or title extractor; extending the synonym list would help.【F:router.py†L16-L37】【F:app.py†L27-L46】【F:Evaluation_GroundTruth.md†L44-L48】
- **Salary tool granularity:** The Gemini-powered salary lookup returns national-level ranges; finer breakdowns (e.g., by state) are not guaranteed.【F:tools.py†L20-L107】【F:Evaluation_GroundTruth.md†L51-L55】
- **External dependency:** Both chat and tool calls require Google Generative AI access; rate limits or API errors surface directly to the UI as error traces.【F:app.py†L35-L71】【F:tools.py†L24-L107】

## Failure Point Insights
The "Difficult Questions" evaluation identified several weak spots, and we addressed or planned mitigations accordingly:

- **D1 – Broad compliance questions:** Retrieval fails when the question spans multiple healthcare roles; we now highlight the scope limitation in answers and recommend narrowing the query.【F:Evaluation_GroundTruth.md†L40-L43】【F:prompts.py†L1-L19】
- **D2 – Ambiguous role titles ("PMs"):** The current keyword and title-extraction hints miss acronyms, so queries like "PMs" stay under-specified; expand those synonym lists to normalise titles before routing/tool calls.【F:app.py†L27-L33】【F:router.py†L16-L37】【F:Evaluation_GroundTruth.md†L45-L49】
- **D3 – State-level salaries:** Gemini lacks per-state salary data; the system now clarifies that only national ranges are available and suggests alternative sources in responses.【F:tools.py†L20-L107】【F:Evaluation_GroundTruth.md†L51-L55】
