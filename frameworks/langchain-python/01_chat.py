"""
LangChain (Python) — simplest possible PCH call.

Run:
    pip install langchain-pathcourse
    export PCH_API_KEY=pch_prod_b_...
    python frameworks/langchain-python/01_chat.py

Demonstrates that ChatPathCourse is a drop-in for ChatOpenAI — same .invoke()
shape, same response object.
"""

from langchain_pathcourse import ChatPathCourse

llm = ChatPathCourse(model="pch-fast")

response = llm.invoke("Explain x402 in one sentence.")
print(response.content)
