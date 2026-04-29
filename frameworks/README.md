# Framework Adapters

Use PathCourse Health from inside the AI agent framework you already use. Every adapter is a
thin wrapper that points the framework's existing OpenAI integration at PCH's gateway. Same
SDK shape, same response format, same streaming — just `pip install` (or `npm install`) and
change one line.

The PCH gateway at `https://gateway.pathcoursehealth.com/v1` is fully OpenAI API-compatible.

## Pick your framework

| Framework | Package | Language | Examples |
|---|---|---|---|
| LangChain | [`langchain-pathcourse`](https://pypi.org/project/langchain-pathcourse/) | Python | [`langchain-python/`](./langchain-python) |
| LangChain.js | [`@pathcourse/langchain`](https://www.npmjs.com/package/@pathcourse/langchain) | TypeScript | [`langchain-js/`](./langchain-js) |
| Vercel AI SDK | [`@pathcourse/ai`](https://www.npmjs.com/package/@pathcourse/ai) | TypeScript / Next.js | [`vercel-ai-sdk/`](./vercel-ai-sdk) |
| CrewAI | [`crewai-pathcourse`](https://pypi.org/project/crewai-pathcourse/) | Python | [`crewai/`](./crewai) |
| Pydantic AI | [`pydantic-ai-pathcourse`](https://pypi.org/project/pydantic-ai-pathcourse/) | Python | [`pydantic-ai/`](./pydantic-ai) |
| AutoGen / AG2 | [`autogen-pathcourse`](https://pypi.org/project/autogen-pathcourse/) | Python | [`autogen/`](./autogen) |

## Authentication (all frameworks)

Set `PCH_API_KEY` in your environment. Get a key at [pathcoursehealth.com](https://pathcoursehealth.com).

```bash
export PCH_API_KEY=pch_prod_b_...
```

If you don't have a key yet, the [autonomous claim flow](../README.md#quick-start--official-sdk)
in the main repo shows how an agent can deposit USDC on Base L2 and claim a key in one call,
no signup required.

## Choosing a model

All adapters accept a `model="..."` argument. The chat-completion models work everywhere:

- Fast response, simple task → `pch-fast`
- Complex reasoning, multi-step → `pch-pro`
- Writing or reviewing code → `pch-coder`
- Long context or premium reasoning → `claude-sonnet` (Gold tier)

Full 15-model catalog: [main README](../README.md#available-models).

## Source code

The adapter packages themselves live in
[`pathcourse-health/pch-framework-adapters`](https://github.com/pathcourse-health/pch-framework-adapters).
This directory is for examples and tutorials — open issues and PRs against this repo for
example improvements, against the adapter monorepo for adapter changes.
