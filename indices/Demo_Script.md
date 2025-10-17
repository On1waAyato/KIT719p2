# Demo Script (Week 13 presentation, < 10 mins)

## 1) Intro (Target users & goals) – 30s
- Target users: graduates/students/career changers in Australia.
- Goal: answer occupation questions grounded in OSCA and show salary via a tool.

## 2) System overview – 60s
- Show the ASCII architecture and explain Router → RAG/Tool → Answer → UI. (See Overview_Architecture.md)

## 3) Live Demo – 5 min
**RAG-only**  
Q: “What are the main tasks of a Project Manager?”  
Expected: grounded sentences with citations like [source: OSCA_20pages.pdf#chunk1], [source: OSCA_20pages.pdf#chunk4].

**Tool-only**  
Q: “What’s the average salary for a nurse in Australia?”  
Expected: answer + “Tool result (Salary)” block with Low/Mid/High and [tool_result: google-genai].

**Hybrid (BOTH)**  
Q: “What skills do Project Managers need, and what’s their average salary in Australia?”  
Expected: skills with citations + salary block; Router chooses BOTH.

## 4) Failure case & learning – 1 min
- Show an ambiguous/over-broad query (from Difficult set) and explain the limitation.

## 5) Wrap up – 30s
- Reiterate: RAG + Tool + Routing + Citations + Local UI + Evaluation.
