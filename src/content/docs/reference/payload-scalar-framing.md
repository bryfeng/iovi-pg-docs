---
title: Payload And Scalar Framing
description: Reference for semantic-layer transition payloads, bundle payloads, and scalar framing.
sidebar:
  order: 5
---

EON base-layer `Data` stores scalar values. Semantic-layer payloads use a framing convention to move between bytes and scalars.

## Transition Payload

Generic semantic-layer child payload:

```text
[SL_ID:4]
[version:2]
[sequence:8]
[prev_state_hash:32]
[new_state_hash:32]
[action_count:2]
[action_len:2][action_json]
...
```

Codecs:

```python
encode_transition_payload(...)
decode_transition_payload(...)
payload_header(payload)
```

Source package:

```text
eon-protocol-schemas/eon_protocol/codecs.py
```

## Bundle Wrapper Payload

```text
[BUNDLE_SL_ID:4]
[version:2]
[bundle_id:32]
[child_count:2]
[child_len:4][child_payload]
...
```

Codecs:

```python
encode_bundle_payload(...)
decode_bundle_payload(...)
```

## Scalar Conversion

```python
payload_bytes_to_scalar_hex(payload)
scalar_hex_to_payload_bytes(scalars)
```

The base layer does not interpret the decoded payload. Semantic-layer verifiers do.
