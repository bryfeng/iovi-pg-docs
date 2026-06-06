---
title: Agent Quickstart
description: Task-oriented entrypoint for AI agents using IOVI semantic-layer services.
sidebar:
  order: 1
---

Use this page when an AI agent needs to spin up a semantic layer or transact within one.

API entrypoints:

- [API Hub](/api/)
- [Agent Smoke Test](/agents/smoke-test/)
- [Payment SL OpenAPI JSON](/openapi/payment-sl.openapi.json)
- [Rendered Payment SL reference](/api/payment-sl/)
- [Rendered Generic Verifier reference](/api/generic-verifier/)
- [Rendered Bundler reference](/api/bundler-engine/)
- [Rendered Marketplace reference](/api/marketplace/)
- [Rendered Base-Layer reference](/api/base-layer/)

Default public services:

```text
PAYMENT_SL=https://eon-payment-sl-demo-production.up.railway.app
VERIFIER=https://verifier-production-7dc3.up.railway.app
BUNDLER_MARKETPLACE=https://bundler-production-b637.up.railway.app
BASE_LAYER=https://iovi-api-production.up.railway.app
```

Prefer the UI first? Open the [IOVI Playground](https://iovi-payment-sl-playground.vercel.app/) and return here for exact endpoint ordering.

## Service Ownership

| Service variable | Owns | Use it for |
| --- | --- | --- |
| `PAYMENT_SL` | Payment semantic-layer sandbox middleware | wallets, semantic-layer registry, actions, batching, devnet submit, embedded sandbox verifier reads |
| `VERIFIER` | Generic verifier service | normalized base-layer event ingestion and accepted state for generic semantic-layer payloads |
| `BUNDLER_MARKETPLACE` | Bundler and marketplace stack | bundle wrapping, AMM quotes, swaps, settlement payloads |
| `BASE_LAYER` | Base-layer posting/read API | wallet address, balance, UTXOs, transfer-with-Data posting |

`PAYMENT_SL` includes embedded verifier endpoints for the sandbox Payment SL flow. `VERIFIER` is the standalone Generic Verifier service. Do not mix those unless the task explicitly crosses from sandbox middleware into generic event ingestion.

## Safe Model

```text
operator posts UTXO, wallet owns semantic state
```

Do not imply the wallet receives the posting UTXO unless the UTXO is explicitly designed as a carrier asset.

`sl_id` values must be hex strings. Use `00010001` for the default Payment SL, or generate isolated test lanes such as `a9bca654`.

## Spin Up A Payment Semantic Layer

Call in order against `PAYMENT_SL`:

```text
PAYMENT_SL POST /wallets                         # create or register operator wallet
PAYMENT_SL POST /operator/init                   # initialize that semantic-layer lane
PAYMENT_SL POST /base-layer/accounts/generate    # optional for devnet posting
PAYMENT_SL POST /semantic-layers
PAYMENT_SL POST /semantic-layers/{sl_id}/assets
PAYMENT_SL GET  /semantic-layers/workbench-state
```

Minimum semantic-layer record:

```json
{
  "name": "Payment SL",
  "sl_id": "00010001",
  "version": "0001",
  "operator_wallet_address": "40_hex_chars",
  "base_layer_account_id": "acct_..."
}
```

## Transact Within A Semantic Layer

Call in order:

```text
PAYMENT_SL POST /wallets
PAYMENT_SL POST /actions/mint
PAYMENT_SL POST /operator/batch
PAYMENT_SL POST /verifier/accept-latest-batch
PAYMENT_SL GET  /balances/{address}
PAYMENT_SL POST /actions/transfer
PAYMENT_SL POST /operator/batch
PAYMENT_SL POST /verifier/accept-latest-batch
PAYMENT_SL GET  /balances/{address}
PAYMENT_SL GET  /verifier/log
```

For the devnet-backed path, replace local accept with:

```text
PAYMENT_SL GET  /devnet/status
PAYMENT_SL POST /devnet/submit-latest-batch
PAYMENT_SL POST /verifier/sync
```

## Verify A Base-Layer Event

Use the normalized event boundary:

```text
GENERIC_VERIFIER POST /verifier/ingest-event
GENERIC_VERIFIER GET  /verifier/state
GENERIC_VERIFIER GET  /verifier/log
```

## Do Not

- Do not treat operator state as final wallet state.
- Do not claim EON verifies semantic-layer validity on the base layer.
- Do not call raw VK submission production custody.
- Do not call devnet scalar encoding a successful base-layer write.
- Do not invent hosted URLs. Use the public URLs above unless the user supplies their own deployment.
