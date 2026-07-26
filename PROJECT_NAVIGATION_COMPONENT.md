# Reusable project navigation

The navigation is isolated in two files:

- `styles/project-navigation.css`
- `includes/project-navigation.html`

It activates only on pages whose `body-classes` include
`project-detail-page`. The component builds its entries from level-two
headings and keeps section numbering synchronized between the article and the
navigation.

## Default project-page mode

Desktop uses a permanent left rail positioned around one quarter of the
viewport from the top. Below 1200px, the rail collapses to an icon-only floating tab a few pixels beneath the measured bottom of the site navbar. The tab opens a drawer and does not reserve a
permanent bar below Quarto's navbar.

## Lecture-note mode

The original full-width secondary bar is still available. Add
`project-nav-secondary-bar` to the page's `body-classes`:

```yaml
body-classes: project-detail-page project-nav-secondary-bar
```

This is a good option for long lecture notes because the current section stays
visible beneath the main navbar on narrower screens.

## Heading controls

Use a normal level-two heading for an automatically numbered navigation entry:

```markdown
## Linear regression
```

Use a shorter navigation label without changing the visible heading:

```markdown
## Estimation and uncertainty {data-nav-title="Estimation"}
```

Keep a heading in the navigation but remove its section number:

```markdown
## References {.unnumbered}
```

Exclude a heading completely:

```markdown
## Appendix {data-nav-exclude}
```

To reuse the component in another Quarto project, copy the two component files
and retain their entries under `css` and `include-after-body` in `_quarto.yml`.


## Collapsed-navbar interaction

The component observes the Quarto navbar and its collapsible menu. When the
main mobile navbar opens, the chapter-navigation tab and drawer are pushed
below its actual expanded height. The tab has a lower stacking level than the
main navbar, so it cannot cover the navbar menu.
