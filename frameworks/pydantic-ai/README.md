# Pydantic AI — `pydantic-ai-pathcourse`

Build typed, production-grade agents on PCH. Pydantic AI's structured-output guarantees, tool
use, and streaming all work unchanged.

## Install

```bash
pip install pydantic-ai pydantic-ai-pathcourse
export PCH_API_KEY=pch_prod_b_...
```

## Examples

| File | What it shows |
|---|---|
| [`01_basic.py`](./01_basic.py) | Single-shot agent run, plain text output |
| [`02_structured_output.py`](./02_structured_output.py) | Pydantic model as `result_type` — typed, validated output |

## How it works

```python
from pydantic_ai import Agent
from pydantic_ai_pathcourse import PathCourseModel

agent = Agent(
    model=PathCourseModel("pch-pro"),
    system_prompt="You are a helpful assistant.",
)

result = agent.run_sync("Explain x402 in one sentence.")
print(result.data)
```

`PathCourseModel(model)` returns a configured `OpenAIModel` — every Pydantic AI feature works
identically to the OpenAI provider, since PCH's gateway is OpenAI API-compatible.

## Why Pydantic AI on PCH

The structured-output story is where Pydantic AI shines. You declare a Pydantic model as the
agent's `result_type`, and the framework guarantees the LLM returns valid data conforming to
that schema. PCH's gateway forwards OpenAI's native structured-output protocol intact, so this
works without any special handling on either side.

## Links

- Package on PyPI: [pypi.org/project/pydantic-ai-pathcourse](https://pypi.org/project/pydantic-ai-pathcourse/)
- Source code: [github.com/pathcourse-health/pch-framework-adapters/tree/main/pydantic-ai-pathcourse](https://github.com/pathcourse-health/pch-framework-adapters/tree/main/pydantic-ai-pathcourse)
- Pydantic AI docs: [ai.pydantic.dev](https://ai.pydantic.dev)
