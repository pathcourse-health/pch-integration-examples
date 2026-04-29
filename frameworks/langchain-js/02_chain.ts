/**
 * LangChain.js — LCEL chain with PCH.
 *
 * Run:
 *     npm install @pathcourse/langchain @langchain/core tsx
 *     export PCH_API_KEY=pch_prod_b_...
 *     npx tsx frameworks/langchain-js/02_chain.ts
 *
 * Shows that LangChain.js's pipe-composition (LCEL) works against PCH
 * unchanged: prompt template -> ChatPathCourse -> StringOutputParser.
 */

import { StringOutputParser } from "@langchain/core/output_parsers";
import { ChatPromptTemplate } from "@langchain/core/prompts";
import { ChatPathCourse } from "@pathcourse/langchain";

const prompt = ChatPromptTemplate.fromMessages([
  ["system", "You are a concise technical writer. Reply in one paragraph, no bullet lists."],
  ["user", "Explain {topic} for a developer who already knows OpenAI APIs."],
]);

const llm = new ChatPathCourse({ model: "pch-pro" });   // pch-pro for stronger reasoning
const chain = prompt.pipe(llm).pipe(new StringOutputParser());

const result = await chain.invoke({ topic: "autonomous USDC billing on Base L2" });
console.log(result);
