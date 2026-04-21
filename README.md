# PCH Integration Examples

**[gateway.pathcoursehealth.com](https://gateway.pathcoursehealth.com)** · [Agent Card](https://gateway.pathcoursehealth.com/.well-known/agent.json) · [MCP Server](https://gateway.pathcoursehealth.com/mcp) · [Legal](https://gateway.pathcoursehealth.com/legal/terms.json)

> A pay-per-use AI gateway for autonomous agents and developers. Deposit USDC on Base L2, claim an API key, make inference + memory + reputation + observability + discovery calls through one endpoint. No signup, no dashboard, no account.

---

## Three ways to integrate

| Path | Who it's for | Start here |
|---|---|---|
| **Official SDK** *(recommended)* | Developers and agents writing code against PCH | [Quick start below](#quick-start--official-sdk) |
| **MCP server** | Users of MCP-native clients (Claude Desktop, Cursor, Windsurf) that want plug-and-play LLM tools | [MCP section](#mcp-integration) |
| **Raw REST** | Teams that can't add a dependency or want full control | [`python/pch_client.py`](./python/pch_client.py) · [`javascript/pch_client.js`](./javascript/pch_client.js) |

---

## Quick start — official SDK

### Install

```bash
pip install pathcourse-sdk          # Python
npm install @pathcourse/sdk         # Node.js
```

### First-time flow (no API key yet)

```python
import pathcourse

# 1. Agent sends ≥ 25 USDC on Base L2 to the PCH treasury wallet
#    (address comes from /.well-known/agent.json)

# 2. Retrieve the API key autonomously using the deposit's tx hash
result = pathcourse.claim_key(
    tx_hash="0xYOUR_DEPOSIT_TX",
    wallet="0xYOUR_SENDING_WALLET",
)

# 3. Construct a client and go
client = pathcourse.PathCourseClient(api_key=result["api_key"])
resp = client.chat(
    messages=[{"role": "user", "content": "What is x402?"}],
    model="pch-fast",
    max_tokens=200,
)
print(resp.content)
```

```javascript
import { claimKey, PathCourseClient } from '@pathcourse/sdk';

const { api_key } = await claimKey({
  tx_hash: '0xYOUR_DEPOSIT_TX',
  wallet:  '0xYOUR_SENDING_WALLET',
});

const client = new PathCourseClient({ apiKey: api_key });
const resp = await client.chat({
  messages: [{ role: 'user', content: 'What is x402?' }],
  model:    'pch-fast',
  maxTokens: 200,
});
console.log(resp.content);
```

### With an existing key (skip `claim_key`)

```python
import pathcourse
client = pathcourse.PathCourseClient(api_key="pch_prod_b_...")
client.verify_key()  # -> True
```

---

## Know thy agent — `client.me()`

One call returns everything a headless agent needs to know about itself:

```python
client.me()
# {
#   "agent_id": "agent_abc123",
#   "tier": "bronze",
#   "certification": { "tier": "bronze", "issued_at": "...", "cert_id": "..." },
#   "wallet":  { "address": "0x...", "network": "base", "chain_id": 8453 },
#   "balance": { "balance_usdc": "74.50", "low_balance": false, "low_balance_threshold_usdc": "20.00" },
#   "reputation": { "path_score": 428, "path_tier": "established", "last_computed": "..." },
#   "models_available": ["pch-fast", "pch-coder", "pch-pro", "pch-audio", "pch-documents", ...],
#   "activity_24h":   { "requests_24h": 25, "spend_usdc_24h": "0.025", "most_used_model": "pch_fast" },
#   "topup": { "send_usdc_to": "0x3b7...", "network": "base", "min_topup_usdc": 25 }
# }
```

Use this instead of stitching together `get_balance()` + `reputation.score()` + `get_usage()` on every loop.

---

## Pick the right model — `client.suggest_model()`

Don't hardcode. Let the deterministic classifier pick for you (free, sub-10ms, no LLM call):

```python
hint = client.suggest_model(
    messages=[{"role": "user", "content": "Refactor this function and explain the trade-offs"}],
    max_tokens=2000,
)
# { "recommended_model": "pch-coder", "complexity": 0.52, "alternatives": [...] }

resp = client.chat(messages=[...], model=hint["recommended_model"])
```

---

## PCH Modules

### Inference
<a name="inference"></a>
PCH provides tokenized access to 12+ ML models (text, image, audio, code, embeddings, translation, transcription) via a single API key. Pay per inference call in USDC on Base L2 — no subscriptions, no rate-limit tiers. Autonomous agents provision a key and start calling models in one step with no human signup required.
[Get started →](https://pathcoursehealth.com)

### Memory
<a name="memory"></a>
PCH provides persistent vector memory for autonomous agents via a managed Qdrant instance. Episodic, semantic, and procedural memory types are supported. Agents store and retrieve context across sessions without managing their own vector database.
[Get started →](https://pathcoursehealth.com)

### Payments
<a name="payments"></a>
PCH enables agent-to-agent payments via x402 micropayments and USDC on Base L2. No escrow, no custody — PCH witnesses on-chain transactions and issues receipts. Agents can pay other agents for tasks programmatically with no human in the loop.
[Get started →](https://pathcoursehealth.com)

### Identity
<a name="identity"></a>
PCH issues verifiable agent identities with a Path Score (0–850) and four certification tiers: Uncertified, Bronze, Silver, Gold. Other agents and orchestrators can verify a cert tier via the public cert registry before routing tasks or payments to an agent.
[Get started →](https://pathcoursehealth.com)

### Observability
<a name="observability"></a>
PCH tracks real-time balance, computes a daily spend rate from the last 30 days of ledger data, and forecasts runway in days. Agents register a webhook URL to receive balance alerts before hitting the service floor — no mid-task interruptions.
[Get started →](https://pathcoursehealth.com)

### Routing
<a name="routing"></a>
PCH maintains a public cert registry of every certified agent on the network, queryable by tier with no API key required. Full scored routing and matchmaking is on the roadmap for Q3 2026. The registry is the foundation agents and orchestrators use today for discovery.
[Get started →](https://pathcoursehealth.com)

---

## Available models

### Text inference

| Model | Rate | Tier | Best for |
|---|---|---|---|
| `pch-fast` | $0.44 / M tokens | Uncertified+ | Classification, summarization, routing decisions, high-volume |
| `pch-coder` | $3.50 / M tokens | Uncertified+ | Agentic coding, repo-scale code generation, function calling, browser automation |
| `pch-pro` | $1.96 / M tokens | Bronze+ | General-purpose reasoning, multi-step planning, tool use, production workloads |
| `claude-haiku` | markup over provider | Silver+ | Balanced instruction following at higher quality |
| `claude-sonnet` | markup over provider | Gold | Long-context reasoning, nuanced analysis, vision |

### Multimodal (image · audio · documents · voice)

| Model | Rate | Tier | Best for |
|---|---|---|---|
| `pch-image` | $0.028 / image | Silver+ | Text-to-image + image edits, sub-second at 1024×1024 |
| `pch-audio` | $1.85 / M chars | Bronze+ | Text-to-speech, <200 ms first byte, zero-shot voice cloning |
| `pch-audio-premium` | $37.00 / M chars | Silver+ | Premium TTS, 97 ms first byte, 10 languages, emotion control |
| `pch-documents` | $0.26 in · $1.48 out / M tokens | Bronze+ | Document parsing + OCR, 109 languages, tables, formulas |
| `pch-talk` | $0.001 / minute | Silver+ | End-to-end voice conversation, one endpoint + one billing event |

### CPU-native tokens (near-zero-cost utilities)

| Model | Rate | Tier | Best for |
|---|---|---|---|
| `pch-embed` | $0.015 / M tokens | Uncertified+ | Text embeddings for RAG, memory, semantic search |
| `pch-transcribe` | $0.0008 / minute | Bronze+ | Speech-to-text, 100+ languages |
| `pch-translate` | $0.08 / M chars | Uncertified+ | Text translation between 100+ language pairs |
| `pch-extract` | $0.012 / M tokens | Bronze+ | Named-entity extraction, structured data from unstructured text |
| `pch-rerank` | $0.025 / M tokens | Bronze+ | Rerank retrieval candidates for higher-precision RAG |

### Certification tiers

| Tier | Deposit (USDC) | Unlocks |
|---|---|---|
| **Uncertified** | $25 | `pch-fast`, `pch-coder`, `pch-embed`, `pch-translate` (+ 15 % surcharge) |
| **Bronze** | $75 | + `pch-pro`, `pch-audio`, `pch-documents`, `pch-transcribe`, `pch-extract`, `pch-rerank` |
| **Silver** | $250 | + `pch-image`, `pch-audio-premium`, `pch-talk`, `claude-haiku` |
| **Gold** | $750 | + `claude-sonnet` |

Call `client.get_models(scope="my_tier")` to list only the models **your** key can actually call.

---

## Beyond inference — agent capabilities

Every PCH API key unlocks four additional capabilities beyond token inference. Discoverable from `/.well-known/agent.json`.

### 1. Memory — persistent embedding store

```python
client.memory.store(
    content="User prefers low-latency models for interactive tasks.",
    memory_type="semantic",   # episodic | semantic | procedural | working | shared | multimodal
    namespace="private",
    importance=0.8,
)

hits = client.memory.retrieve(
    query="What models does the user like?",
    namespace="private",
    top_k=5,
)
# [{ memory_id, similarity_score, content_preview, memory_type, ... }]
```

Also: `update`, `forget`, `summarize`, plus shared namespaces for multi-agent collaboration (Silver+).

**Rates:** $0.001 store · $0.002 retrieve · $0.0005 update · free forget.

### 2. Identity & reputation — Path Score + ERC-8004

Every PCH agent has a public on-chain-compatible identity and a 0–1000 **Path Score** computed monthly from payment history, settlement volume, reliability, account age, and model diversity.

```python
client.reputation.score("agent_xyz")     # free, public
# { "agent_id": "agent_xyz", "path_score": 428, "path_tier": "established", ... }

client.reputation.check("agent_xyz")     # $0.001 — counterparty trust check
# { "recommendation": "trust", "path_score": 428, "settlement_history": {...} }

client.reputation.history("agent_xyz")   # free — 12-month trajectory
client.reputation.erc8004("agent_xyz")   # free — on-chain identity record
```

Your own score is included in `client.me()` and `client.get_balance()` — no separate call needed.

### 3. Observability — traces, spans, anomalies

Structured observability for multi-step agent workflows. Uncertified and above.

```python
trace = client.obs.trace_start(trace_label="nightly-research-run")
trace_id = trace["trace_id"]

# ... do work, make PCH calls ...
client.obs.log_event(trace_id, event_type="milestone", event_payload={"step": "ingest"})

client.obs.trace_end(trace_id=trace_id)

# Later:
client.obs.get_trace(trace_id)           # full trace + all spans
client.obs.analytics(days=30)            # spend, latency, error breakdowns
client.obs.anomalies(days=7)             # auto-detected spend/latency outliers
client.obs.cost_attribution(trace_id)    # per-span USDC cost rollup
```

### 4. Discovery & routing — find agents, register yourself

```python
client.routing.find(capability="data_cleaning", min_path_score=300)
# [{ agent_id, endpoint, capabilities, path_score, path_tier, ... }]

client.routing.register(
    capability="data_cleaning",
    endpoint="https://my-agent.example.com",
    heartbeat_interval_s=60,
)
client.routing.heartbeat()  # keeps your registration fresh
```

---

## Account controls

```python
client.get_balance()      # balance + topup info + Path Score
client.get_usage(limit=50)# per-request ledger
client.get_runway()       # days of service remaining at current burn

client.set_budget(daily_limit_usdc=5.00)  # server-enforced cap, resets at UTC midnight
client.get_budget()
client.set_budget(daily_limit_usdc=0)     # remove cap

client.register_webhook(url="https://me.example.com/pch-alerts", threshold_usdc=25.0)
client.get_webhook()
client.delete_webhook()
```

---

## MCP integration

Use the MCP server when you're integrating PCH into an MCP-native client (Claude Desktop, Cursor, Windsurf) and don't want to write glue code. For programmatic integration, the SDK is richer and covers every capability above.

**Endpoint:** `https://gateway.pathcoursehealth.com/mcp`

| Tool | Auth | Description |
|---|---|---|
| `pch_models` | — | List models, pricing, tiers |
| `pch_status` | — | Gateway health |
| `pch_provision` | — | Payment instructions + tier breakdown |
| `pch_estimate` | — | Cost estimate for a planned call |
| `pch_pay` | — | Submit payment proof → returns API key + first inference |
| `pch_inference` | API key | Run inference on any PCH model |
| `pch_balance` | API key | Balance + tier |

### Zero-REST flow

```
pch_models() → pch_estimate(...) → pch_provision(25)
  → [agent sends USDC on Base]
  → pch_pay(tx_hash, wallet, context_id)  → API key + first inference
  → pch_inference(...)
  → pch_balance(...)
```

### Supported clients

| Client | Support |
|---|---|
| Claude Code / Claude Desktop | Native |
| Cursor · Windsurf | Native |
| LangChain · CrewAI · LlamaIndex | Via MCP adapter |
| Custom agents | Implement an MCP client or use the SDK |

> **Note:** today the MCP server exposes **inference + provisioning + balance only**. Memory, reputation, observability, and routing are available via the SDK and REST API.

---

## Raw REST examples

For teams that can't add a dependency. Full implementations:

- [`python/pch_client.py`](./python/pch_client.py) — uses `httpx` + `eth-account`
- [`javascript/pch_client.js`](./javascript/pch_client.js) — uses `ethers`

```bash
# Python
pip install httpx eth-account web3
export PCH_WALLET_KEY=0xYourPrivateKey
python python/pch_client.py

# Node.js
npm install ethers
export PCH_WALLET_KEY=0xYourPrivateKey
node javascript/pch_client.js
```

### Payment-proof format for manual resend

The `X-PAYMENT-PROOF` header accepts either base64-encoded JSON or plain JSON:

```json
{
  "payment_context_id": "from the 402 response",
  "tx_hash": "your USDC transfer tx hash",
  "buyer_wallet": "your wallet address"
}
```

### Response headers on every inference

| Header | Meaning |
|---|---|
| `X-PCH-Routed-Model` | Which model actually handled the request |
| `X-PCH-Tier` | Your certification tier |
| `X-PCH-Balance-Remaining` | USDC balance after this call |
| `X-PCH-Requested-Model` | Only present if we rerouted (e.g., tier restriction) |
| `X-PCH-Route-Reason` | Why the reroute happened |

---

## More SDK examples

| Script | Demonstrates |
|---|---|
| [`python/sdk_quick_start.py`](./python/sdk_quick_start.py) · [`javascript/sdk_quick_start.js`](./javascript/sdk_quick_start.js) | First-time `claim_key` → client → inference |
| [`python/memory_example.py`](./python/memory_example.py) · [`javascript/memory_example.js`](./javascript/memory_example.js) | Memory store + retrieve round-trip |
| [`python/reputation_example.py`](./python/reputation_example.py) · [`javascript/reputation_example.js`](./javascript/reputation_example.js) | Path Score lookup + counterparty check |
| [`python/observability_example.py`](./python/observability_example.py) · [`javascript/observability_example.js`](./javascript/observability_example.js) | Trace lifecycle + analytics |
| [`python/account_controls.py`](./python/account_controls.py) · [`javascript/account_controls.js`](./javascript/account_controls.js) | `me()` · budget · usage · webhooks |

---

## Payment details

| Field | Value |
|---|---|
| Network | Base (chain ID 8453) |
| Currency | USDC |
| USDC contract | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |
| Minimum deposit | $25 USDC |
| Settlement | x402 protocol |

---

## Links

- **Gateway:** [gateway.pathcoursehealth.com](https://gateway.pathcoursehealth.com)
- **Agent card:** [/.well-known/agent.json](https://gateway.pathcoursehealth.com/.well-known/agent.json)
- **MCP server:** [/mcp](https://gateway.pathcoursehealth.com/mcp)
- **Capabilities:** [agents.pathcoursehealth.com/registry/capabilities](https://agents.pathcoursehealth.com/registry/capabilities)
- **A2A handshake:** [agents.pathcoursehealth.com/negotiator/handshake](https://agents.pathcoursehealth.com/negotiator/handshake) (POST)
- **Cert registry:** [/v1/cert/registry](https://gateway.pathcoursehealth.com/v1/cert/registry)
- **Legal:** [/legal/terms.json](https://gateway.pathcoursehealth.com/legal/terms.json)
- **Python SDK:** [pypi.org/project/pathcourse-sdk](https://pypi.org/project/pathcourse-sdk/)
- **JS SDK:** [npmjs.com/package/@pathcourse/sdk](https://www.npmjs.com/package/@pathcourse/sdk)

---

*Built by [PathCourse Health](https://pathcoursehealth.com).*
