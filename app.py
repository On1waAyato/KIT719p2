import json, yaml, traceback
import os
import getpass
import gradio as gr
from rag import RAGIndexer
from llm_backend import LLM
from tools import SalaryTool
from router import Router
from prompts import SYSTEM_PROMPT, ANSWER_PROMPT

def ensure_api_key():
    """Prompt the user for a Google API key if the environment variable is missing."""
    if os.getenv("GOOGLE_API_KEY"):
        return

    prompt = "Please enter your Google API Key: "
    try:
        api_key = getpass.getpass(prompt)
    except Exception:
        api_key = input(prompt)

    api_key = api_key.strip()
    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY is required to run the app.")

    os.environ["GOOGLE_API_KEY"] = api_key


with open("config.yml", "r") as f:
    CFG = yaml.safe_load(f)

ensure_api_key()

rag_idx = RAGIndexer(CFG["rag"]["embedding_model"], CFG["rag"]["index_dir"])
llm = LLM()
router = Router()
salary_tool = SalaryTool()

def format_citations(chunks):
    seen = set()
    cites = []
    for ch in chunks:
        sid = ch["source_id"]
        if sid not in seen:
            seen.add(sid)
            cites.append(sid)
    return ", ".join(f"[source:{c}]" for c in cites)

def extract_title(question: str):
    # naive extraction; improve as needed
    q = question.lower()
    for hint in ["software engineer","data analyst","project manager","nurse","teacher"]:
        if hint in q:
            return hint
    return question

def qa_system(question: str):
    try:
        route = router.route(question)
        retrieved = []
        tool_result = None

        if route in ("RAG", "BOTH"):
            retrieved = rag_idx.retrieve(question, top_k=CFG["rag"]["top_k"])

        if route in ("TOOL", "BOTH"):
            title = extract_title(question)
            tool_result = salary_tool.lookup(title=title, region=CFG["tools"]["salary_api"]["default_region"])

        context_json = json.dumps([{"source_id": c["source_id"], "text": c["text"][:1200]} for c in retrieved], ensure_ascii=False)
        tool_json = json.dumps(tool_result, ensure_ascii=False) if tool_result else ""
        user_prompt = ANSWER_PROMPT.format(question=question, context_json=context_json, tool_results=tool_json)
        answer = llm.chat(system_prompt=SYSTEM_PROMPT, user_prompt=user_prompt)

        tool_block = ""
        if tool_result:
            k = tool_result
            tool_block = f"""
            <div style='margin-top:8px;padding:8px;border:1px solid #ddd;border-radius:8px'>
            <b>Tool result (Salary):</b>
            <div>Title: {k.get('title')}</div>
            <div>Region: {k.get('region')}</div>
            <div>Low/Mid/High (AUD): {k.get('low')} / {k.get('mid')} / {k.get('high')}</div>
            <div>Source: {k.get('source')}</div>
            </div>
            """
        cites = format_citations(retrieved) if retrieved else ""
        html = f"<div>{answer}</div><div style='margin-top:6px;color:#666'>Citations: {cites}</div>{tool_block}"
        return html
    except Exception as e:
        tb = traceback.format_exc()
        return f"<pre style='color:red'>Error: {e}\n{tb}</pre>"

def build_ui():
    title = CFG["app"]["title"]
    desc = CFG["app"]["description"]
    with gr.Blocks(title=title) as demo:
        gr.Markdown(f"# {title}\n{desc}")
        inp = gr.Textbox(label="Ask me about occupations, tasks/skills, or salaries (AU):")
        out = gr.HTML(label="Answer")
        btn = gr.Button("Ask")
        btn.click(qa_system, inputs=inp, outputs=out)
    return demo

if __name__ == "__main__":
    demo = build_ui()
    demo.launch(server_name=CFG["app"]["host"], server_port=CFG["app"]["port"])
