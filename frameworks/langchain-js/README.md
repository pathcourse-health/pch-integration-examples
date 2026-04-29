# LangChain.js — `@pathcourse/langchain`

Drop-in `ChatOpenAI` replacement for LangChain.js. Every chain, agent, tool, and memory module
works unchanged.

## Install

```bash
npm install @pathcourse/langchain
export PCH_API_KEY=pch_prod_b_...
```

## Examples

| File | What it shows |
|---|---|
| [`01_chat.ts`](./01_chat.ts) | Simplest one-shot — single message in, single response out |
| [`02_chain.ts`](./02_chain.ts) | LCEL chain: prompt → LLM → string output parser |

## How it differs from `ChatOpenAI`

```typescript
// Before
import { ChatOpenAI } from "@langchain/openai";
const llm = new ChatOpenAI({ model: "gpt-4o-mini" });

// After
import { ChatPathCourse } from "@pathcourse/langchain";
const llm = new ChatPathCourse({ model: "pch-fast" });
```

## Embeddings

```typescript
import { PathCourseEmbeddings } from "@pathcourse/langchain";

const embeddings = new PathCourseEmbeddings();    // uses pch-embed
const vector = await embeddings.embedQuery("Path Score");
```

`PathCourseEmbeddings` works with every LangChain.js vector store
(MemoryVectorStore, FAISS, Pinecone, Supabase, etc.).

## Links

- Package on npm: [npmjs.com/package/@pathcourse/langchain](https://www.npmjs.com/package/@pathcourse/langchain)
- Source code: [github.com/pathcourse-health/pch-framework-adapters/tree/main/langchain-pathcourse-js](https://github.com/pathcourse-health/pch-framework-adapters/tree/main/langchain-pathcourse-js)
- LangChain.js docs: [js.langchain.com](https://js.langchain.com)
