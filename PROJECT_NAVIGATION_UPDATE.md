# Project navigation update

- Removed the top “All projects” link from project-detail pages and placed a quiet return link at the end.
- Added automatic two-digit numbering to every project-section navigation entry.
- Side-navigation labels use the visible section title by default.
- A shorter label can be specified without changing the visible heading, for example:

  ```markdown
  ## A long explanatory section title {data-nav-title="Short label"}
  ```

- Anchor clicks now use the measured sticky-navbar height, and level-two sections also have a CSS `scroll-margin-top` fallback.
- Below 1480px the desktop rail becomes a compact “Sections” button and accessible slide-in drawer.
- All changes remain scoped to `project-detail-page`; the global Quarto layout, navbar and footer are unchanged.
