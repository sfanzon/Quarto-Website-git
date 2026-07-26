# Project repository ownership

## Formula 1: `F1-Paper-Code`

**Description:** Reproducible R implementation of the time–rank duality model for separating Formula 1 driver performance from constructor advantage.

The repository is maintained independently from the main website. Use the standalone `F1-Paper-Code` repository as the source for:

- data and R modules;
- tests and reproducibility scripts;
- generated figures;
- the technical Quarto mini-site.

Recommended topics: `r`, `formula-one`, `sports-analytics`, `statistical-modelling`, `reproducible-research`, `econometrics`.

## Ownership of the public pages

- Main website repository: the industry-facing project overview at `https://www.silviofanzon.com/projects/f1-time-rank-duality/`.
- `F1-Paper-Code` repository: R code, data, tests and the independently deployed technical walkthrough at `https://www.silviofanzon.com/F1-Paper-Code/`.
- GitHub README: a concise code landing page linking to both resources.

The main website does not contain or render the full Formula 1 repository. It keeps only the overview page, its static figures and the three small plotting-code snapshots displayed in collapsed callouts.

## Sparse GCG

The existing `github-repos/sparse-gcg-explainer/` folder is unchanged in this pass. No Differential Geometry or Statistical Models repositories are included in this architecture change.
