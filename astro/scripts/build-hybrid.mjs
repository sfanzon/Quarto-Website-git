import { execFileSync } from 'node:child_process';
import { mkdtempSync, readFileSync, rmSync, mkdirSync, cpSync, existsSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, extname, join, relative, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const astroRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const repoRoot = resolve(astroRoot, '..');
const distRoot = join(astroRoot, 'dist');
const technicalRelative = 'projects/f1-time-rank-duality/technical.html';
const technicalSource = join(repoRoot, 'projects/f1-time-rank-duality/technical.qmd');
const stageRoot = mkdtempSync(join(tmpdir(), 'astro-hybrid-'));

function isLocalAsset(reference) {
  return reference && !reference.startsWith('#') && !reference.startsWith('http') &&
    !reference.startsWith('//') && !reference.startsWith('data:') &&
    !reference.startsWith('mailto:') && !reference.startsWith('javascript:') &&
    !reference.split(/[?#]/, 1)[0].endsWith('.html');
}

function copyAsset(reference, sourceBase, destinationBase, copied = new Set()) {
  const clean = reference.split(/[?#]/, 1)[0];
  if (!isLocalAsset(clean)) return;
  const source = resolve(sourceBase, clean);
  const destination = resolve(destinationBase, clean);
  if (!source.startsWith(stageRoot) || !existsSync(source) || copied.has(source)) return;
  copied.add(source);
  mkdirSync(dirname(destination), { recursive: true });
  cpSync(source, destination);
  if (extname(source).toLowerCase() === '.css') {
    const css = readFileSync(source, 'utf8');
    for (const match of css.matchAll(/url\(\s*["']?([^)'"\s]+)["']?\s*\)/g)) {
      copyAsset(match[1], dirname(source), dirname(destination), copied);
    }
  }
}

try {
  execFileSync('npm', ['run', 'build'], { cwd: astroRoot, stdio: 'inherit' });
  execFileSync('quarto', ['render', technicalSource, '--output-dir', stageRoot], { cwd: repoRoot, stdio: 'inherit' });

  const renderedSource = join(stageRoot, technicalRelative);
  const renderedDestination = join(distRoot, technicalRelative);
  mkdirSync(dirname(renderedDestination), { recursive: true });
  cpSync(renderedSource, renderedDestination);

  const html = readFileSync(renderedSource, 'utf8');
  const copied = new Set([renderedSource]);
  for (const match of html.matchAll(/(?:src|href)=["']([^"']+)["']/g)) {
    copyAsset(match[1], dirname(renderedSource), dirname(renderedDestination), copied);
  }

  execFileSync('npm', ['run', 'postbuild'], { cwd: astroRoot, stdio: 'inherit' });
  console.log(`Hybrid build complete: ${relative(astroRoot, renderedDestination)}`);
} finally {
  rmSync(stageRoot, { recursive: true, force: true });
}
