const { test, expect } = require("@playwright/test");
const manifest = require("./baseline-manifest.json");

const combinations = [];

for (const pageTarget of manifest.pages) {
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

test.describe("SCSS visual baseline", () => {
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

      await expect(page.locator("body")).toHaveClass(
        new RegExp(`(?:^|\\s)${theme.bodyClass}(?:\\s|$)`)
      );
      await expect(page).toHaveScreenshot(screenshotName, {
        fullPage: manifest.capture.fullPage
      });
    });
  }
});
