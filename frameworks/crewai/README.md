# CrewAI — `crewai-pathcourse`

Give CrewAI agents autonomous USDC billing on Base L2. Every CrewAI feature — tools, memory,
hierarchical crews, async execution — works unchanged.

## Install

```bash
pip install crewai crewai-pathcourse
export PCH_API_KEY=pch_prod_b_...
```

## Examples

| File | What it shows |
|---|---|
| [`01_basic_crew.py`](./01_basic_crew.py) | Two-agent crew (researcher + writer), one model |
| [`02_mixed_models.py`](./02_mixed_models.py) | Three-agent crew with different PCH models per agent |

## How it works

```python
from crewai import Agent
from crewai_pathcourse import PathCourseLLM

agent = Agent(
    role="Research Analyst",
    goal="Analyze AI agent infrastructure trends",
    backstory="Expert in autonomous agent systems.",
    llm=PathCourseLLM(model="pch-pro"),
)
```

`PathCourseLLM(model)` returns a CrewAI `LLM` instance configured for the PCH gateway.
Internally CrewAI uses LiteLLM, which supports any OpenAI-compatible endpoint — so this is
purely configuration, no special integration code.

## Per-agent model selection

Cheap models for routine work, premium models for hard work — same crew:

```python
planner    = Agent(..., llm=PathCourseLLM(model="pch-pro"))
researcher = Agent(..., llm=PathCourseLLM(model="pch-fast"))
coder      = Agent(..., llm=PathCourseLLM(model="pch-coder"))
```

This is meaningful in production because crews can run thousands of LLM calls per task —
matching model price/capability to each agent's actual job is the difference between $5/run
and $50/run.

## Links

- Package on PyPI: [pypi.org/project/crewai-pathcourse](https://pypi.org/project/crewai-pathcourse/)
- Source code: [github.com/pathcourse-health/pch-framework-adapters/tree/main/crewai-pathcourse](https://github.com/pathcourse-health/pch-framework-adapters/tree/main/crewai-pathcourse)
- CrewAI docs: [docs.crewai.com](https://docs.crewai.com)
