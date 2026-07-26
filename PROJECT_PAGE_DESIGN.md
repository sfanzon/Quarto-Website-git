# Project-page design system

This refinement replaces Quarto's generic margin table of contents with a project-specific editorial system.

## Structure

1. **Compact hero** — smaller title, short lead and project category line.
2. **Resource map** — explicitly separates the project overview, technical walkthrough, source repository and publication links.
3. **Evidence strip** — publication, data, result and delivery at a glance.
4. **Chapter rail** — a quiet desktop-only section list with a subtle active-section marker.
5. **Analysis pipeline** — a non-interactive process diagram. It is visually distinct from navigation and labelled in the prose.

## Reuse

- Shared styles: `styles/project-pages.css`
- Chapter behaviour: `includes/after-body.html`
- Shared project defaults: `projects/_metadata.yml`
- Project-page chapter links are generated automatically from level-two headings. No page-local navigation markup is required.

Project pages use a warm canvas in light mode and a coordinated warm-dark canvas in dark mode. The ordinary website navbar and footer remain unchanged.
