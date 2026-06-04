---
title: Bundler And Marketplace API
description: Endpoint inventory for bundle wrapping and marketplace AMM flows.
sidebar:
  order: 3
---

OpenAPI artifacts:

```text
eon-docs/src/content/openapi/bundler-engine.openapi.json
eon-docs/src/content/openapi/marketplace-bundler.openapi.json
```

## Generic Bundler Engine

```text
GET /health
POST /bundles/wrap
```

`POST /bundles/wrap` accepts a bundle ID and child payload hex values, then returns wrapper payload hex plus scalar `Data`.

## Marketplace Bundler Extensions

```text
GET /
GET /health
POST /bundles/wrap
GET /assets
GET /pools
GET /pools/{pool_id}
GET /quotes/exact-in
POST /pools/create
POST /pools/approve
POST /pools/add-liquidity
POST /pools/remove-liquidity
POST /swaps/exact-in
```

## Common Response Fields

Marketplace action responses include:

```json
{
  "bundle_id": "32-byte-hex",
  "settlement_id": "settlement-...",
  "payload_hex": "hex",
  "data_scalars": ["0x..."],
  "child_payload_hex": ["hex"],
  "child_count": 3,
  "action": {},
  "preflight": {}
}
```
