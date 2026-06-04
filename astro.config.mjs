import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  site: 'https://iovi-pg-docs.vercel.app',
  integrations: [
    starlight({
      title: 'EON Docs',
      description: 'Reference docs for EON semantic layers, middleware APIs, verifiers, and agents.',
      social: [
        {
          icon: 'github',
          label: 'GitHub',
          href: 'https://github.com/theparadigmshifters'
        }
      ],
      tableOfContents: {
        minHeadingLevel: 2,
        maxHeadingLevel: 4
      },
      sidebar: [
        {
          label: 'Start',
          items: [
            { label: 'Overview', slug: 'index' },
            { label: 'Quickstart', slug: 'guides/quickstart' },
            { label: 'Agent Quickstart', slug: 'agents/agent-quickstart' }
          ]
        },
        {
          label: 'Concepts',
          autogenerate: { directory: 'concepts' }
        },
        {
          label: 'Guides',
          autogenerate: { directory: 'guides' }
        },
        {
          label: 'Agents',
          autogenerate: { directory: 'agents' }
        },
        {
          label: 'API',
          collapsed: true,
          items: [
            { label: 'Reference Workspace', slug: 'reference' },
            { label: 'Payloads And Scalars', slug: 'reference/payload-scalar-framing' },
            { label: 'Environment Variables', slug: 'reference/env-vars' }
          ]
        },
      ]
    })
  ]
});
