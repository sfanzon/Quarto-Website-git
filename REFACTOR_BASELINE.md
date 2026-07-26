# Refactor Inventory and Baseline

Recorded 2026-07-26 before the next cleanup and SCSS component pass.

## Validation checkpoint

- Current source checkpoint: `45f0b25` (`Add tiered local test policy`)
- Quarto render: 40 pages rendered successfully
- Midrange suite: `npm test`, 78/78 Chromium checks passed in 56.4 seconds
- Visual baseline: 20 screenshots covering five representative pages, light/dark themes, and desktop/mobile viewports
- Visual baselines were not updated
- The working tree already contains the pending cleanup changes shown by `git status`; this report does not replace or conceal them

## Repository footprint

| Area | Current size | Notes |
| --- | ---: | --- |
| Whole checkout | 450 MB | Includes generated output and local dependencies |
| `.git` | 194 MB | Packed history; no loose objects after `git gc` |
| `docs/` | 112 MB | Generated GitHub Pages output |
| `assets/` | 106 MB | Referenced images, PDFs, fonts and downloads |
| `tests/` | 14 MB | Test code and 20 visual baselines |
| `node_modules/` | 21 MB | Local development dependency, not deployment content |
| `.quarto/` | 768 KB | Regenerable local cache |

The source snapshot contains 490 files: 20 `.qmd` pages, 29 Markdown files,
92 PDFs, 39 PNGs, 19 JavaScript files, 10 CSS files, five SCSS files, and the
structured YAML/BibTeX/JSON content sources.

## Stylesheet baseline

| File or group | Lines |
| --- | ---: |
| `styles/main.scss` | 24 |
| Main SCSS partials | 4,745 |
| Main SCSS total | 4,769 |
| `styles/project-pages.css` | 869 |
| `styles/project-navigation.css` | 360 |
| All project and main styles | 5,998 |

The main SCSS is already 2,814 lines, or 37.1%, smaller than the historical
7,583-line baseline. The next reduction should preserve the current import
order until each component has a visual comparison.

Current cascade signals:

- 600 `!important` declarations across the main and project styles
- 299 of them are in `styles/main/_03-overrides.scss`
- 144 are in `styles/main/_01-foundation.scss`
- `styles/main/_04-current-pages.scss` is the clearest current-component extraction target at 896 lines
- `styles/project-pages.css` is a separate high-value target at 869 lines, but must remain isolated from the main-site cascade
- Theme values are already partly represented as CSS custom properties, but naming and ownership are distributed across partials

## Markup and reuse baseline

The site already centralizes substantial generated content in `includes/` and
builds it from `data/` through `scripts/build-content.py`. The most repeated
live markup families are:

- Publication rows and actions: `publication-entry`, `paper-actions`, `paper-action`
- Teaching rows and actions: `teaching-course`, `teaching-actions`, `teaching-action`
- News disclosures: `news-item`, `news-title`, `news-body`, `news-disclosure`
- Homepage/project cards: `home-project-card`, `project-summary-card`, and their child regions
- Shared page framing: `page-hero`, `compact-page-hero`, `section-heading`, and `eyebrow`

One concrete hard-coding hotspot is `presentations.qmd`, which currently has 45
inline `style` attributes. These should be converted to semantic classes only
after the existing rendered appearance is captured and reviewed.

## Prioritized next targets

1. Extract shared tokens and component primitives from the current live rules,
   beginning with buttons/actions, page headings, cards, and metadata rows.
2. Replace the inline styles in `presentations.qmd` with named classes and
   responsive rules.
3. Consolidate duplicated theme variables and repeated layout declarations,
   starting in `_03-overrides.scss` and `_04-current-pages.scss`.
4. Audit `!important` declarations individually; remove only those whose
   computed-style behavior remains unchanged.
5. Review generated includes and `build-content.py` for repeated HTML patterns
   that can be expressed through shared render helpers or structured data.
6. Keep referenced PDFs and public paths unchanged unless an explicit redirect
   or compatibility plan is added.

## Safety rules for the next phase

- Run `quarto render` after every source, style, script, or configuration batch.
- Run `npm run test:quick` during focused edits.
- Run `npm test` before committing a component batch.
- Run `npm run test:full` after broad structural changes or before deployment.
- Do not update the 20 visual baselines unless the visual change is intentional
  and reviewed.
