# Main SCSS refactor

## Status

Phases 1 through 4 are complete. The cascade is
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
- [x] Consolidate active correction layers component by component.
- [x] Remove legacy selectors absent from source, generated pages and runtime code.
- [x] Harden generated publication markup and standalone project styles.
- [x] Complete the 40-page render and 177-check safety matrix.

The baseline suite passes after the consolidation without updating the saved
screenshots.

## Phase 2 extraction

`styles/main.scss` retains the Quarto defaults and imports the token and rule
layers in their original order:

1. `styles/main/_00-tokens.scss`
2. `styles/main/_01-foundation.scss`
3. `styles/main/_02-editorial.scss`
4. `styles/main/_03-overrides.scss`
5. `styles/main/_04-current-pages.scss`

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
| Homepage role typography | Collapsed six contradictory role-specific corrections into the authoritative current-page layer | 40-page render and 20/20 visual comparisons |
| Homepage profile links | Consolidated container, anchor, mobile and About-link corrections; removed the superseded divider layer | 40-page render and 20/20 visual comparisons |
| Homepage degree | Replaced four desktop/mobile correction blocks with one authoritative rule and one effective mobile adjustment | 40-page render and 20/20 visual comparisons |
| Homepage hero positioning | Folded final scroll-cue values into base/mobile rules and colocated the portrait crop with responsive portrait behavior | 40-page render and 20/20 visual comparisons |
| Homepage section headings | Replaced five size, tracking and text-transform correction blocks with one final shared heading rule | 40-page render and 20/20 visual comparisons |
| Homepage eyebrow labels | Removed the fully overridden homepage label blocks while retaining separate Expertise-page eyebrow styling | 40-page render and 20/20 visual comparisons |
| Unified News component | Removed unreachable `.home-news-*`, `.news-archive-*`, `.news-year-*` and `.news-row` layers; colocated disclosure styling with the live `.news-item` component | 40-page render and 169/169 aggregate checks |
| Obsolete carousels | Removed 267 lines of unreachable project/publication carousel SCSS and the dormant carousel initializer after confirming no source or generated page emits carousel markup | 40-page render and 169/169 aggregate checks |
| Legacy project cards | Removed 42 lines for the superseded `.project-card` grid after confirming current pages use `.home-project-card` and `.project-summary-card` exclusively | 40-page render and 169/169 aggregate checks |
| Legacy theme accordions | Removed 72 lines for unreachable `.theme-accordions`, `.theme-panel`, `.theme-links` and `.method-list` components, including their responsive overrides | 40-page render and 169/169 aggregate checks |
| Legacy publication systems | Removed the superseded selected-paper, publication-row, venue-label, modal and More-menu layers plus their unused generator helper; retained the live archive spacing, rows, theme rails and inline disclosures | 40-page render and 169/169 aggregate checks |
| Legacy profile and footers | Removed the unused profile card, contact-map footer, big footer and fixed small footer families; retained the current `.site-footer` implementation | 40-page render and 169/169 aggregate checks |
| Legacy About and Research layouts | Removed pre-redesign About columns, research themes and hidden homepage metadata; retained the current career narrative and `*-refined` research components | 40-page render and 169/169 aggregate checks |
| Legacy portfolio and project details | Removed the unused portfolio-card grid and dormant project output/code/closing components; retained YAML-driven cards and active F1/GCG project structures | 40-page render and 169/169 aggregate checks |
| Retired utility components | Removed the unused publication toolbar/award panel, old 404 wrapper and superseded teaching metadata aliases | 40-page render and 169/169 aggregate checks |
| Publication label rail | Collapsed five chronological left/right rail experiments into one authoritative desktop/mobile layout | 40-page render and 20/20 visual comparisons |
| Teaching open list | Replaced the timeline and compact-card cascade with one authoritative open-list component while retaining live metadata, actions and disclosures | 40-page render and 20/20 visual comparisons |
| Homepage identity and section rhythm | Consolidated repeated hero role, profile-divider and Featured Projects spacing corrections into their final declarations | 40-page render and 20/20 visual comparisons |
| Shared theme tokens | Moved the light/dark global, Expertise, secondary-blue and homepage accent variables into the ordered token partial | 40-page render and 79/79 Chromium checks |

The current entrypoint and five partials contain 4,753 SCSS lines, down from
7,583 lines at baseline (2,851 lines, or 37.6%). The remaining
selectors that are absent from static source are generated by Quarto,
Bootstrap, Algolia search or runtime navigation and are intentionally retained.

## Phase 4 output hardening

Phase 4 extends the cleanup beyond the main SCSS cascade:

- Publication generation now emits one responsive theme rail per entry instead
  of separate desktop and permanently hidden mobile copies.
- `styles/project-pages.css` is 869 lines, down from 920 after removing seven
  component families absent from source generators, Lua filters, runtime code
  and rendered pages.
- A static regression check prevents the eight retired markup and stylesheet
  class names from returning unnoticed.
- Archive headings, years, action rows and compact inline icons now use shared
  semantic classes instead of page-local inline styles.
- The shared category navigation is named `.section-jump` rather than after
  Publications alone, because it also serves Teaching.
- A static regression check prevents authored QMD and HTML from introducing
  inline style attributes.

The final selector audit leaves only framework/runtime classes and the
Lua-generated `project-at-a-glance-N` variant unmatched in static source.

## Safety test matrix

Run `npm run test:quick` while iterating on focused changes. Its 18 Chromium
checks cover critical pages, interactions, links and scroll restoration.

Run `npm test` before committing after a complete `quarto render`. This default midrange suite
contains 79 Chromium checks: smoke coverage, interactions, links, navigation
regressions and visual comparisons.

Run `npm run test:full` before deployment or after broad structural or
browser-specific changes.
The complete suite contains 177 checks:

- 40 Chromium smoke tests covering every generated page, document structure,
  images, browser errors and failed same-origin resources
- 80 WCAG A/AA checks covering every page in light and dark mode
- 7 Chromium interaction checks for navigation, themes, search, publication
  panels and news controls
- 3 static checks covering local targets, URL fragments, retired components and inline styles
- 9 Chromium critical-path checks, including back-navigation scroll restoration
- 18 matching critical-path checks in Firefox and WebKit
- 30 visual comparisons against the original desktop/iPad/mobile, light/dark
  baselines

The validated checkpoint passes all 177 checks without updating the visual
baselines. External-site availability, deployed-server configuration and
manual assistive-technology behavior remain outside this deterministic local
suite.

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

These fingerprints identify the historical pre-refactor baseline. The saved
screenshots remain the authoritative visual reference.

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
| `ipad` | 820 | 1180 |
| `mobile` | 390 | 844 |

Store captures under `tests/visual/baselines/` using:

`<page>--<theme>--<viewport>.png`

Animations and transitions must be disabled, reduced motion must be enabled,
and capture must wait for `document.fonts.ready`.
