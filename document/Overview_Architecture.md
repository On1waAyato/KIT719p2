# System Overview & Architecture (KIT719 Project 2 – Option A: Career Assistant)

This document describes the overall design, data flow, and the RAG pipeline of the Career Assistant system.

## 1) Overall Design

User → Router → (RAG and/or Tool) → Answer Composer → Gradio UI

```
+-----------+        +---------+        +---------------------+
|   User    | -----> | Router  | -----> |  RAG and/or Tool    |
+-----------+        +----+----+        +----------+----------+
                         |                         |
                         |                         |
                         v                         v
                   +-----+------+           +------+-------+
                   |  RAG (doc) |           |  Salary Tool |
                   +-----+------+           +------+-------+
                         \______________________/          
                                   |                      
                                   v                      
                          +------------------+            
                          |  Answer Composer |            
                          +--------+---------+            
                                   |                      
                                   v                      
                              +----------+                
                              |  Gradio  |                
                              +----------+                
```

- Routing: simple keyword-based routing that returns **RAG / TOOL / BOTH** depending on the question. [source: router.py] fileciteturn11file6
- RAG: retrieves chunks from FAISS built on OSCA PDF(s). [source: ingest.py, rag.py] fileciteturn11file2 fileciteturn11file5
- Tool: queries Google Gemini to obtain salary ranges (with mock fallback logic handled in code). [source: tools.py] fileciteturn11file7
- Orchestration and UI: Gradio-based app; merges RAG and Tool results and renders citations. [source: app.py] fileciteturn11file1

## 2) RAG Pipeline

```
OSCA PDF (~20 pages) --> ingest.py --> chunking --> embeddings (SentenceTransformers)
     |                                                    |
     +---------------------- rag.py ----------------------+
                                |
                                v
                            FAISS Index  <--- persisted under ./indices
                                |
                                v
                            retrieve(query, top_k) --> chunks (source_id, text)
```

- Document ingestion/cleaning and chunking are implemented in **ingest.py**, using a simple fixed-size token split with overlap, then persisted via FAISS. fileciteturn11file2
- At query time, **rag.py** encodes the query, searches FAISS, and returns top-k chunks along with `source_id` and `score`. fileciteturn11file5
- The Gradio app merges chunk texts into the LLM prompt for grounded answering. fileciteturn11file1

## 3) Routing Logic

- Heuristic routing detects **salary/pay/range** keywords for **TOOL**, detects **task/skill/competency/responsibility** for **RAG**, and detects both classes to return **BOTH**. fileciteturn11file6
- This satisfies the assignment requirement to decide when to use RAG, tools, or both. fileciteturn11file0

## 4) Tool Calling (Salary)

- Implemented via **google-genai** client with a JSON schema to encourage structured output (`low/mid/high`). fileciteturn11file7
- Results are displayed in the UI as a labelled block **Tool result (Salary)** with `Title/Region/Low/Mid/High/Source`. fileciteturn11file1
- When the tool is used, the final answer includes a short tool-based summary (e.g., “The average salary is … [tool_result: google-genai]”) to distinguish sources. fileciteturn11file4

## 5) LLM Backend & Prompts

- Backend supports Google Gemini; system prompt and answer prompt enforce **grounding + citations**. fileciteturn11file3 fileciteturn11file4
- The answer template instructs the model to append citations like `[source: <source_id>]` and to add a **Tool result** section if present. fileciteturn11file4

## 6) UI & Error Handling

- **app.py** catches exceptions and returns an HTML `<pre>` block with the traceback to keep the app responsive (graceful handling). fileciteturn11file1
- The UI shows the answer, followed by `Citations: ...` and an optional **Tool result (Salary)** card. fileciteturn11file1

## 7) Alignment with Assignment Requirements

- RAG over ~20 pages OSCA: implemented via FAISS with chunking and retrieval. fileciteturn11file2 fileciteturn11file5
- Tool calling: salary lookup implemented via Google Gemini. fileciteturn11file7
- Routing logic selecting documents, tools, or both: implemented in **router.py**. fileciteturn11file6
- Citations and tool results visible in final outputs: enforced by prompts and rendered in UI. fileciteturn11file4 fileciteturn11file1
- Local Gradio app with clear run instructions (see README). fileciteturn11file1 fileciteturn11file0
