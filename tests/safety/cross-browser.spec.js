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
    await page.goto("/");

    const toggle = page.locator(".menu-toggle");
    await toggle.click();
    await expect(toggle).toHaveAttribute("aria-expanded", "true");
    await expect(page.locator("#navbar-links")).toHaveClass(/\bis-open\b/);
  });

  test("back navigation restores a deep project position", async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto("/projects/f1-time-rank-duality/index.html");
    await page.waitForFunction(
      () => document.documentElement.scrollHeight > window.innerHeight + 500
    );

    const before = await page.evaluate(() => {
      const maximum = document.documentElement.scrollHeight - window.innerHeight;
      const previousScrollBehavior = document.documentElement.style.scrollBehavior;
      document.documentElement.style.scrollBehavior = "auto";
      window.scrollTo({ top: Math.min(1400, maximum), behavior: "auto" });
      const position = window.scrollY;
      document.documentElement.style.scrollBehavior = previousScrollBehavior;
      return position;
    });
    expect(before).toBeGreaterThan(500);

    await page.goto("/");
    await page.goBack({ waitUntil: "load" });

    await expect
      .poll(async () => Math.abs(await page.evaluate(() => window.scrollY) - before))
      .toBeLessThanOrEqual(80);
  });

  test("history restoration survives a load-time scroll reset", async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto("/projects/f1-time-rank-duality/index.html");
    await page.waitForTimeout(120);

    const result = await page.evaluate(async () => {
      const position = { x: 0, y: 1800 };
      const key = `scroll-position:${window.location.pathname}${window.location.search}`;
      window.sessionStorage.setItem(key, JSON.stringify(position));

      const nativeScrollTo = window.scrollTo.bind(window);
      const calls = [];
      window.scrollTo = (...args) => {
        if (args.length === 1 && typeof args[0] === "object") {
          calls.push({ x: args[0].left, y: args[0].top });
        } else {
          calls.push({ x: args[0], y: args[1] });
        }
        nativeScrollTo(...args);
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
