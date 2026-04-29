# LangChain (Python) — `langchain-pathcourse`

Drop-in `ChatOpenAI` replacement. Every LangChain chain, agent, tool, and memory module
works unchanged.

## Install

```bash
pip install langchain-pathcourse
export PCH_API_KEY=pch_prod_b_...
```

## Examples

| File | What it shows |
|---|---|
| [`01_chat.py`](./01_chat.py) | Simplest one-shot — single message in, single response out |
| [`02_chain.py`](./02_chain.py) | LCEL chain: prompt template → LLM → parser |
| [`03_agent.py`](./03_agent.py) | Tool-using agent with two tools |

## How it differs from `ChatOpenAI`

```python
# Before
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o-mini")

# After
from langchain_pathcourse import ChatPathCourse
llm = ChatPathCourse(model="pch-fast")
```

`ChatPathCourse` extends `ChatOpenAI`, so the rest of your code is unchanged. Streaming, tool
calls, structured output, async, callbacks — all work the same way.

## Embeddings

```python
from langchain_pathcourse import PathCourseEmbeddings

embeddings = PathCourseEmbeddings()      # uses pch-embed
vector = embeddings.embed_query("Path Score")
```

`PathCourseEmbeddings` works with every LangChain vector store (FAISS, Chroma, Pinecone,
pgvector, etc.).

## Links

- Package on PyPI: [pypi.org/project/langchain-pathcourse](https://pypi.org/project/langchain-pathcourse/)
- Source code: [github.com/pathcourse-health/pch-framework-adapters/tree/main/langchain-pathcourse](https://github.com/pathcourse-health/pch-framework-adapters/tree/main/langchain-pathcourse)
- LangChain docs: [python.langchain.com](https://python.langchain.com)
