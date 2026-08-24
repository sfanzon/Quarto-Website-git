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
2. Preserve the migrated legacy course Notes, Teaching links and `/blog/...`
   compatibility redirects through launch validation.
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

### Legacy course entries → Notes migration map

All twelve genuine legacy course posts are retained as main-site Quarto Notes.
Their Teaching records link to the migrated Notes and their former `/blog/...`
URLs have compatibility redirects. Separate maintained teaching resources may
coexist later, but they do not replace these historical Notes.

| Legacy title and source | Old URL | Current Teaching record | What it contains | Proposed canonical Notes destination | Teaching link / redirect |
|---|---|---|---|---|---|
| Advanced Functional Analysis (2019/20) — `_posts/2019-09-22-Advanced-Functional-Analysis.md` | `/blog/2019/Advanced-Functional-Analysis/` | `2019-Functional-Analysis` | Graz MSc practical companion: topics, reading, exercise sheets, final exam and assessment. | Main-site Note: `/notes/advanced-functional-analysis-2019-20.html` — **Advanced Functional Analysis**. | Yes / yes. |
| Calculus of Variations (2020/21) — `_posts/2021-02-01-Calculus-of-Variations.md` | `/blog/2021/Calculus-of-Variations/` | `2021-Calculus-Variations` | Graz MSc course: syllabus, schedule, assessment, lecture notes/videos and exercise sheets. | Main-site Note: `/notes/calculus-of-variations-2020-21.html` — **Calculus of Variations**. | Yes / yes. |
| Analysis 3 (2022/23) — `_posts/2022-09-18-Analysis-3.md` | `/blog/2022/Analysis-3/` | `2022-Analysis` | Graz BSc practical companion: class calendar, assessment rules, references and weekly exercise sheets. | Main-site Note: `/notes/analysis-3-2022-23.html` — **Analysis 3**. | Yes / yes. |
| Inverse Problems (2022/23) — `_posts/2022-09-26-Inverse-Problems.md` | `/blog/2022/Inverse-Problems/` | `2022-Inverse-Problems` | Graz MSc practical companion: topics, references, assessments, exercise sheets and Matlab/Python assignments. | Main-site Note: `/notes/inverse-problems-2022-23.html` — **Inverse Problems**. | Yes / yes. |
| Numbers, Sequences and Series (2023/24) — `_posts/2023-06-01-NSS.md` | `/blog/2023/NSS/` | `2023-NSS` | Hull taught edition: course information, lecture notes link, lectures diary, tutorials and homework. | Main-site Note: `/notes/numbers-sequences-and-series-2023-24.html` — **Numbers, Sequences and Series**. | Yes / yes. |
| Differential Geometry (2023/24) — `_posts/2023-06-02-Differential-Geometry.md` | `/blog/2023/Differential-Geometry/` | `2023-Differential-Geometry` | Hull taught edition: course information, lecture notes link, lectures diary and homework. | Main-site Note: `/notes/differential-geometry-2023-24.html` — **Differential Geometry**. | Yes / yes. |
| Differential Geometry (2024/25) — `_posts/2024-09-15-Differential-Geometry.md` | `/blog/2024/Differential-Geometry/` | `2024-Differential-Geometry` | Hull taught edition: course information, lecture notes link, schedule, assessment, lectures diary and homework. | Main-site Note: `/notes/differential-geometry-2024-25.html` — **Differential Geometry**. | Yes / yes. |
| Numbers, Sequences and Series (2024/25) — `_posts/2024-09-15-NSS.md` | `/blog/2024/NSS/` | `2024-NSS` | Hull taught edition: course information, lecture notes link, schedule, tutorials, lectures diary and homework. | Main-site Note: `/notes/numbers-sequences-and-series-2024-25.html` — **Numbers, Sequences and Series**. | Yes / yes. |
| Statistical Models (2023/24) — `_posts/2024-1-4-Statistical-Models.md` | `/blog/2024/Statistical-Models/` | `2024-Statistical-Models` | Hull taught edition: linear-model syllabus, slides link, lectures diary, statistical tables, R code, datasets and homework. | Main-site Note: `/notes/statistical-models-2023-24.html` — **Statistical Models**. | Yes / yes. |
| Statistical Models (2024/25) — `_posts/2025-1-9-Statistical-Models.md` | `/blog/2025/Statistical-Models/` | `2025-Statistical-Models` | Hull taught edition: linear-model syllabus, slides link, lectures diary, statistical tables, R code, datasets and homework. | Main-site Note: `/notes/statistical-models-2024-25.html` — **Statistical Models**. | Yes / yes. |
| Graduate Skills (2025/26) — `_posts/2026-1-1-Graduate-Skills.md` | `/blog/2026/Graduate-Skills/` | `2026-Graduate-Skills` | Hull MSc project-skills course followed by apparently copied Statistical Models material retained verbatim. | Main-site Note: `/notes/graduate-skills-2025-26.html` — **Graduate Skills**. | Yes / yes. |
| Statistical Models (2025/26) — `_posts/2026-1-1-Statistical-Models.md` | `/blog/2026/Statistical-Models/` | `2026-Statistical-Models` | Hull taught edition: linear-model syllabus, slides link, lectures diary, statistical tables, R code, datasets, assessment and deadlines. | Main-site Note: `/notes/statistical-models-2025-26.html` — **Statistical Models**. | Yes / yes. |

### Priority 2 — important improvements

1. Recover only the historical PDFs/slides/resources explicitly selected after
   the inventory decisions; record their new ownership and links.
2. Add focused content/link validation for publications, teaching,
   presentations, supervision, downloads and merged Quarto documents.
3. Review accessibility, metadata, redirects and external-link health across
   the final public route inventory.
4. Remove obsolete transitional source/configuration only after production
   ownership and URL coverage are verified.
5. Review the migrated Graduate Skills Note separately: the legacy source's
   apparently copied Statistical Models material was preserved faithfully and
   requires an explicit later content cleanup.

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
| Teaching | Astro `/teaching/` consumes generated `data/teaching.yml` output; all twelve legacy course pages now survive as Quarto Notes with redirects and recovered linked resources. | Accurate teaching catalogue linked to the historical Notes and any separate maintained resources. | Review Graduate Skills copied material later; otherwise preserve the migrated archive faithfully. | Teaching Notes and hybrid route/resource validation. |
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
3. Run focused route/resource checks across the existing Astro pages and
   migrated Quarto Notes.
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
