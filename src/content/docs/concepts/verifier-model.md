---
title: Verifier Model
description: What the verifier owns and what it deliberately does not own.
sidebar:
  order: 5
---

The verifier is the authority for derived semantic-layer state.

It owns:

- normalized base-event ingestion;
- plugin routing by `SL_ID` and version;
- transition replay;
- checkpoint updates;
- atomic bundle execution;
- verified state and log reads.

It does not own:

- marketplace matching;
- asset-specific policy outside the relevant plugin;
- wallet custody;
- base-layer consensus;
- production authorization secrets.

## Single Transition

For a single semantic-layer payload, the verifier decodes the transition, loads the previous checkpoint, replays the plugin logic, and commits the next checkpoint if the result matches the payload commitment.

## Bundle Transition

For a bundle payload, the verifier unwraps child payloads and stages every child checkpoint. It commits all staged updates only if every child verifies.

That all-or-none commit is the current bundle atomicity boundary.
