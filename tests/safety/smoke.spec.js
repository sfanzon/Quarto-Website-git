const { test, expect } = require("@playwright/test");
const { htmlPages, monitorPage } = require("./site");

test.describe("all-page runtime health", () => {
  for (const pageTarget of htmlPages) {
    test(pageTarget.relativePath, async ({ page, baseURL }) => {
      const diagnostics = monitorPage(page, baseURL);
      const response = await page.goto(pageTarget.urlPath, {
        waitUntil: "load"
      });

      await page.evaluate(() => document.fonts.ready);
      await page.waitForTimeout(100);

      expect(response, "navigation should return a response").not.toBeNull();
      expect(response.status(), "page response status").toBeLessThan(400);
      await expect(page.locator("html")).toHaveAttribute("lang", /.+/);
      await expect(page.locator("body")).toBeVisible();
      await expect(page.locator("main")).toHaveCount(1);
      expect((await page.title()).trim(), "document title").not.toBe("");

    const duplicateIds = await page.locator("body [id]").evaluateAll((elements) => {
        const counts = new Map();
        for (const element of elements) {
          counts.set(element.id, (counts.get(element.id) || 0) + 1);
        }
        return [...counts.entries()]
          .filter(([, count]) => count > 1)
          .map(([id, count]) => `${id} (${count})`);
      });
      const brokenImages = await page.locator("img").evaluateAll((images) =>
        images
          .filter((image) => image.complete && image.naturalWidth === 0)
          .map((image) => image.currentSrc || image.src)
      );

      expect(duplicateIds, "duplicate element IDs").toEqual([]);
      expect(brokenImages, "images that completed without loading").toEqual([]);
      expect(diagnostics.pageErrors, "uncaught page exceptions").toEqual([]);
      expect(diagnostics.consoleErrors, "browser console errors").toEqual([]);
      expect(diagnostics.resourceErrors, "failed same-origin resources").toEqual(
        []
      );
    });
  }
});
