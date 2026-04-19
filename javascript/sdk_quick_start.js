/**
 * SDK quick start — autonomous first-time flow.
 *
 * Run:
 *     npm install @pathcourse/sdk
 *     node javascript/sdk_quick_start.js --tx 0x... --wallet 0x...
 *
 * What this does:
 * 1. Calls claimKey({ tx_hash, wallet }) to retrieve an API key for your
 *    on-chain deposit. Polls up to ~3 min while the gateway reconciles
 *    your USDC transfer on Base.
 * 2. Constructs a PathCourseClient with the returned key.
 * 3. Makes a single pch-fast inference call so you can verify the full loop.
 *
 * If you already have a saved API key, set PCH_API_KEY and skip --tx/--wallet.
 */

import { claimKey, PathCourseClient, PCH_FAST } from '@pathcourse/sdk';

function argFlag(name) {
  const i = process.argv.indexOf(`--${name}`);
  return i >= 0 ? process.argv[i + 1] : null;
}

async function main() {
  let apiKey = process.env.PCH_API_KEY;

  if (!apiKey) {
    const tx     = argFlag('tx');
    const wallet = argFlag('wallet');
    if (!tx || !wallet) {
      console.error('Provide PCH_API_KEY, or both --tx and --wallet.');
      process.exit(1);
    }
    console.log(`Claiming API key for deposit ${tx.slice(0, 10)}...`);
    const r = await claimKey({ tx_hash: tx, wallet });
    apiKey = r.api_key;
    console.log(`  tier     : ${r.tier}`);
    console.log(`  balance  : ${r.balance_usdc} USDC`);
    console.log(`  agent_id : ${r.agent_id}`);
    console.log('  Save this key — it is only shown once.');
  }

  const client = new PathCourseClient({ apiKey });
  if (!(await client.verifyKey())) throw new Error('API key rejected by gateway');
  console.log('verify_key -> OK\n');

  const resp = await client.chat({
    messages:  [{ role: 'user', content: 'Reply with exactly: SDK smoke test OK' }],
    model:     PCH_FAST,
    maxTokens: 20,
  });
  console.log('model    :', resp.model);
  console.log('response :', JSON.stringify(resp.content));
  console.log('usage    :', resp.usage);
}

main().catch((err) => { console.error(err); process.exit(1); });
