# AutoGen / AG2 — `autogen-pathcourse`

Run AutoGen / AG2 multi-agent conversations on PCH. Group chat, code execution, function
calling, custom agents — all unchanged.

## Install

```bash
# AutoGen (Microsoft's original)
pip install pyautogen autogen-pathcourse

# AG2 (community fork)
pip install ag2 autogen-pathcourse

export PCH_API_KEY=pch_prod_b_...
```

## Examples

| File | What it shows |
|---|---|
| [`01_assistant.py`](./01_assistant.py) | Single AssistantAgent + UserProxyAgent — the "hello world" of AutoGen |
| [`02_group_chat.py`](./02_group_chat.py) | Three-agent group chat with mixed PCH models |

## How it works

```python
from autogen import AssistantAgent
from autogen_pathcourse import pch_config

assistant = AssistantAgent(
    name="assistant",
    llm_config={"config_list": pch_config(model="pch-pro")},
    system_message="You are a helpful AI assistant.",
)
```

`pch_config(model)` returns the `config_list` AutoGen expects, with `base_url` pointing at
the PCH gateway and `api_type: "openai"`. AutoGen treats it like any OpenAI-compatible
endpoint, so all features work.

## Per-agent model selection

Run different agents on different PCH models in the same group chat:

```python
planner  = AssistantAgent(name="planner",  llm_config={"config_list": pch_config(model="pch-pro")})
coder    = AssistantAgent(name="coder",    llm_config={"config_list": pch_config(model="pch-coder")})
reviewer = AssistantAgent(name="reviewer", llm_config={"config_list": pch_config(model="pch-fast")})
```

## Links

- Package on PyPI: [pypi.org/project/autogen-pathcourse](https://pypi.org/project/autogen-pathcourse/)
- Source code: [github.com/pathcourse-health/pch-framework-adapters/tree/main/autogen-pathcourse](https://github.com/pathcourse-health/pch-framework-adapters/tree/main/autogen-pathcourse)
- AutoGen docs: [microsoft.github.io/autogen](https://microsoft.github.io/autogen)
- AG2 docs: [ag2.ai](https://ag2.ai)
