---
title: Constraints And Defaults
description: Operational constraints agents should preserve.
sidebar:
  order: 4
---

## Defaults

```text
Payment SL ID: 00010001
Version: 0001
Stock SL ID: 00020001
USD SL ID: 00020002
Settlement SL ID: 00030001
AMM SL ID: 00040001
```

Semantic-layer IDs are hex strings. The public sandbox rejects non-hex `sl_id` values.

## Current Auth Caveat

The sandbox transfer path accepts raw VK and checks:

```text
Hash(vk) == from_address
```

Always describe this as demo authorization.

## Canonical Read Source

Prefer verifier reads:

```text
GET /balances/{address}?source=verifier
GET /verifier/state
GET /verifier/log
```

Use operator reads only for pending state, debugging, or pre-verification previews.

## Payload Rule

EON `Data` is scalar-oriented. Agents should not post arbitrary JSON directly to UTXO data. Encode to payload bytes, then scalar framing.

## Money-Like Assets

When assets are money-like, mention that future production deployments need signed intents, replay protection, and an exit/challenge or recovery model.
