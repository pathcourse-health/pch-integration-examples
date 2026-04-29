/**
 * Vercel AI SDK — simplest one-shot.
 *
 * Run:
 *     npm install @pathcourse/ai ai tsx
 *     export PCH_API_KEY=pch_prod_b_...
 *     npx tsx frameworks/vercel-ai-sdk/generate_text.ts
 *
 * Demonstrates that `pathcourse(model)` is a drop-in for `openai(model)` in
 * any AI SDK call — `generateText`, `generateObject`, `streamText`, etc.
 */

import { generateText } from "ai";
import { pathcourse } from "@pathcourse/ai";

const { text } = await generateText({
  model: pathcourse("pch-fast"),
  prompt: "Explain x402 in one sentence.",
});

console.log(text);
