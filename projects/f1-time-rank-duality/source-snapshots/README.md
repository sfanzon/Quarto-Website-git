# Formula 1 time-rank duality

Reproducible companion code for:

> Fry, J., Brighton, T. & Fanzon, S. (2024). *Faster identification of
> faster Formula 1 drivers via time-rank duality*. **Economics Letters**,
> 237:111671. <https://doi.org/10.1016/j.econlet.2024.111671>

This repository contains the **complete computational pipeline** (both datasets,
Tables 1-3, Section 5, four figures and tests) and the source for the deployed
**technical walkthrough**. The shorter, industry-facing project post lives on
silviofanzon.com so it can share the main website's design and portfolio context.

The central result is reproduced with the correct two-stage comparison:

1. the 2022 results estimate a historical second-driver threshold;
2. 2023 Qatar bookmaker odds are translated into expected ranks;
3. within-team gaps in those odds-implied ranks identify Max Verstappen and
   Fernando Alonso as exceeding the threshold.

![Odds-implied teammate gaps](figures/04_teammate_gaps.png)

## Read or reproduce

- **[Project overview](https://www.silviofanzon.com/projects/f1-time-rank-duality/):** the industry-facing story, selected figures and practical interpretation.
- **[Technical walkthrough](https://www.silviofanzon.com/F1-Paper-Code/):** equations, annotated code, published values, model selection and validation.
- **[Published paper](https://www.silviofanzon.com/assets/pdf/journal/2024-Fry-Bri-Fan.pdf):** the theoretical development and full academic discussion.

The walkthrough is built from `index.qmd` in this repository and deployed as a
small Quarto resource. The project overview is intentionally **not duplicated**
here; the README links back to the canonical website post.

## Repository structure

```text
analysis/reproduce_paper.R   one-command reproduction of Tables 1-3 and Section 5
analysis/generate_figures.R  regenerate all four figures only
R/                           modular base-R implementation
R/figures/                   one exact plotting function per displayed figure
data/qatar2023_odds.csv      Table 1 odds + published reference columns
data/f1_2022_positions.txt   20 drivers x 25 events from the 2022 season
tests/run_tests.R            checks against the paper's published numbers
figures/                     committed R-generated figures for Quarto rendering
index.qmd                    full technical walkthrough and deployed site root
walkthrough.qmd              compatibility redirect to the site root
AUDIT.md                     comparison of the two predecessor repositories
```

## Reproduce and test

The analysis itself requires base R only. No statistical or plotting packages
are used.

```bash
Rscript analysis/reproduce_paper.R
Rscript tests/run_tests.R
```

The reproduction writes CSV tables to `output/` and regenerates all four
figures in `figures/`.

To regenerate only the figures:

```bash
Rscript analysis/generate_figures.R
```

or:

```bash
make figures
```

## Figure provenance

Every displayed figure is generated in **base R** from repository data and
model objects:

1. `01_lambda_estimates.png` — Table 1 odds-implied exponential rates;
2. `02_team_effects.png` — Table 3 constructor coefficients and 95% intervals;
3. `03_driver_vs_team.png` — descriptive 2022 driver averages by constructor;
4. `04_teammate_gaps.png` — Section 5 odds-implied within-team gaps.

The exact plotting function for each figure lives in `R/figures/` and is
included verbatim in the Quarto pages inside collapsed code blocks. The PNGs
are committed so the documentation can render without rerunning R, but
`Rscript analysis/generate_figures.R` is the canonical regeneration command.

Figure 3 is intentionally labelled as **descriptive**. It visualises the raw
2022 averages but is not the final driver-versus-car comparison. Figure 4 is
the correct Section 5 calculation, using 2023 Qatar odds-implied expected ranks.

## Important calibration note

The paper estimates exponential rates by minimising

\[
\sum_i\left(\lambda_i/\sum_j\lambda_j-p_i\right)^2.
\]

This objective identifies only relative rates: every vector
`lambda = c * p`, for `c > 0`, is an exact minimiser. The code therefore:

- uses `lambda = p` as the canonical unit-sum solution;
- reproduces the paper's displayed Table 1 scale only for comparison;
- includes a scale-normalised numerical optimiser as a check, not as the
  primary estimator.

## Quarto

The technical walkthrough uses display-only code blocks, so they do not invoke the
knitr engine and do not require `knitr`/`rmarkdown`. Its layout deliberately uses
standard Quarto components: the shared website navbar, a left resource sidebar,
a right scroll-spy table of contents, local search and the light/dark toggle.
The project-level `pre-render` hook runs the base-R figure script before Quarto
builds the pages:

```bash
quarto preview index.qmd
quarto render
```

A normal `quarto render` therefore regenerates every figure automatically.
To reproduce the CSV tables as well, run:

```bash
Rscript analysis/reproduce_paper.R
quarto render
```

## Documentation architecture

This repository owns the code and the technical walkthrough because they should
change together. The industry-facing project post is owned by the main website.
That gives one canonical source for each layer:

```text
Publication Explainer -> https://www.silviofanzon.com/projects/f1-time-rank-duality/
Publication Code      -> https://github.com/sfanzon/F1-Paper-Code
Project walkthrough   -> https://www.silviofanzon.com/F1-Paper-Code/
```

The GitHub README links to both public pages, but does not duplicate the project
post.

## Website integration

See `WEBSITE_INTEGRATION_REPORT.md` for the navigation, palette, bibliography and
rendering architecture used by the deployed technical resource.

## Citation and licence

If this code, data or the accompanying paper is useful in your work, please cite
the published article. GitHub's **Cite this repository** button also reads the
metadata in `CITATION.cff`.

```bibtex
@article{2024-Fry-Bri-Fan,
  author  = {Fry, John and Brighton, Tom and Fanzon, Silvio},
  title   = {Faster identification of faster Formula 1 drivers via time-rank duality},
  journal = {Economics Letters},
  volume  = {237},
  pages   = {111671},
  year    = {2024},
  doi     = {10.1016/j.econlet.2024.111671}
}
```

Repository: [sfanzon/F1-Paper-Code](https://github.com/sfanzon/F1-Paper-Code)

Code and data are released under CC BY-NC 4.0; see `LICENSE`.
