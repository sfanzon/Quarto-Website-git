import { execFileSync } from 'node:child_process';
import { cpSync, existsSync, mkdirSync, mkdtempSync, readFileSync, readdirSync, rmSync, statSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, extname, join, relative, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const astroRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const repoRoot = resolve(astroRoot, '..');
const projectsRoot = join(repoRoot, 'projects');
const notesRoot = join(repoRoot, 'notes');
const sharedImagesRoot = join(repoRoot, 'assets', 'img');
const sharedPdfRoot = join(repoRoot, 'assets', 'pdf');
const academicCv = join(repoRoot, 'Silvio_Fanzon_Academic_CV.pdf');
const quartoKitchenSink = join(repoRoot, 'dev', 'quarto-kitchen-sink.qmd');
const distRoot = join(astroRoot, 'dist');
const stageRoot = mkdtempSync(join(tmpdir(), 'astro-quarto-documents-'));
const shellRoot = join(distRoot, 'site-shell');
const devRoot = join(distRoot, 'dev');
const stagedDevRoot = join(stageRoot, 'dev');
const siteUrl = 'https://www.silviofanzon.com';
const includeDevTools = process.argv.includes('--include-dev-tools');
const donorOutput = [
	join(distRoot, 'archive'),
	join(distRoot, 'blog'),
	join(distRoot, 'blog.png'),
	join(distRoot, 'rss.xml'),
	join(distRoot, 'tags'),
	join(distRoot, 'team'),
	join(distRoot, 'team.png'),
];
const compatibilityAliases = new Map([
	['about.html', 'about/index.html'],
	['expertise.html', 'expertise/index.html'],
	['publications.html', 'publications/index.html'],
	['research.html', 'research/index.html'],
	['teaching.html', 'teaching/index.html'],
	['news.html', 'news/index.html'],
	['contact.html', 'contact/index.html'],
	['presentations.html', 'presentations/index.html'],
	['supervision.html', 'supervision/index.html'],
	['cv.html', 'cv/index.html'],
	['notes.html', 'notes/index.html'],
]);

function findQuartoSources(directory) {
	return readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
		const path = join(directory, entry.name);
		if (entry.isDirectory()) return findQuartoSources(path);
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
		.filter((path) => !readFileSync(path, 'utf8').includes('<meta name="robots" content="noindex">'))
		.map(sitemapUrl)
		.sort();
	const entries = urls.map((url) => `  <url><loc>${url}</loc></url>`).join('\n');
	writeFileSync(join(distRoot, 'sitemap.xml'), `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${entries}\n</urlset>\n`);
}

function writeCompatibilityAliases() {
	for (const [alias, canonical] of compatibilityAliases) {
		const canonicalPath = join(distRoot, canonical);
		let html = readFileSync(canonicalPath, 'utf8');
		html = replaceOnce(html, /<body([^>]*)>/, (_match, attributes) => `<body${attributes} data-pagefind-ignore="all">`, 'body opening tag');
		html = replaceOnce(html, /<\/head>/, '<meta name="robots" content="noindex"></head>', 'head closing tag');
		writeFileSync(join(distRoot, alias), html);
	}
}

function requireShellArtifact(name) {
	const path = join(shellRoot, name);
	if (!existsSync(path)) throw new Error(`Astro did not emit required shell artifact: ${relative(astroRoot, path)}`);
	return readFileSync(path, 'utf8').replace(/^<!DOCTYPE html>/i, '');
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
	html = replaceOnce(html, /<footer class="site-footer"[\s\S]*?<\/footer>/, '', 'Quarto footer');
	html = replaceOnce(html, /<body([^>]*)>/, (_match, attributes) => `<body${attributes}>${header}`, 'body opening tag');
	html = replaceOnce(html, /<\/head>/, '<link rel="stylesheet" href="/site-shell/site.css"></head>', 'head closing tag');
	html = replaceOnce(html, /<\/body>/, `${footer}</body>`, 'body closing tag');
	return html
		.replace(/<script src="[^"]*\/quarto-search\/[^"]+"><\/script>\s*/g, '')
		.replace(/<script id="quarto-search-options"[^>]*>[\s\S]*?<\/script>\s*/, '')
		.replace(/<div id="quarto-search-results"><\/div>\s*/, '');
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
	if (!source.startsWith(stageRoot) || !existsSync(source) || !statSync(source).isFile() || copied.has(source)) return;
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
	const sources = [...findQuartoSources(projectsRoot), ...findQuartoSources(notesRoot)];
	if (includeDevTools) {
		if (!existsSync(quartoKitchenSink)) throw new Error('Missing Quarto kitchen sink source');
		sources.push(quartoKitchenSink);
	}
	if (!sources.length) throw new Error('No Quarto document pages found');

	execFileSync('npm', ['run', 'build:astro'], {
		cwd: astroRoot,
		env: { ...process.env, SF_INCLUDE_DEV_TOOLS: includeDevTools ? '1' : '0' },
		stdio: 'inherit',
	});
	const header = requireShellArtifact('header/index.html');
	const footer = requireShellArtifact('footer/index.html');
	writeCompatibilityAliases();
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
	const listingsManifest = join(stageRoot, 'listings.json');
	if (existsSync(listingsManifest)) cpSync(listingsManifest, join(distRoot, 'listings.json'));
	else writeFileSync(join(distRoot, 'listings.json'), '[]\n');

	if (existsSync(devRoot)) {
		if (includeDevTools) cpSync(devRoot, stagedDevRoot, { recursive: true });
		rmSync(devRoot, { recursive: true, force: true });
	}
	cpSync(sharedImagesRoot, join(distRoot, 'assets', 'img'), { recursive: true });
	cpSync(sharedPdfRoot, join(distRoot, 'assets', 'pdf'), { recursive: true });
	cpSync(academicCv, join(distRoot, 'Silvio_Fanzon_Academic_CV.pdf'));
	for (const output of donorOutput) rmSync(output, { recursive: true, force: true });
	writeSitemap();
	execFileSync('npm', ['run', 'postbuild'], { cwd: astroRoot, stdio: 'inherit' });
	if (includeDevTools) cpSync(stagedDevRoot, devRoot, { recursive: true });
	console.log(`${includeDevTools ? 'QA' : 'Production'} site build complete: ${sources.length} Quarto document pages merged into dist/`);
} finally {
	rmSync(stageRoot, { recursive: true, force: true });
}
