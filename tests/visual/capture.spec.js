const { test, expect } = require("@playwright/test");
const manifest = require("./baseline-manifest.json");

const combinations = [];
const pageTargets = manifest.pages;

for (const pageTarget of pageTargets) {
  for (const [themeName, theme] of Object.entries(manifest.themes)) {
    for (const [viewportName, viewport] of Object.entries(manifest.viewports)) {
      combinations.push({
        pageTarget,
        themeName,
        theme,
        viewportName,
        viewport
      });
    }
  }
}

test.describe("hybrid visual baseline", () => {
  test.skip(
    ({ browserName }) => browserName !== "chromium",
    "Pixel baselines are intentionally Chromium-specific."
  );

  for (const combination of combinations) {
    const {
      pageTarget,
      themeName,
      theme,
      viewportName,
      viewport
    } = combination;
    const screenshotName =
      `${pageTarget.name}--${themeName}--${viewportName}.png`;

    test(screenshotName, async ({ page }) => {
      await page.setViewportSize(viewport);
      await page.emulateMedia({
        colorScheme: themeName,
        reducedMotion: manifest.capture.reducedMotion
      });
      await page.addInitScript(({ storageKey, storageValue }) => {
        window.localStorage.setItem(storageKey, storageValue);
      }, theme);

      await page.goto(pageTarget.path, { waitUntil: "domcontentloaded" });
      await page.evaluate(() => document.fonts.ready);
      await page.addStyleTag({
        content: `
          *,
          *::before,
          *::after {
            animation-delay: 0s !important;
            animation-duration: 0s !important;
            transition-delay: 0s !important;
            transition-duration: 0s !important;
            caret-color: transparent !important;
          }

          html {
            scroll-behavior: auto !important;
          }
        `
      });
      await page.waitForTimeout(manifest.capture.settleMilliseconds);

      await expect(page.locator("html")).toHaveAttribute("data-theme", theme.rootTheme);
      await expect(page).toHaveScreenshot(screenshotName, {
        fullPage: manifest.capture.fullPage
      });
    });
  }
});
