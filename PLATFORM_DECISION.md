# Platform assessment: retain Quarto, monitor the site shell

## Decision

Keep Quarto for the whole website through the next normal maintenance cycle.
Do not start an Astro migration or a hybrid build now.

An isolated, reversible Astro shell and About-page proof of concept under
`astro/` is approved for comparison. This experiment leaves the Quarto site
canonical and is not a migration decision.

This is not a claim that Quarto is the ideal general-purpose website shell.
The cleanup shows meaningful shell friction. It is a judgment that a migration
would currently add more parallel architecture, visual-matching work and
deployment risk than it would remove.

Lecture notes and technical posts remain Quarto content in every future
scenario. Its Markdown, mathematics, citations, cross-references, executable
documents, code presentation and Mermaid support are a strong fit for them.

## Evidence after cleanup

| Area | Evidence | Assessment |
|---|---|---|
| Editing | Publications, presentations, supervision, teaching, projects, news and notes now have documented canonical sources and validation. | Good. Routine record edits have one obvious source. |
| Technical documents | The site uses Quarto-native mathematics, citations, code/document structure, listings, search, themes and Mermaid assets. | Strong reason to retain Quarto. |
| Build and deployment | A full render covers 22 pages; the content generator is byte-stable; tracked `docs/` remains the intentional GitHub Pages deployment output. | Acceptable and reproducible within a checkout. |
| Validation | Generator, Chromium functional/accessibility, Firefox and WebKit checks all pass after a clean render. | Good operational confidence. |
| Shell customization | The site has 53 SCSS files (5,978 lines), 643 lines of hand-written runtime JavaScript, a 245-line Lua project filter and 1,311 lines of Python generation code. | Substantial, but much of it expresses real site features rather than framework workaround alone. |
| Quarto/Bootstrap boundary | 586 `!important` declarations are concentrated in canonical shell, navbar, archive and project-layout owners. Custom code also handles project navigation, scroll restoration and Mermaid SVG IDs. | Real friction: the site is working around Quarto/Bootstrap markup and lifecycle in several places. |
| Render stability | Repeated renders in one checkout are byte-stable. Fresh checkouts change only Quarto sitemap timestamps and hidden Notes-listing modification-time metadata. | Low-severity churn; reader-visible output, routes and behaviour are stable. |

## What belongs to Quarto, and what belongs to the website

The custom code should not be treated as a single migration opportunity.

- The data generator, publication/archive renderers, project metadata and
  editorial components exist because this is a structured professional site;
  an Astro site would still need equivalent data models and components.
- The SCSS volume largely implements the deliberate visual identity,
  responsive layouts, project experience and archive presentation. A new
  framework would require a careful port, not make that design disappear.
- The concentrated `!important` rules, Quarto navbar geometry handling,
  scroll-restoration timing and Mermaid ID normalization are genuine framework
  boundary costs. They are the relevant evidence to monitor.

In short: the content architecture is not fighting Quarto. The highly polished
site shell sometimes is.

## Why not migrate now

An Astro main site with Quarto technical documents is feasible and not crazy.
It would need an explicit contract for shared navigation, theme, typography,
assets, search, URLs, analytics and deployment. Matching the current look
seamlessly would mean porting the visual system and interactive components,
then maintaining two build paths. That is a product project, not cleanup.

The current site is validated, editable and deployable. No cleanup finding
shows an active Quarto defect that blocks ordinary editing or forces a
migration. `dadangnh/as-folio` demonstrates that Astro can support an
al-folio-shaped site, but it does not show that it can reproduce this custom
site with less maintenance.

## Revisit threshold

Approve a separately scoped platform experiment only if one or more of these
conditions becomes true:

1. A Quarto or Bootstrap upgrade repeatedly breaks the shell, requiring broad
   CSS/JavaScript remediation rather than a local compatibility fix.
2. A routine feature requires another cross-cutting workaround in the global
   shell, rendering pipeline and runtime JavaScript merely to fit Quarto's
   output.
3. The main site needs application-like routing, component reuse or data-driven
   interaction that Quarto cannot support cleanly with the existing generator
   and filter boundaries.
4. A deliberate visual redesign is approved and would require reworking the
   existing Quarto/Bootstrap shell anyway.

If triggered, the experiment should compare a small Astro main-shell proof of
concept against the current site at the same public URLs and visual standard.
It must leave Quarto technical content untouched and make an explicit decision
about build, deployment and shared-design ownership before any migration.

## Current operating rule

Use Quarto-native features where they meet the need. Keep site-specific
behaviour in the documented canonical sources. Do not add post-processing or
new override layers merely to hide Quarto behaviour; record a recurring
boundary problem and reassess it against the threshold above.

See `CLEANUP_PLAN.md` for the cleanup evidence and `SOURCE_MAP.md` for editing
ownership.
