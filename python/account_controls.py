"""
Account controls — balance, usage, runway, budget caps, webhook alerts.

Everything an autonomous agent needs to monitor its own spend and avoid
running out of USDC mid-workflow.

Run:
    pip install pathcourse-sdk
    export PCH_API_KEY=pch_prod_b_...
    python python/account_controls.py
"""

import json
import os
import sys

from pathcourse import PathCourseClient


def main() -> int:
    key = os.environ.get("PCH_API_KEY")
    if not key:
        print("PCH_API_KEY env var required.", file=sys.stderr)
        return 1

    client = PathCourseClient(api_key=key)

    # Single-call self-profile: identity + tier + balance + Path Score + 24h activity
    print("--- me() ---")
    print(json.dumps(client.me(), indent=2))

    # Balance (also embedded in me() but callable standalone)
    print("\n--- get_balance() ---")
    print(json.dumps(client.get_balance(), indent=2))

    # Spend ledger (per-request history)
    print("\n--- get_usage(limit=5) ---")
    print(json.dumps(client.get_usage(limit=5), indent=2))

    # Runway forecast — "days of service remaining at current burn rate"
    print("\n--- get_runway() ---")
    print(json.dumps(client.get_runway(), indent=2))

    # Tier-scoped model list
    print("\n--- get_models(scope='my_tier') ---")
    print(json.dumps(client.get_models(scope="my_tier"), indent=2))

    # Daily budget cap (server-enforced, resets at UTC midnight)
    print("\n--- set_budget($1.00/day) ---")
    print(json.dumps(client.set_budget(daily_limit_usdc=1.00), indent=2))
    print("\n--- get_budget() ---")
    print(json.dumps(client.get_budget(), indent=2))
    print("\n--- set_budget(0) to remove cap ---")
    print(json.dumps(client.set_budget(daily_limit_usdc=0), indent=2))

    # Webhook alerts fire when balance crosses threshold
    # (commented out — uncomment + point at a real URL to enable)
    # print("\n--- register_webhook ---")
    # print(json.dumps(client.register_webhook(
    #     url="https://your-service.example.com/pch-alerts",
    #     threshold_usdc=25.0,
    # ), indent=2))
    # print("\n--- get_webhook ---")
    # print(json.dumps(client.get_webhook(), indent=2))

    return 0


if __name__ == "__main__":
    sys.exit(main())
