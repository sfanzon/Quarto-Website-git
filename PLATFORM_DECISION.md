# Platform decision: retain Quarto

## Decision

Keep Quarto as the website platform for the current cleanup and the next two
content-maintenance cycles. Do not begin an Astro migration or a mixed
Astro–Quarto build now.

## Why Quarto still fits

- The site is primarily an edited publishing system: QMD pages, BibTeX
  citations, mathematical notation, figures, code and static downloads are
  first-class Quarto work.
- Quarto already provides the document build, navigation, search, theming and
  the static `docs/` deployment artefact.
- The content generator and Lua filter extend Quarto at clear boundaries:
  structured records generate archives, while project pages render shared
  document components.

## Where the friction is real

- The bespoke shell (navbar, archive interactions, responsive layout and
  theme-aware styling) needs more custom SCSS and JavaScript than a plain
  Quarto site.
- Generated HTML includes must remain unindented so Markdown does not render
  them as code, and they must exist before a render.
- Tracking `docs/` is appropriate for the current Pages deployment, but it
  makes rendered-output churn visible in every source change.

These are maintenance costs, not a present platform failure. The canonical
source map, generated-output guard and focused test suites exist specifically
to keep them bounded.

## Why not an Astro–Quarto mix now

Astro as the site shell and Quarto for technical posts is viable, but it would
create two layouts, two asset pipelines, two navigation/search integrations and
a visual-parity obligation. Matching the current light/dark editorial design
exactly would be additional migration work, not simplification. It would also
split the data-to-page generation workflow just after it has been consolidated.

## Reconsider only when evidence changes

Run a small, isolated Astro proof of concept only if at least one of these is
true:

1. New non-document pages require component behaviour that is repeatedly hard
   to express and test in Quarto.
2. The shared shell needs frequent Quarto-specific overrides instead of stable
   source-owned components.
3. A concrete performance, routing or integration requirement cannot be met by
   the static Quarto build.

The proof must render one technical article from the current source, preserve
the same URLs and visual identity, use one canonical content source, and deploy
without a second manual step. Adopt it only if it lowers ongoing editing cost;
otherwise retain Quarto.
