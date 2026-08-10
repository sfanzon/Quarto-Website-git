import { execFileSync } from 'node:child_process';
import { cpSync, existsSync, mkdirSync, mkdtempSync, readFileSync, readdirSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, extname, join, relative, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const astroRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const repoRoot = resolve(astroRoot, '..');
const projectsRoot = join(repoRoot, 'projects');
const distRoot = join(astroRoot, 'dist');
const stageRoot = mkdtempSync(join(tmpdir(), 'astro-quarto-projects-'));
const shellRoot = join(distRoot, 'site-shell');
const siteUrl = 'https://www.silviofanzon.com';

function findProjectSources(directory) {
	return readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
		const path = join(directory, entry.name);
		if (entry.isDirectory()) return findProjectSources(path);
		return entry.isFile() && entry.name.endsWith('.qmd') ? [path] : [];
	});
}

function outputPath(source) {
	return relative(repoRoot, source).replace(/\.qmd$/, '.html');
}

function findHtmlFiles(directory) {
	return readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
		const path = join(directory, entry.name);
		if (entry.isDirectory()) return findHtmlFiles(path);
		return entry.isFile() && entry.name.endsWith('.html') ? [path] : [];
	});
}

function sitemapUrl(path) {
	const output = relative(distRoot, path).replaceAll('\\', '/');
	if (output === 'index.html') return `${siteUrl}/`;
	if (output.startsWith('projects/') && output.endsWith('/index.html')) return `${siteUrl}/${output}`;
	if (output.endsWith('/index.html')) return `${siteUrl}/${output.slice(0, -'index.html'.length)}`;
	return `${siteUrl}/${output}`;
}

function writeSitemap() {
	const urls = findHtmlFiles(distRoot)
		.filter((path) => relative(distRoot, path) !== '404.html')
		.map(sitemapUrl)
		.sort();
	const entries = urls.map((url) => `  <url><loc>${url}</loc></url>`).join('\n');
	writeFileSync(join(distRoot, 'sitemap.xml'), `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${entries}\n</urlset>\n`);
}

function requireShellArtifact(name) {
	const path = join(shellRoot, name);
	if (!existsSync(path)) throw new Error(`Astro did not emit required shell artifact: ${relative(astroRoot, path)}`);
	return readFileSync(path, 'utf8');
}

function replaceOnce(html, pattern, replacement, description) {
	let matches = 0;
	const replaced = html.replace(pattern, (...args) => {
		matches += 1;
		return typeof replacement === 'function' ? replacement(...args) : replacement;
	});
	if (matches !== 1) throw new Error(`Expected exactly one ${description}; found ${matches}`);
	return replaced;
}

function applySharedShell(quartoHtml, header, footer) {
	let html = replaceOnce(quartoHtml, /<header id="quarto-header"[\s\S]*?<\/header>\s*/, '', 'Quarto header');
	html = replaceOnce(html, /<footer class="site-footer"[\s\S]*?<\/footer>/, footer, 'Quarto footer');
	html = replaceOnce(html, /<body([^>]*)>/, (_match, attributes) => `<body${attributes}>${header}`, 'body opening tag');
	html = replaceOnce(html, /<\/head>/, '<link rel="stylesheet" href="/site-shell/site.css"></head>', 'head closing tag');
	return html.replace(/<div id="quarto-search-results"><\/div>\s*/, '');
}

function isLocalAsset(reference) {
	return reference && !reference.startsWith('#') && !reference.startsWith('/') && !reference.startsWith('http') &&
		!reference.startsWith('//') && !reference.startsWith('data:') && !reference.startsWith('mailto:') &&
		!reference.startsWith('javascript:') && !reference.split(/[?#]/, 1)[0].endsWith('.html');
}

function copyAsset(reference, sourceBase, destinationBase, copied) {
	const clean = reference.split(/[?#]/, 1)[0];
	if (!isLocalAsset(clean)) return;
	const source = resolve(sourceBase, clean);
	const destination = resolve(destinationBase, clean);
	if (!source.startsWith(stageRoot) || !existsSync(source) || copied.has(source)) return;
	copied.add(source);
	mkdirSync(dirname(destination), { recursive: true });
	cpSync(source, destination);
	if (extname(source).toLowerCase() === '.css') {
		for (const match of readFileSync(source, 'utf8').matchAll(/url\(\s*["']?([^)'"\s]+)["']?\s*\)/g)) {
			copyAsset(match[1], dirname(source), dirname(destination), copied);
		}
	}
}

try {
	const sources = findProjectSources(projectsRoot);
	if (!sources.length) throw new Error('No Quarto project pages found');

	execFileSync('npm', ['run', 'build:astro'], { cwd: astroRoot, stdio: 'inherit' });
	const header = requireShellArtifact('header/index.html');
	const footer = requireShellArtifact('footer/index.html');
	rmSync(join(shellRoot, 'header'), { recursive: true, force: true });
	rmSync(join(shellRoot, 'footer'), { recursive: true, force: true });
	execFileSync('quarto', ['render', ...sources, '--output-dir', stageRoot], { cwd: repoRoot, stdio: 'inherit' });

	const copied = new Set();
	for (const source of sources) {
		const renderedRelative = outputPath(source);
		const renderedSource = join(stageRoot, renderedRelative);
		const renderedDestination = join(distRoot, renderedRelative);
		if (!existsSync(renderedSource)) throw new Error(`Quarto did not render ${renderedRelative}`);

		const html = applySharedShell(readFileSync(renderedSource, 'utf8'), header, footer);
		mkdirSync(dirname(renderedDestination), { recursive: true });
		writeFileSync(renderedDestination, html);
		copied.add(renderedSource);
		for (const match of html.matchAll(/(?:src|href)=["']([^"']+)["']/g)) {
			copyAsset(match[1], dirname(renderedSource), dirname(renderedDestination), copied);
		}
	}

	writeSitemap();
	execFileSync('npm', ['run', 'postbuild'], { cwd: astroRoot, stdio: 'inherit' });
	console.log(`Production site build complete: ${sources.length} Quarto project pages merged into dist/`);
} finally {
	rmSync(stageRoot, { recursive: true, force: true });
}
