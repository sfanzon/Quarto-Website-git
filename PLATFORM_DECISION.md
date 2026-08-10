# Platform assessment: cleanup before reconsideration

## Current decision

Do not prototype, migrate to, or integrate Astro during this cleanup cycle.
Keep the current Quarto site deployable while simplifying and documenting its
actual implementation.

The purpose of this cycle is to discover how much complexity belongs to the
website itself and how much is caused by working against Quarto. Assessing the
platform before the cleanup is complete would measure historical clutter as if
it were a framework limitation.

## Stable requirement

Lecture-note websites and technical posts that benefit from mathematics,
citations, cross-references, executable code or document-oriented structure
remain Quarto content regardless of the eventual main-site platform.

## What will be assessed

At the end of the cleanup, evaluate Quarto against recorded evidence:

- authoring and editing cost;
- build and deployment complexity;
- amount and stability of custom SCSS, JavaScript, Lua and generated HTML;
- frequency of Quarto-specific workarounds;
- accessibility, responsive and theme behaviour;
- suitability for technical documents;
- maintenance cost of the current site shell.

The result may be to retain Quarto, reconsider the main-site platform later, or
run a separately approved experiment. No migration work is included in the
current repository-cleanup plan.

`dadangnh/as-folio` remains useful evidence that Astro can implement an
al-folio-shaped academic website, but it does not by itself show that migrating
this cleaned, customised Quarto site would reduce maintenance.

See `CLEANUP_PLAN.md` for the active plan and final decision gate.
