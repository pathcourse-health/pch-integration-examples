/**
 * Vercel AI SDK — Next.js streaming chat route.
 *
 * File location:
 *     app/api/chat/route.ts
 *
 * Setup:
 *     npm install @pathcourse/ai ai
 *     # .env.local
 *     PCH_API_KEY=pch_prod_b_...
 *
 * What this does:
 * Pairs with the `useChat` hook on the client. Every message the user types
 * gets streamed back token-by-token from PCH via `streamText`. This is the
 * exact pattern every Vercel AI SDK chat tutorial uses — the only change is
 * `pathcourse(...)` instead of `openai(...)`.
 */

import { streamText } from "ai";
import { pathcourse } from "@pathcourse/ai";

export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = await streamText({
    model: pathcourse("pch-fast"),
    messages,
  });

  return result.toDataStreamResponse();
}
