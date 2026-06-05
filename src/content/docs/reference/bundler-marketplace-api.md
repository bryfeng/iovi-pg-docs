---
title: Bundler And Marketplace API
description: Endpoint inventory for bundle wrapping and marketplace AMM flows.
sidebar:
  order: 4
  hidden: true
---

Rendered references and schemas:

- [Bundler Engine rendered API reference](/api/bundler-engine/)
- [Bundler Engine OpenAPI JSON](/openapi/bundler-engine.openapi.json)
- [Marketplace rendered API reference](/api/marketplace/)
- [Marketplace OpenAPI JSON](/openapi/marketplace-bundler.openapi.json)
- [Live Swagger](https://bundler-production-b637.up.railway.app/docs)
- [Live ReDoc](https://bundler-production-b637.up.railway.app/redoc)

Public base URL:

```text
https://bundler-production-b637.up.railway.app
```

## When To Use These APIs

Use the generic bundler engine to wrap child semantic-layer payloads into a parent bundle payload. Use the marketplace extensions for AMM-style quote, liquidity, approval, swap, and settlement flows.

Trust boundary: bundles preserve transport and settlement ordering, but each child semantic layer still owns validity and replay semantics.

Status: public bundler/marketplace endpoint. The generic bundler and marketplace extension schemas currently share the same Railway deployment.

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
