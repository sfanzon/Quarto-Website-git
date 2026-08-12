const { defineConfig } = require("@playwright/test");
const path = require("node:path");

const visualSiteRoot = process.env.VISUAL_SITE_ROOT;
const siteDirectory = visualSiteRoot
  ? path.resolve(visualSiteRoot, "docs")
  : path.resolve(__dirname, "astro", "dist");
const visualBaselinesDirectory = process.env.VISUAL_BASELINES_DIR;
const visualSnapshotPath = visualBaselinesDirectory
  ? path.resolve(visualBaselinesDirectory, "{arg}{ext}")
  : "{testDir}/visual/baselines/{arg}{ext}";

module.exports = defineConfig({
  testDir: "./tests",
  testMatch: "**/*.spec.js",
  fullyParallel: false,
  workers: 1,
  timeout: 45_000,
  expect: {
    timeout: 10_000,
    toHaveScreenshot: {
      animations: "disabled",
      caret: "hide",
      maxDiffPixelRatio: 0.001,
      pathTemplate: visualSnapshotPath
    }
  },
  reporter: [["list"], ["html", { open: "never" }]],
  use: {
    baseURL: "http://127.0.0.1:4321",
    reducedMotion: "reduce",
    screenshot: "only-on-failure",
    trace: "retain-on-failure"
  },
  projects: [
    {
      name: "chromium",
      use: { browserName: "chromium" }
    },
    {
      name: "firefox",
      testMatch: "**/safety/cross-browser.spec.js",
      use: { browserName: "firefox" }
    },
    {
      name: "webkit",
      testMatch: "**/safety/cross-browser.spec.js",
      use: { browserName: "webkit" }
    }
  ],
  webServer: {
    command: "python3 -m http.server 4321 --bind 127.0.0.1",
    cwd: siteDirectory,
    url: "http://127.0.0.1:4321/index.html",
    reuseExistingServer: !process.env.CI,
    timeout: 30_000
  }
});
