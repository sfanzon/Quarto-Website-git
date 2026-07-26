const { test, expect } = require("@playwright/test");
const { criticalPages, monitorPage } = require("./site");

test.describe("cross-browser critical pages", () => {
  for (const urlPath of criticalPages) {
    test(urlPath, async ({ page, baseURL }) => {
      const diagnostics = monitorPage(page, baseURL);
      const response = await page.goto(urlPath, { waitUntil: "load" });
      await page.evaluate(() => document.fonts.ready);

      expect(response.status()).toBeLessThan(400);
      await expect(page.locator("main")).toBeVisible();
      expect(diagnostics.pageErrors).toEqual([]);
      expect(diagnostics.consoleErrors).toEqual([]);
      expect(diagnostics.resourceErrors).toEqual([]);
    });
  }

  test("mobile navigation expands", async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto("/index.html");

    const toggle = page.locator(".navbar-toggler");
    await toggle.click();
    await expect(toggle).toHaveAttribute("aria-expanded", "true");
    await expect(page.locator("#navbarCollapse")).toHaveClass(/\bshow\b/);
  });
});
