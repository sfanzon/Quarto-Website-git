# Migration implementation roadmap

## 1. Current architecture summary

Astro is the production owner of the professional site and shared shell. It
currently owns the homepage, About, Expertise, Research, Projects catalogue,
Publications, Teaching, News, Presentations, Supervision, CV, Contact, Notes
index and 404 routes. `Header.astro`, `Footer.astro` and `shell.css` provide
the navbar, footer, theme control, search and responsive shell on Astro pages
and on injected Quarto pages.

Quarto remains the document owner for every individual project page under
`projects/**` and for long-form note articles under `notes/*.qmd`. The hybrid
build renders those documents in isolation, injects the Astro-owned shell, and
merges them into `astro/dist` without sharing renderer output directories.
Project presentation remains owned by `styles/project/**`, the project filter,
project metadata and hand-written project navigation.

Structured sources remain deliberately split: `data/projects.yml` drives the
catalogue and project metadata; BibTeX files drive publications, presentations
and supervision; `data/teaching.yml` drives teaching; `news/*.md` drives News;
and `notes/*.qmd` plus `projects/**/*.qmd` remain Quarto-authored documents.
Assets are grouped under `assets/img/` and `assets/pdf/`. Generated fragments
under `includes/` are produced by `scripts/build-content.py` and are not
canonical editing targets.

The primary navigation is data-driven in `astro/src/components/Header.astro`:
About, Projects, Expertise, CV, Publications, Teaching and News are primary
links; Notes, Research, Presentations, Supervision and Contact are in More.
The local Dev dropdown is development/QA-only. Project and note pages inherit
the same visible shell after the hybrid merge.

## 2. Migration principles

- Keep Astro as the professional-site and global-shell owner. Retain the
  supported hybrid project/note implementation until the F1 renderer gate
  decides whether polished project explainers should move to Astro.
- Preserve public URLs and the completed decisions in
  `LEGACY_CONTENT_INVENTORY.md`; do not recover or remove disputed historical
  material by assumption.
- Treat the homepage as the distinctive positioning surface. Keep Research,
  Publications and the other evidence pages editorial, restrained and easy to
  audit.
- Use interaction purposefully: interactive behaviour should clarify content
  or navigation rather than act as decoration.
- Prefer source-owner fixes and small explicit components over renderer
  duplication, compatibility layers or broad rewrites.
- Preserve existing Quarto functionality (maths, citations, code, figures,
  callouts and project navigation) while improving only the shell boundary
  where necessary.
- Keep the build deterministic: Astro build, isolated Quarto renders, shell
  merge, final sitemap and Pagefind indexing.

## 3. Implementation priorities

### Priority 1 — essential before launch

1. Keep the current production build and deployment path authoritative and
   reproducible from `astro/dist` while the renderer decision is pending.
2. Resolve broken current links that point at unproduced legacy `/blog/...`
   course pages, while preserving the teaching summaries and audit decisions.
3. Complete route/resource checks for the merged Quarto project and note pages,
   including sitemap, search, shell, assets and legacy URL compatibility.
4. Decide the six deferred inventory items with Silvio before changing or
   deleting any disputed resource: Industry CV, historic CV route, Microscopy
   PDF, missing seminar slides, Curriculum Design links, and Scopus/arXiv
   profile metadata.

### Project-renderer architecture gate

Before choosing native Astro as the general project renderer, migrating other
project explainers, or simplifying/removing the hybrid because of that renderer
decision, build a full-fidelity F1 Astro POC beside the existing Quarto page.
Compare rendered fidelity, authoring ergonomics and maintenance complexity, then
make an explicit renderer decision. This is not inherently a launch blocker:
the site may launch with the current supported hybrid architecture when it is
production-ready.

### Priority 2 — important improvements

1. Recover only the historical PDFs/slides/resources explicitly selected after
   the inventory decisions; record their new ownership and links.
2. Add focused content/link validation for publications, teaching,
   presentations, supervision, downloads and merged Quarto documents.
3. Review accessibility, metadata, redirects and external-link health across
   the final public route inventory.
4. Remove obsolete transitional source/configuration only after production
   ownership and URL coverage are verified.

### Priority 3 — optional polish

1. Improve cross-page related-resource links and optional profile links.
2. Add carefully selected archived historical resources where they strengthen
   the professional site without enlarging the navigation.
3. Apply small typography or interaction refinements only when supported by
   visual review and the established design rules.

## 4. Page-by-page roadmap

| Section | Current state | Target state | Required work | Dependencies |
|---|---|---|---|---|
| Homepage | Astro-owned, visually accepted, consumes generated News and selected publication/project evidence. | Stable professional landing page with no donor/demo content and reliable links. | Keep content stable; verify asset and link coverage during launch checks. | Final route/link validation. |
| Research | Astro-owned `/research/` with three research themes and links into evidence pages/projects. | Editorial research overview that remains concise and points to canonical evidence. | Validate links and remove only demonstrably stale destinations. | Publications/projects ownership; no redesign. |
| Projects | Astro `/projects/` catalogue reads `data/projects.yml`; every detail page remains Quarto in the supported hybrid. | Preserve the catalogue-to-document experience while deciding the final renderer for polished explainers through F1. | Build the full-fidelity F1 Astro POC beside Quarto; compare rendering and authoring before any broader migration. | F1 renderer gate; current hybrid build and Quarto rendering. |
| Publications | Astro `/publications/` consumes generated publication HTML from `data/publications.bib`; resources are audited. | Complete, restrained publication archive with trustworthy PDF/external-resource actions. | Resolve only selected external-resource decisions; add link checks. | Publication audit; generated-content pipeline. |
| Teaching | Astro `/teaching/` consumes generated `data/teaching.yml` output; summaries and selected materials survive. | Accurate teaching catalogue without dead legacy course-page actions. | Decide how to handle legacy `/blog/...` links and recover/archive selected course resources. | Teaching inventory decisions; no page rewrite required. |
| Presentations | Astro `/presentations/` renders 23 BibTeX records; 11 slide/poster files remain local and 10 are absent. | Records remain complete, with deliberately chosen resources and honest links. | Decide which missing slides to recover/archive and verify Curriculum Design links. | Presentation inventory decisions. |
| Supervision | Astro `/supervision/` renders 8 master’s/undergraduate records; the 2025 PhD record is deliberately omitted. | Public supervision page reflects the accepted scope and has no unintended student-resource exposure. | Keep the omission; verify whether any standalone student resources need a separate decision. | Supervision audit; privacy/content review. |
| CV | Astro `/cv/` exposes the academic CV PDF; historic and Industry CV items remain deferred. | Clear academic CV route with intentional compatibility policy. | Decide the Industry CV and historic `/Silvio_Fanzon_CV.pdf` policy before implementing links/redirects. | Silvio’s future decisions; deployment URL policy. |
| About | Astro-owned `/about/` with the accepted career narrative and shared shell. | Stable personal/professional context page with intentional profile links. | Keep the accepted content; verify profile and download links during launch checks. | Profile metadata decision; shared shell. |
| Contact | Astro-owned `/contact/` with current contact/profile actions. | Clear contact path with only intentional public profile links. | Decide whether Scopus/arXiv profile links belong on the public contact surface; otherwise retain the documented omission. | Profile metadata decision; no redesign. |

## 5. Explicit non-goals

- Do not rebuild or preserve generic al-folio demo pages, books, repository
  listings, caches, starter media or template screenshots classified for
  deliberate removal.
- Do not recover disputed PDFs, slide decks, CVs or profile links until the
  decisions in the inventory handoff are made.
- Do not convert individual `projects/**` pages or Quarto note articles until
  the F1 renderer gate supports that decision; do not create duplicate
  implementations beyond the bounded F1 proof of concept.
- Do not replace BibTeX/YAML canonical data with a new content architecture as
  part of ordinary page migration.
- Do not redesign the global shell, project-document presentation or accepted
  homepage merely to make the two renderers look conceptually identical.
- Do not treat generated `docs/`, `astro/dist/`, `includes/` fragments or
  cached indexes as migration sources.

## 6. Implementation sequence

1. Confirm the production branch/build/deployment contract and freeze the
   accepted shell and URL policy.
2. Resolve the six future inventory decisions with Silvio; record any changed
   decisions in the inventory before implementation.
3. Fix only confirmed broken Teaching links and run focused route/resource
   checks across the existing Astro pages.
4. Recover or archive only the selected historical documents/slides, placing
   them under the existing asset ownership and updating their canonical data
   links.
5. Validate the supported hybrid merge end-to-end: Astro pages, Quarto project/note
   pages, shared shell, maths/citations/code, sitemap, Pagefind and downloads.
6. Run accessibility, link, functional and visual checks at representative
   desktop/mobile states; update baselines only for accepted visual changes.
7. If a project-renderer decision is needed, run the F1 architecture gate;
   retain the hybrid if it does not support migration, or only then plan a
   broader showcase-project transition. Do not assume either outcome.
8. Simplify or remove hybrid infrastructure only after that explicit renderer
   decision and the necessary migration work, then perform a final
   inventory-to-route reconciliation.
