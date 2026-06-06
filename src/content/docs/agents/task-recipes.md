---
title: Task Recipes
description: Agent-ready recipes for common EON workflows.
sidebar:
  order: 3
---

## Create A Wallet Registry Entry

Default public services:

```text
PAYMENT_SL=https://eon-payment-sl-demo-production.up.railway.app
VERIFIER=https://verifier-production-7dc3.up.railway.app
BUNDLER_MARKETPLACE=https://bundler-production-b637.up.railway.app
BASE_LAYER=https://iovi-api-production.up.railway.app
```

Exact schemas live in the [API Hub](/api/) and [Payment SL reference](/api/payment-sl/).

Need a runnable end-to-end check first? Use the [Agent Smoke Test](/agents/smoke-test/).

Use hex-only `sl_id` values. The default Payment SL lane is `00010001`; isolated test lanes can be generated as eight hex characters.

```http
POST /wallets
```

```json
{
  "label": "Alice",
  "vk": "alice_vk",
  "kind": "user"
}
```

Store the returned `address`. Do not expose or persist VK material unless the user explicitly asks for sandbox behavior.

## Register A Semantic Layer

```http
POST /semantic-layers
```

```json
{
  "name": "Payment SL",
  "sl_id": "00010001",
  "version": "0001",
  "operator_wallet_address": "40_hex_chars",
  "base_layer_account_id": "acct_...",
  "assets": [
    {
      "asset_id": "PAYMENT",
      "symbol": "USD",
      "name": "Payment token",
      "decimals": 6,
      "asset_type": "fungible"
    }
  ]
}
```

## Move Tokens

```text
POST /actions/transfer
POST /operator/batch
POST /verifier/accept-latest-batch
GET /balances/{recipient}
```

Use `asset_id` when the semantic layer has more than one registered asset.

## Submit To Devnet

```text
GET /devnet/status
POST /operator/batch
POST /devnet/submit-latest-batch
POST /verifier/sync
```

If status is not ready, use `POST /devnet/encode-payload` and report that live submission is unconfigured.

## Build Marketplace Bundle

Use `BUNDLER_MARKETPLACE`.

```text
GET /assets
GET /pools
GET /quotes/exact-in
POST /swaps/exact-in
POST /verifier/ingest-event
GET /verifier/log
```
