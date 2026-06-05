---
title: Base Layer API
description: Endpoint inventory for the base-layer posting and read service.
sidebar:
  order: 5
  hidden: true
---

The base-layer API is a small HTTP service around EON SDK reads and posting.

Use this reference when a service needs to post UTXO transfers with scalar `Data`, inspect wallet address and balance, or read UTXOs and transactions. Semantic-layer meaning is not interpreted here.

Rendered reference and schema:

- [Base-Layer rendered API reference](/api/base-layer/)
- [Base-Layer OpenAPI JSON](/openapi/base-layer.openapi.json)

Public base URL:

```text
https://iovi-api-production.up.railway.app
```

Status: public base-layer API. The live service does not expose Swagger, ReDoc, or `/openapi.json` today, so this checked-in schema is the canonical public reference.

## Endpoints

```text
GET /health
GET /wallet/address
GET /balance?owner=0x...
GET /utxos?owner=0x...&limit=10
GET /transactions/{hash}
POST /transactions/transfer
```

## Transfer With Data

```http
POST /transactions/transfer
```

```json
{
  "recipient": "0x...",
  "amount": 100,
  "fee": 1,
  "data": [12345, "0x00003039"]
}
```

Write routes may require `POSTER_API_KEY`. Send it as `x-api-key` or `Authorization: Bearer` when a key is issued.

## Environment

```text
EON_WALLET_FILE
EON_WALLET_B64
POSTER_API_KEY
EON_API_URL
HOST
PORT
```
