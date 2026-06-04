---
title: Agent Quickstart
description: Task-oriented entrypoint for AI agents using EON semantic-layer services.
sidebar:
  order: 1
---

Use this page when an AI agent needs to spin up a semantic layer or transact within one.

API entrypoints:

- [API Hub](/api/)
- [Payment SL OpenAPI JSON](/openapi/payment-sl.openapi.json)
- [Rendered Payment SL reference](/api/payment-sl/)

Default public sandbox:

```text
https://eon-payment-sl-demo-production.up.railway.app
```

## Safe Model

```text
operator posts UTXO, wallet owns semantic state
```

Do not imply the wallet receives the posting UTXO unless the UTXO is explicitly designed as a carrier asset.

## Spin Up A Payment Semantic Layer

Call in order against the selected `BASE` URL:

```text
POST /operator/init
POST /wallets                    # create or register operator wallet
POST /base-layer/accounts/generate
POST /semantic-layers
POST /semantic-layers/{sl_id}/assets
GET /semantic-layers/workbench-state
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
POST /wallets
POST /actions/mint
POST /operator/batch
POST /verifier/accept-latest-batch
GET /balances/{address}
POST /actions/transfer
POST /operator/batch
POST /verifier/accept-latest-batch
GET /balances/{address}
GET /verifier/log
```

## Verify A Base-Layer Event

Use the normalized event boundary:

```text
POST /verifier/ingest-event
GET /verifier/state
GET /verifier/log
```

## Do Not

- Do not treat operator state as final wallet state.
- Do not claim EON verifies semantic-layer validity on the base layer.
- Do not call raw VK submission production custody.
- Do not call devnet scalar encoding a successful base-layer write.
- Do not invent hosted URLs for verifier, bundler, marketplace, or base-layer services. Use their published schemas unless a deployment URL is supplied.
