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
 * Pure check. Returns { passed: boolean, message: string }.
 *
 * @param {string[]} files – list of changed file paths
 */
export function checkGuard(files) {
  const hasDocs = files.some((f) => f.startsWith("docs/"));
  const hasSource = files.some((f) => !f.startsWith("docs/"));

  if (hasDocs && !hasSource) {
    return {
      passed: false,
      message: [
        "FAIL: only generated docs/ output was changed.",
        "",
        "A commit that touches files under docs/ must also modify at least one",
        "canonical source file outside docs/. Direct edits to generated output",
        "will be lost on the next quarto render.",
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