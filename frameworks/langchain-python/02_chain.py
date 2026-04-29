"""
LangChain (Python) — LCEL chain with PCH.

Run:
    pip install langchain-pathcourse
    export PCH_API_KEY=pch_prod_b_...
    python frameworks/langchain-python/02_chain.py

Shows that LangChain's pipe-composition (LCEL) works against PCH unchanged:
prompt template -> ChatPathCourse -> StrOutputParser.
"""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from langchain_pathcourse import ChatPathCourse

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a concise technical writer. Reply in one paragraph, no bullet lists."),
        ("user", "Explain {topic} for a developer who already knows OpenAI APIs."),
    ]
)

llm = ChatPathCourse(model="pch-pro")     # pch-pro for stronger reasoning
chain = prompt | llm | StrOutputParser()

result = chain.invoke({"topic": "autonomous USDC billing on Base L2"})
print(result)
