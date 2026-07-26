# AGENTS.md

## Purpose

Instructions for coding agents working on `sfanzon/Quarto-Website-git`.

For non-trivial work, also read:

- `ARCHITECTURE.md` — source ownership and implementation architecture
- `DESIGN.md` — visual identity and editorial rules
- `README.md` — build, test and repository orientation

## Core rules

1. **Agents may modify any source needed to complete the task.**
2. **Preserve the existing visual identity.** Do not redesign unrelated parts of the site.
3. **Use canonical sources.** Do not fix source problems by editing generated output.
4. **Prefer coherent architectural fixes over additional patches or overrides.**
5. **Do not overwrite unrelated user changes.**

## Planning

For trivial changes, act directly.

For medium or large changes:

1. inspect the relevant implementation;
2. identify the source of truth and shared dependencies;
3. state a concise plan;
4. implement;
5. render/test;
6. inspect the final diff.

Examples requiring a plan:

- navigation changes;
- shared component changes;
- project-page restructuring;
- CSS architecture refactors;
- data-schema changes;
- build/deployment changes;
- broad responsive work.

## Important sources

| Area | Canonical source |
|---|---|
| Site config/navigation | `_quarto.yml` |
| Projects | `data/projects.yml` |
| Publications | `data/publications.bib` |
| Teaching | `data/teaching_lecturer.bib`, `data/teaching_tutor.bib` |
| News | `news/*.md` |
| Project renderer | `filters/project-components.lua` |
| Global styles | `styles/main.scss`, `styles/main/` |
| Project styles | `styles/project-pages.css`, `styles/project-navigation.css` |
| Content generation | `scripts/build-content.py` |
| Architecture | `ARCHITECTURE.md` |

Generated files under `includes/`, `data/projects.generated.json`, and `docs/` are not canonical sources.

## Scope discipline

Fix closely related issues when necessary for the requested result.

Do not turn a local task into an opportunistic redesign or broad cleanup.

## Design

Read `DESIGN.md` before visual work.

Hard constraints:

- warm editorial visual identity;
- restrained rust/warm accent system;
- compact typography;
- light and dark modes;
- mixed professional audience;
- applied mathematics as the foundation, applications as the evidence;
- no generic data-science, SaaS, AI-startup, or academic-template redesign.

For project pages, preserve the intended hierarchy:

1. category;
2. title;
3. subtitle;
4. author/date;
5. slim Resources row;
6. lightweight At-a-glance summary;
7. Explore Project navigation where applicable;
8. article.

Standard project prose width: **760 px**. Wider figures, code, tables and diagrams are allowed when useful.

## CSS / Quarto

Use the existing token and component system.

Prefer:

- shared variables;
- component-scoped rules;
- semantic HTML;
- structural fixes;
- Quarto-native features when suitable.

Avoid:

- duplicate component implementations;
- chains of `!important`;
- arbitrary pixel nudges without understanding the layout;
- unnecessary JavaScript;
- rebuilding working Quarto functionality.

## Build

Preview:

```bash
quarto preview
```

Render:

```bash
quarto render
```

The pre-render hook runs `scripts/build-content.py`.

## Tests

Small iteration (interactions + static checks, 11 tests):

```bash
npm run test:quick
```

Normal pre-commit validation (smoke + interactions + links + critical regressions, 60 tests):

```bash
npm test
```

Visual regression suite (30 Chromium screenshot comparisons):

```bash
npm run test:visual
```

Broad structural or browser-sensitive changes (full matrix, 188 tests):

```bash
npm run test:full
```

Do not update visual baselines merely to make tests pass. Use `npm run visual:baseline` only for an intentional, inspected visual change.

## Visual validation

For visual/layout work, inspect:

- Desktop: **1440 × 1000**
- iPad: **820 × 1180**
- iPhone: **390 × 844**

Inspect both light and dark mode when relevant.

Check at least:

- overflow;
- navbar/dropdowns;
- project navigation;
- hero;
- Resources;
- At-a-glance;
- article width;
- figures/code/tables;
- related-project section;
- footer.

For substantial responsive work, also check intermediate widths.

If browser tooling is unavailable, complete build/test validation and explicitly state that visual inspection was not performed.

## Accessibility

Preserve:

- keyboard focus;
- contrast;
- semantic headings;
- usable touch targets;
- reduced-motion support;
- meaningful alt text;
- accessible menus/drawers.

Do not solve responsive problems by hiding important content.

## Git

Before significant work:

```bash
git status
git diff
```

After changes:

```bash
git diff --stat
git diff
```

Use a branch or worktree for broad autonomous/refactor work.

Do not rewrite history or discard uncommitted work unless explicitly instructed.

## Definition of done

A task is complete when:

- the requested behaviour works;
- canonical sources remain canonical;
- visual identity is preserved;
- Quarto renders;
- relevant tests pass;
- responsive/theme behaviour is preserved where relevant;
- generated output is reproducible;
- the diff contains only justified changes.

For visual tasks, the rendered result is the source of truth.

## Priority

When instructions conflict:

1. explicit user/task instruction;
2. `AGENTS.md`;
3. `DESIGN.md`;
4. `ARCHITECTURE.md`;
5. established implementation.
