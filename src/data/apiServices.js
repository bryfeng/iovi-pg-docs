export const apiServices = [
  {
    slug: 'payment-sl',
    name: 'Payment SL Sandbox API',
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
    name: 'Generic Verifier API',
    status: 'Schema only',
    schemaUrl: '/openapi/generic-verifier.openapi.json',
    serviceUrl: null,
    endpointLabel: 'No public endpoint yet',
    hideTestRequestButton: true,
    description:
      'Reference schema for ingesting ordered base-layer events and replaying semantic-layer rules. Bring your own verifier deployment URL to call it.'
  },
  {
    slug: 'bundler-engine',
    name: 'Bundler Engine API',
    status: 'Schema only',
    schemaUrl: '/openapi/bundler-engine.openapi.json',
    serviceUrl: null,
    endpointLabel: 'No public endpoint yet',
    hideTestRequestButton: true,
    description:
      'Reference schema for wrapping child semantic-layer payloads into bundle payloads. Bring your own bundler deployment URL to call it.'
  },
  {
    slug: 'marketplace',
    name: 'Marketplace Bundler API',
    status: 'Schema only',
    schemaUrl: '/openapi/marketplace-bundler.openapi.json',
    serviceUrl: null,
    endpointLabel: 'No public endpoint yet',
    hideTestRequestButton: true,
    description:
      'Reference schema for AMM quotes, liquidity actions, approvals, swaps, and marketplace settlement bundles. Bring your own marketplace deployment URL to call it.'
  },
  {
    slug: 'base-layer',
    name: 'Base-Layer API',
    status: 'Schema only',
    schemaUrl: '/openapi/base-layer.openapi.json',
    serviceUrl: null,
    endpointLabel: 'No public endpoint yet',
    hideTestRequestButton: true,
    description:
      'Reference schema for base-layer wallet, balance, UTXO, transaction, and transfer-with-Data endpoints. Bring your own base-layer API deployment URL to call it.'
  }
];
