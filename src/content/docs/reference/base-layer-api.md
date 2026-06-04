---
title: Base Layer API
description: Endpoint inventory for the base-layer posting and read service.
sidebar:
  order: 4
---

The base-layer API is a small HTTP service around EON SDK reads and posting.

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

Write routes require `POSTER_API_KEY` when configured. Send it as `x-api-key` or `Authorization: Bearer`.

## Environment

```text
EON_WALLET_FILE
EON_WALLET_B64
POSTER_API_KEY
EON_API_URL
HOST
PORT
```
