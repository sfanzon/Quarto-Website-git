# Legacy content inventory

## Scope

This first pass covers only files directly under the old `sfanzon.github.io` repository's `_pages/`, `_projects/` and `_posts/` directories. Other collections, data, downloads and assets are intentionally out of scope.

## Summary

| Status | Count |
|---|---:|
| MIGRATED | 10 |
| DELIBERATELY REMOVE | 16 |
| NEEDS REVIEW | 14 |

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

## Old project collection

| Old source | Old project/title | Current equivalent | Status | Notes |
|---|---|---|---|---|
| `_projects/1_project.md` | `project 1` | None | DELIBERATELY REMOVE | Generic al-folio image-grid demonstration. |
| `_projects/2_project.md` | `project 2` | None | DELIBERATELY REMOVE | Generic al-folio image-grid and Giscus demonstration. |
| `_projects/3_project.md` | `project 3 with very long name` | None | DELIBERATELY REMOVE | Generic al-folio redirect demonstration. |
| `_projects/4_project.md` | `project 4` | None | DELIBERATELY REMOVE | Generic al-folio image-grid demonstration. |
| `_projects/5_project.md` | `project 5` | None | DELIBERATELY REMOVE | Generic al-folio image-grid demonstration. |
| `_projects/6_project.md` | `project 6` | None | DELIBERATELY REMOVE | Generic al-folio image-grid demonstration. |
| `_projects/7_project.md` | `project 7` | None | DELIBERATELY REMOVE | Generic al-folio image-grid demonstration. |
| `_projects/8_project.md` | `project 8` | None | DELIBERATELY REMOVE | Generic al-folio image-grid and Giscus demonstration. |
| `_projects/9_project.md` | `project 9` | None | DELIBERATELY REMOVE | Generic al-folio image-grid demonstration. |

## Old posts

| Old source | Title / year | Old public route | Current equivalent | Status | Notes |
|---|---|---|---|---|---|
| `_posts/2019-09-22-Advanced-Functional-Analysis.md` | Advanced Functional Analysis / 2019/20 | `/blog/2019/Advanced-Functional-Analysis/` | `data/teaching.yml` → `/teaching/#2019-Functional-Analysis` | NEEDS REVIEW | Course summary remains, but Teaching still links to this now-unproduced legacy course page; decide whether to migrate/archive it or remove/replace the link. |
| `_posts/2021-02-01-Calculus-of-Variations.md` | Calculus of Variations / 2020/21 | `/blog/2021/Calculus-of-Variations/` | `data/teaching.yml` → `/teaching/#2021-Calculus-Variations` | NEEDS REVIEW | Course summary remains, but Teaching still links to this now-unproduced legacy course page; decide whether to migrate/archive it or remove/replace the link. |
| `_posts/2022-09-18-Analysis-3.md` | Analysis 3 / 2022/23 | `/blog/2022/Analysis-3/` | `data/teaching.yml` → `/teaching/#2022-Analysis` | NEEDS REVIEW | Course summary remains, but Teaching still links to this now-unproduced legacy course page; decide whether to migrate/archive it or remove/replace the link. |
| `_posts/2022-09-26-Inverse-Problems.md` | Inverse Problems / 2022/23 | `/blog/2022/Inverse-Problems/` | `data/teaching.yml` → `/teaching/#2022-Inverse-Problems` | NEEDS REVIEW | Course summary remains, but Teaching still links to this now-unproduced legacy course page; decide whether to migrate/archive it or remove/replace the link. |
| `_posts/2023-06-01-NSS.md` | Numbers, Sequences and Series / 2023/24 | `/blog/2023/NSS/` | `data/teaching.yml` → `/teaching/#2023-NSS` | NEEDS REVIEW | Course summary remains, but Teaching still links to this now-unproduced legacy course page; decide whether to migrate/archive it or remove/replace the link. |
| `_posts/2023-06-02-Differential-Geometry.md` | Differential Geometry / 2023/24 | `/blog/2023/Differential-Geometry/` | `data/teaching.yml` → `/teaching/#2023-Differential-Geometry` | NEEDS REVIEW | Course summary remains, but Teaching still links to this now-unproduced legacy course page; decide whether to migrate/archive it or remove/replace the link. |
| `_posts/2024-09-15-Differential-Geometry.md` | Differential Geometry / 2024/25 | `/blog/2024/Differential-Geometry/` | `data/teaching.yml` → `/teaching/#2024-Differential-Geometry` | NEEDS REVIEW | Course summary remains, but Teaching still links to this now-unproduced legacy course page; decide whether to migrate/archive it or remove/replace the link. |
| `_posts/2024-09-15-NSS.md` | Numbers, Sequences and Series / 2024/25 | `/blog/2024/NSS/` | `data/teaching.yml` → `/teaching/#2024-NSS` | NEEDS REVIEW | Course summary remains, but Teaching still links to this now-unproduced legacy course page; decide whether to migrate/archive it or remove/replace the link. |
| `_posts/2024-1-4-Statistical-Models.md` | Statistical Models / 2023/24 | `/blog/2024/Statistical-Models/` | `data/teaching.yml` → `/teaching/#2024-Statistical-Models` | NEEDS REVIEW | Course summary remains, but Teaching still links to this now-unproduced legacy course page; decide whether to migrate/archive it or remove/replace the link. |
| `_posts/2025-1-9-Statistical-Models.md` | Statistical Models / 2024/25 | `/blog/2025/Statistical-Models/` | `data/teaching.yml` → `/teaching/#2025-Statistical-Models` | NEEDS REVIEW | Course summary remains, but Teaching still links to this now-unproduced legacy course page; decide whether to migrate/archive it or remove/replace the link. |
| `_posts/2026-1-1-Graduate-Skills.md` | Graduate Skills / 2025/26 | `/blog/2026/Graduate-Skills/` | `data/teaching.yml` → `/teaching/#2026-Graduate-Skills` | NEEDS REVIEW | Course summary remains, but Teaching still links to this now-unproduced legacy course page; decide whether to migrate/archive it or remove/replace the link. |
| `_posts/2026-1-1-Statistical-Models.md` | Statistical Models / 2025/26 | `/blog/2026/Statistical-Models/` | `data/teaching.yml` → `/teaching/#2026-Statistical-Models` | NEEDS REVIEW | Course summary remains, but Teaching still links to this now-unproduced legacy course page; decide whether to migrate/archive it or remove/replace the link. |

## Needs review

- `_pages/blog.md`: the posts audit is complete; there is no current production `/blog/` route because donor Astro blog output is explicitly removed.
- `_pages/cv_old.md`: decide whether the historic `/Silvio_Fanzon_CV.pdf` route should remain available or be retired in favour of the academic CV download.
- `_posts/2019-09-22-Advanced-Functional-Analysis.md`: migrate/archive the detailed legacy course page or remove/replace the current Teaching “Course page” link.
- `_posts/2021-02-01-Calculus-of-Variations.md`: migrate/archive the detailed legacy course page or remove/replace the current Teaching “Course page” link.
- `_posts/2022-09-18-Analysis-3.md`: migrate/archive the detailed legacy course page or remove/replace the current Teaching “Course page” link.
- `_posts/2022-09-26-Inverse-Problems.md`: migrate/archive the detailed legacy course page or remove/replace the current Teaching “Course page” link.
- `_posts/2023-06-01-NSS.md`: migrate/archive the detailed legacy course page or remove/replace the current Teaching “Course page” link.
- `_posts/2023-06-02-Differential-Geometry.md`: migrate/archive the detailed legacy course page or remove/replace the current Teaching “Course page” link.
- `_posts/2024-09-15-Differential-Geometry.md`: migrate/archive the detailed legacy course page or remove/replace the current Teaching “Course page” link.
- `_posts/2024-09-15-NSS.md`: migrate/archive the detailed legacy course page or remove/replace the current Teaching “Course page” link.
- `_posts/2024-1-4-Statistical-Models.md`: migrate/archive the detailed legacy course page or remove/replace the current Teaching “Course page” link.
- `_posts/2025-1-9-Statistical-Models.md`: migrate/archive the detailed legacy course page or remove/replace the current Teaching “Course page” link.
- `_posts/2026-1-1-Graduate-Skills.md`: migrate/archive the detailed legacy course page or remove/replace the current Teaching “Course page” link.
- `_posts/2026-1-1-Statistical-Models.md`: migrate/archive the detailed legacy course page or remove/replace the current Teaching “Course page” link.

## Next audit slice

Collections and assets remain unreviewed: old news; teaching, presentation and supervision source data if separate; bibliography/publication source; PDFs/downloads; images/assets; and other old-site data or resource collections not yet accounted for.
