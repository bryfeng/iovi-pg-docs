---
title: Payment SL Middleware API
description: Endpoint inventory for the hosted Payment SL middleware API.
sidebar:
  order: 2
  hidden: true
---

Rendered reference and schema:

- [Payment SL rendered API reference](/api/payment-sl/)
- [Payment SL OpenAPI JSON](/openapi/payment-sl.openapi.json)
- [Live Swagger](https://eon-payment-sl-demo-production.up.railway.app/docs)
- [Live ReDoc](https://eon-payment-sl-demo-production.up.railway.app/redoc)

## When To Use This API

Use this API for the current Payment SL middleware loop: wallet registration, semantic-layer registration, action creation, operator batching, devnet submission boundaries, and local verifier acceptance.

The key boundary is: the operator transports semantic-layer payloads to base-layer UTXO `Data`; wallets own semantic state through VK-derived identity; verifiers decide what state is accepted.

## Endpoint Groups

### Health And Config

```text
GET /
GET /health
GET /config
POST /reset
```

### Operator Lifecycle

```text
POST /operator/init
GET /operator/state
POST /operator/batch
GET /operator/batches
GET /operator/latest-payload
```

### Registries

```text
POST /wallets
GET /wallets
GET /wallets/{address}
POST /base-layer/accounts
GET /base-layer/accounts
POST /base-layer/accounts/generate
POST /semantic-layers
GET /semantic-layers
GET /semantic-layers/workbench-state
POST /semantic-layers/{sl_id}/assets
```

### Actions

```text
GET /balances/{address}
POST /actions/mint
POST /actions/burn
POST /actions/freeze
POST /actions/unfreeze
POST /actions/transfer
GET /pending
GET /pending/all
```

### Devnet And Verification

```text
POST /devnet/encode-payload
GET /devnet/status
POST /devnet/submit-latest-batch
GET /verifier/state
GET /verifier/log
GET /verifier/events
POST /verifier/sync
POST /verifier/accept-latest-batch
POST /verifier/accept-envelope
POST /verifier/envelope-from-payload
POST /verifier/ingest-event
```

## Full Endpoint Inventory

```text
GET /
GET /health
GET /config
POST /reset
POST /operator/init
GET /operator/state
POST /wallets
GET /wallets
GET /wallets/{address}
POST /base-layer/accounts
GET /base-layer/accounts
POST /base-layer/accounts/generate
POST /semantic-layers
GET /semantic-layers
GET /semantic-layers/workbench-state
POST /semantic-layers/{sl_id}/assets
GET /balances/{address}
POST /actions/mint
POST /actions/burn
POST /actions/freeze
POST /actions/unfreeze
POST /actions/transfer
GET /pending
GET /pending/all
POST /operator/batch
GET /operator/batches
GET /operator/latest-payload
POST /devnet/encode-payload
GET /devnet/status
POST /devnet/submit-latest-batch
GET /verifier/state
GET /verifier/log
GET /verifier/events
POST /verifier/sync
POST /verifier/accept-latest-batch
POST /verifier/accept-envelope
POST /verifier/envelope-from-payload
POST /verifier/ingest-event
```

## Default Base URL

```text
PUBLIC_EON_PAYMENT_API_URL
PUBLIC_PAYMENT_SL_API_URL
```

The playground default is:

```text
https://eon-payment-sl-demo-production.up.railway.app
```

First public check:

```bash
curl https://eon-payment-sl-demo-production.up.railway.app/health
```

## Canonical Flow

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
```

## Important Boundaries

- Operator state is useful for batching, but verifier reads are the accepted semantic-layer state.
- Raw VK submission is serviceable for the playground and should become signed intents or production auth downstream.
- Scalar encoding proves that payload bytes can be carried as `Data`; it does not prove final base-layer inclusion.
