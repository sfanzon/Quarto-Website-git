This repository is both the reproducible codebase and the source of the technical
walkthrough. The site root is `index.qmd`; there is no intermediate description
page.

### Local preview

```bash
quarto preview index.qmd
```

### Full build

```bash
quarto render
```

The pre-render hook regenerates the four figures with base R. Configure GitHub
Pages for the repository's Quarto output using your existing deployment workflow.
The intended public route is:

- https://www.silviofanzon.com/F1-Paper-Code/

The rendered resource uses the main-site navbar, local search and colour toggle, a right on-page table of contents. Navigation links back to:

- project overview: index.qmd
- main website: https://www.silviofanzon.com/
- repository: https://github.com/sfanzon/F1-Paper-Code
