/**
 * LangChain.js — simplest possible PCH call.
 *
 * Run:
 *     npm install @pathcourse/langchain tsx
 *     export PCH_API_KEY=pch_prod_b_...
 *     npx tsx frameworks/langchain-js/01_chat.ts
 *
 * Demonstrates that ChatPathCourse is a drop-in for ChatOpenAI — same
 * .invoke() shape, same response object.
 */

import { ChatPathCourse } from "@pathcourse/langchain";

const llm = new ChatPathCourse({ model: "pch-fast" });

const response = await llm.invoke("Explain x402 in one sentence.");
console.log(response.content);
