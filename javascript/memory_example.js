/**
 * Memory round-trip example.
 *
 * Stores a short fact, retrieves it by semantic query, shows the top hit.
 *
 * Run:
 *     npm install @pathcourse/sdk
 *     PCH_API_KEY=pch_prod_b_... node javascript/memory_example.js
 */

import { randomUUID } from 'node:crypto';
import { PathCourseClient } from '@pathcourse/sdk';

async function main() {
  const apiKey = process.env.PCH_API_KEY;
  if (!apiKey) { console.error('PCH_API_KEY env var required.'); process.exit(1); }

  const client = new PathCourseClient({ apiKey });

  const marker  = randomUUID().slice(0, 8);
  const content = `Memory test [${marker}]: the capital of Japan is Tokyo.`;

  console.log('store  :', JSON.stringify(content));
  const storeR = await client.memory.store({
    content,
    memoryType: 'semantic',   // episodic | semantic | procedural | working | shared | multimodal
    namespace:  'private',
    importance: 0.8,
  });
  console.log('  memory_id        :', storeR.memory_id);
  console.log('  balance_remaining:', storeR.balance_remaining);

  const retr = await client.memory.retrieve({
    query:     'What is the capital of Japan?',
    namespace: 'private',
    topK:      3,
  });
  const hits = retr.results || [];
  console.log(`\nretrieve: ${hits.length} hit(s)`);
  for (const h of hits.slice(0, 3)) {
    console.log(
      `  - score=${h.similarity_score}  id=${(h.memory_id || '').slice(0, 8)}...  ` +
      `content_preview=${JSON.stringify(h.content_preview)}`
    );
  }

  // Memory retrieve returns content_preview (first 200 chars) — not full
  // stored text. Full content is only used to generate the embedding.
  console.log('\ncost this request:', retr.cost_usdc, 'USDC');
}

main().catch((err) => { console.error(err); process.exit(1); });
