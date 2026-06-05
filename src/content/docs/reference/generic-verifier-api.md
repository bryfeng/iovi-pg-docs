---
title: Generic Verifier API
description: Endpoint inventory for verifier ingestion and read APIs.
sidebar:
  order: 3
  hidden: true
---

Rendered reference and schema:

- [Generic Verifier rendered API reference](/api/generic-verifier/)
- [Generic Verifier OpenAPI JSON](/openapi/generic-verifier.openapi.json)
- [Live Swagger](https://verifier-production-7dc3.up.railway.app/docs)
- [Live ReDoc](https://verifier-production-7dc3.up.railway.app/redoc)

Public base URL:

```text
https://verifier-production-7dc3.up.railway.app
```

## When To Use This API

Use this API when a semantic layer needs to ingest ordered UTXO data and replay it through local validity rules. The verifier is the service that turns observed base-layer data into accepted semantic-layer state.

Acceptance rule: read `/verifier/state` or `/verifier/log` after ingesting events; do not treat operator state or scalar encoding as final.

Status: public verifier endpoint. State reads require an `sl_id`; the current marketplace verifier root advertises `amm_sl_id` as `00040001`.

## Endpoints

```text
GET /health
POST /verifier/ingest-event
GET /verifier/events
GET /verifier/state
GET /verifier/log
```

## Ingest Event

```http
POST /verifier/ingest-event
```

```json
{
  "cursor": "devnet:1:0:0",
  "network_id": "devnet",
  "height": 1,
  "block_hash": null,
  "tx_hash": "0x...",
  "tx_index": 0,
  "output_index": 0,
  "utxo_id": "0x...",
  "owner": "0x...",
  "amount": "1",
  "data_scalars": ["0x..."],
  "payload_hex": null,
  "event_key": null
}
```

## Read State

```http
GET /verifier/state?sl_id=00010001&version=0001
GET /verifier/log?sl_id=00010001
GET /verifier/events
```
