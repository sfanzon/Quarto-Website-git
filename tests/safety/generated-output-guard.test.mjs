import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import test from "node:test";

import { checkGuard, getChangedFiles } from "./generated-output-guard.mjs";

const guardPath = resolve("tests/safety/generated-output-guard.mjs");

test("rejects docs-only changes", () => {
  assert.equal(checkGuard(["docs/index.html"]).passed, false);
});

test("rejects generated include-only changes", () => {
  assert.equal(checkGuard(["includes/home-news.qmd"]).passed, false);
});

test("accepts generated output accompanied by canonical source", () => {
  assert.equal(
    checkGuard(["docs/index.html", "index.qmd"]).passed,
    true
  );
});

test("the CLI runs when invoked with a relative path", () => {
  const result = spawnSync(
    process.execPath,
    ["tests/safety/generated-output-guard.mjs"],
    {
      cwd: resolve("."),
      env: { ...process.env, GUARD_TEST_PATHS: "docs/index.html" },
      encoding: "utf-8",
    }
  );

  assert.equal(result.status, 1);
  assert.match(result.stdout, /FAIL: only generated output/);
});

test("the CLI runs when invoked with an absolute path", () => {
  const result = spawnSync(process.execPath, [guardPath], {
    env: { ...process.env, GUARD_TEST_PATHS: "includes/news-all.qmd" },
    encoding: "utf-8",
  });

  assert.equal(result.status, 1);
  assert.match(result.stdout, /FAIL: only generated output/);
});

test("changed-file discovery includes untracked files", (context) => {
  const repository = mkdtempSync(join(tmpdir(), "generated-guard-"));
  context.after(() => rmSync(repository, { recursive: true, force: true }));
  const git = (...args) => {
    const result = spawnSync("git", args, {
      cwd: repository,
      encoding: "utf-8",
    });
    assert.equal(result.status, 0, result.stderr);
  };

  git("init", "--quiet");
  writeFileSync(join(repository, "tracked.txt"), "tracked\n");
  git("add", "tracked.txt");
  git(
    "-c",
    "user.name=Guard Test",
    "-c",
    "user.email=guard@example.invalid",
    "commit",
    "--quiet",
    "-m",
    "fixture"
  );
  writeFileSync(join(repository, "untracked.txt"), "untracked\n");

  assert.deepEqual(getChangedFiles({ cwd: repository }), ["untracked.txt"]);
});
