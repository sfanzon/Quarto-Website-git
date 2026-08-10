import { execFileSync } from 'node:child_process';
import { mkdtempSync, readFileSync, writeFileSync, rmSync, mkdirSync, cpSync, existsSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, extname, join, relative, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const astroRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const repoRoot = resolve(astroRoot, '..');
const distRoot = join(astroRoot, 'dist');
const technicalRelative = 'projects/f1-time-rank-duality/technical.html';
const technicalSource = join(repoRoot, 'projects/f1-time-rank-duality/technical.qmd');
const stageRoot = mkdtempSync(join(tmpdir(), 'astro-hybrid-'));

const hybridShellScript = `<script type="module">
const root = document.documentElement;
const themeButton = document.querySelector('.theme-toggle');
const menuButton = document.querySelector('.menu-toggle');
const navLinks = document.querySelector('#navbar-links');
const setThemeLabel = () => {
  const dark = root.dataset.theme === 'dark';
  themeButton?.setAttribute('aria-label', dark ? 'Switch to light mode' : 'Switch to dark mode');
};
const syncAstroTheme = () => {
  const dark = document.body.classList.contains('quarto-dark');
  root.dataset.theme = dark ? 'dark' : 'light';
  root.style.colorScheme = dark ? 'dark' : 'light';
  localStorage.setItem('theme', dark ? 'dark' : 'light');
  setThemeLabel();
};
themeButton?.addEventListener('click', () => {
  if (typeof window.quartoToggleColorScheme === 'function') {
    window.quartoToggleColorScheme();
    syncAstroTheme();
  } else {
    const theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
    root.dataset.theme = theme;
    root.style.colorScheme = theme;
    localStorage.setItem('theme', theme);
    setThemeLabel();
  }
});
menuButton?.addEventListener('click', () => {
  const open = menuButton.getAttribute('aria-expanded') !== 'true';
  menuButton.setAttribute('aria-expanded', String(open));
  menuButton.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
  navLinks?.classList.toggle('is-open', open);
});
if (typeof window.quartoToggleColorScheme === 'function') {
  const requested = localStorage.getItem('theme');
  const currentDark = document.body.classList.contains('quarto-dark');
  if ((requested === 'dark') !== currentDark && (requested === 'dark' || requested === 'light')) {
    window.quartoToggleColorScheme();
  }
  syncAstroTheme();
} else {
  setThemeLabel();
}
</script>`;

function applyAstroShell(quartoHtml) {
  const astroHtml = readFileSync(join(distRoot, 'index.html'), 'utf8');
  const header = astroHtml.match(/<header class="site-header">[\s\S]*?<\/header>/)?.[0];
  const footer = astroHtml.match(/<footer class="site-footer"[\s\S]*?<\/footer>/)?.[0];
  if (!header || !footer) throw new Error('Unable to extract Astro site chrome from the built homepage');

  const globalCss = readFileSync(join(astroRoot, 'src/styles/global.css'), 'utf8');
  const editorialMarker = globalCss.indexOf('/* Shared editorial page primitives */');
  const footerMarker = globalCss.indexOf('/* Footer */');
  const responsiveMarker = globalCss.indexOf('@media (max-width: 991.98px)');
  const shellCss = [
    globalCss.slice(0, editorialMarker),
    globalCss.slice(footerMarker, responsiveMarker),
    globalCss.slice(responsiveMarker)
  ].join('\n');
  const shellOverrides = `
#quarto-header { display: none !important; }
body > #quarto-content { padding-top: 0 !important; }
`;

  return quartoHtml
    .replace(/<div id="quarto-search-results"><\/div>\s*/, '')
    .replace(/<header id="quarto-header"[\s\S]*?<\/header>\s*/, '')
    .replace('</head>', `<style id="astro-site-shell">${shellCss}</style><style id="astro-hybrid-shell-overrides">${shellOverrides}</style></head>`)
    .replace(/<body([^>]*)>/, `<body$1>${header}`)
    .replace('</body>', `${hybridShellScript}</body>`)
    .replace(/<footer class="site-footer"[\s\S]*?<\/footer>/, footer);
}

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

  const html = applyAstroShell(readFileSync(renderedSource, 'utf8'));
  writeFileSync(renderedDestination, html);
  const copied = new Set([renderedSource]);
  for (const match of html.matchAll(/(?:src|href)=["']([^"']+)["']/g)) {
    copyAsset(match[1], dirname(renderedSource), dirname(renderedDestination), copied);
  }

  execFileSync('npm', ['run', 'postbuild'], { cwd: astroRoot, stdio: 'inherit' });
  console.log(`Hybrid build complete: ${relative(astroRoot, renderedDestination)}`);
} finally {
  rmSync(stageRoot, { recursive: true, force: true });
}
