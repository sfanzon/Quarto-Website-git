# Repository instructions

- Run `quarto render` after changing site source, styles, scripts or configuration.
- Run `npm run test:quick` while iterating on small, focused changes.
- Run `npm test` before committing. It is the default midrange suite.
- Run `npm run test:full` before deployment and after broad structural changes or browser-specific fixes.
- Do not update visual baselines unless an intentional visual change has been reviewed.
- Treat `docs/` as generated output; edit source files and render instead.
