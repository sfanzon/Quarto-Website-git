# Source ownership map

> "I want to change X on the site. Which source file should I inspect first?"

This is the canonical “what controls what?” map for the hybrid Astro + Quarto
production architecture. Keep every visible component and behaviour mapped to
one obvious owner here when its ownership changes.

The production platform boundary is recorded in `PLATFORM_DECISION.md`.
Astro owns the main professional site and shared shell; Quarto owns every
individual project page. Do not infer a source move from a matching public URL.

Target external publishing topology and resource ownership are recorded in
`PUBLISHING_ARCHITECTURE.md`; consult it for subdomains, standalone Quarto
repositories, GitHub Pages ownership, future asset hosting and the target
renderer-decision process. The project/note ownership recorded below is the
current supported hybrid implementation; it may change only after the F1
renderer gate is resolved and a migration task moves the canonical sources.

## Astro production foundation

| File | Description |
|---|---|
| `astro/src/components/Header.astro` | Canonical shared navbar structure, active navigation state, theme control, data-driven dropdown menus and mobile navigation behaviour |
| `astro/src/components/SiteSearch.astro` | Canonical shared search button, dialog and Pagefind lazy-loading/search behaviour |
| `astro/src/components/Footer.astro` | Canonical shared footer |
| `astro/src/components/BackToTop.astro` | Canonical shared back-to-top markup and behaviour; included once through `Footer.astro` on Astro and injected Quarto pages |
| `astro/src/styles/shell.css` | Canonical shared shell tokens, navbar, footer, back-to-top, responsive shell and shared-search presentation |
| `astro/src/styles/global.css` | Ordinary Astro page styling; imports `shell.css` for Astro-page use |
| `astro/src/pages/site-shell/header.astro` | Build-only navbar fragment for Quarto documents; removed from the final site after merge |
| `astro/src/pages/site-shell/footer.astro` | Build-only footer fragment for Quarto documents; removed from the final site after merge |
| `astro/src/pages/site-shell/site.css.ts` | Explicit emitted stylesheet artifact for Quarto documents |
| `astro/scripts/build-site.mjs` | Builds Astro, renders Quarto project and note documents in isolation, merges them into `astro/dist/`, then writes the final sitemap and Pagefind index |
| `astro/scripts/dev-site.mjs` | Local hybrid development watcher: invokes the QA merge, serves `astro/dist/`, and watches canonical Astro/Quarto project and note inputs for rebuilds |
| `astro/src/pages/index.astro` | Direct production owner for the homepage; consumes `includes/home-news.html` |
| `astro/src/styles/home.css` | Production homepage composition and static hero gradient styling |
| `astro/src/pages/notes.astro` | Production owner for `/notes/`; reads front matter directly from canonical `notes/*.qmd` sources |
| `astro/src/styles/notes.css` | Production `/notes/` index presentation |
| `astro/src/pages/projects.astro` | Production owner for the `/projects/` catalogue |
| `astro/src/data/projects.ts` | Astro loader for canonical `data/projects.yml` |
| `astro/src/styles/projects.css` | Production `/projects/` catalogue styling |
| `astro/src/pages/about.astro` | Production owner for `/about/`; preserves the accepted career narrative and hierarchy |
| `astro/src/pages/expertise.astro` | Production owner for `/expertise/` and its five capability sections |
| `astro/src/styles/expertise.css` | Production `/expertise/` page styling |
| `astro/src/pages/research.astro` | Production owner for `/research/` and its three research themes |
| `astro/src/styles/research.css` | Production `/research/` page styling |
| `astro/src/pages/publications.astro` | Production owner for `/publications/` and its page hierarchy |
| `astro/src/components/PublicationArchive.astro` | Consumes the generated publication archive and owns publication-specific citation-copy behaviour |
| `astro/src/components/DisclosureArchive.astro` | Shared accessible Abstract/BibTeX disclosure and abstract-math behaviour for Publications, Teaching, Presentations and Supervision |
| `astro/src/styles/archive-actions.css` | Canonical shared disclosure action and Abstract-panel presentation for Publications, Teaching, Presentations and Supervision |
| `astro/src/styles/publications.css` | Production `/publications/` archive styling |
| `astro/src/styles/section-jump.css` | Shared Astro in-page section navigation used by Publications and Teaching |
| `astro/src/pages/teaching.astro` | Production owner for `/teaching/`; consumes `includes/teaching-list.html` |
| `astro/src/styles/teaching.css` | Production `/teaching/` page styling |
| `astro/src/pages/news.astro` | Production owner for `/news/`; consumes `includes/news-all.html` and owns archive search behaviour |
| `astro/src/styles/news-component.css` | Canonical News row/disclosure styling shared by Homepage and `/news/` |
| `astro/src/styles/news.css` | Production `/news/` archive/search-only styling |
| `astro/src/pages/contact.astro` | Production owner and direct content source for `/contact/` |
| `astro/src/styles/contact.css` | Production `/contact/` page styling |
| `astro/src/pages/presentations.astro` | Production owner for `/presentations/`; consumes `includes/presentations.html` |
| `astro/src/pages/supervision.astro` | Production owner for `/supervision/`; consumes `includes/supervision.html` |
| `astro/src/styles/record-archive.css` | Shared generated-record layout for Presentations and Supervision |
| `astro/src/styles/presentations.css` | Presentation-page introduction and invited marker |
| `astro/src/styles/supervision.css` | Supervision-page introduction |
| `astro/src/pages/cv.astro` | Direct production owner for `/cv/` |
| `astro/src/pages/404.astro` | Direct production owner for the static `404.html` artifact |
| `astro/scripts/build-site.mjs` (`compatibilityAliases`) | Emits noindex copies of canonical Astro pages at the former `.html` URLs for static-host compatibility |

Quarto's `projects/f1-time-rank-duality/index.qmd` is the sole owner of the
F1 overview URL; no Astro detail route exists.

## Development visual QA

| File | Description |
|---|---|
| `astro/src/pages/dev/kitchen-sink.astro` | Development-only Astro production-pattern inventory |
| `astro/src/components/dev/TechnicalSpecimens.mdx` | Dev-only genuine Astro Markdown, Shiki code and KaTeX math specimens |
| `dev/quarto-kitchen-sink.qmd` | Dev-only genuine Quarto document-pattern inventory, merged through the shared shell during QA builds |
| `astro/src/pages/dev/viewports.astro` | Development-only responsive dashboard for both kitchen sinks and real routes |
| `astro/src/styles/dev-tools.css` | QA page chrome, token swatches, controls and viewport frames only |
| `astro/scripts/build-site.mjs` + `npm run build:qa` | Retains `/dev/` locally while keeping it out of sitemap and Pagefind; production `build:site` removes it |

The Notes index is Astro-owned. Quarto remains the production renderer for the
canonical `notes/*.qmd` articles, which the hybrid build publishes at their
existing `/notes/<slug>.html` URLs.

## Project pages (Quarto production owner)

| File | Description |
|---|---|
| `projects/*/index.qmd` | Long-form project explainer pages |
| `projects/f1-time-rank-duality/technical.qmd` | Formula 1 technical note |
| `projects/f1-time-rank-duality/code.qmd` | Formula 1 code companion |
| `projects/_metadata.yml` | Shared project page defaults |
| `filters/project-components.lua` | Quarto Lua filter — renders project heroes, resource links, At-a-glance summaries, Explore Project navigation, and related-project suggestions |

All individual project pages remain Quarto-rendered in production, including
`projects/*/index.qmd`. `data/projects.yml`, project-specific includes,
filters and styles remain their canonical owners. Astro does not own a project
detail route.

## Content data (structured sources)

| File | Description |
|---|---|
| `data/publications.bib` | Single source for all publications |
| `data/presentations_*.bib` | Presentation records grouped as talks, posters and institutional presentations |
| `data/supervision_*.bib` | Supervision records grouped as master’s and undergraduate projects |
| `data/projects.yml` | Single source for project cards, metadata and navigation |
| `data/teaching.yml` | Single teaching record, with `role: lecturer` or `role: tutor` |
| `data/coauthors.yml` | Co-author homepage URL map |
| `data/citations/numeric.csl` | Shared citation style for project pages |
| `data/optional-local-assets.txt` | All intentionally absent local assets, with their future repository paths |
| `news/*.md` | Dated news entries (filenames: `YYYY-MM-DD.md`) |
| `notes/*.qmd` | Long-form technical notes |
| `notes/_metadata.yml` | Shared note-page defaults |

## Generated content

| File | Description |
|---|---|
| `scripts/build-content.py` | Pre-render hook — writes the remaining generated HTML fragments and project JSON |

### Includes generated by `scripts/build-content.py`

| Generated file | Canonical source | Generator path |
|---|---|---|
| `data/projects.generated.json` | `data/projects.yml` | `portfolio.load_projects()` → JSON snapshot for `filters/project-components.lua` |
| `includes/home-news.html` | `news/*.md` (latest 8; consumed by `index.astro`) | `news.load_news()` → `news.render_news_component(searchable=False)` |
| `includes/news-all.html` | `news/*.md` (all; consumed by `news.astro`) | `news.load_news()` → `news.render_news_component()` |
| `includes/publications-all.html` | `data/publications.bib` (all, grouped; consumed by `PublicationArchive.astro`) | `publications.load_publications()` → `publication_rendering.render_publication_archive()` |
| `includes/presentations.html` | `data/presentations_*.bib` | `presentations.load_presentations()` → `presentations.render_presentations_archive()` |
| `includes/supervision.html` | `data/supervision_*.bib` | `supervision.load_supervision()` → `supervision.render_supervision_archive()` |
| `includes/teaching-list.html` | `data/teaching.yml` | `teaching.load_teaching()` → `teaching_section()` |

`data/coauthors.yml` is optional enrichment consumed only while the publication
renderers add co-author homepage links. It does not produce its own include.

### Hand-written includes (canonical source)

| File | Description |
|---|---|
| `includes/site-footer.html` | Site footer markup |
| `includes/project-navigation.html` | Project-page left-rail / drawer navigation |
| `includes/after-body.html` | Scripts and markup injected after `</body>` |
| `includes/scroll-restoration-head.html` | Scroll position restoration injected into `<head>` |
| `includes/mermaid-svg-ids.html` | Mermaid SVG ID normalization injected into `<head>` |

### Runtime behaviour in hand-written includes

| Source | Runtime target | Purpose |
|---|---|---|
| `includes/scroll-restoration-head.html` + `includes/after-body.html` | browser back/forward navigation and `sessionStorage` | Prevent a visible flash at the top of a restored page and restore its saved scroll position after Quarto's Safari scroll workaround. |
| `includes/after-body.html` | `.callout-header[data-bs-toggle="collapse"]` | Adds keyboard activation to Quarto/Bootstrap collapsible callout headers. |
| `includes/after-body.html` | overflowing `pre` elements | Makes horizontally or vertically scrollable code regions keyboard-focusable. |
| `includes/project-navigation.html` | `.project-detail-page` headings and Quarto navbar | Builds the responsive project chapter rail/drawer and synchronizes its geometry and active section. |
| `includes/mermaid-svg-ids.html` | Mermaid SVGs under `.cell-output-display` | Namespaces diagram IDs after Quarto/Mermaid render so multiple diagrams cannot collide. |

Astro owns the production navbar, footer and theme control, including on merged
Quarto documents. Quarto still supplies document-specific Bootstrap,
math/code and Mermaid behaviour; these legacy includes add only the site-specific
behaviour listed above.

## Styles

| File | Description |
|---|---|
| `styles/main.scss` | Lean Quarto document foundation entry point |
| `styles/main/_00-tokens.scss` | Quarto document tokens used by projects and note articles |
| `styles/main/_01-foundation.scss` | Base element styles, typography, layout primitives |
| `styles/main/_12-page-shell.scss` | Quarto document shell and content container styles |
| `styles/components/_notes.scss` | Long-form Quarto note presentation |

`styles/project.scss` is the project-only SCSS entry point. It compiles the
partials under `styles/project/` separately from the global `styles/main.scss`
chain. Its `_article.scss` and `_article-controls.scss` files are currently
temporary manifests for the corresponding subdirectories; `_navigation.scss`
is already the canonical project-navigation owner.

### Style control index

This table records the canonical owner for migrated components and the current
location of components that still await consolidation. During the style
refactor, do not add a new rule to a transitional owner when a canonical owner
already exists.

| Visible area | Current owner | Status |
|---|---|---|
| Production design tokens, colours and shared widths | `astro/src/styles/shell.css` | Canonical |
| Production navbar, theme control, More dropdown and mobile navigation behaviour | `astro/src/components/Header.astro` | Canonical |
| Production navbar, footer and responsive shell presentation | `astro/src/styles/shell.css` | Canonical |
| Production site-search behaviour | `astro/src/components/SiteSearch.astro` | Canonical |
| Production site-search presentation | `astro/src/styles/shell.css` (`.site-search-*`) | Canonical |
| Production Expertise page | `astro/src/pages/expertise.astro` + `astro/src/styles/expertise.css` | Canonical |
| Production About page | `astro/src/pages/about.astro` + `astro/src/styles/global.css` (`/* About page */`) | Canonical |
| Production Research page | `astro/src/pages/research.astro` + `astro/src/styles/research.css` | Canonical |
| Production footer | `astro/src/components/Footer.astro` + `astro/src/styles/shell.css` | Canonical |
| Quarto document shell | `styles/main/_12-page-shell.scss` | Canonical for Quarto documents |
| Notes index | `astro/src/pages/notes.astro` + `astro/src/styles/notes.css` | Canonical |
| Long-form note pages | `styles/components/_notes.scss` | Canonical |
| Project article foundation and presentation | `styles/project/_article.scss` | Canonical, project-only |
| Project article context controls | `styles/project/_article-controls.scss` | Canonical, project-only |
| Project chapter navigation | `styles/project/_navigation.scss` | Canonical, project-only |
| Homepage composition | `astro/src/pages/index.astro` + `astro/src/styles/home.css` | Canonical |
| Production Publications page | `astro/src/pages/publications.astro` + `astro/src/components/PublicationArchive.astro` + `astro/src/styles/publications.css` | Canonical; records and markup originate from `data/publications.bib` through `includes/publications-all.html` |
| Shared archive disclosure action and Abstract panel | `astro/src/styles/archive-actions.css` + `astro/src/components/DisclosureArchive.astro` | Canonical for Publications, Teaching, Presentations and Supervision |
| Production Teaching page | `astro/src/pages/teaching.astro` + `astro/src/styles/teaching.css` | Canonical; records temporarily originate from `data/teaching.yml` through `includes/teaching-list.html` |
| Production Contact page | `astro/src/pages/contact.astro` + `astro/src/styles/contact.css` | Canonical |
| Homepage + archive News rows | `scripts/sitegen/news.py` + `astro/src/styles/news-component.css` | Canonical shared markup and presentation |
| Production News search | `astro/src/pages/news.astro` + `astro/src/styles/news.css` | Canonical archive-only behaviour and presentation |
| Production Presentations | `astro/src/pages/presentations.astro` + `astro/src/styles/presentations.css` + `astro/src/styles/record-archive.css` | Canonical page; records remain `data/presentations_*.bib` via `includes/presentations.html` |
| Production Supervision | `astro/src/pages/supervision.astro` + `astro/src/styles/supervision.css` + `astro/src/styles/record-archive.css` | Canonical page; records remain `data/supervision_*.bib` via `includes/supervision.html` |

## Lua filters

| File | Description |
|---|---|
| `filters/project-components.lua` | Project-page rendering filter |

## Build and test

| File | Description |
|---|---|
| `_quarto.yml` | Site configuration, navigation, theme, pre-render hook |
| `scripts/build-content.py` | Pre-render content generator |
| `tests/safety/` | Smoke, interaction, link, accessibility, and cross-browser tests |
| `tests/visual/` | Visual regression screenshot tests |

## Generated output (never canonical source)

| Directory | Description |
|---|---|
| `docs/` | Rendered static site for deployment |
| `astro/dist/` | Final Astro + Quarto production artifact |

All files under `docs/` and `astro/dist/` are generated. Never edit them directly.
