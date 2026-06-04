---
title: Quickstart
description: The smallest useful EON developer loop.
sidebar:
  order: 1
---

This quickstart demonstrates the current semantic-layer loop against the public Payment SL sandbox. It does not require production custody.

## 1. Check The Sandbox

Base URL:

```text
https://eon-payment-sl-demo-production.up.railway.app
```

First request:

```bash
BASE=https://eon-payment-sl-demo-production.up.railway.app
curl "$BASE/health"
```

Full API references:

- [EON API Hub](/api/)
- [Rendered Payment SL reference](/api/payment-sl/)
- [OpenAPI JSON](/openapi/payment-sl.openapi.json)
- [Live Swagger](https://eon-payment-sl-demo-production.up.railway.app/docs)

## 2. Initialize The Layer

```bash
curl -X POST "$BASE/operator/init" \
  -H "Content-Type: application/json" \
  -d '{"issuer_vk":"circle_inc_verification_key","reset_existing":false}'
```

This initializes operator-local state for the sandbox Payment semantic layer.

## 3. Register Wallets

```bash
curl -X POST "$BASE/wallets" \
  -H "Content-Type: application/json" \
  -d '{"label":"Alice","vk":"alice_vk","kind":"user"}'
```

```bash
curl -X POST "$BASE/wallets" \
  -H "Content-Type: application/json" \
  -d '{"label":"Bob","vk":"bob_vk","kind":"user"}'
```

Store the returned `address` values. Sandbox VK values are not production custody.

## 4. Mint, Batch, Verify

Replace `alice_wallet_address` with the returned Alice address:

```bash
curl -X POST "$BASE/actions/mint" \
  -H "Content-Type: application/json" \
  -d '{"to_address":"alice_wallet_address","amount":1000,"asset_id":"USD"}'

curl -X POST "$BASE/operator/batch"
curl -X POST "$BASE/verifier/accept-latest-batch"
curl "$BASE/balances/alice_wallet_address"
```

The wallet balance is accepted only after verifier replay.

## 5. Transfer, Batch, Verify

```bash
curl -X POST "$BASE/actions/transfer" \
  -H "Content-Type: application/json" \
  -d '{"from_address":"alice_wallet_address","to_address":"bob_wallet_address","amount":250,"asset_id":"USD","vk":"alice_vk"}'

curl -X POST "$BASE/operator/batch"
curl -X POST "$BASE/verifier/accept-latest-batch"
curl "$BASE/balances/alice_wallet_address"
curl "$BASE/balances/bob_wallet_address"
```

This is the core pattern: intent, operator batch, ordered payload, verifier-accepted state.

## Local Development

If you are running the middleware locally instead of the sandbox:

```bash
cd payment_sl
pip install -r requirements.txt
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

Then set:

```bash
BASE=http://localhost:8000
```
