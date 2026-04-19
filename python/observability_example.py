"""
Observability example — trace a multi-step workflow.

Traces group related PCH calls so you can later inspect cost, latency,
and decision flow. Useful for debugging agent loops and attributing spend
across sub-tasks.

Run:
    pip install pathcourse-sdk
    export PCH_API_KEY=pch_prod_b_...
    python python/observability_example.py
"""

import os
import sys

from pathcourse import PathCourseClient, PCH_FAST


def main() -> int:
    key = os.environ.get("PCH_API_KEY")
    if not key:
        print("PCH_API_KEY env var required.", file=sys.stderr)
        return 1

    client = PathCourseClient(api_key=key)

    # Close any leftover open trace — only one can be active per agent
    for t in (client.obs.list_traces(status="open", limit=5).get("traces", []) or []):
        client.obs.trace_end(trace_id=t["trace_id"])

    trace = client.obs.trace_start(trace_label="demo-research-run")
    trace_id = trace["trace_id"]
    print(f"trace_id: {trace_id}")

    # Milestone event — attaches metadata to the trace without a billable call
    client.obs.log_event(
        trace_id,
        event_type="milestone",
        event_payload={"step": "starting"},
    )

    # An actual PCH call — the gateway auto-attributes this span to the trace
    resp = client.chat(
        messages=[{"role": "user", "content": "One-sentence summary of x402"}],
        model=PCH_FAST,
        max_tokens=80,
    )
    print(f"inference response: {resp.content!r}")

    # Close the trace
    end = client.obs.trace_end(trace_id=trace_id)
    print(f"trace closed: status={end.get('trace_status')}")

    # Pull the full trace + any spans recorded
    full = client.obs.get_trace(trace_id)
    print(f"span count : {full.get('span_count')}")
    print(f"total cost : {full.get('total_cost_usdc')} USDC")

    # Rolling analytics across all recent traces
    an = client.obs.analytics(days=7)
    print(f"\n7-day analytics: {an}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
