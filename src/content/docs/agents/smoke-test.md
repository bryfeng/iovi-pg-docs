---
title: Agent Smoke Test
description: Runnable public-sandbox script for an agent to create wallets, register a layer, mint, transfer, batch, and verify.
sidebar:
  order: 2
---

Use this when an external agent needs to prove it can transact inside a semantic layer without reading the architecture docs first.

This script uses a unique hex `sl_id` lane, the default Payment asset, and the Payment SL sandbox's embedded verifier. It does not reset shared state.

```bash
node --input-type=module <<'EOF'
const BASE = process.env.PAYMENT_SL ?? 'https://eon-payment-sl-demo-production.up.railway.app';
const slId = Date.now().toString(16).slice(-8).padStart(8, '0');
const version = '0001';
const suffix = `${slId}_${Math.random().toString(16).slice(2, 8)}`;

async function request(path, options = {}) {
  const response = await fetch(`${BASE}${path}`, {
    method: options.method ?? 'GET',
    headers: options.body ? { 'content-type': 'application/json' } : undefined,
    body: options.body ? JSON.stringify(options.body) : undefined
  });

  const text = await response.text();
  const body = text ? JSON.parse(text) : {};

  if (!response.ok) {
    throw new Error(`${response.status} ${path}: ${JSON.stringify(body)}`);
  }

  return body;
}

const layerQuery = `sl_id=${slId}&version=${version}`;

console.log('health', await request('/health'));

const operator = await request('/wallets', {
  method: 'POST',
  body: { label: `Agent Operator ${suffix}`, vk: `operator_vk_${suffix}`, kind: 'sl_operator' }
});

const alice = await request('/wallets', {
  method: 'POST',
  body: { label: `Agent Alice ${suffix}`, vk: `alice_vk_${suffix}`, kind: 'user' }
});

const bob = await request('/wallets', {
  method: 'POST',
  body: { label: `Agent Bob ${suffix}`, vk: `bob_vk_${suffix}`, kind: 'user' }
});

await request('/operator/init', {
  method: 'POST',
  body: {
    issuer_vk: `issuer_vk_${suffix}`,
    reset_existing: false,
    sl_id: slId,
    version,
    operator_wallet_address: operator.address
  }
});

await request('/semantic-layers', {
  method: 'POST',
  body: {
    name: `Agent Smoke ${slId}`,
    sl_id: slId,
    version,
    operator_wallet_address: operator.address
  }
});

await request('/actions/mint', {
  method: 'POST',
  body: { to_address: alice.address, amount: 2, sl_id: slId, version }
});
await request(`/operator/batch?${layerQuery}`, { method: 'POST' });
await request(`/verifier/accept-latest-batch?${layerQuery}`, { method: 'POST' });

await request('/actions/transfer', {
  method: 'POST',
  body: {
    from_address: alice.address,
    to_address: bob.address,
    amount: 1,
    vk: `alice_vk_${suffix}`,
    sl_id: slId,
    version
  }
});
await request(`/operator/batch?${layerQuery}`, { method: 'POST' });
await request(`/verifier/accept-latest-batch?${layerQuery}`, { method: 'POST' });

const aliceBalance = await request(
  `/balances/${alice.address}?source=verifier&${layerQuery}`
);
const bobBalance = await request(
  `/balances/${bob.address}?source=verifier&${layerQuery}`
);
const state = await request(`/verifier/state?${layerQuery}`);

console.log(JSON.stringify({
  sl_id: slId,
  version,
  alice: aliceBalance.balance,
  bob: bobBalance.balance,
  accepted_payloads: state.accepted_payloads
}, null, 2));
EOF
```

Expected final shape:

```json
{
  "sl_id": "hex_lane",
  "version": "0001",
  "alice": 1,
  "bob": 1,
  "accepted_payloads": 2
}
```

If the sandbox rejects the layer ID, generate a fresh hex-only `sl_id`. Non-hex lane IDs are invalid.

This smoke test intentionally uses the default Payment asset. Test custom asset registration as a separate scenario from [Task Recipes](/agents/task-recipes/).

For devnet-backed submission, use `POST /devnet/submit-latest-batch` and then poll `GET /operator/batches` or `POST /verifier/sync` until the batch reports `verification_source: "devnet_utxo"`.
