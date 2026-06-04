---
title: Marketplace Bundles
description: How cross-semantic-layer marketplace events are represented.
sidebar:
  order: 6
---

Marketplace bundles coordinate value and state across semantic layers.

The bundle wrapper is an atomic envelope:

```text
Bundle Wrapper
  Settlement child
  Issuer child A
  Issuer child B
  Optional AMM or fee child
```

## Roles

- **Marketplace:** discovery, order entry, quotes, and UX.
- **Bundler:** constructs compatible child payloads and wraps them.
- **Settlement SL:** records clearing terms and expected legs.
- **Issuer SLs:** apply asset-specific movements.
- **Verifier:** checks every child and commits all or none.

## Trust Boundary

The marketplace and bundler are useful coordinators. They are not final truth. Wallets and observers should rely on verifier-accepted state.

## Current Implementation

The deployable stack exposes:

- generic bundle wrapping;
- asset and pool reads;
- exact-in quotes;
- pool creation;
- pool approval;
- liquidity operations;
- exact-in swaps.
