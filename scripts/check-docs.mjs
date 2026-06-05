import { existsSync, readFileSync, readdirSync } from 'node:fs';
import { dirname, extname, join, normalize, resolve } from 'node:path';

const root = resolve(import.meta.dirname, '..');
const docsRoot = join(root, 'src', 'content', 'docs');
const openApiRoot = join(root, 'src', 'content', 'openapi');
const publicOpenApiRoot = join(root, 'public', 'openapi');
const distRoot = join(root, 'dist');
const requiredSchemas = [
  'base-layer.openapi.json',
  'payment-sl.openapi.json',
  'generic-verifier.openapi.json',
  'bundler-engine.openapi.json',
  'marketplace-bundler.openapi.json'
];
const forbiddenPublicApiPatterns = [/localhost/i, /127\.0\.0\.1/i, /Reference \/ deploy locally/i];

const failures = [];

for (const schema of requiredSchemas) {
  const sourcePath = join(openApiRoot, schema);
  const publicPath = join(publicOpenApiRoot, schema);
  if (!existsSync(sourcePath)) {
    failures.push(`missing source OpenAPI artifact: ${schema}`);
    continue;
  }
  if (!existsSync(publicPath)) {
    failures.push(`missing public OpenAPI artifact: ${schema}`);
  } else if (readFileSync(sourcePath, 'utf8') !== readFileSync(publicPath, 'utf8')) {
    failures.push(`public OpenAPI artifact does not match source artifact: ${schema}`);
  } else {
    const publicSchema = readFileSync(publicPath, 'utf8');
    for (const pattern of forbiddenPublicApiPatterns) {
      if (pattern.test(publicSchema)) {
        failures.push(`public OpenAPI artifact contains public-facing placeholder leak ${pattern}: ${schema}`);
      }
    }
  }

  const parsed = JSON.parse(readFileSync(sourcePath, 'utf8'));
  if (!parsed.openapi || !parsed.paths || Object.keys(parsed.paths).length === 0) {
    failures.push(`invalid OpenAPI artifact: ${schema}`);
  }
  if (!parsed.servers || parsed.servers.length === 0) {
    failures.push(`OpenAPI artifact has no servers: ${schema}`);
  }

  for (const [route, methods] of Object.entries(parsed.paths ?? {})) {
    for (const [method, operation] of Object.entries(methods)) {
      if (!operation.description) {
        failures.push(`${schema} ${method.toUpperCase()} ${route} missing description`);
      }
      if (operation.requestBody && !JSON.stringify(operation.requestBody).includes('"example"')) {
        failures.push(`${schema} ${method.toUpperCase()} ${route} missing request example`);
      }
      if (!JSON.stringify(operation.responses ?? {}).includes('"example"')) {
        failures.push(`${schema} ${method.toUpperCase()} ${route} missing response example`);
      }
    }
  }
}

const builtApiRoot = join(distRoot, 'api');
if (existsSync(builtApiRoot)) {
  for (const file of walk(builtApiRoot)) {
    if (extname(file) !== '.html') continue;
    const source = readFileSync(file, 'utf8');
    for (const pattern of forbiddenPublicApiPatterns) {
      if (pattern.test(source)) {
        failures.push(`${relative(file)} contains public-facing placeholder leak ${pattern}`);
      }
    }
  }
}

for (const file of walk(docsRoot)) {
  if (!['.md', '.mdx'].includes(extname(file))) continue;
  const source = readFileSync(file, 'utf8');
  for (const link of markdownLinks(source)) {
    if (isExternal(link) || link.startsWith('#') || link.startsWith('mailto:')) continue;
    if (link.startsWith('/')) {
      if (!distTargetExists(link)) {
        failures.push(`${relative(file)} links to missing built target: ${link}`);
      }
      continue;
    }
    const target = stripHashAndQuery(link);
    if (!target || target.startsWith('api-reference:')) continue;

    const resolved = resolve(dirname(file), target);
    const candidates = [
      resolved,
      `${resolved}.md`,
      `${resolved}.mdx`,
      join(resolved, 'index.md'),
      join(resolved, 'index.mdx')
    ];
    if (!candidates.some((candidate) => existsSync(candidate))) {
      failures.push(`${relative(file)} links to missing local target: ${link}`);
    }
  }
}

if (failures.length > 0) {
  console.error(failures.map((failure) => `- ${failure}`).join('\n'));
  process.exit(1);
}

console.log('docs checks passed');

function* walk(dir) {
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    const path = join(dir, entry.name);
    if (entry.isDirectory()) yield* walk(path);
    else yield path;
  }
}

function markdownLinks(source) {
  const links = [];
  const pattern = /(?<!!)\[[^\]]+\]\(([^)]+)\)/g;
  let match;
  while ((match = pattern.exec(source))) {
    links.push(match[1].trim());
  }
  return links;
}

function stripHashAndQuery(value) {
  return value.split('#')[0].split('?')[0];
}

function isExternal(value) {
  return /^[a-z][a-z0-9+.-]*:/i.test(value);
}

function relative(path) {
  return normalize(path).replace(`${normalize(root)}/`, '');
}

function distTargetExists(link) {
  const target = stripHashAndQuery(link);
  if (!target || target === '/') return existsSync(join(distRoot, 'index.html'));

  const clean = target.replace(/^\/+/, '');
  const resolved = resolve(distRoot, clean);
  const candidates = [
    resolved,
    `${resolved}.html`,
    join(resolved, 'index.html')
  ];
  return candidates.some((candidate) => existsSync(candidate));
}
