# Vercel AI SDK — `@pathcourse/ai`

Drop-in `@ai-sdk/openai` replacement. Every Vercel AI SDK feature — `generateText`,
`streamText`, `generateObject`, tool calls, the `useChat` hook — works against PCH.

## Install

```bash
npm install @pathcourse/ai ai
# .env.local
PCH_API_KEY=pch_prod_b_...
```

## Examples

| File | What it shows |
|---|---|
| [`route.ts`](./route.ts) | Next.js streaming chat route — paste into `app/api/chat/route.ts` |
| [`generate_text.ts`](./generate_text.ts) | Simplest one-shot using `generateText` |

## How it differs from `@ai-sdk/openai`

```typescript
// Before
import { openai } from "@ai-sdk/openai";
const result = await generateText({ model: openai("gpt-4o-mini"), prompt });

// After
import { pathcourse } from "@pathcourse/ai";
const result = await generateText({ model: pathcourse("pch-fast"), prompt });
```

## Explicit construction (custom env var, multiple keys, etc.)

```typescript
import { createPathCourse } from "@pathcourse/ai";

const pathcourse = createPathCourse({ apiKey: process.env.PCH_API_KEY_PROD });

const { text } = await generateText({
  model: pathcourse("pch-pro"),
  prompt: "Plan a multi-step research workflow.",
});
```

## Embeddings

```typescript
import { pathcourseEmbedding } from "@pathcourse/ai";
import { embed } from "ai";

const { embedding } = await embed({
  model: pathcourseEmbedding(),
  value: "Path Score",
});
```

## Links

- Package on npm: [npmjs.com/package/@pathcourse/ai](https://www.npmjs.com/package/@pathcourse/ai)
- Source code: [github.com/pathcourse-health/pch-framework-adapters/tree/main/pathcourse-ai-sdk](https://github.com/pathcourse-health/pch-framework-adapters/tree/main/pathcourse-ai-sdk)
- Vercel AI SDK docs: [sdk.vercel.ai](https://sdk.vercel.ai)
