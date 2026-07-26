# F1 and FC-GCG project integration

## What was integrated

Two supplied Claude/Fable projects are now first-class pages in the Quarto website:

- `f1-time-rank-duality.qmd` → `/f1-time-rank-duality.html`
- `sparse-gcg.qmd` → `/sparse-gcg.html`

They are treated simultaneously as portfolio projects and accessible research explainers. This avoids maintaining a short project page and a duplicate blog post containing the same material.

## Changes to the supplied projects

The underlying questions, mathematical explanations, figures and code examples were preserved. Changes were deliberately limited to website integration and accuracy:

- removed blog-style dates and converted the posts into durable project pages;
- added concise evidence strips describing the question, methods, implementation and outputs;
- clarified co-authorship and the relationship to the formal papers;
- changed executable R code to a displayed workflow and used the supplied precomputed figure, so website rendering does not depend on R being installed;
- strengthened the GCG benchmark caveat: the experiment is illustrative and favourable to FC-GCG, not a universal comparison with all specialised lasso solvers;
- added clear sections explaining reproducibility, limitations and transferable skills;
- bundled the complete supplied source projects as downloadable ZIP files.

## Website integration

### Homepage

The three visible project cards are now:

1. Formula 1 time–rank duality
2. Sparse optimisation with FC-GCG
3. Applied statistical modelling course

This combination shows statistical modelling and communication, algorithm implementation and evaluation, and documentation/learning design. No carousel is used.

### Projects page

The Projects page now leads with the two fully inspectable publication-grounded projects. Dynamic imaging, teaching materials, materials modelling and the website remain as complementary examples.

Every major card identifies the question, approach, evidence and skills demonstrated beyond the mathematics.

### Publications

The relevant publication entries now include an `Explainer` action:

- *Faster identification of faster Formula 1 drivers via time-rank duality* → F1 project page
- *Asymptotic linear convergence of Fully-Corrective Generalized Conditional Gradient methods* → FC-GCG project page

Their `Code` actions currently download the supplied source archives.

## Repository links

The GitHub URLs proposed inside the supplied project files were not yet publicly available when this integration was completed. To avoid deploying broken links, the live website uses local source downloads:

- `/assets/downloads/f1-time-rank-duality.zip`
- `/assets/downloads/sparse-gcg-demo.zip`

Once separate repositories are published, replace these values in:

- `data/projects.yml`
- `data/publications.bib`
- the action links in the two project `.qmd` files

The intended repository names are:

- `sfanzon/F1-Paper-Code` (code, data, tests and walkthrough source)
- `sfanzon/sparse-gcg-demo`

## Validation

- `scripts/build-content.py` runs successfully and regenerates homepage/project/publication components.
- The FC-GCG convergence experiment was run successfully in the integration environment. It reproduced an 11-nonzero optimum and termination after 12 recorded FC-GCG iterations with the supplied KKT tolerance.
- The F1 R analysis could not be rerun because R was not installed in the environment. Its supplied code, data and generated figure were retained without inventing new outputs.
- Source `.qmd` files and pre-rendered `docs` pages were both updated.
- New pages were added to `docs/search.json` and `docs/sitemap.xml`.


## Current F1 ownership

The F1 industry explainer is maintained in the website repository. The technical walkthrough is deployed separately from `F1-Paper-Code` at `https://www.silviofanzon.com/F1-Paper-Code/`. The former local walkthrough route is a redirect only.
