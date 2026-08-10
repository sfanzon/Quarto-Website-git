# Platform decision: Astro main site, Quarto project documents

## Decision

Astro is the production owner of the main professional website and its global
shell. Quarto remains the production owner of every individual project page.
The public `/projects/` route is the Astro project catalogue; existing project
URLs beneath `/projects/<slug>/` remain Quarto-rendered documents.

This replaces the earlier "retain Quarto" decision. The accepted Astro/Quarto
POC established that the two tools can build one static site without changing
project authoring or public project URLs.

## Ownership boundary

| Area | Production owner |
|---|---|
| Main professional pages and `/projects/` catalogue | Astro |
| Navbar, footer, theme control and global design tokens | Astro |
| All `projects/**` pages, including F1 overview, technical and code views | Quarto |
| Project metadata, filters, includes and project-only styles | Existing Quarto sources |
| Other scientific or document-oriented content | Quarto where appropriate |

The experimental Astro F1 overview is not a production route owner. During
the production merge, Quarto's `projects/f1-time-rank-duality/index.qmd`
deliberately replaces that experimental output.

## Production build contract

`npm run build:site` from `astro/` produces the deployable static site in
`astro/dist`:

1. Astro builds its pages and explicit shell artifacts.
2. Quarto renders only `projects/**/*.qmd` to an isolated temporary directory.
3. The build applies Astro's emitted header, footer and stylesheet to each
   rendered project document, then copies each document and its referenced
   assets into `astro/dist`.
4. Pagefind runs only after the merged tree is complete.

Astro and Quarto never write to the same output directory. The shell boundary
is explicit (`/site-shell/header/`, `/site-shell/footer/` and
`/site-shell/site.css`), rather than being scraped from a rendered Astro page or
identified by F1-specific markers. The merge removes Quarto's structural shell
and preserves the Quarto article body, project navigation and document assets.

## Migration constraints

- Do not convert project pages to Astro or move their canonical source files.
- Preserve existing project URLs and relative project navigation.
- Do not edit `docs/`; it remains legacy generated output until deployment is
  switched to the Astro build artifact.
- Migrate ordinary Astro pages separately, with visual parity and canonical
  source ownership decided page by page.
- Do not introduce a separate shared-design repository unless a future need
  justifies it.

See `ARCHITECTURE.md` for the implementation boundary and `SOURCE_MAP.md` for
the canonical source map.
