---
title: Payment SL Middleware API
description: Endpoint inventory for the hosted Payment SL middleware API.
sidebar:
  order: 1
---

OpenAPI artifact:

```text
eon-docs/src/content/openapi/payment-sl.openapi.json
```

## Core Endpoints

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

## Canonical Flow

```text
POST /operator/init
POST /wallets
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
