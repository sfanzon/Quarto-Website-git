# Astro–Quarto working plan

## Goal

Test whether Astro should replace Quarto as the owner of the main professional
website while retaining Quarto wherever it is genuinely the better authoring
and rendering tool.

This is an incremental proof, not authorization for a full migration.

## Non-negotiable requirements

1. Lecture notes remain Quarto projects.
2. Technical and mathematical posts that benefit from citations,
   cross-references, executable code, equations or document structure remain
   Quarto.
3. Astro and Quarto output must look and behave like one website. Framework
   changes must be invisible or nearly invisible to readers.
4. Preserve the current warm editorial identity, URL structure, responsive
   behaviour, accessibility and light/dark modes.
5. Every piece of content, navigation and metadata has one canonical source.
6. Production remains the current Quarto site until the experiment passes its
   decision gate.

## Proposed ownership

| Responsibility | Owner |
|---|---|
| Homepage and ordinary pages | Astro |
| Global routing and website structure | Astro |
| Project, writing and news catalogues | Astro |
| Publications, teaching and supervision archives | Astro, reading the existing structured data |
| Industry-facing project overviews | Astro |
| Ordinary prose articles | Astro Markdown or MDX |
| Mathematical and scientific technical posts | Quarto |
| Executable analysis and document-style walkthroughs | Quarto |
| Lecture-note websites | Separate Quarto projects |
| Brand tokens and global visual rules | Shared framework-neutral contract |
| Navbar and footer behaviour | Framework-native implementations generated from shared data |
| Final build, collision checks, search and sitemap | Main website build pipeline |

Astro owns the catalogue even when an entry links to a Quarto-rendered page.
Quarto owns only the documents assigned to it.

## Shared visual contract

Start inside this repository. Do not create a separate design-system repository
until at least two independent sites consume the contract successfully.

Share only stable identity primitives:

- colours and light/dark tokens;
- typography and font loading;
- the 1180/820/720 px width system;
- global gutters, link treatment and focus styles;
- navigation and footer data;
- logo, favicon and common icons;
- theme-state names and persistence rules.

Do not share one universal interactive navbar HTML fragment. Astro and Quarto
should render their own accessible navbar from the same data. Likewise, keep
Astro cards and filters, Quarto citations and callouts, and course navigation in
their owning framework.

## Content sources

Retain the cleaned canonical records wherever possible:

- `data/projects.yml`;
- `data/publications.bib`;
- `data/presentations_*.bib`;
- `data/supervision_*.bib`;
- `data/teaching.yml`;
- `data/coauthors.yml`;
- `news/*.md`;
- technical `.qmd` documents and their bibliographies.

The Astro prototype must consume these sources directly or through a small
tested adapter. Do not create parallel Astro-only copies of the same records.

## Output architecture

Build each renderer into a staging directory and assemble the deployable site
only after both succeed:

```text
Astro build  ──────> staging/astro/
Quarto render ─────> staging/quarto/
                         │
collision + URL checks ──┤
                         ▼
                       dist/
```

Astro owns the main routes. Quarto may write only to explicitly assigned paths,
for example:

```text
/projects/f1-time-rank-duality/technical/
/writing/<technical-post>/
```

The assembly step must fail on an undeclared path collision. It must not rely on
copy order to decide which renderer wins.

Astro owns the combined sitemap, RSS and catalogue metadata. Full-site search
runs after output assembly so it indexes both Astro and Quarto HTML. Quarto's
site-wide search and navigation are disabled for embedded technical documents.

## Vertical-slice experiment

Build only this slice first:

```text
/                                           Astro homepage
/projects/                                  Astro catalogue
/projects/f1-time-rank-duality/             Astro overview
/projects/f1-time-rank-duality/technical/   Quarto document
```

Also apply the same visual contract to one existing lecture-note repository,
without changing its Quarto sidebar, page TOC, equations, code or course
structure.

Use `dadangnh/as-folio` as an architectural reference for BibTeX, academic
content and Astro conventions. Do not fork it or inherit its visual design and
full dependency stack unless the prototype demonstrates a specific advantage.

## Execution phases

### Phase 0 — Preserve the reference

- finish the current Quarto cleanup;
- keep the working production build deployable;
- record representative light/dark screenshots at desktop, tablet and mobile;
- preserve existing routes and content sources as the comparison baseline.

### Phase 1 — Extract the visual contract locally

- expose the current colour, typography, width and spacing tokens in a
  framework-neutral form;
- define canonical navigation/footer data and theme-state behaviour;
- keep component styles in their current framework owners;
- document which global rules are allowed to cross the boundary.

### Phase 2 — Build the Astro half of the slice

- scaffold an isolated Astro prototype that cannot overwrite `docs/`;
- implement the homepage, Projects catalogue and F1 overview;
- read the existing project data rather than duplicating it;
- preserve current URLs, metadata, responsive behaviour and design identity.

### Phase 3 — Integrate the Quarto technical page

- render the existing F1 technical source into its assigned staging path;
- apply the shared tokens, typography, navbar/footer data and theme protocol;
- retain Quarto-native equations, citations, code, figures and document
  semantics;
- remove embedded Quarto features that duplicate Astro's site-level ownership.

### Phase 4 — Assemble one site

- add one build command for Astro, Quarto and output assembly;
- add explicit path ownership and collision checks;
- make asset paths work in local preview and at the production domain;
- generate combined search, sitemap and RSS after assembly;
- document local preview and deployment.

### Phase 5 — Validate seamless integration

Compare Astro and Quarto pages at:

- desktop: 1440 × 1000;
- tablet: 820 × 1180;
- mobile: 390 × 844;
- light and dark modes.

Verify:

- identical navbar/footer geometry and interaction;
- consistent typography, colours, gutters and width system;
- theme state persists when crossing renderer boundaries;
- no flash of the wrong theme;
- keyboard focus, menus and touch targets remain accessible;
- the F1 overview/technical transition feels continuous;
- no broken assets, links, canonical URLs or metadata;
- one-command clean build and preview.

### Phase 6 — Decision gate

Proceed only if Astro materially simplifies ordinary website development and
the cross-renderer cost remains small and testable.

Stop and retain the all-Quarto site if visual fixes, asset handling, previewing,
navigation or theme behaviour need recurring renderer-specific patches.

### Phase 7 — Incremental migration after approval

If the experiment passes:

1. migrate global catalogues and ordinary pages;
2. migrate industry-facing project overviews;
3. classify each note as Astro prose or Quarto technical content;
4. keep technical posts in Quarto without rewriting them merely for platform
   uniformity;
5. integrate lecture-note repositories through versioned releases of the
   proven visual contract;
6. retire old Quarto-owned main-site routes only after URL and content parity is
   verified.

## Success criteria

The architecture is acceptable only when:

- readers cannot meaningfully tell which renderer produced a page;
- technical posts and lecture notes retain all useful Quarto capabilities;
- ordinary website editing is simpler in Astro;
- one source drives each catalogue and navigation element;
- one command produces a complete deployable site;
- one automated suite checks both renderers together;
- adding a new Astro article or Quarto technical post is documented and
  unsurprising.

## Immediate next action

Complete Phase 0, then create the isolated vertical slice. Do not restructure
the production repository or deploy Astro before the slice is reviewed and
accepted.
