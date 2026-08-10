# Repository cleanup and Quarto assessment plan

## Objective

Make this repository smaller, clearer and easier to edit by:

1. removing material proven to be unused;
2. consolidating repeated content into canonical structured sources;
3. documenting source ownership, build, testing and deployment;
4. preserving the current visual identity and public URLs;
5. measuring the remaining Quarto friction after cleanup;
6. deciding whether Quarto is still appropriate without starting a migration.

Work should be delivered as small reviewable commits. Every task must identify
its canonical sources, preserve unrelated changes, validate proportionally and
provide a commit message.

## Scope boundaries

This cycle does not include:

- an Astro prototype, migration or hybrid build;
- a redesign;
- untracking `docs/`, which is the current GitHub Pages deployment output;
- removing intentionally retained duplicate PDFs solely to reduce size;
- adding intentionally omitted assets listed in
  `data/optional-local-assets.txt`;
- restructuring separate lecture-note or project repositories.

Lecture notes and technical posts remain Quarto content.

## Model allocation

Use **Luna** for narrow mechanical work with explicit files and expected output.
Use **Terra** for repository-wide audits, source-ownership changes and bounded
refactors requiring judgment. Use **Sol** only for coordination, reviewing
cross-cutting evidence and the final platform assessment.

No task should combine unrelated cleanup categories merely to fill a model
turn.

## Completed foundation

The following work is already complete and should not be repeated:

- source ownership documented in `SOURCE_MAP.md` and `ARCHITECTURE.md`;
- visual/editorial rules documented in `DESIGN.md`;
- build, dependency and test workflow documented and pinned;
- generated-output guard added for `docs/` and generated includes;
- redundant root `listings.json` removed;
- obsolete refactor reports and unreferenced note images removed;
- project citation styles consolidated into `data/citations/numeric.csl`;
- teaching consolidated into `data/teaching.yml`;
- presentations consolidated into `data/presentations_*.bib`;
- supervision consolidated into `data/supervision_*.bib`, with cancelled PhD
  supervision omitted;
- missing-but-intentional local assets declared in
  `data/optional-local-assets.txt`;
- generated teaching, presentation and supervision archives validated through
  the content generator and browser checks.

## Remaining execution plan

### Task 1 — Reproducibility audit

**Model:** Terra  
**Status:** complete

Results:

- the content generator is byte-stable across consecutive runs;
- full Quarto renders are byte-stable within one checkout;
- all generated includes have canonical-source coverage in the generated-output
  guard;
- rendered Quarto listing and Mermaid support assets are present;
- fresh checkouts differ only in Quarto's sitemap timestamps and hidden Notes
  listing file-modification sort metadata, documented in `TESTING.md`.

No source workaround was added. These are retained as explicit Quarto friction
for Task 9 rather than disguised by post-processing generated output.

Commit message: `docs: record Quarto render reproducibility limits`

### Task 2 — Structured-data schema audit

**Model:** Terra  
**Status:** complete
**Risk:** medium  
**Depends on:** Task 1

Audit the canonical BibTeX and YAML records without changing editorial content.

Work:

- verify required fields, role/type values and identifier uniqueness;
- check identifiers across publications, presentations, supervision, teaching
  and projects where they become HTML anchors;
- identify fields stored but never rendered or validated;
- add focused validation only for stable invariants;
- document intentionally preserved archival fields and optional asset links.

Do not convert BibTeX to another format merely for uniformity.

Done when malformed or ambiguous records fail early with actionable messages
and legitimate optional fields remain supported.

Suggested commit message: `test: strengthen structured content validation`

Results:

- publication, presentation, supervision and teaching IDs are unique within
  their rendered archive pages; publication IDs now receive the same early
  duplicate check as the other BibTeX archives;
- project metadata now has one loader that validates required card fields,
  unique project IDs, label shape, optional `featured` flags and related-project
  references before both generated cards and the Lua filter consume it;
- all current records pass these checks;
- standard BibTeX fields such as DOI, URL, volume and pages remain deliberately
  preserved for reusable citations even where the archive does not display
  every field; optional local download links remain governed by
  `data/optional-local-assets.txt`.

### Task 3 — Generator ownership and editability audit

**Model:** Terra  
**Status:** complete
**Risk:** medium  
**Depends on:** Task 2

Review `scripts/sitegen/` for duplication, unclear ownership and editing traps.

Work:

- map each generated include to its loader, renderer and canonical data source;
- remove dead functions and imports proven unused;
- consolidate helpers only where the same semantic operation is duplicated;
- keep presentation, supervision, teaching and publication renderers separate
  where their data models genuinely differ;
- add focused unit tests for any refactored boundary;
- keep generated HTML out of hand editing.

Done when adding or editing a record requires changing one obvious source and
the generator remains readable without premature abstraction.

Suggested commit message: `refactor: clarify generated content ownership`

Results:

- `SOURCE_MAP.md` now maps every generated file to its canonical data source,
  loader and renderer;
- the audit found no dead production helper or import to remove;
- the separate publication, presentation, supervision, teaching, project and
  news paths are intentional: their validation and rendering rules differ, so
  merging them would obscure ownership without removing meaningful duplication.

### Task 4 — Includes and runtime JavaScript audit

**Model:** Terra  
**Status:** complete
**Risk:** medium  
**Depends on:** Task 1

Audit hand-written includes and client-side behaviour against rendered output.

Work:

- verify every hand-written include is loaded and documented;
- map each runtime handler to the markup that uses it;
- remove handlers or fragments only when source and rendered searches plus
  interaction tests prove them unused;
- retain necessary Quarto, Bootstrap, search, Mermaid and theme integration;
- avoid replacing working Quarto functionality with custom JavaScript.

Done when every include and handler has a documented purpose and no proven dead
runtime code remains.

Suggested commit message: `refactor: remove unused runtime site code`

Results:

- `SOURCE_MAP.md` now records every hand-written runtime handler, its markup
  target and purpose;
- removed the obsolete custom navbar-active handler: current Quarto navigation
  has no `data-path` attributes for it to act on;
- retained the supported Quarto/Bootstrap callout, search, Mermaid, theme and
  navigation integrations, with their ownership made explicit.

### Task 5 — Stylesheet evidence audit

**Model:** Terra  
**Status:** complete
**Risk:** high  
**Depends on:** Tasks 1 and 4

Audit SCSS ownership and duplication without redesigning the site.

Work:

- verify import graphs for `styles/main.scss` and `styles/project.scss`;
- find duplicate declarations and selectors with overlapping ownership;
- check candidate unused selectors against source, rendered HTML and runtime
  class creation;
- remove only rules proven obsolete;
- move rules to their documented canonical owner when ownership is split;
- preserve responsive behaviour, accessibility and both themes.

Do not judge quality by selector or `!important` counts alone; Quarto and
Bootstrap integration must be evaluated structurally.

Done when remaining rules have clear owners and the visual regression suite
shows no unintended change.

Suggested commit message: `refactor: remove proven unused site styles`

Results:

- the 53 SCSS files form one explicit global entry chain and one separate
  project-only entry chain; component manifests make the import order and
  ownership of homepage, expertise and publication refinements explicit;
- no unowned override file, duplicate import path or safely removable rule was
  found;
- the 586 `!important` declarations are concentrated in canonical
  Quarto/Bootstrap boundary owners (page shell, navbar, archive entries and
  project layouts), rather than isolated late patches. They are retained to
  preserve the tested visual identity and recorded as Quarto friction for
  Task 9, not treated as a count to reduce blindly.

### Task 6 — Asset and link integrity audit

**Model:** Luna  
**Status:** complete
**Risk:** low  
**Depends on:** Tasks 2 and 3

Repeat the asset audit after data and generator changes.

Work:

- identify unreferenced tracked assets;
- distinguish intentional missing local assets using the manifest;
- validate internal paths, fragments and generated downloads;
- report byte-identical retained assets without deleting them;
- remove only files with no source, output or documented compatibility role.

Done when every retained asset is referenced, intentionally absent, or
explicitly retained for compatibility.

Suggested commit message: `chore: remove unreferenced site assets`

Results:

- all 57 tracked source assets have a canonical-source reference; no asset met
  the deletion threshold;
- all nine intentionally absent local presentation files remain declared only
  in `data/optional-local-assets.txt` and are not present unexpectedly;
- browser validation confirms the 22 rendered HTML pages resolve local targets
  and fragments correctly;
- `docs/assets` is the required Quarto deployment copy of tracked `assets/`,
  not a competing source archive.

### Task 7 — Documentation consistency pass

**Model:** Luna  
**Status:** complete
**Risk:** low  
**Depends on:** Tasks 1–6

Reconcile `README.md`, `AGENTS.md`, `ARCHITECTURE.md`, `SOURCE_MAP.md`,
`DESIGN.md` and `TESTING.md` with the final implementation.

Work:

- verify file paths, commands, generated/canonical distinctions and test names;
- remove repeated guidance when one document can own it and others can link;
- retain short editor-oriented instructions near the relevant source map;
- ensure the GitHub Pages `docs/` workflow is described accurately;
- remove superseded planning language.

Done when a new editor can answer “which file do I change?”, “how do I render?”
and “what do I test?” without reading implementation history.

Suggested commit message: `docs: reconcile repository editing guidance`

Results:

- README now states the current tracked-`docs/` GitHub Pages deployment model
  and makes clear that this repository has no deployment workflow to edit;
- test documentation now matches the current 16 generator tests and 121-test
  Chromium `test:full` command, while preserving the separate Firefox/WebKit
  command;
- redundant generated-JSON documentation was removed from the source map;
- canonical-source, render and test guidance is consistent across the editor
  documentation set.

### Task 8 — Final validation and cleanup report

**Model:** Terra  
**Status:** complete
**Risk:** medium  
**Depends on:** Tasks 1–7

Run the proportionate final validation and inspect the complete diff/history.

Work:

- run a clean content generation and Quarto render;
- run generator, functional, accessibility and relevant visual tests;
- inspect desktop, tablet and mobile in light and dark modes;
- verify generated output matches canonical sources;
- summarize removed material, consolidated sources and known retained debt.

Done when the production site is deployable and all remaining limitations are
explicit.

Suggested commit message: `chore: complete repository cleanup validation`

Results:

- `quarto render` completed successfully for all 22 source pages, with content
  generation and local asset validation passing;
- 16 generator tests, 47 Chromium functional tests, 44 Chromium accessibility
  tests and 18 Firefox/WebKit critical-path tests passed;
- no visual baselines were updated. Pixel comparisons remain CI-authoritative
  because the local font environment differs from the controlled Linux runner;
- the cleanup removed only proven unused source material and consolidated
  editable records into their documented canonical sources. Remaining accepted
  limits are the nine intentionally omitted assets, tracked `docs/` deployment
  output, and Quarto's documented fresh-checkout timestamp/mtime churn.

### Task 9 — Quarto fit assessment

**Model:** Sol  
**Status:** complete
**Risk:** decision only  
**Depends on:** Task 8

Assess the cleaned repository rather than the historical implementation.

Record evidence in these categories:

| Category | Question |
|---|---|
| Authoring | Does Quarto make technical and ordinary content easy to edit? |
| Native value | Which citations, maths, code, search and document features are genuinely useful? |
| Shell friction | Which navbar, layout, responsive and theme behaviours require workarounds? |
| Build cost | How much custom Python, Lua, SCSS and JavaScript exists because of Quarto? |
| Stability | Do Quarto upgrades or renders create recurring unexplained changes? |
| Alternatives | Would another platform remove more complexity than it introduces? |

Possible conclusions are:

- retain Quarto for the whole site;
- retain Quarto now but revisit the main-site shell later;
- approve a separately scoped platform experiment.

Do not implement a platform change as part of this task.

Done when `PLATFORM_DECISION.md` contains an evidence-based conclusion and the
specific conditions that would justify revisiting it.

Suggested commit message: `docs: assess Quarto after repository cleanup`

Result: retain Quarto for the whole site through the next normal maintenance
cycle, while monitoring the customized shell. `PLATFORM_DECISION.md` records
the technical-document value, measured shell friction, render-stability result
and concrete threshold for approving a separately scoped platform experiment.

## Task discipline

For every Terra or Luna task:

1. inspect `git status` and the relevant canonical sources;
2. state the bounded plan;
3. change only the named cleanup category;
4. run the smallest meaningful validation;
5. inspect the final diff;
6. report limitations and a commit message;
7. stop before the next task.

If an audit finds no justified change, record the evidence and move on without
manufacturing a commit.
