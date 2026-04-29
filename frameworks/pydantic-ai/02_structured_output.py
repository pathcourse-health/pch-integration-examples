"""
Pydantic AI — structured output on PCH.

Run:
    pip install pydantic-ai pydantic-ai-pathcourse
    export PCH_API_KEY=pch_prod_b_...
    python frameworks/pydantic-ai/02_structured_output.py

Demonstrates Pydantic AI's killer feature on PCH: declare a Pydantic model
as result_type, get back a validated, typed instance. The gateway forwards
OpenAI's structured-output protocol unchanged.
"""

from pydantic import BaseModel, Field
from pydantic_ai import Agent

from pydantic_ai_pathcourse import PathCourseModel


class InfraReport(BaseModel):
    summary: str = Field(description="One-paragraph summary of the analysis")
    requirements: list[str] = Field(description="Key infrastructure requirements")
    risk_level: int = Field(ge=1, le=5, description="Overall risk on 1-5 scale")
    recommended_tier: str = Field(description="One of: uncertified, bronze, silver, gold")


agent = Agent(
    model=PathCourseModel("pch-pro"),
    result_type=InfraReport,
    system_prompt="You are a technical risk analyst for AI agent infrastructure decisions.",
)

result = agent.run_sync(
    "A fintech startup wants to deploy 50 autonomous agents that issue refunds. "
    "Analyze the infrastructure requirements and risk level."
)

# result.data is a validated InfraReport instance — IDE autocomplete works,
# fields are type-checked, the LLM is guaranteed to return matching shape.
report: InfraReport = result.data
print(f"Risk level:        {report.risk_level}/5")
print(f"Recommended tier:  {report.recommended_tier}")
print(f"Summary:           {report.summary}")
print("Requirements:")
for req in report.requirements:
    print(f"  - {req}")
