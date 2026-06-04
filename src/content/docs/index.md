---
title: EON Docs
description: Build semantic layers on EON using ordered UTXO data, middleware APIs, verifiers, and agent-ready workflows.
sidebar:
  order: 1
---

EON gives semantic layers a base layer for canonical ordering and retrievable opaque data. The base layer does not decide whether a payload is valid for an application. Each semantic layer owns its own validity rules.

The short version:

- **Base layer:** orders transactions and stores scalar `Data` on UTXOs.
- **Semantic layer:** defines `S_next = F(S_current, Input)` and decides what posted data means.
- **Wallet:** authorizes semantic intent and owns semantic state through VK-derived identity.
- **Operator:** batches or transports semantic-layer inputs to the base layer.
- **Verifier:** reads ordered data, replays semantic rules, and publishes accepted state.

## Start Here

- [Quickstart](guides/quickstart/) for the smallest useful developer loop.
- [Mental Model](concepts/mental-model/) for the architecture and trust boundary.
- [Payment SL End To End](guides/payment-sl-end-to-end/) for the current middleware flow.
- [Agent Quickstart](agents/agent-quickstart/) for AI agents that need to spin up or transact inside a semantic layer.
- Need exact endpoints or schemas? Start with the external-facing [API Hub](/api/).

## Current Docs Boundary

These docs describe the current serviceable implementation and the intended direction. The system already supports semantic-layer registration, wallet registry, operator batching, payload scalar framing, devnet submission boundaries, verifier replay, and marketplace bundle construction.

Downstream work remains: signed intents, stronger replay protection, richer devnet polling, production custody replacing raw VK submission, and exit/challenge mechanics for money-like assets.
