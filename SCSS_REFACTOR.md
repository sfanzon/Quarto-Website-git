# Main SCSS refactor

## Status

Phases 1 and 2 are complete, and Phase 3 is underway. The current cascade is
fingerprinted, the visual capture matrix is defined in
`tests/visual/baseline-manifest.json`, and the rule layers are extracted into
ordered partials.

- [x] Record the source and rendered CSS fingerprints.
- [x] Define representative pages, themes and viewports.
- [x] Inventory the current cascade layers.
- [x] Capture the 20 baseline screenshots.
- [x] Confirm the baseline set before moving any SCSS.
- [x] Extract the unchanged rules into four ordered partials.
- [x] Render the full site and compare all 20 screenshots.

The baseline suite passes after the extraction without updating the saved
screenshots.

## Phase 2 extraction

`styles/main.scss` retains the Quarto defaults and imports the rule layers in
their original order:

1. `styles/main/_01-foundation.scss`
2. `styles/main/_02-editorial.scss`
3. `styles/main/_03-overrides.scss`
4. `styles/main/_04-current-pages.scss`

Concatenating those partials after the first 20 lines of the entrypoint
reproduces the original 210,650-byte file exactly, including its SHA-256
fingerprint. Quarto renders all 40 pages successfully and all 20 Playwright
comparisons pass.

Quarto 1.9.38 follows the imports during SCSS analysis and appends its generated
CSS variable-export block. This changes the generated Bootstrap CSS hashes but
not the imported rule bytes or any captured pixels.

## Phase 3 consolidation log

| Family | Change | Verification |
| --- | --- | --- |
| Publication metadata | Replaced three consecutive correction layers with one authoritative base block and the existing responsive breakpoints | 40-page render and 20/20 visual comparisons |
| Teaching list | Removed superseded timeline, card and separator layers; retained one authoritative open-list layout | 40-page render and 20/20 visual comparisons |

## Baseline identity

- Source commit: `e319c4c079d7159283719f3beddcd8d0abba9bf6`
- Quarto: `1.9.38`
- `styles/main.scss`: 7,583 lines, 210,650 bytes
- SCSS SHA-256:
  `75f1533f999b45721a2cffc51fa34c92f33f7c8875a42e74b65c5088160a7a13`
- Light CSS SHA-256:
  `4ff9ff6c8c244e4515bd3346d86bad23a325bd64e5171906f3cb7fc92689b720`
- Dark CSS SHA-256:
  `ba349ace7c8e8bd45abd424f698e9fd78b7aa26301dc9f9b3de6502c6ebeb8ba`

The source commit identifies the last committed site state. The fingerprints
are the authoritative baseline when the worktree contains unrelated changes.

## Visual matrix

Capture every page as a full-page PNG in both light and dark mode:

| Page | Purpose |
| --- | --- |
| `index.html` | Homepage hero, editorial sections, cards, news and footer |
| `publications.html` | Metadata rail, actions, typography and long lists |
| `teaching.html` | Year groups, course entries and responsive actions |
| `projects.html` | Shared project cards and portfolio layout |
| `projects/f1-time-rank-duality/index.html` | Project navigation and article components |

Use these fixed viewports:

| Name | Width | Height |
| --- | ---: | ---: |
| `desktop` | 1440 | 1000 |
| `mobile` | 390 | 844 |

Store captures under `tests/visual/baselines/` using:

`<page>--<theme>--<viewport>.png`

Animations and transitions must be disabled, reduced motion must be enabled,
and capture must wait for `document.fonts.ready`.

## Cascade inventory

The current file contains 79 media queries, 778 `!important` declarations and
11 explicit `body.quarto-dark` blocks. These numbers are not cleanup targets by
themselves; they are warning signals that order and specificity are carrying
substantial behavior.

The existing cascade has four broad strata:

| Lines | Current responsibility |
| --- | --- |
| 1-1724 | Bootstrap defaults, theme variables, shell, typography, navbar, footer and legacy components |
| 1725-3496 | First editorial redesign and page-level systems |
| 3497-6568 | Successive navbar, homepage, publication, teaching, search and news corrections |
| 6569-7583 | Current career narrative, responsive ordering and project-page presentation |

These are audit ranges, not proposed partial boundaries. Phase 2 must preserve
the exact declaration order while extracting partials.

## Refactor sequence

1. Capture and approve all baseline screenshots.
2. Extract unchanged rules into ordered partials.
3. Render and compare all 20 screenshots.
4. Consolidate one component family per commit.
5. Render all 40 pages and compare after every family.

The first extraction must not rename selectors, combine declarations, change
specificity or reorder media queries.
