# Evaluation Report

This report summarizes baseline and difficult question evaluations for the career-assistant system, verifying how the router, RAG retriever, and salary tool work together.

## Baseline Questions (5)

### B1. Core Tasks for Project Managers (RAG)
1️⃣ **User Question:** “What are the main tasks of a project manager in the OSCA guide?”
2️⃣ **Document References:** `OSCA_20pages.pdf#chunk1`, `OSCA_20pages.pdf#chunk4`
3️⃣ **Manual Ground-Truth Answer:** The guide states that project managers plan, organize, direct, and control organizational operations. For ICT projects they develop detailed plans covering deliverables, timelines, resource allocations, and budgets, while managing risks, implementing technical solutions, and maintaining quality processes.
4️⃣ **System Output Correct?:** **Y** – The response matched the manual answer and listed the same chunk references.

### B2. Australian Project Manager Salaries (Tool)
1️⃣ **User Question:** “What’s the average salary for a project manager in Australia?”
2️⃣ **Tool Output:** `SalaryTool` (Google Gemini Flash) returned low 120,000 / mid 160,000 / high 220,000 AUD.
3️⃣ **Manual Ground-Truth Answer:** Based on the same tool snapshot, Australian project managers earn about 160,000 AUD on average within a 120,000–220,000 AUD range.
4️⃣ **System Output Correct?:** **Y** – The answer showed the same three-tier salary card and cited google-genai as the source.

### B3. Project Manager Skills + Salary (BOTH)
1️⃣ **User Question:** “What skills do project managers need and what salary should I expect in Australia?”
2️⃣ **Document / Tool References:** `OSCA_20pages.pdf#chunk4`; `SalaryTool` (low 90,000 / mid 130,000 / high 180,000 AUD).
3️⃣ **Manual Ground-Truth Answer:** Required skills include leadership, project planning, communication, teamwork, risk management, and quality assurance. Expected salary range is 90,000–180,000 AUD with an average around 130,000 AUD.
4️⃣ **System Output Correct?:** **Y** – The router chose BOTH, and the response included a skill paragraph with chunk citations plus the salary tool card.

### B4. Enrolled Nurse Responsibilities (RAG)
1️⃣ **User Question:** “List the typical duties of an enrolled nurse covered by OSCA.”
2️⃣ **Document References:** `OSCA_20pages.pdf#chunk7`
3️⃣ **Manual Ground-Truth Answer:** The document notes that nurses provide direct patient care, administer medications, monitor conditions, assist with rehabilitation, and collaborate within multidisciplinary teams.
4️⃣ **System Output Correct?:** **Y** – The reply covered each duty and cited chunk7.

### B5. Australian Nurse Salaries (Tool)
1️⃣ **User Question:** “What is the typical salary range for nurses in Australia?”
2️⃣ **Tool Output:** `SalaryTool` returned 70,000 / 85,000 / 120,000 AUD.
3️⃣ **Manual Ground-Truth Answer:** The tool snapshot aligns with public salary data, showing an average of roughly 85,000 AUD.
4️⃣ **System Output Correct?:** **Y** – The system presented the same range values and noted the tool source in its summary.

## Difficult Questions (3)

### D1. Broad Healthcare Compliance (Outside RAG Scope)
1️⃣ **User Question:** “What are the regulatory compliance requirements across all healthcare roles in Australia?”
2️⃣ **Manual Ground-Truth Answer:** Highlight common themes (registration, workplace health and safety, privacy) while emphasizing that the OSCA core document covers specific roles only. It cannot provide a complete compliance guide, so the user should narrow the question.
3️⃣ **System Output:** After stating no documents were found, the system still generated a generic paragraph without stressing the scope limitation.
4️⃣ **Failure Analysis:** **Retrieval failure + coverage gap.** The RAG index contains a single PDF, yet the router still chose RAG, leading to insufficient context and no explicit disclosure of the mismatch.

### D2. Acronym Coverage Gap
1️⃣ **User Question:** “What skills do PMs need?”
2️⃣ **Manual Ground-Truth Answer:** Interpret “PMs” as “Project Managers,” then cite `OSCA_20pages.pdf#chunk4` for leadership, planning, communication, and risk management skills.
3️⃣ **System Output:** Retrieval produced only generic skill statements with missing citations because the acronym “PMs” failed to connect to the indexed “project manager” passages.
4️⃣ **Failure Analysis:** **Acronym coverage gap.** Neither the keyword heuristics nor the `extract_title()` hints map “PMs” to “project manager,” so the query lacks focused retrieval or tool grounding. Expanding those synonym lists should fix it.

### D3. State-Level Salary Breakdown
1️⃣ **User Question:** “What’s the average salary for software engineers in each Australian state?”
2️⃣ **Manual Ground-Truth Answer:** The tool provides national data only, so the correct reply should share the nationwide range (e.g., 95,000–140,000 AUD), explain that state-level breakdowns are unavailable, and recommend government data portals.
3️⃣ **System Output:** SalaryTool returned national figures, and the system relayed them without clarifying the missing state detail.
4️⃣ **Failure Analysis:** **Tool granularity limits.** The generation prompt should add fallback guidance or redirect users to external sources when finer-grained data is absent.

---

Overall, the system performs reliably for routine queries within its current corpus and tool set, but routing coverage and response templates still need improvements for cross-domain, acronym-heavy, and high-granularity requests.
