# Platform decision: test Astro as the website owner

## Decision

Keep the current Quarto site as production while building one isolated vertical
slice that tests Astro as the owner of the professional website.

Quarto is not being evaluated for removal. It remains the required renderer for:

- lecture-note websites;
- mathematical and scientific technical posts;
- documents that need citations, cross-references, executable code or other
  document-oriented features.

The experiment asks only whether Astro should own the normal website shell,
catalogues, landing pages and non-technical content.

## Current hypothesis

Astro is likely a better long-term owner for ordinary website architecture.
Quarto remains the better specialist scientific-document renderer. Both must
consume the same small visual contract so that moving between them feels like
moving between pages of one website.

The Astro implementation of al-folio in `dadangnh/as-folio` is evidence that
Astro can cover the conventional academic-portfolio surface. It is a reference,
not a dependency or an automatic migration target: this website has its own
editorial identity, structured sources and project architecture.

## Decision gate

Do not migrate the full site until the vertical slice proves all of the
following:

1. Astro and Quarto pages are visually seamless in light and dark modes.
2. Existing public URLs can be preserved.
3. Navigation, theme state, metadata, search and assets work across both
   renderers.
4. The complete site builds and previews with one documented command.
5. Content and navigation have one canonical source rather than synchronized
   manual copies.
6. Ongoing editing is simpler than in the current all-Quarto implementation.

If the proof fails any of these conditions, retain the cleaned-up Quarto site.
The detailed experiment and migration sequence are in `ASTRO_QUARTO_PLAN.md`.
