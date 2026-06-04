---
title: Troubleshooting
description: Common failures when building against EON semantic-layer services.
sidebar:
  order: 6
---

## API Reports Uninitialized

Call:

```http
POST /operator/init
```

If you are intentionally replacing shared state, pass `reset_existing: true`.

## Batch Has No Effect On Balance

Check whether the verifier accepted the batch:

```http
POST /verifier/accept-latest-batch
GET /balances/{address}?source=verifier
```

Operator-local state and verifier-accepted state are separate views.

## Devnet Submission Returns 503

The API is not configured with a live submitter or bound base-layer account. You can still use `POST /devnet/encode-payload` to inspect the scalar payload.

## Transfer Is Rejected

In the current sandbox, transfers must include a raw VK whose hash matches `from_address`.

Production should replace this with signatures or proofs.

## Verifier Sync Times Out

A timeout does not prove the base-layer post is missing. It means the verifier did not observe and accept the expected sequence/hash before the timeout.

Check:

```http
GET /devnet/status
GET /verifier/events
GET /verifier/log
```

## Payload Cannot Decode

Confirm the payload uses the expected scalar framing and semantic-layer payload format. See [Payload And Scalar Framing](../reference/payload-scalar-framing/).
