#!/usr/bin/env node

/**
 * generated-output-guard.mjs
 *
 * Cheap guardrail: fail if generated output changed but no canonical
 * source file was also modified.
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

import { execFileSync } from "child_process";
import { fileURLToPath } from "url";
import { resolve } from "path";

const GENERATED_PATHS = new Set([
  "data/projects.generated.json",
  "includes/home-news.qmd",
  "includes/home-notes.html",
  "includes/home-projects.html",
  "includes/presentations.html",
  "includes/supervision.html",
  "includes/home-publications-list.html",
  "includes/news-all.qmd",
  "includes/news-all.html",
  "includes/projects-portfolio.html",
  "includes/publications-all.html",
  "includes/teaching-list.html",
]);

/**
 * Pure check. Returns { passed: boolean, message: string }.
 *
 * @param {string[]} files – list of changed file paths
 */
export function checkGuard(files) {
  const hasGenerated = files.some(
    (f) => f.startsWith("docs/") || GENERATED_PATHS.has(f)
  );
  const hasSource = files.some(
    (f) => !f.startsWith("docs/") && !GENERATED_PATHS.has(f)
  );

  if (hasGenerated && !hasSource) {
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

export function getChangedFiles({
  baseRef = process.env.BASE_REF || "HEAD",
  testPaths = process.env.GUARD_TEST_PATHS,
  cwd = process.cwd(),
} = {}) {
  if (testPaths) {
    return testPaths.split(/\s+/).filter(Boolean);
  }

  const changed = execFileSync("git", ["diff", "--name-only", baseRef], {
    encoding: "utf-8",
    cwd,
  });
  const untracked = execFileSync(
    "git",
    ["ls-files", "--others", "--exclude-standard"],
    { encoding: "utf-8", cwd }
  );

  return [
    ...new Set(
      `${changed}\n${untracked}`
        .split("\n")
        .map((file) => file.trim())
        .filter(Boolean)
    ),
  ];
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

if (
  process.argv[1] &&
  fileURLToPath(import.meta.url) === resolve(process.argv[1])
) {
  main();
}
