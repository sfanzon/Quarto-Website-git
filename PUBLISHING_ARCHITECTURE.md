# Publishing architecture

> **Canonical target publishing architecture**<br>
> **Agreed 2026-08-21**

This document describes the target publishing topology, not necessarily the
current implementation state. Current implementation mechanics remain in
`ARCHITECTURE.md` until migrated. Future agents must not change this
architecture casually: a change requires an explicit user decision and its
rationale recorded here.

> **Astro is the curated professional front door. Independent Quarto
> repositories remain self-contained. GitHub organizations provide native
> category namespaces for notes and technical resources. Static academic
> assets may later move to a dedicated assets repository. Public taxonomy is
> designed for humans; deployment remains simple and local to each repository.**

## Main website

Repository: `sfanzon/Quarto-Website-git`<br>
Public site: <https://silviofanzon.com/>

Astro is the curated professional communication layer. It owns the
professional identity, homepage, Research, Projects catalogue, Publications,
Teaching catalogue, Presentations catalogue, CV, News/writing, polished
portfolio explainers and navigation to deeper resources. It must not become
responsible for building every independent Quarto resource.

## Main-site renderer endpoint

The publishing topology in this document remains canonical and unchanged. The
main-site renderer endpoint is now **native Astro**.

### Main website — native Astro

The homepage, About, Expertise, Research and other index/catalogue pages,
Projects catalogue, Publications, Teaching catalogue, Presentations catalogue,
CV, News/writing and other normal professional-site pages belong natively in
Astro. This also includes polished portfolio/showcase explainers: F1,
Sparse-FCGCG, Statistical Models and future equivalent project pages.

The main site must not permanently render Quarto project or note documents and
merge them into `astro/dist`.

### Independent Quarto

Quarto remains the appropriate home for the actual Statistical Models course,
long mathematical or scientific notes, deep technical/reproducibility
resources, citation-heavy documents, computational/reproducible scientific
documents and other material that benefits from Quarto document semantics.
Those resources remain independently deployed under the notes and technical
topology defined below.

### Current and target implementation

The current transitional implementation is:

```text
main repository
├── Astro
└── Quarto project/note sources
        ↓
render Quarto
        ↓
temporary staging
        ↓
merge into Astro output
        ↓
astro/dist
```

The target main-site implementation is:

```text
Astro
    ↓
Astro build
    ↓
silviofanzon.com
```

Independently, a Quarto resource repository follows:

```text
Quarto resource repository
    ↓
GitHub Actions
    ↓
GitHub Pages
    ↓
notes.silviofanzon.com/<repo>/
or technical.silviofanzon.com/<repo>/
```

The hybrid Quarto → temporary render → merge pipeline is transitional, not
part of the final target architecture. Remove that machinery after the
relevant content migrations are complete rather than preserving it as
permanent infrastructure.

Astro and Quarto have different roles, not a quality hierarchy. Astro serves
portfolio/showcase pages that benefit from the main component system, bespoke
editorial layouts, purposeful interaction and direct integration with the
professional site. Quarto serves equations, citations, long scientific
documents, course structure, reproducibility, computational material and
technical notes.

### Project migration and preservation

Use this target rule for current and future work:

- polished portfolio/showcase explainer → native Astro;
- deep technical/reproducibility resource → standalone Quarto under `technical.`;
- maintained course or lecture notes → standalone Quarto under `notes.`.

Renderer migration does not imply a redesign or content rewrite. When moving a
Quarto project explainer to Astro, preserve accepted prose, equations,
figures, citations, code examples, hierarchy, design decisions and existing
assets unless a user explicitly directs otherwise.

For F1, <https://silviofanzon.com/projects/f1-time-rank-duality/> is the
native Astro polished explainer and
<https://technical.silviofanzon.com/F1-TimeRank-Duality/> is the independent
Quarto technical/reproducibility resource. Migrate the existing project
content rather than restarting it: preserve its narrative, responsible
interpretation material, analysis pipeline, R snippets and accepted visual
decisions.

For Sparse-FCGCG, <https://silviofanzon.com/projects/sparse-fcgcg/> is the
native Astro polished explainer and
<https://technical.silviofanzon.com/Sparse-FCGCG/> is the independent Quarto
technical/reproducibility resource. Migrate accepted content without an
unnecessary rewrite.

For Statistical Models, <https://silviofanzon.com/projects/statistical-models/>
is the native Astro polished project/showcase page and
<https://notes.silviofanzon.com/Statistical-Models/> is the full standalone
Quarto course. Do not move the course itself into Astro.

## Notes namespace

Target namespace: <https://notes.silviofanzon.com/><br>
GitHub organization: `sfanzon-notes`<br>
Organization Pages repository: `sfanzon-notes/sfanzon-notes.github.io`

The organization Pages site owns the custom domain. Project sites inherit the
native path under that domain:

- `sfanzon-notes/Statistical-Models` → `/Statistical-Models/`
- `sfanzon-notes/2026-Statistical-Models-Slides` → `/2026-Statistical-Models-Slides/`
- `sfanzon-notes/2025-Statistical-Models-Slides` → `/2025-Statistical-Models-Slides/`
- `sfanzon-notes/2024-Statistical-Models-Slides` → `/2024-Statistical-Models-Slides/`
- `sfanzon-notes/2024-Differential-Geometry-Notes`
- `sfanzon-notes/2023-Differential-Geometry-Notes`
- `sfanzon-notes/2024-Differential-Geometry-Revision`
- `sfanzon-notes/2024-NSS-Notes`
- `sfanzon-notes/2023-NSS-Notes`
- `sfanzon-notes/2024-NSS-Revision`

This namespace contains maintained courses, lecture notes, substantial
teaching resources, historical taught editions and revision material. A
resource containing slides remains a teaching resource; it does not imply a
`slides.` namespace.

The future year-independent Statistical Models repository is
`sfanzon-notes/Statistical-Models`, titled **Statistical Models** with the
subtitle **Lecture notes and computational examples**. It should retain the
strongest/latest mathematics, R, examples, datasets, appendices, references
and licence while removing Hull-specific logistics. The polished project page
remains `/projects/statistical-models/` on the main site.

Do not create canonical Differential Geometry or NSS repositories merely for
symmetry; create them only with a real intention to maintain year-independent
editions.

## Technical namespace

Target namespace: <https://technical.silviofanzon.com/><br>
GitHub organization: `sfanzon-technical`<br>
Organization Pages repository: `sfanzon-technical/sfanzon-technical.github.io`

Target resources:

- `sfanzon-technical/F1-TimeRank-Duality`
- `sfanzon-technical/Sparse-FCGCG`

Each technical repository is self-contained: it owns implementation/code,
data and analysis where appropriate, reproducibility material, its Quarto
technical minisite, build and GitHub Pages deployment. The main site links to
these resources but does not render them.

For F1, `/projects/f1-time-rank-duality/` is the polished Astro explainer,
`https://technical.silviofanzon.com/F1-TimeRank-Duality/` is the detailed
technical/reproducibility resource, and the GitHub repository remains the
source for code and version history. Sparse-FCGCG follows the same principle.
There is no subdomain per technical project.

## Independent Quarto rule

An independent resource repository is self-contained:

```text
repository/
├── .qmd source
├── _quarto.yml
├── local CSS/includes
├── required local figures/data
├── GitHub Actions workflow
└── GitHub Pages deployment
```

Its flow is: push to the resource repository → GitHub Actions renders Quarto →
GitHub Pages deploys it → `silviofanzon.com` links outward. Do not introduce a
cross-repository Astro/Quarto mega-build, proxy routing for cosmetic URLs,
Cloudflare/Netlify routing for this purpose, or duplicated implementations.

## Assets namespace (future)

Reserve <https://assets.silviofanzon.com/> for a future `Website-Assets`
repository. Suggested public folders are `papers/`, `presentations/`,
`posters/`, `figures/`, `images/`, `downloads/` and `media/`. This is for
ordinary public PDFs, papers, presentation PDFs, posters, figures, images and
downloads—not unlimited storage for large datasets, video archives or binary
backups. `Website-Assets` is expected to be a single repository initially, so
it does not require another GitHub organization. Its GitHub Pages site may
directly own `assets.silviofanzon.com`. Create an assets organization only if
multiple independent asset repositories later genuinely need to share that
namespace.

## Presentations and slides

Do not create `slides.silviofanzon.com` now. Beamer PDFs belong in the Astro
`/presentations/` catalogue and, later, the assets namespace. The existing
`2024-Curriculum-Design-Slides` Reveal.js presentation remains a standalone
exception. Reconsider a slides namespace only if a substantial collection of
independently deployed web-native decks develops.

## Target public tree

```text
silviofanzon.com
├── projects/
│   ├── f1-time-rank-duality/ → technical.silviofanzon.com/F1-TimeRank-Duality/
│   ├── sparse-fcgcg/         → technical.silviofanzon.com/Sparse-FCGCG/
│   └── statistical-models/   → notes.silviofanzon.com/Statistical-Models/
├── teaching/                 → catalogue/history and links to notes resources
├── presentations/            → catalogue, PDFs/assets and occasional web deck
└── normal Astro sections

notes.silviofanzon.com
├── Statistical-Models/
├── 2026-Statistical-Models-Slides/
├── 2025-Statistical-Models-Slides/
├── 2024-Statistical-Models-Slides/
├── 2024-Differential-Geometry-Notes/
├── 2023-Differential-Geometry-Notes/
├── 2024-Differential-Geometry-Revision/
├── 2024-NSS-Notes/
├── 2023-NSS-Notes/
└── 2024-NSS-Revision/

technical.silviofanzon.com
├── F1-TimeRank-Duality/
└── Sparse-FCGCG/

assets.silviofanzon.com        [future]
├── papers/  ├── presentations/  ├── posters/
├── figures/ ├── images/         └── downloads/

slides.silviofanzon.com        [not now]
```

## GitHub and DNS model

There is one human GitHub account, `sfanzon`. `sfanzon-notes` and
`sfanzon-technical` are organizations administered by that account, not
separate user identities. Both may use public GitHub Free repositories.

For notes, configure the organization Pages repository with custom domain
`notes.silviofanzon.com` and DNS CNAME `notes.silviofanzon.com` →
`sfanzon-notes.github.io`. Project repositories inherit
`notes.silviofanzon.com/<repository-name>/`. Use the analogous setup for
`sfanzon-technical` and `technical.silviofanzon.com`. Repositories intended to
inherit the organization domain should not independently override it.

Repository transfers and public Pages URL migration are different. GitHub may
redirect repository URLs, but an old Pages URL must not be assumed to redirect.
For every live URL, check external usage and preserve it temporarily, redirect
from the main site, or intentionally retire it. Migrate incrementally, never
as a big bang.

## Visual continuity

Independent Quarto sites should belong to the same family without sharing a
coupled build: warm editorial identity, charcoal, warm off-white, restrained
rust, native/system sans, compatible widths, restrained borders and compact
chrome, with little or no decorative animation for technical resources.
Quarto may reproduce this language through its own CSS/includes.

## Naming and decision rules

Use the semantic public namespaces `silviofanzon.com`,
`notes.silviofanzon.com`, `technical.silviofanzon.com` and
`assets.silviofanzon.com`. Do not casually add `research.`, `projects.`,
`teaching.`, `archive.`, `code.` or `data.` subdomains. Keep meaningful
repository names such as `F1-TimeRank-Duality`, `Sparse-FCGCG` and the dated
course resources; do not rename repositories for cosmetic URLs.

Classify future resources as follows:

- polished public narrative → Astro / `silviofanzon.com`;
- maintained course or lecture notes → `sfanzon-notes` / notes subdomain;
- substantial technical/reproducibility site → `sfanzon-technical` / technical subdomain;
- paper, poster, figure or static download → eventually `Website-Assets` / assets subdomain;
- Beamer PDF → presentation catalogue + assets; occasional HTML deck → standalone exception; many web-native decks → reconsider slides only then.

## Non-goals and governance

This architecture does not call for one subdomain per project, multiple
personal GitHub accounts, proxy routers, Netlify/Cloudflare routing, a central
cross-repository build, forcing repository names to mirror website taxonomy,
year-independent versions of every historical course, a slides subdomain now,
or GitHub Pages as unlimited heavy-file storage.

**Astro is the curated professional front door. Independent Quarto repositories
remain self-contained. GitHub organizations provide native category namespaces
for notes and technical resources. Static academic assets may later move to a
dedicated assets repository. Public taxonomy is designed for humans; deployment
remains simple and local to each repository.**
