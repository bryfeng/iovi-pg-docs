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

`GET /assets` returns verifier-indexed assets plus capability flags. An asset is pool-ready when it has `amm_asset_movements`; this means its semantic-layer verifier can consume bundle-bound pool movement actions such as `pool_swap_in`, `pool_swap_out`, `pool_deposit`, and `pool_withdraw`.

Payment SL assets are transferable when registered. To participate in marketplace bundles, their Payment SL lane must also be tracked by the marketplace verifier so the asset child transition can be verified atomically with AMM and settlement children.

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

## Swap Requirements

For an exact-in swap bundle to verify:

- both asset refs must exist in accepted verifier state;
- the pool must exist in accepted AMM state for those exact asset refs;
- the trader VK must match the input asset owner address;
- the input asset state must have sufficient verified balance;
- the output asset state must have sufficient pool escrow;
- AMM quote math must produce `amount_out >= min_amount_out`;
- every asset movement must reference the same `bundle_id` and match one AMM movement leg;
- settlement must observe the same child legs declared in the bundle;
- all child transitions must advance from the verifier's latest accepted checkpoints.
