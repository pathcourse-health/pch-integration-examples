"""
CrewAI — mixed-model crew on PCH.

Run:
    pip install crewai crewai-pathcourse
    export PCH_API_KEY=pch_prod_b_...
    python frameworks/crewai/02_mixed_models.py

Each agent uses a PCH model matched to its job:
  planner    -> pch-pro    ($1.96/M tokens, deep reasoning)
  coder      -> pch-coder  ($3.50/M tokens, code-tuned)
  reviewer   -> pch-fast   ($0.44/M tokens, quick checks)

Real production crews can save 5-10x on LLM cost by sizing models per agent
instead of putting every agent on the most-expensive option.
"""

from crewai import Agent, Crew, Task

from crewai_pathcourse import PathCourseLLM

planner = Agent(
    role="Solutions Architect",
    goal="Plan the implementation of a new feature",
    backstory="You design clean, maintainable solutions and break them into tasks.",
    llm=PathCourseLLM(model="pch-pro"),
    verbose=True,
)

coder = Agent(
    role="Senior Engineer",
    goal="Write production-ready code following the architect's plan",
    backstory="You write clean, tested Python with type hints and docstrings.",
    llm=PathCourseLLM(model="pch-coder"),
    verbose=True,
)

reviewer = Agent(
    role="Code Reviewer",
    goal="Spot bugs, style issues, and missing edge cases",
    backstory="You read code carefully and write tight, actionable reviews.",
    llm=PathCourseLLM(model="pch-fast"),
    verbose=True,
)

plan = Task(
    description="Plan a Python function `usdc_to_atomic(amount: float) -> int` that converts USDC to its 6-decimal atomic representation. Note edge cases.",
    expected_output="A concise design doc: function signature, behavior, and 3 edge cases to handle.",
    agent=planner,
)

implement = Task(
    description="Implement the function from the plan. Include the docstring and at least 4 unit tests.",
    expected_output="A Python file with the function and tests.",
    agent=coder,
    context=[plan],
)

review = Task(
    description="Review the code and tests. Identify any issues. Be specific — line numbers, suggested fixes.",
    expected_output="A bulleted code-review reply.",
    agent=reviewer,
    context=[implement],
)

crew = Crew(agents=[planner, coder, reviewer], tasks=[plan, implement, review])
print("\n=== FINAL OUTPUT ===\n", crew.kickoff())
