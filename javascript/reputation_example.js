/**
 * Reputation example — Path Score lookup + counterparty trust check.
 *
 * Path Score is a 0–850 reputation metric computed monthly from payment
 * history, settlement volume, reliability, account age, and model diversity.
 * Every PCH agent has one. It surfaces in /v1/balance, /v1/me, and
 * /v1/reputation/score/{agent_id}.
 *
 * Run:
 *     npm install @pathcourse/sdk
 *     PCH_API_KEY=pch_prod_b_... node javascript/reputation_example.js <other_agent_id>
 */

import { PathCourseClient } from '@pathcourse/sdk';

async function main() {
  const apiKey = process.env.PCH_API_KEY;
  if (!apiKey) { console.error('PCH_API_KEY env var required.'); process.exit(1); }

  const client = new PathCourseClient({ apiKey });

  // Your own score, embedded in the self-profile
  const me = await client.me();
  console.log('Your score:');
  console.log('  agent_id  :', me.agent_id);
  console.log('  path_score:', me.reputation.path_score);
  console.log('  path_tier :', me.reputation.path_tier);

  // Public lookup for another agent (free)
  const target = process.argv[2] || me.agent_id;
  console.log(`\nPublic score lookup for ${target}:`);
  try {
    const s = await client.reputation.score(target);
    console.log('  path_score   :', s.path_score);
    console.log('  path_tier    :', s.path_tier);
    console.log('  last_computed:', s.last_computed);
  } catch (err) {
    console.log(`  ${err.name}: ${err.message}`);
  }

  // Counterparty trust check — $0.001, returns recommendation + settlement history
  console.log(`\nCounterparty check for ${target} (costs $0.001):`);
  try {
    console.log(' ', await client.reputation.check(target));
  } catch (err) {
    console.log(`  ${err.name}: ${err.message}`);
  }
}

main().catch((err) => { console.error(err); process.exit(1); });
