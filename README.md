# Career Assistant RAG + Tool System

## Scenario
We built the system as a **Career Assistant for Australian job seekers**. The brief required a helper that can answer OSCA-derived occupation questions and supplement them with live labour-market insights. We kept the scenario instead of inventing a new domain because the provided OSCA (Occupational Skills and Competencies Assessment) PDF already covers Australian roles, tasks, and skills; combining that corpus with a salary lookup tool gives students and professionals a single place to research duties and pay.

## Documents & Tools Used
- **Grounding documents (RAG knowledge base):**
  - `data/OSCA_20pages.pdf` → chunked and embedded via `ingest.py`, stored under `indices/`.
- **External tools / APIs:**
  - **SalaryTool** → wraps Google Generative AI (Gemini) to obtain low/mid/high annual salary ranges in AUD.
  - No web search or math-specific APIs beyond the salary call.

## LLMs & Frameworks
- **LLM:** Google Gemini Flash (`models/gemini-2.0-flash`) accessed through the `google-genai` Python SDK.
- **Embedding model:** `sentence-transformers/all-MiniLM-L6-v2` for document encoding, searched with **FAISS**.
- **Frameworks & libraries:** Gradio UI, PyYAML for config, SentenceTransformers + FAISS for retrieval, and google-genai for both chat and tool outputs.

## Routing Logic
1. Every user query is lower-cased and checked for keyword groups inside `router.py`.
2. Salary-related keywords (e.g., "salary", "wage", "income") trigger the **TOOL** path; skill/task keywords trigger **RAG**; if both categories are present, the router returns **BOTH** so the system combines retrieval with the salary tool.
3. The Gradio app reads the route and:
   - Calls `RAGIndexer.retrieve(...)` when **RAG** or **BOTH** is chosen.
   - Calls `SalaryTool.lookup(...)` when **TOOL** or **BOTH** is chosen, mapping the query to a job title via `extract_title`.
4. Retrieved context, tool JSON, and prompts in `prompts.py` are merged so the LLM produces a grounded answer with citations and an optional tool block.

## Run Instructions
1. **Install dependencies** (Python 3.10+):
   ```bash
   pip install -r requirements.txt
   ```
2. **Prepare the OSCA index** (only once per document set):
   ```bash
   python ingest.py
   ```
   This reads PDFs from `./data`, chunks them, and saves a FAISS index in `./indices`.
3. **Set credentials:** export `GOOGLE_API_KEY` in your shell so both the LLM client and salary tool can call Gemini. If you skip this step, running `python app.py` will prompt you in the terminal to enter the key before the app launches.【F:app.py†L1-L30】【F:llm_backend.py†L24-L46】【F:tools.py†L24-L33】
4. **Launch the app:**
   ```bash
   python app.py
   ```
   The Gradio UI starts at `http://127.0.0.1:7861` by default. Ask career questions, inspect citations, and verify salary tool cards.
5. **Test retrieval-only logic:** temporarily disable the tool or ask skill-based queries (see Examples) to confirm citation rendering.

## Examples
1. **Hybrid (BOTH):**
   - *Input:* "What does an enrolled nurse do, and what salary should I expect in Australia?"
   - *Expected output:* Answer summarises duties with `[source:OSCA_20pages.pdf#chunkX]` citations and appends a "Tool result (Salary)" card showing low/mid/high salary in AUD sourced from Google Gemini.
2. **RAG only:**
   - *Input:* "List the key responsibilities of a project manager in the OSCA guide."
   - *Expected output:* Paragraph grounded in OSCA chunks with citations; no salary block because routing selects RAG only.

## Limitations
- **Document scope:** Only the supplied ~20-page OSCA excerpt is indexed, so questions outside those occupations or requiring cross-document synthesis may fail.
- **Keyword routing:** Acronyms or novel phrasing (e.g., "PMs" for project managers) might bypass the heuristic router or title extractor; extending the synonym list would help.
- **Salary tool granularity:** The Gemini-powered salary lookup returns national-level ranges; finer breakdowns (e.g., by state) are not guaranteed.
- **External dependency:** Both chat and tool calls require Google Generative AI access; rate limits or API errors surface directly to the UI as error traces.

## Failure Point Insights
The "Difficult Questions" evaluation identified several weak spots, and we addressed or planned mitigations accordingly:

- **D1 – Broad compliance questions:** Retrieval fails when the question spans multiple healthcare roles; we now highlight the scope limitation in answers and recommend narrowing the query.
- **D2 – Ambiguous role titles ("PMs"):** The current keyword and title-extraction hints miss acronyms, so queries like "PMs" stay under-specified; expand those synonym lists to normalise titles before routing/tool calls.
- **D3 – State-level salaries:** Gemini lacks per-state salary data; the system now clarifies that only national ranges are available and suggests alternative sources in responses.
