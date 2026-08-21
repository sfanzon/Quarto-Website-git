# Legacy content inventory

## Scope

This inventory covers files directly under the old `sfanzon.github.io` repository's `_pages/`, `_projects/`, `_posts/` and `_news/` directories, plus the Teaching, presentation, supervision and CV/document records and resources needed to verify content coverage. Other collections, data, downloads and assets remain out of scope unless listed in an audit slice.

## Summary

| Status | Count |
|---|---:|
| MIGRATED | 32 |
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

## Old news

| Old source | Date | Old content | Current equivalent | Status | Notes |
|---|---|---|---|---|---|
| `_news/2023-04-03.md` | 2023-04-03 | Joining the University of Hull | `news/2023-04-03.md` | MIGRATED | Same announcement; title and category added. |
| `_news/2023-04-12.md` | 2023-04-12 | Launching silviofanzon.com | `news/2023-04-12.md` | MIGRATED | Same announcement; title and category added. |
| `_news/2023-04-17.md` | 2023-04-17 | Joining the Inverse Problems International Association | `news/2023-04-17.md` | MIGRATED | Same announcement; title and category added. |
| `_news/2023-05-12.md` | 2023-05-12 | Joining the PRIMO Research Group | `news/2023-05-12.md` | MIGRATED | Same announcement; title and category added. |
| `_news/2023-06-01.md` | 2023-06-01 | Beginning the PCAP programme | `news/2023-06-01.md` | MIGRATED | Same announcement; title and category added. |
| `_news/2023-07-13.md` | 2023-07-13 | Conditional-gradient paper published in Mathematical Programming | `news/2023-07-13.md` | MIGRATED | Same announcement; title/category added and publication link now uses a compatibility `.html` route. |
| `_news/2023-09-04.md` | 2023-09-04 | Presenting dynamic imaging research at AIP 2023 | `news/2023-09-04.md` | MIGRATED | Same announcement; title and category added. |
| `_news/2023-09-20.md` | 2023-09-20 | Teaching in Autumn 2023 | `news/2023-09-20.md` | MIGRATED | Same announcement; title/category added and Teaching links now use compatibility `.html` routes. |
| `_news/2023-12-22.md` | 2023-12-22 | Formula 1 time-rank preprint and reproducible code released | `news/2023-12-22.md` | MIGRATED | Same announcement; title/category added, publication link uses a compatibility `.html` route, and code link changed host. |
| `_news/2024-01-01.md` | 2024-01-01 | Teaching Statistical Models in 2023/24 | `news/2024-01-01.md` | MIGRATED | Same announcement; Teaching link uses a compatibility `.html` route, but legacy course-page link remains and targets an unproduced `/blog/...` route. |
| `_news/2024-03-25.md` | 2024-03-25 | Formula 1 paper published in Economics Letters | `news/2024-03-25.md` | MIGRATED | Same announcement; title/category added, publication link uses a compatibility `.html` route, and code link changed host. |
| `_news/2024-05-14.md` | 2024-05-14 | Reflective teaching case studies completed | `news/2024-05-14.md` | MIGRATED | Same announcement; title/category added and publication link now uses a compatibility `.html` route. |
| `_news/2024-06-18.md` | 2024-06-18 | Curling strategy preprint released | `news/2024-06-18.md` | MIGRATED | Same announcement; title/category added and publication link now uses a compatibility `.html` route. |
| `_news/2024-08-01.md` | 2024-08-01 | Statistical Models curriculum review completed | `news/2024-08-01.md` | MIGRATED | Same announcement; title/category added and Teaching/Presentations links now use compatibility `.html` routes. |
| `_news/2024-09-15.md` | 2024-09-15 | Teaching in Autumn 2024 | `news/2024-09-15.md` | MIGRATED | Same announcement; title/category added and Teaching links now use compatibility `.html` routes. |
| `_news/2025-01-10.md` | 2025-01-10 | Teaching Statistical Models in 2024/25 | `news/2025-01-10.md` | MIGRATED | Same announcement; Teaching link uses a compatibility `.html` route, but legacy course-page link remains and targets an unproduced `/blog/...` route. |
| `_news/2025-02-18.md` | 2025-02-18 | Curling strategy paper published in Managerial Finance | `news/2025-02-18.md` | MIGRATED | Same announcement; title/category added and publication link now uses a compatibility `.html` route. |
| `_news/2025-03-20.md` | 2025-03-20 | Teaching philosophy statement published | `news/2025-03-20.md` | MIGRATED | Same announcement; title and category added. |
| `_news/2025-08-01.md` | 2025-08-01 | Awarded Fellowship of the Higher Education Academy | `news/2025-08-01.md` | MIGRATED | Same announcement; title and category added. |
| `_news/2025-12-16.md` | 2025-12-16 | Speaking at the Young Analysts in Rome workshop | `news/2025-12-16.md` | MIGRATED | Same announcement; title and category added. |
| `_news/2026-02-10.md` | 2026-02-10 | Presenting at the University of Hull Research Sandpit | `news/2026-02-10.md` | MIGRATED | Same announcement; title and category added. |
| `_news/2026-03-17.md` | 2026-03-17 | Formula 1 benchmarking preprint released | `news/2026-03-17.md` | MIGRATED | Same announcement; title/category added and publication link now uses a compatibility `.html` route. |

## Publications and associated resources

This slice audits 17 publication records and 7 associated publication/resource records against the current hybrid publication archive.

| Publication/resource | Old source | Current destination | Status | Notes |
|---|---|---|---|---|
| Benchmarking Formula 1 results using a normal model | `_bibliography/publications_journal.bib#2026-Fry-Fan-Aus-Bri` | `data/publications.bib#2026-Fry-Fan-Aus-Bri` → `/publications/#2026-Fry-Fan-Aus-Bri` | MIGRATED | Authors, arXiv record and PDF are preserved; the current arXiv identifier corrects the legacy BibTeX value. |
| Elementary econometric and strategic analysis of curling matches | `_bibliography/publications_journal.bib#2025-Fry-Aus-Fan` | `data/publications.bib#2025-Fry-Aus-Fan` → `/publications/#2025-Fry-Aus-Fan` | MIGRATED | Authors, journal/DOI, arXiv link and final PDF are preserved. |
| Asymptotic linear convergence of Fully–Corrective Generalized Conditional Gradient methods | `_bibliography/publications_journal.bib#2024-Bre-Car-Fan-Wal` | `data/publications.bib#2024-Bre-Car-Fan-Wal` → `/publications/#2024-Bre-Car-Fan-Wal` | MIGRATED | Authors, journal/DOI, PDF, short slides, code and the local sparse-GCG explainer are preserved. |
| Faster identification of faster Formula 1 drivers via time-rank duality | `_bibliography/publications_journal.bib#2024-Fry-Bri-Fan` | `data/publications.bib#2024-Fry-Bri-Fan` → `/publications/#2024-Fry-Bri-Fan` | MIGRATED | Authors, journal/DOI, PDF and code repository are preserved; the code destination now uses the GitHub repository. |
| A Generalized Conditional Gradient Method for Dynamic Inverse Problems with Optimal Transport Regularization | `_bibliography/publications_journal.bib#2023-Bre-Car-Fan-Rom` | `data/publications.bib#2023-Bre-Car-Fan-Rom` → `/publications/#2023-Bre-Car-Fan-Rom` | MIGRATED | Authors, journal/DOI, arXiv, PDF, code, poster and video are preserved. |
| A superposition principle for the inhomogeneous continuity equation with Hellinger–Kantorovich-regular coefficients | `_bibliography/publications_journal.bib#2022-Bre-Car-Fan` | `data/publications.bib#2022-Bre-Car-Fan` → `/publications/#2022-Bre-Car-Fan` | MIGRATED | Authors, journal/DOI, arXiv and PDF are preserved. |
| On the extremal points of the ball of the Benamou–Brenier energy | `_bibliography/publications_journal.bib#2021-Bre-Car-Fan-Rom` | `data/publications.bib#2021-Bre-Car-Fan-Rom` → `/publications/#2021-Bre-Car-Fan-Rom` | MIGRATED | Authors, journal/DOI, arXiv, PDF and slides are preserved. |
| An optimal transport approach for solving dynamic inverse problems in spaces of measures | `_bibliography/publications_journal.bib#2020-Bre-Fan` | `data/publications.bib#2020-Bre-Fan` → `/publications/#2020-Bre-Fan` | MIGRATED | Authors, journal/DOI, arXiv, PDF and slides are preserved. |
| Uniform distribution of dislocations in Peierls–Nabarro models for semi-coherent interfaces | `_bibliography/publications_journal.bib#2020-Fan-Pon-Sca` | `data/publications.bib#2020-Fan-Pon-Sca` → `/publications/#2020-Fan-Pon-Sca` | MIGRATED | Authors, journal/DOI, arXiv, PDF and slides are preserved. |
| Derivation of Linearized Polycrystals from a Two-Dimensional System of Edge Dislocations | `_bibliography/publications_journal.bib#2019-Fan-Pal-Pon` | `data/publications.bib#2019-Fan-Pal-Pon` → `/publications/#2019-Fan-Pal-Pon` | MIGRATED | Authors, journal/DOI, arXiv, PDF and slides are preserved. |
| Optimal lower exponent for the higher gradient integrability of solutions to two-phase elliptic equations in two dimensions | `_bibliography/publications_journal.bib#2017-Fan-Pal` | `data/publications.bib#2017-Fan-Pal` → `/publications/#2017-Fan-Pal` | MIGRATED | Authors, journal/DOI, arXiv, PDF and slides are preserved. |
| A Variational Model for Dislocations at Semi-coherent Interfaces | `_bibliography/publications_journal.bib#2017-Fan-Pal-Pon` | `data/publications.bib#2017-Fan-Pal-Pon` → `/publications/#2017-Fan-Pal-Pon` | MIGRATED | Authors, journal/DOI, arXiv, PDF, slides and poster are preserved. |
| Geometric patterns and microstructures in the study of material defects and composites | `_bibliography/publications_theses.bib#2018-Fan-PhD` | `data/publications.bib#2018-Fan-PhD` → `/publications/#2018-Fan-PhD` | MIGRATED | Thesis authorship, PDF and viva slides are preserved; the external repository link is audited separately below. |
| A variational approach to topological singularities in two-dimensions (in Italian) | `_bibliography/publications_theses.bib#2014-Fan-MSc` | `data/publications.bib#2014-Fan-MSc` → `/publications/#2014-Fan-MSc` | MIGRATED | Author, thesis PDF and citation are preserved. |
| The isoperimetric problem (in Italian) | `_bibliography/publications_theses.bib#2011-Fan-BSc` | `data/publications.bib#2011-Fan-BSc` → `/publications/#2011-Fan-BSc` | MIGRATED | Author, thesis PDF and citation are preserved. |
| Optimal Transport Based Convex Hybrid Image and Motion-Field Reconstruction | `_bibliography/publications_miscellaneous.bib#2021-ISMRM` | `data/publications.bib#2021-ISMRM` → `/publications/#2021-ISMRM` | MIGRATED | Authors, conference, abstract and citation are preserved; the external archive resource is audited separately below. |
| Lecture Notes on Ordinary Differential Equations (in Italian) | `_bibliography/publications_miscellaneous.bib#2013-ODE-Book` | `data/publications.bib#2013-ODE-Book` → `/publications/#2013-ODE-Book` | MIGRATED | Authors, publisher, book link, PDF and citation are preserved. |
| Legacy 2024 curling preprint record and PDF | `_bibliography/publications_preprint.bib#2024-Fry-Aus-Fan` | `data/publications.bib#2025-Fry-Aus-Fan` | MERGED | The preprint is represented by the current journal record and arXiv link; the standalone legacy preprint PDF is not retained separately. |
| Journal publication PDFs | `pdf` fields in `_bibliography/publications_journal.bib` | `assets/pdf/journal/` and publication archive PDF actions | PRESERVED | All 12 legacy journal PDF paths have corresponding current assets. |
| Journal slides and posters | `slides`/`poster` fields in `_bibliography/publications_journal.bib` | `assets/pdf/journal/slides/` and `assets/pdf/journal/poster/` | PRESERVED | All BibTeX-referenced journal slides/posters are present and linked where the current record exposes them. |
| Code, project and video resources | `code`/`video` fields in `_bibliography/publications_journal.bib` | Current publication actions, GitHub repositories and `/projects/sparse-gcg/` | MIGRATED | F1 and DGCG code, the sparse-GCG explainer/project, and the DGCG video remain available; F1 code uses its GitHub destination. |
| Thesis, book PDF and viva-slide resources | `pdf`/`slides` fields in `_bibliography/publications_theses.bib` and `_bibliography/publications_miscellaneous.bib` | `assets/pdf/thesis/`, `assets/pdf/teaching/2013/` and `assets/pdf/seminars/slides/2018/` | PRESERVED | All referenced thesis, book and PhD viva PDF resources are present. |
| ISMRM archive page | `html`/`url` in `_bibliography/publications_miscellaneous.bib#2021-ISMRM` | No current external archive link in `data/publications.bib` or the rendered record | NEEDS REVIEW | The publication record and abstract migrated, but the legacy ISMRM archive destination is not currently exposed. |
| Sussex PhD repository page | `url` in `_bibliography/publications_theses.bib#2018-Fan-PhD` | Current thesis record retains the legacy repository URL | NEEDS REVIEW | The thesis PDF and viva slides are present, but `srodev.sussex.ac.uk` may be an outdated repository destination and needs verification. |

## Teaching resources

The old Teaching page and its 21 lecturer/tutor records are represented by `astro/src/pages/teaching.astro` and `data/teaching.yml`; there is no separate current Quarto Teaching page. The 12 detailed course posts remain separately listed as `NEEDS REVIEW` above because their pages and attached teaching material are not part of the current production output.

| Teaching item | Old source | Current destination | Status | Notes |
|---|---|---|---|---|
| Teaching catalogue and role/year structure | `_pages/teaching.md`, `_bibliography/teaching_lecturer.bib`, `_bibliography/teaching_tutor.bib` | `astro/src/pages/teaching.astro`, `data/teaching.yml` → `/teaching/` | MIGRATED | All 21 old teaching records have current catalogue entries, including lecturer, tutor, venue, year and course metadata. |
| 2013 Ordinary Differential Equations notes | `_bibliography/teaching_tutor.bib#2013-ODE`, `assets/pdf/teaching/2013/Appunti_EDO.pdf` | `data/teaching.yml`, `assets/pdf/teaching/2013/Appunti_EDO.pdf` | PRESERVED | The Italian lecture notes PDF and Google Books link remain available. |
| Course taster slides | `assets/pdf/teaching/2023-Differential-Geometry/`, `2024-Differential-Geometry/`, `2024-Statistical-Models/`, `2025-Statistical-Models/`, `2026-Statistical-Models/` | Matching files under `assets/pdf/teaching/` and current Teaching entries | PRESERVED | Five legacy taster PDFs remain present and linked from the current catalogue. |
| Detailed course PDFs, exercises, exams, coding archives and teaching scripts | Resource files linked by the 2019, 2021 and 2022 course posts and the 2024–2026 Statistical Models posts | None in current production | NEEDS REVIEW | The old repository contains 166 resource files not present in the current teaching asset tree; decide which lecture notes, exercise sheets, exams, coding archives and scripts merit recovery or archival. |
| External course pages, lecture notes, revision pages and Canvas links | URLs in old teaching records/posts | External URLs retained in `data/teaching.yml` | NEEDS REVIEW | Canvas and selected notes/revision links remain represented, but the 12 legacy `/blog/...` course-page links target unproduced routes and the availability of other external course pages should be checked. |

## Presentations and talks

The old seminar bibliographies contain 23 presentation records: 15 talks, 4 posters and 4 institutional presentations. The current Astro Presentations page renders the same 23 records from the three current BibTeX sources.

| Presentation/resource | Old source | Current destination | Status | Notes |
|---|---|---|---|---|
| Presentation, talk and poster records | `_bibliography/seminars_talks.bib`, `_bibliography/seminars_posters.bib`, `_bibliography/seminars_institutional.bib` | `data/presentations_talks.bib`, `data/presentations_posters.bib`, `data/presentations_institutional.bib` → `/presentations/` | MIGRATED | All 23 substantive records, titles, dates, venues and abstracts are represented in the current Astro archive. |
| Preserved seminar slides and posters | `assets/pdf/seminars/` | `assets/pdf/seminars/` and current presentation actions | PRESERVED | 11 legacy slide/poster files remain present, including the 2016 CMU, 2017 Levico, 2021 TraDE, 2023 Göttingen, 2024 taster, 2025 Sapienza and 2026 Hull materials. |
| Missing seminar slides | `assets/pdf/seminars/slides/2018/2018-Graz-Slides.pdf`, `2018-Lisbon-Slides.pdf`; 2019 Berlin/Paris/Vienna; 2021 Parma; 2022 Edinburgh/Graz/Sussex; 2023 Sussex | No current local asset | NEEDS REVIEW | Retain as a future recovery/archive decision; do not delete the legacy copies from any recovery source. |
| Curriculum Design slides and video | `slides` and `video` fields for `2024-Curriculum-Design` | External slide URL and YouTube video in the current record | NEEDS REVIEW | Retain as a future verification decision; do not remove the preserved external links now. |

## Supervision

The old supervision bibliographies contain 9 records: 1 PhD, 3 master’s and 5 undergraduate projects. The current Astro archive renders the 8 master’s/undergraduate records, while the old PhD record is absent from the current source and page.

| Supervision item/resource | Old source | Current destination | Status | Notes |
|---|---|---|---|---|
| Master’s and undergraduate supervision records | `_bibliography/supervision_master.bib`, `_bibliography/supervision_undergraduate.bib` | `data/supervision_master.bib`, `data/supervision_undergraduate.bib` → `/supervision/` | MIGRATED | All 8 records preserve the student identifiers, project titles, degree category, institution, year and abstract. |
| 2025 PhD supervision record | `_bibliography/supervision_phd.bib#2025-Austin` | None in current `data/` or `/supervision/` | DELIBERATELY REMOVE | The old “Statistical Models for Sports” record is omitted because it is not part of the current public supervision content; no recovery is planned. |
| Supervision-associated files and public links | Supervision bibliography records and old `/pages/supervision.md` | None identified in current supervision data/page | NEEDS REVIEW | No linked dissertation PDFs, reports, repositories or other public project resources were found in either supervision source set; verify whether any standalone student material exists elsewhere before closing this audit. |

## CV and downloadable documents

The old CV page offered academic and industry downloads, while a separate legacy route exposed a generated CV document. The current Astro CV page exposes the academic PDF only.

| Document or route | Old source | Current destination | Status | Notes |
|---|---|---|---|---|
| CV page | `_pages/cv.md` (`/cv/`) | `astro/src/pages/cv.astro` → `/cv/` | MIGRATED | The page and its Projects/Publications cross-links are preserved; the current page intentionally lists only the academic CV. |
| Academic CV PDF | `Silvio_Fanzon_Academic_CV.pdf` linked by `_pages/cv.md` | `Silvio_Fanzon_Academic_CV.pdf` → `/Silvio_Fanzon_Academic_CV.pdf` | PRESERVED | The same named PDF exists at the repository root and is copied into the hybrid output. |
| Industry CV download | `/Silvio_Fanzon_Industry_CV.pdf` link in `_pages/cv.md` | None found in the old repository or current site | NEEDS REVIEW | Retain as a future user decision; no historical link or document is removed now. |
| Historic `/Silvio_Fanzon_CV.pdf` route | `_pages/cv_old.md` | None in current production | NEEDS REVIEW | Retain as a future compatibility decision; no redirect or removal is made in this audit. |
| Teaching statement and PCAP case studies | `assets/pdf/news/2025/Fanzon_Teaching_Philosophy.pdf`, `assets/pdf/news/2024/Fanzon_Case_Study_{1,2}.pdf` | Matching files under `assets/pdf/news/` and current News links | PRESERVED | These meaningful professional documents remain available; they are cross-referenced by the completed News/Teaching audits. |
| Microscopy Hull event PDF | `assets/pdf/events/2023/Microscopy_Hull.pdf` and duplicate `assets/pdf/news/2023/Microscopy_Hull.pdf` | None found in current assets or content | NEEDS REVIEW | Retain as a potentially recoverable public resource; future user decision required before recovery, archival or removal. |

## Remaining collections and assets

This slice checks the old structured data and standalone asset folders not covered by the preceding content audits, excluding build output, caches and theme implementation files.

| Collection/resource | Old source | Current destination | Status | Notes |
|---|---|---|---|---|
| Coauthor profile links | `_data/coauthors.yml` | `data/coauthors.yml` and rendered publication author links | MERGED | The meaningful coauthor names and profile URLs are retained through current publication data and generated records. |
| Social/profile metadata | `_data/socials.yml` | Astro Contact/profile links | NEEDS REVIEW | LinkedIn, GitHub, Scholar, ResearchGate, ORCID and email are represented; retain the Scopus/arXiv omission as a future profile decision. |
| Venue metadata | `_data/venues.yml` | Publication/presentation source records and generated links | MERGED | Journal, thesis, seminar and publisher destinations are consumed by the audited records; no separate public venue collection remains. |
| Repository listing data | `_data/repositories.yml` | None | DELIBERATELY REMOVE | The file contains only al-folio starter repositories and placeholder GitHub users, not Silvio-specific public content. |
| Scholar cache | `_data/scholar_cache.yml` | None | DELIBERATELY REMOVE | Cached template data (`N/A`) is implementation state, not meaningful public content. |
| Bookshelf entry | `_books/the_godfather.md` | None | DELIBERATELY REMOVE | Generic al-folio/Carl Sagan template residue, unrelated to Silvio’s published content. |
| Profile photographs | `assets/img/silvioimg.jpeg`, `prof_pic.jpg`, `prof_pic_color.png` | `assets/img/profile/silvioimg.png` and homepage/About usage | MIGRATED | The current profile image is the deliberate production asset; the old variants are not separately referenced. |
| Generic demo media and data | `assets/audio/`, `assets/video/`, `assets/jupyter/`, `assets/html/`, `assets/json/`, `assets/plotly/`, demo screenshots/GIFs and book-cover images under `assets/img/` | None | DELIBERATELY REMOVE | These are al-folio starter demonstrations or template media, not meaningful Silvio-specific public resources. |

## Final reconciliation decisions

These six items remain `NEEDS REVIEW` in their source rows because they are intentionally deferred to a future user decision. The PhD record is explicitly omitted below rather than left unresolved.

| Item | Decision | Rationale | Later implementation |
|---|---|---|---|
| Missing Industry CV | **FUTURE USER DECISION** | The old CV page links to an Industry CV, but no corresponding file exists in the audited old repository or current site. | Later: recover/recreate and link it, or retire the historical reference after confirmation. |
| Historic `/Silvio_Fanzon_CV.pdf` route | **FUTURE USER DECISION** | It was historically public, but its intended compatibility behaviour is not established. | Later: add a compatibility route/document or retire it; no redirect is created now. |
| Microscopy Hull PDF | **FUTURE USER DECISION** | Two legacy copies exist without a surviving page/news reference, but the PDF may be a useful public resource. | Later: recover one copy or archive it; do not delete it now. |
| Missing seminar slide PDFs | **FUTURE USER DECISION** | Ten slides are absent locally while their presentation records remain. | Later: recover selected files or archive them intentionally; no assets are deleted now. |
| Curriculum Design slides/video links | **FUTURE USER DECISION** | External destinations are preserved, but continued availability and preferred hosting are unverified. | Later: verify links and optionally replace them; do not remove them now. |
| Missing 2025 PhD supervision record | **DELIBERATELY REMOVE / OMIT** | It is not part of the current public supervision content. | No recovery or implementation work remains for this record. |
| Scopus/arXiv profile metadata | **FUTURE USER DECISION** | Old metadata contains profile identifiers not surfaced as standalone current links. | Later: add profile links if desired, or document intentional omission. |

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
- `2021-ISMRM`: decide whether to restore the legacy archive link for the migrated conference record.
- `2018-Fan-PhD`: verify or replace the legacy Sussex repository destination.
- Teaching resources: decide which of the 166 missing detailed course files should be recovered or archived.
- Teaching links: decide whether to migrate/archive the detailed `/blog/...` course pages or remove/replace the current Teaching links, and verify the remaining external notes/revision/course destinations.
- Presentations: decide whether to recover or archive the ten missing seminar slide PDFs and verify the external Curriculum Design slide/video links.
- Supervision: the missing 2025 PhD record is deliberately omitted; standalone-resource verification remains covered by the supervision audit.
- CV/documents: decide the fate of the missing Industry CV, historic `/Silvio_Fanzon_CV.pdf` route, and old Microscopy Hull PDF.
- Remaining collections/assets: decide whether to expose Scopus/arXiv profile links and resolve any legacy resource decisions recorded above.

## Next audit slice

The substantive legacy collections and downloads have now been inventoried. Final migration/design work should wait for the six future user decisions above and the other historical-resource decisions retained in `NEEDS REVIEW`.
