---
title: Devnet Data Posting
description: Encode and post semantic-layer payloads into EON UTXO Data.
sidebar:
  order: 3
---

EON `Data` is scalar-oriented. Semantic-layer payload bytes must be framed into scalars before posting.

## Encode A Payload

```http
POST /devnet/encode-payload
```

```json
{
  "payload_hex": "hex"
}
```

The response includes:

```json
{
  "payload_hex": "hex",
  "data_scalars": ["0x..."]
}
```

## Submit Latest Batch

```http
POST /devnet/submit-latest-batch
```

```json
{
  "force": false,
  "wait_for_verifier": true,
  "verifier_timeout_seconds": 120,
  "verifier_poll_interval_seconds": 5
}
```

The API returns `503` if no live submitter or bound base-layer account is configured. That is intentional: encoding a payload is not the same thing as writing it to devnet.

## Base-Layer Posting API

The base-layer API also exposes direct transfer posting with scalar data:

- [Rendered Base-Layer reference](/api/base-layer/)
- [Base-Layer OpenAPI JSON](/openapi/base-layer.openapi.json)

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

Use the base-layer API when you need the explicit UTXO transaction surface. Use Payment SL devnet endpoints when you want the middleware to bind the latest semantic-layer batch to the posting account.
