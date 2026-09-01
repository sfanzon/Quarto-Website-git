# DESIGN.md

# Silvio Fanzon website design system

Stable visual, editorial and positioning rules for `silviofanzon.com`.

For implementation ownership and build architecture, see `ARCHITECTURE.md`.

## 1. Design intent

The site should feel:

**editorial · mathematical · warm · modern · precise · personal · restrained**

It should not feel like:

**a university template · SaaS dashboard · generic portfolio · AI-startup site · generic data-science site**

The visual identity is a hard constraint.

## 2. Positioning

Core principle:

> **Applied mathematics as the foundation; applications as the evidence.**

The site should communicate deep mathematical, statistical and computational expertise applied to real problems.

Do not position Silvio primarily as a generic data scientist.

Relevant themes include:

- optimisation;
- inverse problems;
- statistics and forecasting;
- PDEs and variational methods;
- optimal transport;
- scientific computing;
- algorithm design;
- computational modelling;
- imaging;
- sports analytics.

Industry-facing material should make practical value clear without hiding the mathematics.

## 3. Audience

The audience is mixed:

- technical industry readers;
- recruiters and hiring managers;
- researchers and collaborators;
- students;
- scientific-computing practitioners;
- readers arriving through a project or publication.

Academic and industry material should feel like two views of one coherent professional identity.

## 4. Visual identity

Core language:

**warm neutrals + rust accents + charcoal typography + restrained surfaces + controlled whitespace**

Use colour for hierarchy, state and interaction rather than decoration.

Avoid unrelated brand colours and trend-driven effects.

### Current colour family

Global light-mode accents include approximately:

```css
--global-theme-color: #a8522f;
--global-hover-color: #824735;
--global-navbar-color: #1c1c1d;
--global-navbar-text-color: #e8e8e8;
--global-section-bg: #f6f1e9;
--global-warm-bg: #f7f2ee;
--global-warm-border: #e4d3c8;
--homepage-orange-accent: #9b4828;
```

Project pages use warm surfaces around:

```css
--project-canvas: #f8f3eb;
--project-surface: #fffdf9;
--project-ink-muted: #625b54;
--project-line: #dfd4c7;
--project-soft-accent: #efe0d6;
```

Dark mode should retain the same warm character, not become a cold inversion.

A restrained blue family may be used for secondary informational purposes, but rust/warm tones remain the primary identity.

## 5. Typography

Use compact editorial hierarchy rather than landing-page drama.

Priorities:

1. readability;
2. hierarchy;
3. mathematical legibility;
4. restraint.

The global typeface remains the native/system sans-serif stack unless explicitly reconsidered.

### Project H1

Keep broadly around:

```css
font-size: clamp(1.95rem, 3.15vw, 2.95rem);
```

Strong but compact; avoid oversized display titles.

### Subtitle

Keep visually lighter and moderately sized, approximately:

```css
font-size: clamp(1rem, 1.35vw, 1.14rem);
```

Prefer width/spacing over enlargement.

### H2

Project H2 headings should be slightly quieter than the current implementation and clearly subordinate to H1.

Use spacing, grouping and contrast before increasing type size.

### Body

Target roughly 15–16 px-equivalent body text, with 16 px preferred for sustained prose.

Never shrink body text merely to look minimalist.

## 6. Width system

The site uses three content widths, distinguished by content type rather than page name:

- **site shell: 1180 px (`--site-content-width`)** — the overall outer measure for every page, containing the header, footer and maximal content area.
- **general reading / mixed content: 820 px (`--site-reading-width`)** — for introductions, summaries, callouts, mixed text/visual content, supporting material, figures, code, tables and other technical/visual elements.
- **sustained prose: 720 px (`--site-prose-width`)** — for long-form article prose, technical narrative, explanatory sections, and other contexts where comfortable line length benefits sustained reading.

Figures, code, tables, diagrams and other technical/visual elements may use the 820 px reading width or wider where useful.

Do not widen prose because one visual component needs extra room.

## 7. Project-page opening

Preferred hierarchy:

```text
EYEBROW / CATEGORY

TITLE

SUBTITLE

AUTHOR                       PUBLISHED

RESOURCES
Paper · Journal · GitHub · Data

QUESTION          MODEL          FINDING

EXPLORE PROJECT
01 Overview   02 Technical   03 Code & data

ARTICLE
```

Not every project requires every component.

### Hero

The hero contains:

- category/eyebrow;
- title;
- subtitle;
- compact author/date metadata.

It should remain editorial and vertically compact.

### Resources

Paper, journal, GitHub, data and similar links belong in a **slim utility row immediately below the hero**.

Resources are not Author/Published metadata.

Avoid cards, long descriptions and dashboard styling.

### At a glance

Keep a lightweight summary of at most three items.

Labels may vary by project, for example:

- Question / Model / Finding;
- Problem / Algorithm / Behaviour;
- Problem / Approach / Beyond maths.

It should feel like an editorial abstract strip, not three dashboard cards.

### Explore Project

Overview / Technical Walkthrough / Code & Data are levels of engagement, distinct from external Resources.

The navigator may have more structure, but must remain secondary to the article.

## 8. Project views

### Overview

For industry, recruiters, collaborators and technical generalists.

Emphasise:

- problem;
- method;
- evidence;
- result;
- relevance;
- selected figures.

### Technical walkthrough

For researchers, technical readers, students and reproducibility.

May contain:

- mathematics;
- derivations;
- algorithms;
- implementation;
- code;
- detailed figures;
- citations.

### Code & Data

Focus on:

- implementation;
- inputs/outputs;
- tests;
- reproducibility;
- run/deployment instructions.

Where a standalone repository exists, it remains canonical for implementation and version history.

## 9. Project navigation

Long project pages may use a numbered section rail.

Desktop:

- left rail;
- visually secondary;
- clear current-section state.

Narrow screens:

- accessible icon-led drawer;
- positioned below the global navbar;
- global navbar always has higher stacking priority.

Do not let navigation unnecessarily reduce article width.

## 10. Continue exploring

Related projects mark the transition from reading to browsing.

They may be wider than the 720 px prose column.

Keep the section:

- quieter than the hero;
- clearly separated from article content;
- compact;
- limited to meaningful related work.

It should not feel like a second homepage.

## 11. Homepage

The homepage is:

> **identity + selected evidence**

It should quickly answer:

1. Who is this person?
2. What kinds of problems does he work on?
3. What evidence supports that?
4. Where should I go next?

It is not a complete CV, bibliography or project catalogue.

Surface selected:

- identity/expertise;
- projects;
- publications;
- news.

## 12. Page roles

### Expertise

Translate mathematical background into capabilities and problem-solving areas.

### Research

Show mathematical depth, theory, themes, collaborations and publications.

### Projects

Show inspectable applied evidence: modelling, algorithms, computation, reproducibility and communication.

### Publications

Own the complete academic record.

### Teaching

Show communication, course design and educational work.

## 13. Section headers

Major landing-page sections should share an editorial rhythm:

```text
EYEBROW

Main section title
──────────────────

Short description                         Action →
```

Keep this consistent without turning headers into cards.

## 14. Project cards

Cards should make the work interesting first.

Prefer:

- domain/eyebrow;
- title;
- concise explanation;
- meaningful visual;
- one primary action.

Avoid:

- badge/tag overload;
- technology-logo rows;
- multiple competing buttons;
- unnecessary metrics.

Homepage featured projects and the Projects page should use the same canonical data.

## 15. Navbar

Navigation should prioritise useful destinations over biography repetition.

The current architecture is the baseline.

The homepage already performs much of the identity function, so About may become less prominent or move under More during a deliberate navigation refinement.

Do not restructure navigation as a side effect of unrelated work.

## 16. Footer

Preferred authorship:

> **Designed & developed by Silvio Fanzon**

A source-code link is appropriate.

Do not promote the framework with “Built with Quarto” unless explicitly requested.

## 17. Components and surfaces

Cards are not the default container for ordinary content.

Use bounded surfaces for genuinely discrete objects such as:

- projects;
- comparisons;
- evidence blocks;
- navigation/resource objects.

Prefer subtle borders to heavy shadows.

Keep corner radii moderate.

## 18. Figures and technical content

Figures should be large enough to inspect and remain scientifically clear.

Use:

- consistent spacing;
- useful captions;
- meaningful alt text;
- wider breakouts when needed.

Edit generated scientific figures through their source pipeline whenever possible.

## 19. Motion

The page itself remains stable. Motion comes from meaningful elements arriving,
responding and reacting; it should reinforce hierarchy or interaction rather
than act as decoration.

The homepage may use restrained entrance and interaction animation. Major
showcase/project pages may use bespoke interaction selectively. Research, news
and technical reading pages should remain predominantly static.

Appropriate:

- hover feedback;
- drawer transitions;
- active navigation state;
- restrained, one-time homepage hero entrance.

Avoid:

- parallax;
- animated backgrounds, gradients, blobs or glows;
- scroll-jacking;
- cursor-reactive effects;
- generic repeated scroll-triggered reveal systems;
- gratuitous animation or movement that slows reading.

Respect `prefers-reduced-motion` for any motion that does exist.

## 20. Accessibility

Preserve:

- readable contrast;
- keyboard focus;
- semantic headings;
- usable touch targets;
- reduced-motion support;
- meaningful alt text;
- responsive typography;
- accessible menus/drawers.

Minimalism must not reduce usability.

## 21. Avoid

Do not drift toward:

- generic blue tech branding;
- AI-startup aesthetics;
- glassmorphism;
- neon accents;
- huge display typography;
- excessive gradients;
- excessive cards/pills;
- icon-heavy UI;
- dashboard metadata;
- generic academic or portfolio themes.

## 22. Decision rule

Before adding a component, ask:

> **Does this make the work easier to understand or navigate?**

If not, do not add it.

Prefer editorial clarity over decoration and hierarchy over enlargement.
