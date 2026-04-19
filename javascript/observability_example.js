/**
 * Observability example — trace a multi-step workflow.
 *
 * Traces group related PCH calls so you can later inspect cost, latency,
 * and decision flow. Useful for debugging agent loops and attributing
 * spend across sub-tasks.
 *
 * Run:
 *     npm install @pathcourse/sdk
 *     PCH_API_KEY=pch_prod_b_... node javascript/observability_example.js
 */

import { PathCourseClient, PCH_FAST } from '@pathcourse/sdk';

async function main() {
  const apiKey = process.env.PCH_API_KEY;
  if (!apiKey) { console.error('PCH_API_KEY env var required.'); process.exit(1); }

  const client = new PathCourseClient({ apiKey });

  // Close any leftover open trace — only one can be active per agent
  const openList = await client.obs.listTraces({ status: 'open', limit: 5 });
  for (const t of (openList.traces || [])) {
    await client.obs.traceEnd({ traceId: t.trace_id });
  }

  const trace = await client.obs.traceStart({ traceLabel: 'demo-research-run' });
  const traceId = trace.trace_id;
  console.log('trace_id:', traceId);

  // Milestone event — metadata on the trace, no billable call
  await client.obs.logEvent({
    traceId,
    eventType:    'milestone',
    eventPayload: { step: 'starting' },
  });

  // An actual PCH call — the gateway auto-attributes this span to the trace
  const resp = await client.chat({
    messages:  [{ role: 'user', content: 'One-sentence summary of x402' }],
    model:     PCH_FAST,
    maxTokens: 80,
  });
  console.log('inference response:', JSON.stringify(resp.content));

  const end = await client.obs.traceEnd({ traceId });
  console.log('trace closed: status=', end.trace_status);

  const full = await client.obs.getTrace(traceId);
  console.log('span count:', full.span_count);
  console.log('total cost:', full.total_cost_usdc, 'USDC');

  const an = await client.obs.analytics({ days: 7 });
  console.log('\n7-day analytics:', an);
}

main().catch((err) => { console.error(err); process.exit(1); });
