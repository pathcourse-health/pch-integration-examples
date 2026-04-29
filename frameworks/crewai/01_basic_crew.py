"""
CrewAI — basic two-agent crew on PCH.

Run:
    pip install crewai crewai-pathcourse
    export PCH_API_KEY=pch_prod_b_...
    python frameworks/crewai/01_basic_crew.py

Demonstrates the simplest CrewAI setup — researcher + writer, both backed
by pch-pro. The PathCourseLLM factory is the only PCH-specific line; the
rest is standard CrewAI.
"""

from crewai import Agent, Crew, Task

from crewai_pathcourse import PathCourseLLM

llm = PathCourseLLM(model="pch-pro")

researcher = Agent(
    role="Research Analyst",
    goal="Find the key requirements for autonomous AI agent infrastructure",
    backstory="You are an expert in autonomous agent systems and web3 infrastructure.",
    llm=llm,
    verbose=True,
)

writer = Agent(
    role="Technical Writer",
    goal="Write a clear, concise technical summary",
    backstory="You write precise technical documentation aimed at developers.",
    llm=llm,
    verbose=True,
)

research_task = Task(
    description="Research the 5 most important infrastructure requirements for autonomous AI agents.",
    expected_output="A bullet list of 5 requirements with one-sentence rationale each.",
    agent=researcher,
)

write_task = Task(
    description="Write a 200-word summary of the research findings, suitable for a developer-focused blog post.",
    expected_output="A 200-word technical summary in plain prose.",
    agent=writer,
)

crew = Crew(agents=[researcher, writer], tasks=[research_task, write_task])
result = crew.kickoff()
print("\n=== FINAL OUTPUT ===\n", result)
