# Evaluation – Ground Truth (Baseline & Difficult)

This file contains a small benchmark to verify system behaviour. Prepare your OSCA 20-page subset and run the app, then compare outputs to the gold answers below.

---
## Baseline (Passing) Questions

### 1) Tasks of Project Managers (RAG)
**Q:** What are the main tasks of a Project Manager?  
**Gold answer:** Project Managers plan, organise, direct, control, and coordinate operations within organisations [source: OSCA_20pages.pdf#chunk1]. For ICT projects, their main tasks include creating detailed project plans outlining deliverables, timelines, resource allocation, and budgeting, as well as managing risks to ensure smooth execution and delivery [source: OSCA_20pages.pdf#chunk4]. They also manage the selection, implementation, and integration of new technology solutions and implement and maintain quality assurance processes [source: OSCA_20pages.pdf#chunk4].  
**Gold citations:** [source: OSCA_20pages.pdf#chunk1], [source: OSCA_20pages.pdf#chunk4]

### 2) Salary for Project Manager (Tool)
**Q:** What’s the average salary for a Project Manager in Australia?  
**Gold (tool_result):** The average salary for a project manager in Australia is around 160,000 AUD. The salary range is typically between 120,000 and 220,000 AUD [tool_result: google-genai].  
**Tool result (Salary):**  
Title: project manager  
Region: Australia  
Low/Mid/High (AUD): 120000 / 160000 / 220000  
Source: google-genai

### 3) Skills + Salary (BOTH)
**Q:** What skills do Project Managers need, and what’s their average salary in Australia?  
**Gold answer:** Project Managers require leadership, planning, communication, teamwork, risk management, and quality assurance skills [source: OSCA_20pages.pdf#chunk4]. The average salary in Australia is around 130,000 AUD, with a typical range from 90,000 to 180,000 AUD [tool_result: google-genai].  
**Gold citations:** [source: OSCA_20pages.pdf#chunk4]  
**Tool result (Salary):**  
Title: project manager  
Region: Australia  
Low/Mid/High (AUD): 90000 / 130000 / 180000  
Source: google-genai

### 4) Tasks of Nurses (RAG)
**Q:** What tasks do nurses perform?  
**Gold answer:** Nurses provide patient care, administer medications, monitor patient conditions, assist in rehabilitation, and collaborate within multidisciplinary healthcare teams [source: OSCA_20pages.pdf#chunk7].  
**Gold citations:** [source: OSCA_20pages.pdf#chunk7]

### 5) Salary for Nurse (Tool)
**Q:** What’s the average salary for a nurse in Australia?  
**Gold (tool_result):** The average salary for nurses in Australia ranges from 70,000 to 120,000 AUD, with a median salary of 85,000 AUD [tool_result: google-genai].  
**Tool result (Salary):**  
Title: nurse  
Region: Australia  
Low/Mid/High (AUD): 70000 / 85000 / 120000  
Source: google-genai

### 6) Skills for Software Engineer (RAG)
**Q:** What skills do software engineers need?  
**Gold answer:** Software engineers require programming proficiency, problem-solving, version control, testing, and teamwork/communication skills [source: OSCA_20pages.pdf#chunk2].  
**Gold citations:** [source: OSCA_20pages.pdf#chunk2]

---
## Difficult Questions (Failure-Point Analysis)

### D1) Very broad & cross-occupation
**Q:** What are the regulatory compliance requirements across all healthcare roles in Australia?  
**Expected behaviour:** RAG likely fails or retrieves too generic context due to scope; the correct answer would need multiple documents beyond the OSCA subset.  
**Failure point:** Document coverage gap (scope too broad).  
**Gold (manual):** Briefly list typical compliance themes and state that the current OSCA subset is insufficient; recommend narrowing the question.

### D2) Ambiguous role title
**Q:** What skills do PMs need?  
**Expected behaviour:** Router may not detect “PMs” → mis-route; retrieval may miss “Project Manager” synonyms.  
**Failure point:** Lexical mismatch; add synonyms or an alias map in `extract_title()` and router keyword lists.  
**Gold (manual):** Clarify “Project Manager”, then answer as in Baseline (skills + citations).

### D3) Numeric breakdown by state
**Q:** What’s the average salary for software engineers in each Australian state?  
**Expected behaviour:** Tool may produce one national figure and fail to break down by state.  
**Failure point:** Tool scope limitation (no per-state granularity).  
**Gold (manual):** Provide national range with a note that state-level data is not available in the selected tool; suggest alternative data sources.

---
## Checklist for Running the Evaluation
- Confirm FAISS index is built via `python ingest.py` before testing. [source: ingest.py] fileciteturn11file2
- In `config.yml`, set model provider and Gemini model properly to avoid 404. [source: llm_backend.py] fileciteturn11file3
- Ensure routing for hybrid questions returns **BOTH**. [source: router.py] fileciteturn11file6
- During demo, show the final outputs include both **[source: …]** and **[tool_result: google-genai]**. [source: prompts.py, app.py] fileciteturn11file4 fileciteturn11file1
