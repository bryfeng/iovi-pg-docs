export const apiServices = [
  {
    slug: 'payment-sl',
    name: 'IOVI Payment SL Sandbox API',
    status: 'Public sandbox',
    schemaUrl: '/openapi/payment-sl.openapi.json',
    serviceUrl: 'https://eon-payment-sl-demo-production.up.railway.app',
    endpointLabel: 'https://eon-payment-sl-demo-production.up.railway.app',
    hideTestRequestButton: false,
    description:
      'Register wallets, create Payment semantic-layer actions, batch them, and read verifier-accepted state.'
  },
  {
    slug: 'generic-verifier',
    name: 'IOVI Generic Verifier API',
    status: 'Public verifier',
    schemaUrl: '/openapi/generic-verifier.openapi.json',
    serviceUrl: 'https://verifier-production-7dc3.up.railway.app',
    endpointLabel: 'https://verifier-production-7dc3.up.railway.app',
    hideTestRequestButton: false,
    description:
      'Public verifier endpoint for ingesting ordered base-layer events and replaying semantic-layer rules into accepted local state.'
  },
  {
    slug: 'bundler-engine',
    name: 'IOVI Bundler Engine API',
    status: 'Public sandbox',
    schemaUrl: '/openapi/bundler-engine.openapi.json',
    serviceUrl: 'https://bundler-production-b637.up.railway.app',
    endpointLabel: 'https://bundler-production-b637.up.railway.app',
    hideTestRequestButton: false,
    description:
      'Public bundler endpoint for wrapping child semantic-layer payloads into bundle payloads.'
  },
  {
    slug: 'marketplace',
    name: 'IOVI Marketplace Bundler API',
    status: 'Public sandbox',
    schemaUrl: '/openapi/marketplace-bundler.openapi.json',
    serviceUrl: 'https://bundler-production-b637.up.railway.app',
    endpointLabel: 'https://bundler-production-b637.up.railway.app',
    hideTestRequestButton: false,
    description:
      'Public marketplace endpoint for AMM quotes, liquidity actions, approvals, swaps, and marketplace settlement bundles.'
  },
  {
    slug: 'base-layer',
    name: 'IOVI Base-Layer API',
    status: 'Public base-layer API',
    schemaUrl: '/openapi/base-layer.openapi.json',
    serviceUrl: 'https://iovi-api-production.up.railway.app',
    endpointLabel: 'https://iovi-api-production.up.railway.app',
    hideTestRequestButton: true,
    description:
      'Public base-layer endpoint for wallet, balance, UTXO, transaction, and transfer-with-Data reads and writes. Write routes may require an API key.'
  }
];
