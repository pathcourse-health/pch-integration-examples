"""
Pydantic AI — basic agent run on PCH.

Run:
    pip install pydantic-ai pydantic-ai-pathcourse
    export PCH_API_KEY=pch_prod_b_...
    python frameworks/pydantic-ai/01_basic.py

Demonstrates the simplest Pydantic AI setup against PCH — single agent,
plain text output, no tools or structured output.
"""

from pydantic_ai import Agent

from pydantic_ai_pathcourse import PathCourseModel

agent = Agent(
    model=PathCourseModel("pch-pro"),
    system_prompt="You are an expert in autonomous AI agent infrastructure. Be concise.",
)

result = agent.run_sync("What's the difference between Path Score and ERC-8004?")
print(result.data)
