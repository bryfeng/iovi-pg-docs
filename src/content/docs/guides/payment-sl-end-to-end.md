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
- [IOVI API Hub](/api/)

## Flow

1. Register the operator and user wallets.
2. Initialize operator state for the semantic-layer lane.
3. Register semantic-layer metadata.
4. Queue issuer or wallet actions.
5. Batch pending actions.
6. Optionally inspect or submit the payload.
7. Verify the payload.
8. Read verified balances and logs.

## Endpoint Sequence

Use `BASE=https://eon-payment-sl-demo-production.up.railway.app` for the public sandbox.

```text
POST /wallets                         # operator wallet
POST /wallets                         # user wallets
POST /operator/init
POST /semantic-layers
POST /actions/mint
POST /operator/batch
POST /verifier/accept-latest-batch
GET /balances/{address}
POST /actions/transfer
POST /operator/batch
POST /verifier/accept-latest-batch
GET /verifier/state
GET /verifier/log
```

Create the operator wallet first when you want `POST /operator/init` to bind an `operator_wallet_address`. `GET /health` reports service-level readiness, not whether a fresh `sl_id` lane has already been registered.

After `POST /operator/batch`, use `GET /operator/latest-payload` to inspect the canonical payload for the lane. `POST /devnet/encode-payload` is optional payload framing; it is not required before `POST /verifier/accept-latest-batch`.

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
