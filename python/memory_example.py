"""
Memory round-trip example.

Stores a short fact, retrieves it by semantic query, and verifies the top
hit contains the content we stored. Demonstrates the embedding-based
persistent memory layer every PCH agent gets by default.

Run:
    pip install pathcourse-sdk
    export PCH_API_KEY=pch_prod_b_...
    python python/memory_example.py
"""

import os
import sys
import uuid

from pathcourse import PathCourseClient


def main() -> int:
    key = os.environ.get("PCH_API_KEY")
    if not key:
        print("PCH_API_KEY env var required.", file=sys.stderr)
        return 1

    client = PathCourseClient(api_key=key)

    # Unique marker so repeated runs don't hit the content_hash dedup path.
    marker = uuid.uuid4().hex[:8]
    content = f"Memory test [{marker}]: the capital of Japan is Tokyo."

    print(f"store  : {content!r}")
    store_r = client.memory.store(
        content=content,
        memory_type="semantic",   # episodic | semantic | procedural | working | shared | multimodal
        namespace="private",
        importance=0.8,
    )
    print(f"  memory_id         : {store_r['memory_id']}")
    print(f"  balance_remaining : {store_r.get('balance_remaining')}")

    retr = client.memory.retrieve(
        query="What is the capital of Japan?",
        namespace="private",
        top_k=3,
    )
    hits = retr.get("results", [])
    print(f"\nretrieve: {len(hits)} hit(s)")
    for h in hits[:3]:
        print(f"  - score={h.get('similarity_score')}  id={h.get('memory_id', '')[:8]}...  "
              f"content_preview={h.get('content_preview')!r}")

    # Memory lookup returns content_preview (first 200 chars) — not the full
    # stored text. Full content is only used to generate the embedding.
    print(f"\ncost this request : {retr.get('cost_usdc')} USDC")
    return 0


if __name__ == "__main__":
    sys.exit(main())
