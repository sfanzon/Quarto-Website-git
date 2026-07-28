# Testing Architecture

## Test categories

| Command | Scope | Environment |
|---|---|---|
| `npm run test:quick` | 11 Chromium checks: interactions, links, static guards | Local or CI |
| `npm test` | 60 Chromium checks: all-page smoke, interactions, links, navigation | Local or CI |
| `npm run cross-browser:test` | 18 checks across Firefox + WebKit | Local or CI |
| `npm run test:visual` | 30 full-page Chromium screenshot comparisons | **CI only** (see below) |
| `npm run test:full` | 188 checks: all of the above + accessibility | **CI only** (includes visual) |

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
- **Playwright**: 1.62.0 (exact, pinned in `package.json`)
- **Chromium**: version bundled with Playwright 1.62.0
- **Fonts**: `fonts-roboto` installed explicitly for deterministic rendering

The CI environment is the **single source of truth** for visual baselines.

### When visual tests run

- **Pull requests** that touch styles, content, data, filters, or build configuration
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

### Current baseline state

The existing baselines were captured on macOS with San Francisco font rendering. They are **not compatible** with the Linux CI environment and will fail until regenerated.

To make visual tests pass in CI:

1. Trigger the "Update Visual Baselines" workflow
2. Review and commit the new Linux baselines
3. Future visual comparisons will use these CI baselines

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
| `tests/safety/generated-output-guard.mjs` | Static guard for retired components and inline styles |
| `.github/workflows/visual-tests.yml` | CI: visual regression tests |
| `.github/workflows/update-visual-baselines.yml` | CI: manual baseline regeneration |
