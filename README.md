# Silvio Fanzon — Quarto portfolio website

This repository contains the source and pre-rendered output for **silviofanzon.com**. It is a heavily customised Quarto website designed to present research, technical projects, teaching and professional experience to both academic and industry audiences.

## Main structure

- `index.qmd` — homepage and professional positioning
- `about.qmd` — career narrative and professional transition
- `expertise.qmd` — transferable capabilities
- `research.qmd` — academic research themes
- `projects.qmd` — inspectable modelling, software and communication work
- `data/publications.bib` — single publication source
- `data/projects.yml` — single source for homepage and Projects-page cards
- `news/` — dated news entries
- `scripts/build-content.py` — generates reusable HTML/QMD fragments
- `styles/main.scss` — site-wide visual system
- `docs/` — pre-rendered website for deployment
- `ARCHITECTURE.md` — source ownership and project-page architecture

## Build locally

Install Quarto and Python with PyYAML, then run:

```bash
quarto preview
```

For a complete static render:

```bash
quarto render
```

The Quarto pre-render hook runs `scripts/build-content.py`, which rebuilds publication, project, teaching and news fragments from their structured sources.

## Test locally

While iterating on a small change, run the quick critical-path suite:

```bash
npm run test:quick
```

Before committing, run the default midrange suite:

```bash
npm test
```

It checks every rendered page in Chromium, key interactions and links, navigation
regressions and visual baselines. Before deployment or after broad structural
or browser-specific changes, run the complete Chromium, Firefox and WebKit matrix:

```bash
npm run test:full
```

Only directly referenced assets are stored under `assets/`. Images are grouped
by brand, profile and project, while downloadable files are grouped by journal,
seminar, news, teaching and thesis purpose. Unlinked archive material remains
outside this lightweight repository snapshot.

## Design principles

- concise homepage with deeper evidence available after the main narrative;
- separate **Expertise** and **Research** pages;
- visible project selection rather than hidden carousel content;
- clear mobile reading order, with section links after the content;
- academic depth translated into modelling, computation, communication and leadership evidence;
- maintainable content generated from BibTeX, YAML and dated Markdown.

See `ARCHITECTURE.md` for source ownership, project-page behaviour and design direction.

## Project architecture

Portfolio explainers live inside this website and inherit the shared Quarto theme:

```text
projects/
├── _metadata.yml
├── f1-time-rank-duality/
│   ├── index.qmd          # plain-language overview
│   ├── technical.qmd      # presentation-adapted technical walkthrough
│   ├── code.qmd           # code, data and deployment guide
│   ├── snapshots/         # Markdown included by the two detailed views
│   ├── figures/
│   └── downloads/         # complete repository snapshot
├── f1-time-rank-duality-previous/
│   ├── index.qmd          # visible archived website version
│   └── images/
└── sparse-gcg/
    ├── index.qmd          # conceptual explainer + pedagogical demo
    └── images/
```

The substantial R/Python implementations live in separate repositories:

- `sfanzon/F1-Paper-Code`
- `sfanzon/sparse-gcg-explainer`

The website pages contain explanation, equations, static figures and selected
annotated code. Expensive experiments run in the project repositories; their
committed outputs are then incorporated into this site. The F1 project keeps
three local presentation views while `sfanzon/F1-Paper-Code` remains canonical
for the implementation, data, tests and independently deployed mini-site.

The `docs/` directory is generated output and should not be edited manually.
