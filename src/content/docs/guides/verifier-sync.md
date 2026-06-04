---
title: Verifier Sync
description: Bring ordered base-layer data into verifier-accepted semantic state.
sidebar:
  order: 4
---

The verifier accepts normalized base events. A normalized event is the adapter boundary between EON data-bearing outputs and semantic-layer replay.

## Ingest One Event

```http
POST /verifier/ingest-event
```

```json
{
  "cursor": "devnet:1:0:0",
  "network_id": "devnet",
  "height": 1,
  "tx_hash": "0x...",
  "tx_index": 0,
  "output_index": 0,
  "utxo_id": "0x...",
  "owner": "0x...",
  "amount": "1",
  "data_scalars": ["0x..."]
}
```

## Poll For A Batch

```http
POST /verifier/sync
```

```json
{
  "sl_id": "00010001",
  "version": "0001",
  "posting_owner": "0x64_hex_chars",
  "expected_sequence": 8,
  "expected_state_hash": "hex",
  "timeout_seconds": 120,
  "poll_interval_seconds": 5
}
```

`status: "verified"` means the checkpoint reached the expected sequence and state hash.

`status: "timeout"` means the payload may still exist on the base layer, but this verifier has not observed and accepted it yet.

## Read Results

```http
GET /verifier/events
GET /verifier/state?sl_id=00010001&version=0001
GET /verifier/log?sl_id=00010001
```
