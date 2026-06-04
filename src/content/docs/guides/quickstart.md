---
title: Quickstart
description: The smallest useful EON developer loop.
sidebar:
  order: 1
---

This quickstart demonstrates the current semantic-layer loop without requiring production custody.

## 1. Start With The Payment SL API

Use the hosted Payment SL middleware API or run it locally:

```bash
cd payment_sl
pip install -r requirements.txt
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

Open the API docs:

```text
http://localhost:8000/docs
```

## 2. Initialize The Layer

```http
POST /operator/init
```

```json
{
  "issuer_vk": "circle_inc_verification_key",
  "reset_existing": false
}
```

## 3. Register Wallets

```http
POST /wallets
```

```json
{
  "label": "Alice",
  "vk": "alice_vk",
  "kind": "user"
}
```

Repeat for Bob.

## 4. Mint, Batch, Verify

```http
POST /actions/mint
POST /operator/batch
POST /verifier/accept-latest-batch
GET /balances/{alice_address}
```

The wallet balance is accepted only after verifier replay.

## 5. Transfer, Batch, Verify

```http
POST /actions/transfer
POST /operator/batch
POST /verifier/accept-latest-batch
GET /balances/{alice_address}
GET /balances/{bob_address}
```

This is the core pattern: intent, operator batch, ordered payload, verifier-accepted state.
