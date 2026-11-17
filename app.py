import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import streamlit as st
from dotenv import load_dotenv
from shared.llm_client import chat,LLMError
import importlib.util
load_dotenv()
def load_module(name,path):
 spec=importlib.util.spec_from_file_location(name,path); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod
base=Path(__file__).resolve().parents[1]
rag=load_module("rag_core",base/"04_RAG_Document_QA"/"rag_core.py")
agent=load_module("agent_core",base/"05_AI_Agent_Tools"/"agent.py")
st.set_page_config(page_title="CampusAI",page_icon="🎓")
st.title("🎓 CampusAI — Study & Career Assistant")
st.caption("Capstone: prompts + optional LLM API + local document retrieval + safe tools.")
with st.sidebar:
 mode=st.selectbox("Mode",["Study assistant","Document Q&A","Tool assistant"])
 instruction=st.text_area("Custom instructions","Be concise, practical and honest. Do not invent facts.")
 uploaded=st.file_uploader("Upload TXT/MD for Q&A",type=["txt","md"])
 st.caption("Set OPENAI_API_KEY in .env for hosted model responses.")
if "history" not in st.session_state: st.session_state.history=[]
for m in st.session_state.history:
 with st.chat_message(m["role"]): st.markdown(m["content"])
q=st.chat_input("Ask a question...")
if q:
 st.session_state.history.append({"role":"user","content":q})
 with st.chat_message("user"): st.markdown(q)
 if mode=="Tool assistant":
  r=agent.run_agent(q); answer=f"**Plan:** {r['plan']}\n\n**Tool:** {r['tool']}\n\n**Result:** {r['result']}"
 elif mode=="Document Q&A":
  if uploaded:
   text=uploaded.getvalue().decode("utf-8",errors="ignore")
   answer=rag.grounded_answer(q,rag.retrieve(q,rag.chunk_text(text),3))
  else: answer="Upload a non-confidential TXT or Markdown document first. This local retrieval baseline uses lexical matching, not embeddings."
 else:
  try: answer=chat([{"role":"system","content":instruction}]+st.session_state.history[-10:])
  except LLMError as e: answer="API not available: "+str(e)+"\n\nNo real model response was generated."
 with st.chat_message("assistant"): st.markdown(answer)
 st.session_state.history.append({"role":"assistant","content":answer})
if st.button("Clear conversation"):
 st.session_state.history=[]; st.rerun()
