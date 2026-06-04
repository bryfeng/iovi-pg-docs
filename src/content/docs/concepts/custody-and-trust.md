---
title: Custody And Trust
description: How to reason about semantic ownership and money-like assets.
sidebar:
  order: 7
---

The current architecture is coherent because the base-layer UTXO is a publication vehicle, not necessarily the asset itself.

For identity, app state, metadata, reputation, and sandbox assets, this model is natural:

```text
wallet authorizes semantic transition
operator posts ordered payload
verifier reconstructs wallet state
```

## Money-Like Assets

For money-like assets, authorization alone is not enough. The wallet should eventually have a way to recover or withdraw value if an operator disappears, censors, or publishes bad state.

Future production designs may add:

- signed and expiring intents;
- fraud or validity proofs;
- exit/challenge windows;
- data-availability guarantees;
- wallet-carried proof chains;
- federated or multisig custody boundaries where appropriate.

## Current Safe Wording

Use this wording in docs and agent prompts:

```text
The operator transports wallet-authorized semantic proofs to the base layer.
The operator is not the source of truth for ownership.
Verifier rules, wallet authorization, and canonical ordering define accepted semantic state.
```
