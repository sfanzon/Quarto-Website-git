# Silvio Fanzon — Quarto portfolio website

This repository contains the source and pre-rendered output for **silviofanzon.com**. It is a heavily customised Quarto website designed to present research, technical projects, teaching and professional experience to both academic and industry audiences.

## Main structure

- `index.qmd` — homepage and professional positioning
- `about.qmd` — career narrative and transition
- `expertise.qmd` — transferable capabilities
- `research.qmd` — academic research themes
- `projects.qmd` — inspectable modelling, software and communication work
- `data/publications.bib` — single publication source
- `data/projects.yml` — single source for homepage and Projects-page cards
- `news/` — dated news entries
- `scripts/build-content.py` — generates reusable HTML/QMD fragments
- `styles/main.scss` — site-wide visual system
- `docs/` — pre-rendered website for deployment

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

## Design principles

- concise homepage with deeper evidence available after the main narrative;
- separate **Expertise** and **Research** pages;
- visible project selection rather than hidden carousel content;
- clear mobile reading order, with section links after the content;
- academic depth translated into modelling, computation, communication and leadership evidence;
- maintainable content generated from BibTeX, YAML and dated Markdown.

See `WEBSITE_REDESIGN_REPORT.md` for the positioning rationale and recommended next portfolio projects.

## Project architecture

Portfolio explainers live inside this website and inherit the shared Quarto theme:

```text
projects/
├── _metadata.yml
├── f1-time-rank-duality/
│   ├── index.qmd          # plain-language overview
│   ├── walkthrough.qmd    # compatibility redirect to the separately deployed walkthrough
│   ├── figures/
│   └── data/
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

The website pages should contain explanation, equations, static figures and selected annotated code. Run expensive experiments in the project repositories, commit the resulting outputs, then render the website. The F1 project is an exception in depth—not architecture: its technical page explains the actual companion R workflow, but still uses committed results rather than executing during every site build. The `docs/` directory is generated output and should not be edited manually.


The F1 technical walkthrough is built from the code repository and deployed at
`https://www.silviofanzon.com/F1-Paper-Code/`. The website keeps only the industry-facing project post and a
compatibility redirect for the former local walkthrough URL.
