---
title: Marketplace AMM Bundle
description: Use the bundler and verifier APIs for marketplace settlement flows.
sidebar:
  order: 5
---

The marketplace stack coordinates cross-semantic-layer movement with bundle payloads.

## Service Roles

- Bundler API builds or wraps payloads.
- Generic verifier ingests ordered events and commits accepted checkpoints.
- Issuer plugins own asset balances and policy.
- Settlement plugin owns clearing records.
- AMM plugin owns pool state.

## Discover Assets And Pools

```http
GET /assets
GET /pools
GET /pools/{pool_id}
```

## Quote A Swap

```http
GET /quotes/exact-in?pool_id=...&input_sl_id=...&input_version=0001&input_asset_id=USD&amount_in=100
```

## Build Marketplace Actions

```http
POST /pools/create
POST /pools/approve
POST /pools/add-liquidity
POST /pools/remove-liquidity
POST /swaps/exact-in
```

Responses include:

```json
{
  "bundle_id": "32-byte-hex",
  "settlement_id": "settlement-...",
  "payload_hex": "hex",
  "data_scalars": ["0x..."],
  "child_payload_hex": ["hex"],
  "child_count": 3
}
```

## Verify A Bundle

Post the returned `data_scalars` as a normalized verifier event:

```http
POST /verifier/ingest-event
```

Then read:

```http
GET /verifier/state?sl_id=00040001&version=0001
GET /verifier/log
```
