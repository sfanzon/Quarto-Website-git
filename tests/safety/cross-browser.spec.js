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

  test("back navigation restores a deep publication position", async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto("/publications.html");

    const resource = page.locator('.publication-entry a[href*="/projects/"]').first();
    await resource.scrollIntoViewIfNeeded();
    await resource.evaluate((link) => link.removeAttribute("target"));
    const before = await page.evaluate(() => window.scrollY);
    expect(before).toBeGreaterThan(500);

    await Promise.all([
      page.waitForURL(/\/projects\//),
      resource.click()
    ]);
    await page.goBack({ waitUntil: "load" });

    await expect
      .poll(async () => Math.abs(await page.evaluate(() => window.scrollY) - before))
      .toBeLessThanOrEqual(80);
  });

  test("history restoration survives a load-time scroll reset", async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto("/publications.html");
    await page.waitForTimeout(120);

    const result = await page.evaluate(async () => {
      const position = { x: 0, y: 1800 };
      const key = `scroll-position:${window.location.pathname}${window.location.search}`;
      window.sessionStorage.setItem(key, JSON.stringify(position));

      const nativeScrollTo = window.scrollTo.bind(window);
      const calls = [];
      window.scrollTo = (x, y) => {
        calls.push({ x, y });
        nativeScrollTo(x, y);
      };

      window.setTimeout(() => window.scrollTo(0, 0), 40);
      const pageshow = new Event("pageshow");
      Object.defineProperty(pageshow, "persisted", { value: true });
      window.dispatchEvent(pageshow);
      await new Promise((resolve) => window.setTimeout(resolve, 140));
      window.scrollTo = nativeScrollTo;

      return { position, lastCall: calls.at(-1) };
    });

    expect(result.lastCall).toEqual(result.position);
  });
});
