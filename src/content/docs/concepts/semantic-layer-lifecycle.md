---
title: Semantic Layer Lifecycle
description: How a semantic layer moves from registry metadata to verified state.
sidebar:
  order: 4
---

A semantic layer moves through a simple lifecycle.

## 1. Define The Layer

Choose:

- `sl_id`;
- `version`;
- operator wallet address;
- base-layer posting account;
- asset metadata if the layer tracks assets;
- verifier rules and payload format.

## 2. Initialize State

The middleware creates genesis operator state and sets the next sequence number to `1`.

## 3. Queue Inputs

Wallets, issuers, or applications submit semantic intents such as mint, burn, transfer, freeze, asset registration, or marketplace bundle operations.

## 4. Batch Inputs

The operator runs `F(S, Input)`, applies valid actions, rejects invalid actions, and emits a canonical payload with previous and new state hashes.

## 5. Publish Data

The payload is encoded into scalar `Data` and can be posted to EON through the base-layer API or a submitter command.

## 6. Verify

The verifier ingests the payload, checks ordering and state hashes, replays semantic rules, and stores a checkpoint.

## 7. Read Verified State

Wallets, apps, and agents read balances, state, events, and logs from the verifier-facing API, not from operator-local state.
