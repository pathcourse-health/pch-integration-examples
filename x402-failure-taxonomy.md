# x402 Failure Taxonomy — PCH Implementation

This document describes the structured failure-class envelope returned by
PCH's x402 gateway on every 4xx/503 response in the payment flow. It mirrors
the canonical enum at
[`gateway/lib/x402_failures.js`](https://github.com/pathcourse-health/pch-platform/blob/master/gateway/lib/x402_failures.js)
in the (private) gateway repository — this file is the public reference for
external integrators (notably the
[`presidio-hardened-x402`](https://github.com/presidio-hardened-x402)
conformance test suite).

**Live endpoints:**

- **Mainnet** (real Base USDC, $5 minimum deposit):
  `POST https://gateway.pathcoursehealth.com/v1/chat/completions`
- **Sepolia** (testnet USDC at `0x036CbD53842c5426634e7929541eC2318f3dCF7e`):
  `POST https://gateway-sepolia.pathcoursehealth.com/v1/chat/completions`

Hit either with no `Authorization` header and no `X-API-KEY` to receive a
spec-compliant 402 with `chain_id` (8453 mainnet / 84532 Sepolia) and a
5-minute `payment_context_id`. POST is required — GET returns 404 (no
browser-navigation handler by design).

---

## Response envelope

Every 4xx/503 response from the payment path carries this shape:

```json
{
  "error":   "<legacy-error-code>",
  "message": "<human-readable explanation>",
  "failure": {
    "type":    "<one of 8 failure types>",
    "subtype": "<one of 18 subtypes, or null>",
    "message": "<same as top-level message>",
    "<extra fields per type>": "..."
  }
}
```

The top-level `error` and `message` fields are preserved for backwards
compatibility. New integrations should branch on `failure.type` /
`failure.subtype`.

---

## The 8 failure types

| Type | HTTP | Meaning |
|---|---|---|
| `invalid_proof` | 400 | The `X-PAYMENT-PROOF` header is malformed, undecodable, or missing required fields. |
| `metadata_mismatch` | 400 | The proof references a real `payment_context_id`, but a field in the proof disagrees with what the gateway recorded (tx hash, sender wallet, amount, chain). |
| `underpayment` | 402 | The on-chain payment was successfully received, but the amount is less than `payment_context.required_amount_usdc`. |
| `expired` | 410 | The `payment_context` is past its `expires_at` (5-minute TTL) or its proof has aged out. |
| `replay_rejected` | 409 | An attempt to reuse a finalized payment (already-paid context, already-processed tx hash). |
| `policy_violation` | 403 | The request violates a gateway policy: tier-too-low for the requested model, unsupported scheme, etc. |
| `provisioning_timeout` | 503 | Payment was valid but the auto-provisioner exceeded its 55-second SLA. Retry the resend with the same `X-PAYMENT-PROOF`. |
| `configuration_error` | 503 | Gateway misconfiguration (treasury wallet missing, facilitator unreachable). Should never fire in healthy deployment. |

---

## The 18 subtypes

### `invalid_proof` subtypes

- `proof_decode_failed` — `X-PAYMENT-PROOF` couldn't be base64-decoded, or the decoded body is not valid JSON.
- `missing_required_fields` — the proof JSON is missing one or more of: `payment_context_id`, `tx_hash`, `buyer_wallet`. The `failure.missing_fields` field lists which.

### `metadata_mismatch` subtypes

- `tx_hash_mismatch` — the `tx_hash` in the proof does not match the tx the gateway saw funding the context. `failure.expected` and `failure.got` carry both values.
- `wallet_mismatch` — the `buyer_wallet` in the proof does not match the wallet that funded the context. `failure.expected` and `failure.got` carry both values.
- `amount_below_required` — internal-only signal used by the validator; rarely surfaced.
- `chain_id_mismatch` — proof references the wrong network (e.g. mainnet proof against the Sepolia gateway).
- `context_not_found` — `payment_context_id` is not in Redis and the facilitator fallback couldn't verify it. Either the context expired or never existed.

### `underpayment` subtypes

- `onchain_amount_too_low` — `paid_amount_usdc < required_amount_usdc`. `failure.required_amount_usdc` and `failure.paid_amount_usdc` are both included.

### `expired` subtypes

- `context_expired` — current time exceeds the context's `expires_at`. `failure.expires_at` is included.
- `proof_ttl_exceeded` — proof was generated against a context that has since aged out.

### `replay_rejected` subtypes

- `context_already_paid` — the context's status is already `paid` and the proof references a different `tx_hash` than the one that paid it.
- `tx_already_processed` — the tx hash is in the gateway's webhook-dedup window (24h).

### `policy_violation` subtypes

- `tier_too_low` — agent's certification tier doesn't allow the requested model.
- `model_not_in_tier` — same as above, surfaced from a different code path.
- `unsupported_scheme` — request specified a scheme other than `x402`.

### `provisioning_timeout` subtypes

- `auto_provisioner_sla` — the Auto-Provisioner ECS task didn't write `provisioned_key:{context_id}` within 55 seconds. Payment was received; retry the resend.

### `configuration_error` subtypes

- `treasury_not_configured` — `PCH_TREASURY_WALLET` not set on the gateway. Should never fire in production.
- `facilitator_unreachable` — the gateway tried the x402 facilitator's `/verify` fallback (when Redis context is missing) and the facilitator returned an error.

---

## Example failure responses

### Malformed proof header

```bash
curl -s -X POST https://gateway-sepolia.pathcoursehealth.com/v1/chat/completions \
  -H 'X-PAYMENT-PROOF: not-valid-base64-or-json' \
  -H 'Content-Type: application/json' \
  -d '{"model":"pch-fast","messages":[{"role":"user","content":"hi"}]}'
```

```json
{
  "error":   "invalid_payment_proof",
  "message": "Invalid X-PAYMENT-PROOF — send base64-encoded or plain JSON: ...",
  "failure": {
    "type":    "invalid_proof",
    "subtype": "proof_decode_failed",
    "message": "Invalid X-PAYMENT-PROOF — send base64-encoded or plain JSON: ..."
  }
}
```

HTTP status: **400**

### Tx-hash mismatch

```json
{
  "error":   "invalid_payment_proof",
  "message": "tx_hash in proof does not match the tx that funded this context",
  "failure": {
    "type":      "metadata_mismatch",
    "subtype":   "tx_hash_mismatch",
    "message":   "tx_hash in proof does not match the tx that funded this context",
    "context_id": "0bb5015f-08df-4b52-beda-36c6fd0a1835",
    "expected":   "0xabc123...",
    "got":        "0xdef456..."
  }
}
```

HTTP status: **400**

### Underpayment

```json
{
  "error":   "underpayment",
  "message": "Underpayment: 2.5 USDC received, 5.0 required",
  "failure": {
    "type":                "underpayment",
    "subtype":             "onchain_amount_too_low",
    "message":             "Underpayment: 2.5 USDC received, 5.0 required",
    "context_id":          "0bb5015f-08df-4b52-beda-36c6fd0a1835",
    "required_amount_usdc": 5.00,
    "paid_amount_usdc":     2.50,
    "tx_hash":              "0xabc123..."
  }
}
```

HTTP status: **402**

### Provisioning timeout

```json
{
  "error":   "provisioning_timeout",
  "message": "Provisioning did not complete within 55 seconds. Your payment was received. Retry with the same X-PAYMENT-PROOF header.",
  "failure": {
    "type":       "provisioning_timeout",
    "subtype":    "auto_provisioner_sla",
    "message":    "Provisioning did not complete within 55 seconds. ...",
    "context_id": "0bb5015f-08df-4b52-beda-36c6fd0a1835"
  }
}
```

HTTP status: **503**

---

## Webhook event for established agents

Established agents (those that have completed at least one provisioning
flow) can register a webhook URL via `billing:{agent_id}:webhook_url`. When
a payment fails for that agent (e.g. an underpayment on a top-up), the
gateway fires a `payment_failed` event:

```json
{
  "event":    "payment_failed",
  "agent_id": "agent_abc...",
  "failure":  {
    "type":    "underpayment",
    "subtype": "onchain_amount_too_low",
    "message": "Underpayment: 2.5 USDC received, 5.0 required",
    "required_amount_usdc": 5.00,
    "paid_amount_usdc":     2.50
  },
  "context": {
    "context_id": "0bb5015f-08df-4b52-beda-36c6fd0a1835",
    "tx_hash":    "0xabc..."
  },
  "ts": "2026-05-03T21:30:00.000Z"
}
```

Webhook events are not fired for anonymous Pattern 1 buyers (no agent_id
yet) — those see the inline 4xx response body instead.

---

## Stability guarantees

- **Failure type names are stable.** Once added, a `type` value will not
  be removed or repurposed. Adding new types is treated as a major change
  and signaled with deprecation warnings on the existing types it might
  affect.
- **Subtype names may grow.** New `subtype` values may be added under
  existing types in any release — treat them as enum-additive. If your
  conformance test asserts on a specific subtype, expect that subtype to
  remain stable; expect new subtypes to appear over time.
- **Top-level `error` and `message` fields stay.** Legacy clients that
  branch on `error` will keep working.

---

## Reporting issues

If your test suite needs a failure type or subtype that doesn't exist yet,
or if you observe a 4xx/503 response that's missing the `failure` block,
open an issue here in `pch-integration-examples` (or in the conformance
suite repo and ping the PCH team). The taxonomy is intentionally extensible.
