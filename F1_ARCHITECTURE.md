# Formula 1 project architecture

The Formula 1 project is intentionally split into two independently rendered repositories.

- `projects/f1-time-rank-duality/index.qmd` is the polished project overview on the main website.
- The separate `F1-Paper-Code` repository owns the full technical walkthrough, data, analysis code, tests, and its independent Quarto mini-site.

The main website does not run the Formula 1 analysis or render the technical mini-site. The three collapsed plotting examples on the overview page are stable local snapshots under `projects/f1-time-rank-duality/snippets/`; the displayed figures remain static website assets under `figures/`.
