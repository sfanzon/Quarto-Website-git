const fs = require("node:fs");
const path = require("node:path");
const { test, expect } = require("@playwright/test");
const { htmlPages, repositoryRoot, siteRoot } = require("./site");

const ignoredSchemes = /^(?:data:|mailto:|tel:|javascript:|blob:)/i;
const optionalLocalAssets = new Set(
  fs.readFileSync(
    path.join(repositoryRoot, "data/optional-local-assets.txt"),
    "utf8"
  )
    .split("\n")
    .map((line) => line.trim())
    .filter((line) => line && !line.startsWith("#"))
);

function localTarget(reference, sourceRelativePath) {
  const trimmed = reference.trim();
  if (
    !trimmed ||
    trimmed.startsWith("//") ||
    ignoredSchemes.test(trimmed)
  ) {
    return null;
  }

  const resolved = new URL(
    trimmed,
    `https://local.test/${sourceRelativePath}`
  );
  if (resolved.origin !== "https://local.test") return null;

  let pathname = decodeURIComponent(resolved.pathname);
  if (pathname.endsWith("/")) pathname += "index.html";
  return {
    relativePath: pathname.replace(/^\/+/, ""),
    fragment: decodeURIComponent(resolved.hash.slice(1))
  };
}

function targetFile(relativePath) {
  const target = path.join(siteRoot, relativePath);
  if (fs.existsSync(target) && fs.statSync(target).isFile()) return target;
  const indexTarget = path.join(target, "index.html");
  return fs.existsSync(indexTarget) ? indexTarget : null;
}

function fragmentExists(file, fragment) {
  if (!fragment || path.extname(file).toLowerCase() !== ".html") return true;
  const html = fs.readFileSync(file, "utf8");
  const anchors = new Set(
    [...html.matchAll(/\b(?:id|name)=["']([^"']+)["']/gi)].map(
      (match) => match[1]
    )
  );
  return anchors.has(fragment);
}

test("all generated HTML and CSS references resolve locally", async () => {
  const missing = new Set();
  const attributePattern = /\b(?:href|src|poster)=["']([^"']+)["']/gi;
  const cssUrlPattern = /url\(\s*["']?([^"')]+)["']?\s*\)/gi;

  for (const pageTarget of htmlPages) {
    const html = fs.readFileSync(
      path.join(siteRoot, pageTarget.relativePath),
      "utf8"
    );
    for (const match of html.matchAll(attributePattern)) {
      const target = localTarget(match[1], pageTarget.relativePath);
      if (!target) continue;
      const file = targetFile(target.relativePath);
      if (!file && !optionalLocalAssets.has(target.relativePath)) {
        missing.add(`${pageTarget.relativePath} -> ${match[1]}`);
      } else if (!fragmentExists(file, target.fragment)) {
        missing.add(
          `${pageTarget.relativePath} -> ${match[1]} (missing fragment)`
        );
      }
    }
  }

  for (const cssRelativePath of fs.globSync("**/*.css", { cwd: siteRoot })) {
    const css = fs.readFileSync(path.join(siteRoot, cssRelativePath), "utf8");
    for (const match of css.matchAll(cssUrlPattern)) {
      const target = localTarget(match[1], cssRelativePath);
      if (target && !targetFile(target.relativePath)) {
        missing.add(`${cssRelativePath} -> ${match[1]}`);
      }
    }
  }

  expect([...missing].sort(), "missing local HTML/CSS targets").toEqual([]);
});

test("Notes canonical routes and compatibility alias are published correctly", async () => {
  const sitemap = fs.readFileSync(path.join(siteRoot, "sitemap.xml"), "utf8");
  for (const route of [
    "/notes/",
    "/notes/ai-agents-practical-stack-2026-qwen9-128k-copilot-opencode-no-gemini-free.html",
    "/notes/ai-real-project-lessons.html",
    "/notes/how-i-use-ai.html",
    "/notes/portable-ai-rules-workflow.html"
  ]) {
    expect(sitemap).toContain(`https://www.silviofanzon.com${route}`);
  }
  expect(sitemap).not.toContain("https://www.silviofanzon.com/notes.html");

  const alias = fs.readFileSync(path.join(siteRoot, "notes.html"), "utf8");
  expect(alias).toContain('<meta name="robots" content="noindex">');
  expect(alias).toMatch(/<body[^>]*data-pagefind-ignore="all"/);

  const listings = JSON.parse(fs.readFileSync(path.join(siteRoot, "listings.json"), "utf8"));
  expect(listings).toEqual([]);
});

test("retired component classes remain absent from the rendered site", async () => {
  const retiredClasses = [
    "publication-side-meta",
    "publication-themes-mobile",
    "project-closing-actions",
    "project-demonstrates",
    "project-output-grid",
    "project-resource-actions",
    "project-resource-publication",
    "project-summary-band"
  ];
  const renderedFiles = [
    ...htmlPages.map((page) => page.relativePath),
    ...fs.globSync("**/*.css", { cwd: siteRoot })
  ];
  const rendered = renderedFiles
    .map((relativePath) => fs.readFileSync(path.join(siteRoot, relativePath), "utf8"))
    .join("\n");

  for (const className of retiredClasses) {
    expect(rendered, `retired class still rendered: ${className}`)
      .not.toContain(className);
  }
});

test("source markup keeps presentation styles in reusable classes", async () => {
  const sourceMarkupFiles = [
    ...fs.globSync("**/*.qmd", { cwd: repositoryRoot }),
    ...fs.globSync("**/*.html", { cwd: repositoryRoot })
  ].filter(
    (relativePath) =>
      !relativePath.startsWith("docs/") &&
      !relativePath.startsWith("astro/dist/") &&
      !relativePath.startsWith("node_modules/") &&
      !relativePath.startsWith("playwright-report/") &&
      !relativePath.startsWith("test-results/")
  );
  const inlineStyleFiles = sourceMarkupFiles.filter((relativePath) =>
    /\bstyle\s*=/i.test(
      fs.readFileSync(path.join(repositoryRoot, relativePath), "utf8")
    )
  );

  expect(inlineStyleFiles, "source markup should not use inline styles").toEqual([]);
});
