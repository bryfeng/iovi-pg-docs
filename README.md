# EON Docs

Dedicated Astro Starlight docs for EON semantic layers, middleware APIs, verifier flows, marketplace bundles, and AI-agent task recipes.

## Local Development

```bash
npm install
npm run generate:openapi
npm run dev
```

Open:

```text
http://localhost:4321
```

## Scripts

```bash
npm run dev              # run Starlight locally
npm run build            # build static docs
npm run check            # regenerate OpenAPI, type-check, build, and link-check docs
npm run generate:openapi # write checked-in OpenAPI artifacts
```

Generated schemas live in:

```text
src/content/openapi/
```

The public agent entrypoint is:

```text
public/llms.txt
```

## Source Material

The docs consolidate existing repo material instead of replacing it blindly:

- `EON_DESIGN_BRIEF.md`
- `payment_sl/API.md`
- `payment_sl/ARCHITECTURE.md`
- `eon-playground/docs/*`
- `eon-marketplace-stack/docs/*`
- `eon-base-layer-api/README.md`
- `eon-sdk/README.md`
