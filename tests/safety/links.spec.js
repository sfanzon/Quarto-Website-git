const fs = require("node:fs");
const path = require("node:path");
const { test, expect } = require("@playwright/test");
const { docsRoot, htmlPages } = require("./site");

const ignoredSchemes = /^(?:data:|mailto:|tel:|javascript:|blob:)/i;

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
  const target = path.join(docsRoot, relativePath);
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
      path.join(docsRoot, pageTarget.relativePath),
      "utf8"
    );
    for (const match of html.matchAll(attributePattern)) {
      const target = localTarget(match[1], pageTarget.relativePath);
      if (!target) continue;
      const file = targetFile(target.relativePath);
      if (!file) {
        missing.add(`${pageTarget.relativePath} -> ${match[1]}`);
      } else if (!fragmentExists(file, target.fragment)) {
        missing.add(
          `${pageTarget.relativePath} -> ${match[1]} (missing fragment)`
        );
      }
    }
  }

  for (const cssRelativePath of fs.globSync("**/*.css", { cwd: docsRoot })) {
    const css = fs.readFileSync(path.join(docsRoot, cssRelativePath), "utf8");
    for (const match of css.matchAll(cssUrlPattern)) {
      const target = localTarget(match[1], cssRelativePath);
      if (target && !targetFile(target.relativePath)) {
        missing.add(`${cssRelativePath} -> ${match[1]}`);
      }
    }
  }

  expect([...missing].sort(), "missing local HTML/CSS targets").toEqual([]);
});
