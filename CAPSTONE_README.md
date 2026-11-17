# Capstone — CampusAI Study & Career Assistant

Problem: students need a simple place for study help, document-based answers and small learning utilities.

Integrated parts:
1. Prompt engineering through editable system instructions.
2. Optional OpenAI-compatible LLM API using environment variables.
3. Document Q&A through chunking and local lexical retrieval.
4. Tool assistant with a safe calculator and read-only knowledge search.
5. Streamlit chat UI and session history.

Run from root: `streamlit run 06_GenAI_Capstone/app.py`

Limitations: hosted API needs your own key and may cost money; RAG is lexical baseline, not embedding/vector DB; files are processed in session memory; agent routing is deterministic, not autonomous. No deployment is included. Review security and privacy before deployment.
