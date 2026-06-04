---
title: Agent Glossary
description: Compact terms for EON agent workflows.
sidebar:
  order: 4
---

## Terms

**Base layer:** UTXO chain that orders transactions and stores scalar `Data`.

**Semantic layer:** Application-specific state machine with its own validity rules.

**Wallet:** VK-derived identity that authorizes semantic intent and owns semantic state.

**Operator:** Role that batches and posts semantic-layer payloads.

**Verifier:** Indexer/replayer that accepts or rejects semantic-layer transitions.

**UTXO Data:** Opaque scalar vector attached to a base-layer output.

**Payload hex:** Canonical byte payload encoded as hex before scalar framing.

**Data scalars:** Scalar words suitable for EON UTXO `Data`.

**Bundle:** Atomic wrapper containing multiple child semantic-layer payloads.

**Settlement SL:** Semantic layer that records clearing terms and expected bundle legs.

**Issuer SL:** Semantic layer that owns asset balances and policy.

**Checkpoint:** Latest verifier-accepted state for one semantic layer and version.
