"""
SDK quick start — autonomous first-time flow.

Run:
    pip install pathcourse-sdk
    python python/sdk_quick_start.py \
        --tx 0xYOUR_DEPOSIT_TX \
        --wallet 0xYOUR_SENDING_WALLET

What this does:
1. Calls pathcourse.claim_key(tx_hash, wallet) to retrieve an API key for
   your on-chain deposit. Polls up to ~3 min while the gateway reconciles
   your USDC transfer on Base.
2. Constructs a PathCourseClient with the returned key.
3. Makes a single pch-fast inference call so you can verify the full loop.

If you already have a saved API key and just want to test the client,
set PCH_API_KEY instead and skip --tx / --wallet.
"""

import argparse
import os
import sys

import pathcourse
from pathcourse import PathCourseClient, PCH_FAST


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tx",     help="Base L2 tx hash of your USDC deposit to the PCH treasury")
    parser.add_argument("--wallet", help="Sending wallet address (0x...)")
    args = parser.parse_args()

    api_key = os.environ.get("PCH_API_KEY")
    if not api_key:
        if not args.tx or not args.wallet:
            print("Provide PCH_API_KEY, or both --tx and --wallet.", file=sys.stderr)
            return 1
        print(f"Claiming API key for deposit {args.tx[:10]}... ", flush=True)
        result = pathcourse.claim_key(tx_hash=args.tx, wallet=args.wallet)
        api_key = result["api_key"]
        print(f"  tier     : {result.get('tier')}")
        print(f"  balance  : {result.get('balance_usdc')} USDC")
        print(f"  agent_id : {result.get('agent_id')}")
        print("  Save this key — it is only shown once.")

    client = PathCourseClient(api_key=api_key)
    assert client.verify_key(), "API key rejected by gateway"
    print("verify_key -> OK\n")

    resp = client.chat(
        messages=[{"role": "user", "content": "Reply with exactly: SDK smoke test OK"}],
        model=PCH_FAST,
        max_tokens=20,
    )
    print(f"model    : {resp.model}")
    print(f"response : {resp.content!r}")
    print(f"usage    : {resp.usage}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
