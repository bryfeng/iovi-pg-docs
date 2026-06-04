import { existsSync, readFileSync, readdirSync } from 'node:fs';
import { dirname, extname, join, normalize, resolve } from 'node:path';

const root = resolve(import.meta.dirname, '..');
const docsRoot = join(root, 'src', 'content', 'docs');
const openApiRoot = join(root, 'src', 'content', 'openapi');
const requiredSchemas = [
  'payment-sl.openapi.json',
  'generic-verifier.openapi.json',
  'bundler-engine.openapi.json',
  'marketplace-bundler.openapi.json'
];

const failures = [];

for (const schema of requiredSchemas) {
  const path = join(openApiRoot, schema);
  if (!existsSync(path)) {
    failures.push(`missing OpenAPI artifact: ${schema}`);
    continue;
  }

  const parsed = JSON.parse(readFileSync(path, 'utf8'));
  if (!parsed.openapi || !parsed.paths || Object.keys(parsed.paths).length === 0) {
    failures.push(`invalid OpenAPI artifact: ${schema}`);
  }
}

for (const file of walk(docsRoot)) {
  if (!['.md', '.mdx'].includes(extname(file))) continue;
  const source = readFileSync(file, 'utf8');
  for (const link of markdownLinks(source)) {
    if (isExternal(link) || link.startsWith('#') || link.startsWith('mailto:')) continue;
    if (link.startsWith('/')) continue;
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
