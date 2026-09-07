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

const canonicalProjectDocumentPaths = [
  "/projects/f1-time-rank-duality/index.html",
  "/projects/f1-time-rank-duality/technical.html",
  "/projects/f1-time-rank-duality/code.html",
  "/projects/sparse-gcg/index.html"
];

const canonicalNoteArticlePaths = [
  "/notes/ai-agents-practical-stack-2026-qwen9-128k-copilot-opencode-no-gemini-free.html",
  "/notes/ai-real-project-lessons.html",
  "/notes/how-i-use-ai.html",
  "/notes/portable-ai-rules-workflow.html",
  "/notes/advanced-functional-analysis-2019-20.html",
  "/notes/calculus-of-variations-2020-21.html",
  "/notes/analysis-3-2022-23.html",
  "/notes/inverse-problems-2022-23.html",
  "/notes/numbers-sequences-and-series-2023-24.html",
  "/notes/differential-geometry-2023-24.html",
  "/notes/differential-geometry-2024-25.html",
  "/notes/numbers-sequences-and-series-2024-25.html",
  "/notes/statistical-models-2023-24.html",
  "/notes/statistical-models-2024-25.html",
  "/notes/graduate-skills-2025-26.html",
  "/notes/statistical-models-2025-26.html"
];

const canonicalMergedDocumentPaths = [
  ...canonicalProjectDocumentPaths,
  ...canonicalNoteArticlePaths
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
  canonicalMergedDocumentPaths,
  htmlPages,
  monitorPage,
  repositoryRoot,
  siteRoot
};
