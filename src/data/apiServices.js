export const apiServices = [
  {
    slug: 'payment-sl',
    name: 'Payment SL Sandbox API',
    status: 'Public sandbox',
    schemaUrl: '/openapi/payment-sl.openapi.json',
    serviceUrl: 'https://eon-payment-sl-demo-production.up.railway.app',
    hideTestRequestButton: false,
    description:
      'Register wallets, create Payment semantic-layer actions, batch them, and read verifier-accepted state.'
  },
  {
    slug: 'generic-verifier',
    name: 'Generic Verifier API',
    status: 'Reference / deploy locally',
    schemaUrl: '/openapi/generic-verifier.openapi.json',
    serviceUrl: 'http://localhost:8000',
    hideTestRequestButton: true,
    description:
      'Ingest ordered base-layer events and replay semantic-layer rules into accepted local state.'
  },
  {
    slug: 'bundler-engine',
    name: 'Bundler Engine API',
    status: 'Reference / deploy locally',
    schemaUrl: '/openapi/bundler-engine.openapi.json',
    serviceUrl: 'http://localhost:8000',
    hideTestRequestButton: true,
    description: 'Wrap child semantic-layer payloads into bundle payloads carried by UTXO Data.'
  },
  {
    slug: 'marketplace',
    name: 'Marketplace Bundler API',
    status: 'Reference / deploy locally',
    schemaUrl: '/openapi/marketplace-bundler.openapi.json',
    serviceUrl: 'http://localhost:8000',
    hideTestRequestButton: true,
    description:
      'Create AMM quotes, liquidity actions, approvals, swaps, and marketplace settlement bundles.'
  },
  {
    slug: 'base-layer',
    name: 'Base-Layer API',
    status: 'Reference / deploy locally',
    schemaUrl: '/openapi/base-layer.openapi.json',
    serviceUrl: 'http://localhost:8000',
    hideTestRequestButton: true,
    description: 'Read base-layer wallet, balance, UTXO, and transaction data or post transfers with Data.'
  }
];
