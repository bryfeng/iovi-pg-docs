---
title: Wallets And Identity
description: How VK-derived addresses participate in semantic-layer state.
sidebar:
  order: 2
---

EON identity is based on verification keys.

```text
address = Hash(VK)
```

The current Payment SL sandbox uses raw VK submission for demo authorization:

```text
Hash(vk) == from_address
```

That is not production custody. It is a temporary bridge so the middleware can demonstrate wallet-authorized transfers without implementing signatures or proofs yet.

## Wallet State Versus UTXO Ownership

A wallet may control semantic-layer state without receiving the base-layer UTXO that carried the event. This is aligned with the current design.

The base-layer UTXO acts as a durable ordered message. The wallet owns semantic state because valid semantic-layer rules attribute that state to the wallet address.

## Production Direction

For production money-like assets, replace raw VK submission with:

- signed intents or proof-based authorization;
- nonces or replay protection;
- domain-separated payload signing;
- expiry for marketplace intents;
- an exit, challenge, or recovery path when the semantic asset represents redeemable value.
