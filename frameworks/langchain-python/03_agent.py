"""
LangChain (Python) — tool-using agent on PCH.

Run:
    pip install langchain-pathcourse langchain
    export PCH_API_KEY=pch_prod_b_...
    python frameworks/langchain-python/03_agent.py

Shows a tool-calling agent backed by PCH. Two tools — get_balance and
list_models — and the LLM picks which to call. Agents work because PCH
forwards OpenAI's native tool-call protocol unchanged.
"""

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool

from langchain_pathcourse import ChatPathCourse


@tool
def get_balance(agent_id: str) -> str:
    """Look up the USDC balance for a PCH agent."""
    # Real call would hit PCH's /v1/me or /v1/balance endpoints.
    return f"Agent {agent_id} has 42.50 USDC available."


@tool
def list_models() -> str:
    """Return the catalog of PCH models the caller can access."""
    return "pch-fast, pch-pro, pch-coder, pch-embed, claude-haiku, claude-sonnet"


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an assistant for the PathCourse Health platform. Use tools to answer questions about agents."),
        ("user", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

llm = ChatPathCourse(model="pch-pro")
agent = create_tool_calling_agent(llm, [get_balance, list_models], prompt)
executor = AgentExecutor(agent=agent, tools=[get_balance, list_models], verbose=True)

result = executor.invoke({"input": "What's the balance for agent abc123, and what models can I use?"})
print("\nFINAL ANSWER:", result["output"])
