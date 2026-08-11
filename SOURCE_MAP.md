# Source ownership map

> "I want to change X on the site. Which source file should I inspect first?"

This is the canonical “what controls what?” map for the hybrid Astro + Quarto
production architecture. Keep every visible component and behaviour mapped to
one obvious owner here when its ownership changes.

The production platform boundary is recorded in `PLATFORM_DECISION.md`.
Astro owns the main professional site and shared shell; Quarto owns every
individual project page. Do not infer a source move from a matching public URL.

## Astro production foundation

| File | Description |
|---|---|
| `astro/src/components/Header.astro` | Canonical shared navbar structure, active navigation state, theme control, More dropdown and mobile navigation behaviour |
| `astro/src/components/SiteSearch.astro` | Canonical shared search button, dialog and Pagefind lazy-loading/search behaviour |
| `astro/src/components/Footer.astro` | Canonical shared footer |
| `astro/src/styles/shell.css` | Canonical shared shell tokens, navbar, footer, responsive shell and shared-search presentation |
| `astro/src/styles/global.css` | Ordinary Astro page styling; imports `shell.css` for Astro-page use |
| `astro/src/pages/site-shell/header.astro` | Build-only navbar fragment for Quarto documents; removed from the final site after merge |
| `astro/src/pages/site-shell/footer.astro` | Build-only footer fragment for Quarto documents; removed from the final site after merge |
| `astro/src/pages/site-shell/site.css.ts` | Explicit emitted stylesheet artifact for Quarto documents |
| `astro/scripts/build-site.mjs` | Builds Astro, renders Quarto projects in isolation, merges them into `astro/dist/`, then writes the final sitemap and Pagefind index |
| `astro/src/pages/projects.astro` | Production owner for the `/projects/` catalogue |
| `astro/src/data/projects.ts` | Astro loader for canonical `data/projects.yml` |
| `astro/src/styles/projects.css` | Production `/projects/` catalogue styling |

Quarto's `projects/f1-time-rank-duality/index.qmd` is the sole owner of the
F1 overview URL; no Astro detail route exists.

## Top-level pages

| File | Description |
|---|---|
| `index.qmd` | Homepage — professional positioning + selected evidence |
| `about.qmd` | Career narrative and professional transition |
| `expertise.qmd` | Transferable capabilities |
| `research.qmd` | Academic research themes |
| `projects.qmd` | Project listing page |
| `publications.qmd` | Full publication archive |
| `teaching.qmd` | Teaching activity |
| `news.qmd` | News archive page |
| `notes.qmd` | Notes archive page |
| `contact.qmd` | Contact information |
| `cv.qmd` | Curriculum vitae |
| `presentations.qmd` | Presentations |
| `supervision.qmd` | Student supervision |
| `404.qmd` | Custom 404 page |

Until an ordinary page is deliberately migrated, its root `.qmd` remains its
canonical source. Top-level `.qmd` files intentionally remain at repository
root because Quarto mirrors source paths into output URLs. Moving them under
`pages/` would change canonical public URLs. Do not reopen this decision.

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
| `scripts/build-content.py` | Pre-render hook — reads structured data sources and writes generated HTML/QMD fragments |

### Includes generated by `scripts/build-content.py`

| Generated file | Canonical source | Generator path |
|---|---|---|
| `data/projects.generated.json` | `data/projects.yml` | `portfolio.load_projects()` → JSON snapshot for `filters/project-components.lua` |
| `includes/home-news.qmd` | `news/*.md` (latest 8) | `news.load_news()` → `news.render_news_qmd()` |
| `includes/home-notes.html` | `notes/*.qmd` (latest 4) | `portfolio.load_featured_notes()` → `portfolio.render_featured_note()` |
| `includes/home-projects.html` | `data/projects.yml` (featured) | `portfolio.load_projects()` → `portfolio.render_featured_projects()` |
| `includes/home-publications-list.html` | `data/publications.bib` (selected) | `publications.load_publications()` → `publication_rendering.render_selected_publications()` |
| `includes/news-all.qmd` | `news/*.md` (all) | `news.load_news()` → `news.render_news_qmd()` |
| `includes/projects-portfolio.html` | `data/projects.yml` (all) | `portfolio.load_projects()` → `portfolio.render_projects_portfolio()` |
| `includes/publications-all.html` | `data/publications.bib` (all, grouped) | `publications.load_publications()` → `publication_rendering.render_publication_archive()` |
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
| `includes/after-body.html` | `.abstract-toggle`, `.bibtex-toggle`, `.publication-entry` | Open one publication, presentation or supervision detail panel at a time; typeset mathematics when an abstract opens. |
| `includes/after-body.html` | `.publication-entry .bibtex pre code` | Adds the Copy citation control to generated publication BibTeX panels. |
| `includes/after-body.html` | `[data-news-component]` | Filters generated News archive entries client-side. |
| `includes/after-body.html` | `.callout-header[data-bs-toggle="collapse"]` | Adds keyboard activation to Quarto/Bootstrap collapsible callout headers. |
| `includes/after-body.html` | Quarto search popup `.aa-DetachedContainer .aa-Input` | Applies the accessible site-search label when Quarto inserts the detached search dialog. |
| `includes/after-body.html` | overflowing `pre` elements | Makes horizontally or vertically scrollable code regions keyboard-focusable. |
| `includes/project-navigation.html` | `.project-detail-page` headings and Quarto navbar | Builds the responsive project chapter rail/drawer and synchronizes its geometry and active section. |
| `includes/mermaid-svg-ids.html` | Mermaid SVGs under `.cell-output-display` | Namespaces diagram IDs after Quarto/Mermaid render so multiple diagrams cannot collide. |

Astro owns the production navbar, footer and theme control, including on merged
Quarto project documents. Quarto still supplies document-specific Bootstrap,
search and Mermaid behaviour; these legacy includes add only the site-specific
behaviour listed above.

## Styles

| File | Description |
|---|---|
| `styles/main.scss` | SCSS entry point — imports all files below |
| `styles/main/_00-tokens.scss` | Legacy Quarto global tokens required while ordinary Quarto pages remain in transition |
| `styles/main/_01-foundation.scss` | Base element styles, typography, layout primitives |
| `styles/main/_02-shared-editorial.scss` | Shared standard-page and compact-hero editorial primitives |
| `styles/main/_10-navbar.scss` + `styles/main/navbar/` | Legacy Quarto navbar required while ordinary Quarto pages remain in transition |
| `styles/main/_11-footer.scss` | Legacy Quarto footer required while ordinary Quarto pages remain in transition |
| `styles/main/_12-page-shell.scss` | Page shell and layout container styles |
| `styles/components/_archive.scss` | Shared archive headings, actions and compact inline icons |
| `styles/components/_archive-entries.scss` | Shared archive rows, metadata, badges and actions |
| `styles/components/_section-jump.scss` | Shared publication and teaching in-page navigation |
| `styles/components/_home.scss` | Homepage layout, profile, editorial, and responsive refinements; later sections intentionally refine earlier rules |
| `styles/components/_disclosures.scss` | Shared abstract/BibTeX visibility, panels and inline controls |
| `styles/components/_notes.scss` | Homepage note rows, Notes archive and long-form note pages |
| `styles/components/_project-cards.scss` | Shared homepage and Projects archive cards, including labels and archived state |
| `styles/components/_teaching.scss` | Teaching introduction, role/year hierarchy, course lists and material actions |
| `styles/components/_contact.scss` | Contact details, email and professional-profile directory |
| `styles/components/_news.scss` | Homepage News preview, News archive, search and responsive disclosure rows |
| `styles/components/_search-popup.scss` | Legacy Quarto search overlay for unmigrated Quarto pages; not the production hybrid site-search owner |
| `styles/components/_expertise.scss` | Homepage Expertise preview and full Expertise page; later sections intentionally refine shared preview rules |
| `styles/components/_about.scss` | Homepage background/approach previews and full About page |
| `styles/components/_research.scss` | Research page hierarchy, themes, evidence and related links |
| `styles/components/_publications.scss` | Homepage publication selections and Publications archive; later sections intentionally refine shared entry styles |

`styles/project.scss` is the project-only SCSS entry point. It compiles the
partials under `styles/project/` separately from the global `styles/main.scss`
chain. Its `_article.scss` and `_article-controls.scss` files are currently
temporary manifests for the corresponding subdirectories; `_navigation.scss`
is already the canonical project-navigation owner.

### SCSS consolidation guardrails

The global and project stylesheets are independent entry chains. Preserve the
import order within a component when consolidating it: later partials often
intentionally refine earlier rules. Do not merge the two entry chains, move
Quarto/Bootstrap defaults out of `styles/main.scss`, or edit generated CSS in
`docs/`.

Consolidate one visible component at a time into its manifest file, then remove
only that component's leaf partials. Keep the navbar modules and shared archive
and disclosure components separate unless an exact ownership overlap is proven.
Every consolidation requires a render plus responsive light/dark validation;
the CI visual comparison is authoritative for accepting a visual change.

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
| Legacy Quarto search popup | `styles/components/_search-popup.scss` | Canonical only for unmigrated Quarto pages |
| Homepage Expertise preview and Expertise page | `styles/components/_expertise.scss` | Canonical |
| Homepage background/approach previews and About page | `styles/components/_about.scss` | Canonical |
| Research page | `styles/components/_research.scss` (`.about-section-heading` remains shared from `_about.scss`) | Canonical |
| Production footer | `astro/src/components/Footer.astro` + `astro/src/styles/shell.css` | Canonical |
| Outer page shell | `styles/main/_12-page-shell.scss` | Canonical |
| Homepage note selection | `styles/components/_notes.scss` | Canonical |
| Notes archive | `styles/components/_notes.scss` | Canonical |
| Long-form note pages | `styles/components/_notes.scss` | Canonical |
| Legacy Quarto project cards | `styles/components/_project-cards.scss` | Canonical for legacy Quarto rendering; `astro/src/styles/projects.css` owns the migrated Astro catalogue |
| Project article foundation and presentation | `styles/project/_article.scss` | Canonical, project-only |
| Project article context controls | `styles/project/_article-controls.scss` | Canonical, project-only |
| Project chapter navigation | `styles/project/_navigation.scss` | Canonical, project-only |
| Homepage composition | `styles/components/_home.scss` | Canonical |
| Bootstrap-era archive rows | `styles/components/_archive-entries.scss` | Canonical |
| Archive section jumps | `styles/components/_section-jump.scss` | Canonical |
| Expandable abstracts and BibTeX panels | `styles/components/_disclosures.scss` | Canonical |
| Homepage publication selections and Publications archive | `styles/components/_publications.scss` (shared archive/disclosure primitives live in their dedicated components) | Canonical |
| Teaching | `styles/components/_teaching.scss` | Canonical |
| Contact | `styles/components/_contact.scss` | Canonical |
| News | `styles/components/_news.scss` | Canonical |

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
