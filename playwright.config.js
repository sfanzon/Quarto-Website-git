const { defineConfig } = require("@playwright/test");

module.exports = defineConfig({
  testDir: "./tests/visual",
  testMatch: "capture.spec.js",
  fullyParallel: false,
  workers: 1,
  timeout: 45_000,
  expect: {
    timeout: 10_000,
    toHaveScreenshot: {
      animations: "disabled",
      caret: "hide",
      maxDiffPixelRatio: 0.001,
      pathTemplate: "{testDir}/baselines/{arg}{ext}"
    }
  },
  reporter: [["list"], ["html", { open: "never" }]],
  use: {
    baseURL: "http://127.0.0.1:4321",
    browserName: "chromium",
    reducedMotion: "reduce",
    screenshot: "only-on-failure",
    trace: "retain-on-failure"
  },
  webServer: {
    command: "python3 -m http.server 4321 --bind 127.0.0.1 --directory docs",
    url: "http://127.0.0.1:4321/index.html",
    reuseExistingServer: true,
    timeout: 30_000
  }
});
