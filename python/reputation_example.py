"""
Reputation example — Path Score lookup + counterparty trust check.

Path Score is a 0–850 reputation metric computed monthly from payment
history, settlement volume, reliability, account age, and model diversity.
Every PCH agent has one. It surfaces in /v1/balance, /v1/me, and
/v1/reputation/score/{agent_id}.

Run:
    pip install pathcourse-sdk
    export PCH_API_KEY=pch_prod_b_...
    python python/reputation_example.py <other_agent_id>
"""

import os
import sys

from pathcourse import PathCourseClient


def main() -> int:
    key = os.environ.get("PCH_API_KEY")
    if not key:
        print("PCH_API_KEY env var required.", file=sys.stderr)
        return 1

    client = PathCourseClient(api_key=key)

    # Your own score, included in the self-profile
    me = client.me()
    print("Your score:")
    print(f"  agent_id   : {me['agent_id']}")
    print(f"  path_score : {me['reputation']['path_score']}")
    print(f"  path_tier  : {me['reputation']['path_tier']}")

    # Optional: look up another agent's public score (free)
    target = sys.argv[1] if len(sys.argv) > 1 else me["agent_id"]
    print(f"\nPublic score lookup for {target}:")
    try:
        s = client.reputation.score(target)
        print(f"  path_score    : {s.get('path_score')}")
        print(f"  path_tier     : {s.get('path_tier')}")
        print(f"  last_computed : {s.get('last_computed')}")
    except Exception as e:
        print(f"  {type(e).__name__}: {e}")

    # Counterparty trust check — $0.001, returns recommendation + settlement history
    print(f"\nCounterparty check for {target} (costs $0.001):")
    try:
        c = client.reputation.check(target)
        print(f"  {c}")
    except Exception as e:
        print(f"  {type(e).__name__}: {e}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
