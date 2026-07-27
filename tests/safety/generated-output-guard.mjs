#!/usr/bin/env node

/**
 * generated-output-guard.mjs
 *
 * Cheap guardrail: fail if files under docs/ changed but no canonical
 * source file outside docs/ was also modified.
 *
 * Usage:
 *   node tests/safety/generated-output-guard.mjs
 *
 * Environment:
 *   BASE_REF         – git ref to compare against (e.g. origin/main)
 *                      Defaults to HEAD when unset.
 *   GUARD_TEST_PATHS – inject a space-separated file list for testing
 *                      (skips git entirely).
 */

import { execSync } from "child_process";

/**
 * Paths outside docs/ that are generated output, not canonical source.
 * See SOURCE_MAP.md for the full distinction.
 */
const GENERATED_OUTSIDE_DOCS = new Set([
  "data/projects.generated.json",
  "includes/home-news.qmd",
  "includes/home-projects.html",
  "includes/home-publications-list.html",
  "includes/news-all.qmd",
  "includes/projects-portfolio.html",
  "includes/publications-all.html",
  "includes/teaching-list.html",
]);

const GENERATED_PATHS = new Set([
  "data/projects.generated.json",
  "includes/home-news.qmd",
  "includes/home-projects.html",
  "includes/home-publications-list.html",
  "includes/news-all.qmd",
  "includes/projects-portfolio.html",
  "includes/publications-all.html",
  "includes/teaching-list.html",
]);

function isCanonicalSource(path) {
  if (path.startsWith("docs/")) return false;
  if (GENERATED_OUTSIDE_DOCS.has(path)) return false;
  return true;
}

/**
 * Pure check. Returns { passed: boolean, message: string }.
 *
 * @param {string[]} files – list of changed file paths
 */
export function checkGuard(files) {
  const hasDocs = files.some((f) => f.startsWith("docs/"));
  const hasSource = files.some(
    (f) => !f.startsWith("docs/") && !GENERATED_PATHS.has(f)
  );

  if (hasDocs && !hasSource) {
    return {
      passed: false,
      message: [
        "FAIL: only generated output (docs/ or generated includes/data) was changed.",
        "",
        "A commit that touches generated output must also modify at least one",
        "canonical source file. Direct edits to generated files will be lost",
        "on the next quarto render.",
        "",
      ].join("\n"),
    };
  }

  return { passed: true, message: "PASS" };
}

function getChangedFiles() {
  const testPaths = process.env.GUARD_TEST_PATHS;
  if (testPaths) {
    return testPaths.split(/\s+/).filter(Boolean);
  }

  const baseRef = process.env.BASE_REF || "HEAD";
  const stdout = execSync(`git diff --name-only "${baseRef}"`, {
    encoding: "utf-8",
  });
  return stdout.split("\n").filter(Boolean);
}

function main() {
  const files = getChangedFiles();
  const result = checkGuard(files);

  if (files.length > 0) {
    console.log("Changed files:\n");
    for (const f of files) {
      console.log(`  ${f}`);
    }
    console.log();
  }

  console.log(result.message);

  if (!result.passed) {
    process.exit(1);
  }
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}

