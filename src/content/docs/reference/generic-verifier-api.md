---
title: Generic Verifier API
description: Endpoint inventory for verifier ingestion and read APIs.
sidebar:
  order: 2
---

OpenAPI artifact:

```text
eon-docs/src/content/openapi/generic-verifier.openapi.json
```

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
