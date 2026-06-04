---
title: UTXO Data Bus
description: How EON UTXO data works as the rollup bus for semantic layers.
sidebar:
  order: 3
---

The current architecture treats base-layer UTXOs as a rollup bus.

The UTXO is not always the asset. It is often the transport:

1. A wallet, issuer, or application creates semantic-layer input.
2. An operator batches or packages the input.
3. The operator posts scalar `Data` through a base-layer UTXO.
4. Verifiers read ordered outputs and decode the payload.
5. Semantic-layer state updates if replay succeeds.

## Data Is Scalar-Oriented

EON `Data` is an ordered vector of scalar values, not native JSON.

Richer data needs an application-level encoding:

```text
application payload
-> canonical bytes
-> framed scalar values
-> UTXO Data
```

Decoding reverses the process:

```text
UTXO Data
-> scalar values
-> payload bytes
-> semantic-layer payload
```

## Why The Bus Model Works

The bus gives semantic layers:

- canonical ordering;
- retrievable payloads;
- a shared publication substrate;
- independent verifier replay;
- room to choose raw inputs, compressed inputs, commitments, or proofs later.
