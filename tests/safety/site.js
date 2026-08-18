const fs = require("node:fs");
const path = require("node:path");

const repositoryRoot = path.resolve(__dirname, "../..");
const siteRoot = path.join(repositoryRoot, "astro", "dist");

const htmlPages = fs
  .globSync("**/*.html", { cwd: siteRoot })
  .sort()
  .map((relativePath) => ({
    relativePath,
    urlPath: `/${relativePath}`
  }));

const criticalPages = [
  "/",
  "/about/",
  "/projects/",
  "/publications/",
  "/teaching/",
  "/news/",
  "/contact/",
  "/presentations/",
  "/supervision/",
  "/cv/",
  "/notes/",
  "/notes/how-i-use-ai.html",
  "/projects/f1-time-rank-duality/index.html"
];

function monitorPage(page, baseURL) {
  const origin = new URL(baseURL).origin;
  const consoleErrors = [];
  const pageErrors = [];
  const resourceErrors = [];

  page.on("console", (message) => {
    if (message.type() === "error") consoleErrors.push(message.text());
  });
  page.on("pageerror", (error) => pageErrors.push(error.message));
  page.on("requestfailed", (request) => {
    const url = new URL(request.url());
    if (url.origin === origin) {
      resourceErrors.push(
        `${request.failure()?.errorText || "request failed"} ${url.pathname}`
      );
    }
  });
  page.on("response", (response) => {
    const url = new URL(response.url());
    if (url.origin === origin && response.status() >= 400) {
      resourceErrors.push(`${response.status()} ${url.pathname}`);
    }
  });

  return { consoleErrors, pageErrors, resourceErrors };
}

module.exports = {
  criticalPages,
  htmlPages,
  monitorPage,
  repositoryRoot,
  siteRoot
};
