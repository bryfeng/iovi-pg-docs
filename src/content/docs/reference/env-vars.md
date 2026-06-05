---
title: Environment Variables
description: Common environment variables across the EON playground services.
sidebar:
  order: 6
---

## Playground Frontend

```text
PUBLIC_EON_PAYMENT_API_URL
PUBLIC_PAYMENT_SL_API_URL
PUBLIC_EON_BUNDLER_URL
PUBLIC_EON_VERIFIER_URL
PUBLIC_EON_BASE_LAYER_API_URL
PUBLIC_EON_DEVNET_RPC_URL
PUBLIC_EON_DOCS_URL
```

Public GTM defaults:

```text
PUBLIC_EON_PAYMENT_API_URL=https://eon-payment-sl-demo-production.up.railway.app
PUBLIC_PAYMENT_SL_API_URL=https://eon-payment-sl-demo-production.up.railway.app
PUBLIC_EON_BUNDLER_URL=https://bundler-production-b637.up.railway.app
PUBLIC_EON_VERIFIER_URL=https://verifier-production-7dc3.up.railway.app
PUBLIC_EON_BASE_LAYER_API_URL=https://iovi-api-production.up.railway.app
PUBLIC_EON_DOCS_URL=https://iovi-pg-docs.vercel.app
```

## Payment SL Middleware

```text
PAYMENT_SL_DB_PATH
RAILWAY_VOLUME_MOUNT_PATH
EON_DEVNET_API_URL
EON_DEVNET_SUBMIT_CMD
EON_KEY_ENCRYPTION_SECRET
EON_OPERATOR_WALLET_FILE
```

## Generic Verifier / Marketplace Stack

```text
EON_VERIFIER_DB_PATH
EON_VERIFIER_URL
STOCK_SL_ID
USD_SL_ID
AMM_SL_ID
SETTLEMENT_SL_ID
STOCK_ISSUER_VK
USD_ISSUER_VK
CORS_ALLOW_ORIGINS
```

## Base-Layer API

```text
EON_WALLET_FILE
EON_WALLET_B64
POSTER_API_KEY
EON_API_URL
HOST
PORT
```
