import { apiServices } from '../src/data/apiServices.js';

const origin = process.env.SMOKE_ORIGIN || 'https://eon-payment-sl-playground.vercel.app';
const timeoutMs = Number(process.env.SMOKE_TIMEOUT_MS || 15000);

const checksByService = {
  'payment-sl': ['/health', '/config', '/devnet/status', '/openapi.json'],
  'generic-verifier': ['/', '/health', '/verifier/log', '/openapi.json'],
  'bundler-engine': ['/', '/health', '/openapi.json'],
  marketplace: ['/assets', '/pools'],
  'base-layer': ['/health', '/wallet/address']
};

const failures = [];

for (const service of apiServices) {
  const paths = checksByService[service.slug];
  if (!paths) continue;

  if (!service.serviceUrl) {
    failures.push(`${service.slug} has no public serviceUrl`);
    continue;
  }

  const results = [];
  for (const path of paths) {
    results.push(await check(service, path));
  }

  if (service.slug === 'base-layer') {
    const walletAddress = results.find((result) => result.path === '/wallet/address')?.json?.address;
    if (!walletAddress) {
      failures.push('base-layer /wallet/address did not return an address');
    } else {
      await check(service, `/utxos?owner=${encodeURIComponent(walletAddress)}&limit=1`);
    }
  }
}

if (failures.length > 0) {
  console.error(failures.map((failure) => `- ${failure}`).join('\n'));
  process.exit(1);
}

console.log('public API smoke checks passed');

async function check(service, path) {
  const url = new URL(path, service.serviceUrl).toString();
  let response;
  let bodyText = '';

  try {
    response = await fetch(url, {
      headers: {
        Accept: 'application/json',
        Origin: origin
      },
      signal: AbortSignal.timeout(timeoutMs)
    });
    bodyText = await response.text();
  } catch (error) {
    failures.push(`${service.slug} ${url} request failed: ${error.message}`);
    return { path, json: null };
  }

  const cors = response.headers.get('access-control-allow-origin');
  if (!response.ok) {
    failures.push(`${service.slug} ${url} returned HTTP ${response.status}: ${truncate(bodyText)}`);
  }
  if (cors !== '*' && cors !== origin) {
    failures.push(`${service.slug} ${url} missing usable CORS header for ${origin}; got ${cors || 'none'}`);
  }

  let json = null;
  const contentType = response.headers.get('content-type') || '';
  if (contentType.includes('application/json') && bodyText) {
    try {
      json = JSON.parse(bodyText);
    } catch (error) {
      failures.push(`${service.slug} ${url} returned invalid JSON: ${error.message}`);
    }
  }

  console.log(`ok ${service.slug} ${path} ${response.status} cors=${cors || 'none'}`);
  return { path, json };
}

function truncate(value) {
  return value.length <= 240 ? value : `${value.slice(0, 240)}...`;
}
