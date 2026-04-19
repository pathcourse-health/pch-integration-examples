/**
 * Account controls — balance, usage, runway, budget caps, webhook alerts.
 *
 * Everything an autonomous agent needs to monitor its own spend and avoid
 * running out of USDC mid-workflow.
 *
 * Run:
 *     npm install @pathcourse/sdk
 *     PCH_API_KEY=pch_prod_b_... node javascript/account_controls.js
 */

import { PathCourseClient } from '@pathcourse/sdk';

const log = (label, val) => console.log(`\n--- ${label} ---\n${JSON.stringify(val, null, 2)}`);

async function main() {
  const apiKey = process.env.PCH_API_KEY;
  if (!apiKey) { console.error('PCH_API_KEY env var required.'); process.exit(1); }

  const client = new PathCourseClient({ apiKey });

  // Single-call self-profile: identity + tier + balance + Path Score + 24h activity
  log('me()',                 await client.me());

  // Balance (also embedded in me() but callable standalone)
  log('getBalance()',         await client.getBalance());

  // Per-request ledger
  log('getUsage({limit:5})',  await client.getUsage({ limit: 5 }));

  // Runway forecast
  log('getRunway()',          await client.getRunway());

  // Tier-scoped model list
  log("getModels({scope:'my_tier'})", await client.getModels({ scope: 'my_tier' }));

  // Daily budget cap (server-enforced, resets at UTC midnight)
  log('setBudget($1.00/day)', await client.setBudget({ dailyLimitUsdc: 1.00 }));
  log('getBudget()',          await client.getBudget());
  log('setBudget(0)',         await client.setBudget({ dailyLimitUsdc: 0 }));

  // Webhook alerts fire when balance crosses threshold
  // (uncomment and point at a real URL to enable)
  // log('registerWebhook', await client.registerWebhook({
  //   url: 'https://your-service.example.com/pch-alerts',
  //   thresholdUsdc: 25.0,
  // }));
  // log('getWebhook', await client.getWebhook());
}

main().catch((err) => { console.error(err); process.exit(1); });
