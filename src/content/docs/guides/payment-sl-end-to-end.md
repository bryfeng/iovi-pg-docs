---
title: Payment SL End To End
description: Run the full Payment SL middleware flow.
sidebar:
  order: 2
---

The Payment SL models a centralized-issuer payment token semantic layer.

Public sandbox:

```text
https://eon-payment-sl-demo-production.up.railway.app
```

API references:

- [Rendered Payment SL reference](/api/payment-sl/)
- [Payment SL OpenAPI JSON](/openapi/payment-sl.openapi.json)
- [EON API Hub](/api/)

## Flow

1. Initialize operator state.
2. Register wallets.
3. Register semantic-layer metadata.
4. Queue issuer or wallet actions.
5. Batch pending actions.
6. Submit or encode the payload.
7. Verify the payload.
8. Read verified balances and logs.

## Endpoint Sequence

Use `BASE=https://eon-payment-sl-demo-production.up.railway.app` for the public sandbox.

```text
POST /operator/init
POST /wallets
POST /semantic-layers
POST /actions/mint
POST /operator/batch
POST /devnet/encode-payload
POST /verifier/accept-latest-batch
GET /balances/{address}
POST /actions/transfer
POST /operator/batch
POST /verifier/accept-latest-batch
GET /verifier/state
GET /verifier/log
```

## Important Boundary

`POST /operator/batch` advances operator-local state and creates a canonical payload. It does not by itself make wallet state verifier-accepted.

Use one of these verification paths:

- `POST /verifier/accept-latest-batch` for fast sandbox replay;
- `POST /verifier/ingest-event` for normalized event ingestion;
- `POST /verifier/sync` for bounded polling against configured base-layer data.

## Read Path

Wallets and apps should read from verifier state:

```http
GET /balances/{address}?source=verifier
GET /verifier/state
GET /verifier/log
```

Operator state is useful for debugging pending work, but it is not the accepted read surface.
