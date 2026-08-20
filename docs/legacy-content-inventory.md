# Legacy content inventory

## Scope

This first pass covers only files directly under the old `sfanzon.github.io` repository's `_pages/` directory. Collections, data, downloads and assets are intentionally out of scope.

## Summary

| Status | Count |
|---|---:|
| MIGRATED | 10 |
| DELIBERATELY REMOVE | 7 |
| NEEDS REVIEW | 2 |

## Old pages

| Old source | Old public route | Current equivalent | Status | Notes |
|---|---|---|---|---|
| `_pages/404.md` | `/404.html` | `astro/src/pages/404.astro` | MIGRATED | Current static 404 route. |
| `_pages/about.md` | `/` | `astro/src/pages/index.astro` | MIGRATED | Former homepage; current homepage replaces its presentation. |
| `_pages/about_einstein.md` | No front matter; not a rendered page | None | DELIBERATELY REMOVE | al-folio biography placeholder. |
| `_pages/blog.md` | `/blog/` | None in production; donor Astro blog output is explicitly removed | NEEDS REVIEW | Old posts are a later audit slice; no current production blog route is confirmed. |
| `_pages/books.md` | `/books/` | None | DELIBERATELY REMOVE | al-folio bookshelf template and Carl Sagan sample copy. |
| `_pages/contact.md` | `/contact/` | `astro/src/pages/contact.astro` | MIGRATED | Current Contact page owns the route. |
| `_pages/cv.md` | `/cv/` | `astro/src/pages/cv.astro` | MIGRATED | Current CV page owns the route. |
| `_pages/cv_default.md` | `/cv_default/` | None | DELIBERATELY REMOVE | al-folio example CV (`example_pdf.pdf`). |
| `_pages/cv_old.md` | `/Silvio_Fanzon_CV.pdf` | Current academic CV download: `/Silvio_Fanzon_Academic_CV.pdf` | NEEDS REVIEW | Historic CV filename/route needs an explicit retention or removal decision. |
| `_pages/dropdown.md` | No explicit permalink | None | DELIBERATELY REMOVE | al-folio submenu demonstration. |
| `_pages/news.md` | `/news/` | `astro/src/pages/news.astro` | MIGRATED | Current News archive owns the route. |
| `_pages/presentations.md` | `/presentations/` | `astro/src/pages/presentations.astro` | MIGRATED | Current Presentations page owns the route. |
| `_pages/profiles.md` | `/people/` | None | DELIBERATELY REMOVE | al-folio lab/people profile example using placeholder content. |
| `_pages/projects.md` | `/projects/` | `astro/src/pages/projects.astro` | MIGRATED | Current Projects catalogue owns the route. |
| `_pages/publications.md` | `/publications/` | `astro/src/pages/publications.astro` | MIGRATED | Current Publications archive owns the route. |
| `_pages/publications_with_preprints_replace.md` | Blank `permalink`; no explicit public route | None | DELIBERATELY REMOVE | Alternative/replacement Publications source, not an active route. |
| `_pages/repositories.md` | `/repositories/` | None | DELIBERATELY REMOVE | al-folio repository-template page. |
| `_pages/supervision.md` | `/supervision/` | `astro/src/pages/supervision.astro` | MIGRATED | Current Supervision page owns the route. |
| `_pages/teaching.md` | `/teaching/` | `astro/src/pages/teaching.astro` | MIGRATED | Current Teaching page owns the route. |

## Needs review

- `_pages/blog.md`: old posts are a later audit slice; there is no confirmed current production `/blog/` route because donor Astro blog output is explicitly removed.
- `_pages/cv_old.md`: decide whether the historic `/Silvio_Fanzon_CV.pdf` route should remain available or be retired in favour of the academic CV download.

## Next audit slice

Collections and assets remain unreviewed: projects; posts/news; teaching, presentation and supervision source records if separate; PDFs/downloads; and images/assets.
