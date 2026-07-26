const fs = require("node:fs");
const path = require("node:path");

const repositoryRoot = path.resolve(__dirname, "../..");
const docsRoot = path.join(repositoryRoot, "docs");

const htmlPages = fs
  .globSync("**/*.html", { cwd: docsRoot })
  .sort()
  .map((relativePath) => ({
    relativePath,
    urlPath: `/${relativePath}`
  }));

const criticalPages = [
  "/index.html",
  "/publications.html",
  "/teaching.html",
  "/projects.html",
  "/news.html",
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
  docsRoot,
  htmlPages,
  monitorPage,
  repositoryRoot
};
