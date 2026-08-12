const { test, expect } = require("@playwright/test");
const AxeBuilder = require("@axe-core/playwright").default;
const { htmlPages } = require("./site");

test.describe("WCAG accessibility", () => {
  for (const colorScheme of ["light", "dark"]) {
    for (const pageTarget of htmlPages) {
      test(`${pageTarget.relativePath} (${colorScheme})`, async ({ page }) => {
        await page.addInitScript((scheme) => {
          window.localStorage.setItem("theme", scheme);
        }, colorScheme);
        await page.goto(pageTarget.urlPath, { waitUntil: "load" });
        await page.evaluate(() => document.fonts.ready);

        const results = await new AxeBuilder({ page })
          .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"])
          .analyze();

        const violations = results.violations.map((violation) => ({
          id: violation.id,
          impact: violation.impact,
          description: violation.description,
          targets: violation.nodes.map((node) => node.target.join(" "))
        }));

        expect(violations, "WCAG A/AA violations").toEqual([]);
      });
    }
  }
});
