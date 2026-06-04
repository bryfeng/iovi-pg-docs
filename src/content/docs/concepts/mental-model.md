---
title: Mental Model
description: The core EON architecture in one pass.
sidebar:
  order: 1
---

EON separates canonicity from validity.

**Canonicity is shared. Validity is sovereign.**

The base layer gives everyone a common ordered history and retrievable data. It does not parse, execute, or validate semantic-layer payloads. Semantic layers define their own state machines, verification rules, state schemas, and trust boundaries.

## Base Layer

The base layer is UTXO-based. Each output has:

```text
{ Amount, Owner, Data }
```

`Data` is the semantic-layer boundary. It is stored, ordered, and made retrievable, but it is opaque to base-layer nodes.

## Semantic Layer

A semantic layer is a state machine:

```text
S_next = F(S_current, Input)
```

The semantic layer defines:

- the transition function `F`;
- the payload encoding;
- the authorization model;
- the verifier strategy;
- the state and checkpoint model.

## Verifier

A verifier consumes ordered base-layer data and reconstructs semantic-layer state. In the current Path (a) strategy, the operator posts raw inputs plus state-hash commitments, and verifiers re-execute the rules.

For a valid event, the verifier checks:

- the payload framing;
- the semantic-layer ID and version;
- sequence continuity;
- previous state hash;
- action authorization;
- the computed new state hash.

## Operator

The operator is a transport and batching role. It can propose state transitions by posting data, but it should not be the final source of truth for semantic state.

For the current architecture:

```text
operator posts UTXO, wallet owns semantic state
```

The posted UTXO is the publication envelope. It is not necessarily the object owned by the wallet.
