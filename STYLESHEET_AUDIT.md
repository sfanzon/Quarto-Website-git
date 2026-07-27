# Stylesheet Architecture Audit

> **Historical pre-refactor audit.** This document records the stylesheet state and recommendations as assessed on 27 July 2026 before the subsequent SCSS consolidation and cleanup work. It is retained as a historical reference, not as the current architecture guide. For current ownership and implementation, use `SOURCE_MAP.md`, `ARCHITECTURE.md`, and `SCSS_REFACTOR.md`.


**Date:** 27 July 2026
**Scope:** All stylesheets under `styles/`
**Total `!important` declarations:** ~602 (across all files)

---

## 1. File Inventory & Responsibilities

| File | Lines | Role | `!important` count |
|---|---|---|---|
| `styles/main/_01-foundation.scss` | 1078 | Base layer: layout grid, navbar, footer, homepage hero, section headings, publication entries, color-scheme toggle, search, responsive breakpoints | Moderate |
| `styles/main/_02-editorial.scss` | 867 | Editorial layer: chrome width, navbar/footer chrome, section headings, publication layout, homepage sections, news page, mobile overrides | Moderate |
| `styles/main/_03-overrides.scss` | 1771 | Override layer: navbar dropdowns, homepage hero, publication entries, expertise page, search popup, news component, homepage editorial headings, publication layout 2026 | **Very high** |
| `styles/main/_04-current-pages.scss` | ~920 | Current-page-specific: archive headings, about page, research page, news preview, teaching page, supervision page | Moderate |
| `styles/project-pages.css` | ~860 | Project detail pages: hero, at-a-glance, resource map, related projects, end footer, responsive | Moderate |
| `styles/project-navigation.css` | ~360 | Project chapter rail: sticky sidebar, chapter navigation, secondary nav, responsive | Low |

---

## 2. Architecture Assessment

### 2.1 Strengths

- **Clear layering:** Foundation → Editorial → Overrides → Current-pages is a sensible cascade.
- **CSS custom properties:** Extensive use of `--global-*`, `--expertise-*`, `--project-*` tokens.
- **Responsive design:** Consistent mobile-first breakpoints (`991.98px`, `767.98px`, `680px`).
- **Dark/light mode:** Proper `quarto-light`/`quarto-dark` body class scoping.
- **Accessibility:** Focus-visible styles, reduced-motion support, semantic headings.

### 2.2 Critical Issues

#### 2.2.1 `!important` Proliferation (~602 declarations)

This is the single biggest architectural debt. `!important` is used as the primary mechanism for overriding Quarto's default styles rather than using higher-specificity selectors or restructuring the source.

**Worst offenders in `_03-overrides.scss`:**
- `.navbar .dropdown-menu` — 6+ `!important` declarations
- `.home-hero` — 15+ `!important` declarations
- `.home-publication-row`, `.publication-archive-row` — 10+ `!important` declarations
- `.publication-theme-rail` — 15+ `!important` declarations
- `.aa-DetachedContainer *` — 60+ `!important` declarations (search popup)
- `.home-editorial-heading .section-title` — 6+ `!important` declarations

**Impact:**
- Makes debugging extremely difficult
- Any new style must also use `!important` to override
- Prevents clean component-level overrides
- Increases maintenance burden significantly

#### 2.2.2 Duplicate Selectors Across Files

The same selectors are styled in multiple files, creating a fragile cascade:

| Selector | `_01-foundation.scss` | `_02-editorial.scss` | `_03-overrides.scss` |
|---|---|---|---|
| `#navbar` | Lines 383-395 | Lines 155-165, 456-463 | — |
| `.navbar-brand` | Lines 404-420 | Lines 168-175, 467-469, 760-770 | Lines 13-20 |
| `.navbar .nav-link` | Lines 426-447 | Lines 176-198, 470, 772-788 | Lines 23-34 |
| `.navbar .dropdown-menu` | — | Lines 202-211, 233-234 | Lines 4-10, 32-43 |
| `.section-heading` | Lines 1037-1055 | Lines 133-148, 720-725 | Lines 1333-1403 |
| `.home-publication-row` | — | Lines 291-326 | Lines 1437-1546 |
| `.site-footer` | Lines 69-70 | Lines 73-102, 707, 864 | — |

#### 2.2.3 Specificity Escalation

The cascade has become a specificity arms race:
1. `_01-foundation.scss` defines base styles (low specificity)
2. `_02-editorial.scss` overrides with slightly higher specificity
3. `_03-overrides.scss` overrides with `!important`
4. `_04-current-pages.scss` sometimes adds yet another layer

**Example — `.section-title`:**
- `_01-foundation.scss` line 1040: `.home-page .section-heading .section-title` (0,3,0)
- `_03-overrides.scss` line 1333: `body.home-page .home-editorial-heading .section-title` (0,4,0) + `!important`
- `_03-overrides.scss` line 1395: `body.home-page .home-editorial-heading .section-title` (0,4,0) + `!important` (different values!)

#### 2.2.4 Mixed Units & Inconsistent Spacing

- Mix of `rem`, `clamp()`, `vw`, `svh`, `dvh` without a clear system
- Some values use `!important` on spacing properties (margin, padding) where cascade should suffice
- Inconsistent use of `clamp()` ranges (some use 3-value, some 2-value)

#### 2.2.5 Hardcoded Values vs. Custom Properties

Several values that should be tokens are hardcoded:
- `#f6f3ee` (search hover background) — should be a variable
- `58px` (navbar height override) — should reference `--project-navbar-height`
- Various font sizes in `clamp()` that don't use the type scale

---

## 3. File-by-File Analysis

### 3.1 `_01-foundation.scss` (1078 lines)

**Role:** True foundation — layout grid, page structure, base component styles.

**Issues:**
- Lines 383-510: Navbar styles are comprehensive but some selectors are overly broad (e.g., `.navbar a`)
- Lines 717-870: Color-scheme toggle has significant duplication between light/dark variants
- Lines 1000-1078: Homepage hero and section styles are clean but overlap with `_03-overrides.scss`

**Recommendation:** Keep as-is. This is the healthiest file.

### 3.2 `_02-editorial.scss` (867 lines)

**Role:** Editorial chrome — site width, navbar/footer chrome, section headings, publication layout.

**Issues:**
- Lines 5-6: `--site-chrome-width: 1240px` is a good token but only used here
- Lines 12-66: Navbar chrome styles are clean but overlap significantly with `_01-foundation.scss`
- Lines 73-102: Footer styles are well-structured with grid layout
- Lines 155-251: Second navbar block duplicates `_01-foundation.scss` lines 383-510
- Lines 456-470: Third navbar block — clearly a specificity escalation
- Lines 760-870: Fourth navbar block with responsive — this is the override layer

**Recommendation:** Consolidate navbar styles into a single location. Remove duplicates.

### 3.3 `_03-overrides.scss` (1771 lines)

**Role:** The "catch-all" override file. Largest and most problematic.

**Issues:**
- Lines 1-50: Navbar dropdown overrides — clean but should be in `_02-editorial.scss`
- Lines 52-100: Publication entry overrides — reasonable
- Lines 112-236: Homepage hero overrides — heavy `!important` usage
- Lines 239-390: 2026 homepage publication parity — moderate
- Lines 400-583: Expertise page — well-structured, moderate `!important`
- Lines 648-830: About page — clean
- Lines 830-935: Homepage lead/summary — moderate
- Lines 1000-1090: Restrained headings + expertise compact — clean
- Lines 1107-1318: Search popup — **60+ `!important` declarations** for Algolia/Quarto search
- Lines 1320-1403: Homepage editorial headings — duplicates `_01-foundation.scss` section-heading
- Lines 1405-1546: 2026 publication layout — **heavy `!important`**, duplicates `_02-editorial.scss`
- Lines 1548-1771: News component — **clean, well-structured, minimal `!important`**

**Recommendation:** This file needs the most attention. The news component (lines 1548-1771) is a model for how the rest should look.

### 3.4 `_04-current-pages.scss` (~920 lines)

**Role:** Page-specific styles for about, research, teaching, supervision, news preview.

**Issues:**
- Lines 1-50: Archive section headings — clean
- Lines 205-288: About page — well-structured
- Lines 325-436: Research page — moderate
- Lines 577-920: Teaching, supervision, news preview — moderate

**Recommendation:** This is the second-healthiest file. Keep as-is.

### 3.5 `project-pages.css` (~860 lines)

**Role:** Project detail page components (hero, at-a-glance, resource map, related).

**Issues:**
- Lines 135-157: Responsive overrides use `!important` for width/margin
- Lines 486-487: `.project-page-end` width override
- Lines 828-837: Duplicate width/max-width declarations

**Recommendation:** Moderate. Could be cleaned up but not urgent.

### 3.6 `project-navigation.css` (~360 lines)

**Role:** Project chapter rail (sticky sidebar navigation).

**Issues:**
- Lines 135-157: Responsive overrides use `!important` for layout
- Lines 177-238: Mobile rail styles — clean

**Recommendation:** Healthiest file. Minimal issues.

---

## 4. Specific Problem Patterns

### 4.1 The `.navbar` Quadruple Definition

The navbar is styled in **four separate locations**:

1. `_01-foundation.scss` lines 383-510 — Base navbar
2. `_02-editorial.scss` lines 12-66 — Chrome width
3. `_02-editorial.scss` lines 155-251 — Editorial navbar
4. `_02-editorial.scss` lines 456-870 — Responsive navbar
5. `_03-overrides.scss` lines 1-50 — Dropdown overrides

**Fix:** Consolidate into `_02-editorial.scss` only, with `_01-foundation.scss` providing only layout grid tokens.

### 4.2 The `.section-heading` Duplication

1. `_01-foundation.scss` lines 1037-1055 — Base section heading
2. `_02-editorial.scss` lines 133-148 — Editorial section heading
3. `_03-overrides.scss` lines 1320-1403 — Homepage editorial heading (with `!important`)

**Fix:** Keep base in `_01-foundation.scss`, homepage variant in `_02-editorial.scss`, remove from `_03-overrides.scss`.

### 4.3 The Publication Layout Triple Cascade

1. `_01-foundation.scss` lines 1056-1069 — Base publication styles
2. `_02-editorial.scss` lines 291-326 — Publication section
3. `_03-overrides.scss` lines 52-100, 239-390, 1417-1546 — Publication overrides

**Fix:** Consolidate into `_02-editorial.scss` with a single source of truth.

### 4.4 The Search Popup (`aa-*`) Isolation

The search popup styles (lines 1107-1318 in `_03-overrides.scss`) are well-isolated but use 60+ `!important` declarations. This is because Quarto's Algolia search injects inline styles.

**Fix:** Move to a dedicated partial (`styles/main/_05-search.scss`) and accept `!important` as necessary for third-party widget overrides.

---

## 5. Recommended Refactoring Strategy

### Phase 1 (Low effort, high impact)
1. Move search popup styles to `styles/main/_05-search.scss`
2. Move news component from `_03-overrides.scss` to `_02-editorial.scss`
3. Remove duplicate `.section-heading` from `_03-overrides.scss`

### Phase 2 (Medium effort)
4. Consolidate navbar styles: keep base in `_01-foundation.scss`, move all chrome/responsive to `_02-editorial.scss`, remove from `_03-overrides.scss`
5. Consolidate publication layout: keep base in `_01-foundation.scss`, move all layout to `_02-editorial.scss`, remove from `_03-overrides.scss`

### Phase 3 (High effort)
6. Audit and remove `!important` where specificity can be increased instead
7. Create a proper token system for `clamp()` ranges
8. Replace hardcoded colors with CSS custom properties

---

## 6. Quick Wins (No Refactor Needed)

These are isolated issues that can be fixed immediately:

| Location | Issue | Fix |
|---|---|---|
| `_03-overrides.scss:1299` | Hardcoded `#f6f3ee` | Use `var(--global-search-hover-bg)` |
| `_03-overrides.scss:1315` | Hardcoded `#f6f3ee` | Same |
| `_03-overrides.scss:220` | Hardcoded `58px` | Use `var(--project-navbar-height)` |
| `_03-overrides.scss:229` | Hardcoded `58px` | Same |
| `_03-overrides.scss:236` | Hardcoded `58px` | Same |
| `project-navigation.css:137-157` | Duplicate width/margin `!important` | Consolidate into single rule |

---

## 7. Summary

| Metric | Value |
|---|---|
| Total stylesheets | 6 |
| Total lines | ~5,856 |
| `!important` declarations | ~602 |
| Files needing attention (high) | `_03-overrides.scss` |
| Files needing attention (medium) | `_02-editorial.scss` |
| Files needing attention (low) | `project-pages.css` |
| Healthy files | `_01-foundation.scss`, `_04-current-pages.scss`, `project-navigation.css` |

The core problem is that `_03-overrides.scss` has become a dumping ground for "make it work" styles rather than a true override layer. The news component (lines 1548-1771) demonstrates that the codebase *can* produce clean, maintainable CSS — the rest of the file should be refactored to match that standard.
