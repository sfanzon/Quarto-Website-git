# Testing Architecture

## Test categories

| Command | Scope | Environment |
|---|---|---|
| `npm run test:quick` | 16 Chromium checks plus 16 generator tests and 6 generated-output guard tests | Local or CI |
| `npm test` | 47 Chromium checks plus 16 generator tests: all-page smoke, interactions, links, navigation | Local or CI |
| `npm run test:accessibility` | 44 Chromium WCAG A/AA checks | Local or CI |
| `npm run cross-browser:test` | 18 checks across Firefox + WebKit | Local or CI |
| `npm run test:visual` | 30 full-page Chromium screenshot comparisons | **CI only** (see below) |
| Pull-request visual workflow | 66 base-versus-head screenshot comparisons | **CI only** |
| `npm run test:full` | 121 Chromium checks: smoke, interactions, links, layout, accessibility and visual (it does not run generator, guard, Firefox or WebKit tests) | **CI only** (includes visual) |

## Visual regression tests

### Why CI-only

The site's font stack is:

```
-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
"Helvetica Neue", Arial, sans-serif
```

This resolves to a different font on every platform:

| Platform | Resolved font |
|---|---|
| macOS | San Francisco (Apple proprietary) |
| Windows | Segoe UI |
| Linux (CI) | Roboto |

Pixel-level screenshot comparisons are only reproducible when font rendering is deterministic. Running visual tests locally on macOS will produce different pixels than the CI environment, even when the site is unchanged.

### CI environment

Visual tests run in GitHub Actions on `ubuntu-22.04` with:

- **Node**: 22
- **Python**: 3.12 with PyYAML 6.0.3 from `requirements.txt`
- **Playwright**: 1.62.0 (exact, pinned in `package.json`)
- **Chromium**: version bundled with Playwright 1.62.0
- **Quarto**: 1.9.38 (site is rendered from source in CI before screenshots)
- **Fonts**: `fonts-roboto` installed explicitly for deterministic rendering

The CI environment is the **single source of truth** for pixel comparisons.

### Build workflow

Pull requests render both revisions and compare them directly:

```
base source ──→ quarto render ──→ temporary base screenshots
                                             ↓ compare
head source ──→ quarto render ──→ head screenshots
```

The base and head renders use the same runner, Chromium build, fonts, Quarto
version and test harness. This removes uncertainty caused by stale permanent
screenshots: a failure identifies a visual difference introduced by the pull
request itself.

If there is no difference, the check passes automatically. If there is a
difference, CI uploads the `base-head-visual-diffs` artifact and fails the
check. After reviewing that artifact, apply the `visual-change-approved` pull
request label only when every difference is intentional. Label changes rerun
the workflow; an approved visual difference then passes without changing any
screenshots.

Manual visual runs and the baseline-update workflow retain the reviewed,
committed-baseline model. They follow the usual `source → quarto render → docs/
→ screenshots` recipe. Pull-request comparison screenshots are temporary and
never overwrite the committed baselines.

### When visual tests run

- **Pull requests** that touch styles, content, data, filters, or build
  configuration compare base with head across 11 representative pages, three
  viewports and both themes (66 comparisons)
- **Manual trigger** via `workflow_dispatch` on the Actions tab

They do NOT run on every push. Visual tests are expensive and intentional.

### Updating baselines

Baselines must never update automatically. When an intentional visual change occurs:

1. Review the change locally
2. Trigger the **"Update Visual Baselines"** workflow from the Actions tab
3. Provide a reason for the change
4. Download the generated artifact
5. Review every screenshot carefully
6. Commit the new baselines to `tests/visual/baselines/`

This permanent-baseline update is separate from approving a pull-request diff.
The `visual-change-approved` label records review of that PR; it never updates
or replaces committed screenshots.

### Current baseline state

The 30 committed baselines cover five representative pages and remain the
reviewed reference set for manual runs. Pull-request checks additionally cover
About, Expertise, Research, News, the Notes archive and a representative note
article without requiring permanent screenshots for those pages.

To regenerate baselines after an intentional visual change, trigger the "Update Visual Baselines" workflow, review the artifacts, and commit the result.

### Local development workflow

For normal source changes:

```bash
quarto render           # render the site
npm run test:quick      # fast validation
npm test                # pre-commit validation
```

For visual changes, after rendering:

```bash
npm run test:visual     # run locally (will differ from CI baselines)
# Inspect failures visually — they indicate a real rendering change
# Push and let CI confirm against the controlled environment
```

Local visual test results are informative but not authoritative. The CI run is the gate.

### Hybrid visual QA pages

```bash
cd astro
npm run build:qa
npm run preview
```

Inspect `/dev/kitchen-sink/` for current production patterns and
`/dev/viewports/` for real-route frames at 375, 430, 820, 1180 and 1440 CSS
pixels. Use the navbar breakpoint mode to compare 991, 992 and 993 pixels.
Normal `npm run build:site` removes these routes from `dist/`; neither build
adds them to the sitemap or Pagefind.

For an automatically rebuilt local hybrid site, use:

```bash
cd astro
npm run dev:hybrid
```

It serves the QA merge from `astro/dist/`, including `/dev/`, and watches the
Astro sources and canonical Quarto project inputs. Reload after its completed
rebuild message; use `npm run dev` when only Astro routes are needed.

## Test infrastructure files

| File | Purpose |
|---|---|
| `tests/visual/capture.spec.js` | Screenshot capture and comparison logic |
| `tests/visual/baseline-manifest.json` | Pages, viewports, themes, and baseline metadata |
| `tests/visual/baselines/*.png` | Reference screenshots (CI-generated) |
| `tests/safety/smoke.spec.js` | All-page runtime health checks |
| `tests/safety/interactions.spec.js` | Navigation, theme, search, and UI interaction checks |
| `tests/safety/links.spec.js` | Internal link and fragment validity |
| `tests/safety/cross-browser.spec.js` | Critical path checks in Firefox + WebKit |
| `tests/safety/accessibility.spec.js` | WCAG A/AA checks |
| `tests/safety/generated-output-guard.mjs` | Prevents generated-only changes without a canonical source change |
| `.github/workflows/visual-tests.yml` | CI: visual regression tests |
| `.github/workflows/functional-tests.yml` | CI: fresh render plus functional, accessibility, and cross-browser tests |
| `.github/workflows/update-visual-baselines.yml` | CI: manual baseline regeneration |

## Render reproducibility

The Python content generator is byte-stable: two consecutive runs from the
same checkout produce identical generated includes and
`data/projects.generated.json`.

Quarto rendering is byte-stable when repeated in the same checkout. Two fresh
checkouts of the same revision differ in only two generated outputs:

| Output | Source of difference | Owner |
|---|---|---|
| `docs/sitemap.xml` | Quarto writes render-time `lastmod` values for every page | Quarto website sitemap |
| `docs/notes.html` | Quarto's native document listing embeds source filesystem modification times in hidden sort metadata | `notes.qmd` native listing |

These differences do not change reader-visible content, routes, assets or
behaviour. They are known Quarto-generated deployment churn, not source drift.
Do not hand-edit either output. Any future change to remove this churn must be
a separately reviewed architectural decision, because it would replace or
post-process Quarto-native sitemap or listing behaviour.
