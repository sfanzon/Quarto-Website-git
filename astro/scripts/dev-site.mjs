import { spawn } from 'node:child_process';
import { existsSync, readdirSync, statSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const astroRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const repoRoot = resolve(astroRoot, '..');
const watchPaths = [
	joinAstro('src'),
	joinAstro('public'),
	joinRepo('projects'),
	joinRepo('notes'),
	joinRepo('dev'),
	joinRepo('data/projects.yml'),
	joinRepo('data/citations'),
	joinRepo('filters/project-components.lua'),
	joinRepo('scripts/build-content.py'),
	joinRepo('styles/main.scss'),
	joinRepo('styles/main'),
	joinRepo('styles/components'),
	joinRepo('styles/project.scss'),
	joinRepo('styles/project'),
	joinRepo('_quarto.yml'),
	joinRepo('includes/site-footer.html'),
	joinRepo('includes/project-navigation.html'),
	joinRepo('includes/after-body.html'),
	joinRepo('includes/scroll-restoration-head.html'),
	joinRepo('includes/mermaid-svg-ids.html'),
	joinAstro('astro.config.mjs'),
	joinAstro('package.json'),
].filter(existsSync);

let buildRunning = false;
let buildQueued = false;
let rebuildTimer;
let preview;
let sourceSnapshot;
let stopping = false;

function joinAstro(path) {
	return resolve(astroRoot, path);
}

function joinRepo(path) {
	return resolve(repoRoot, path);
}

function run(command, args) {
	return new Promise((resolvePromise, reject) => {
		const child = spawn(command, args, { cwd: astroRoot, stdio: 'inherit' });
		child.once('error', reject);
		child.once('exit', (code) => {
			if (code === 0) resolvePromise();
			else reject(new Error(`${command} ${args.join(' ')} exited with code ${code}`));
		});
	});
}

async function build() {
	if (buildRunning) {
		buildQueued = true;
		return true;
	}

	buildRunning = true;
	console.log('\nRebuilding hybrid development site…');
	try {
		await run('npm', ['run', 'build:qa']);
		console.log('Hybrid development site ready. Reload the browser to see the update.');
		return true;
	} catch (error) {
		console.error(`Hybrid rebuild failed: ${error.message}`);
		return false;
	} finally {
		buildRunning = false;
		if (buildQueued) {
			buildQueued = false;
			void build();
		}
	}
}

function queueBuild() {
	clearTimeout(rebuildTimer);
	rebuildTimer = setTimeout(() => void build(), 180);
}

function startPreview() {
	preview = spawn('npm', ['run', 'preview', '--', '--host', '127.0.0.1'], {
		cwd: astroRoot,
		stdio: 'inherit',
	});
	preview.once('error', (error) => console.error(`Preview server failed: ${error.message}`));
	preview.once('exit', (code, signal) => {
		if (stopping) return;
		console.error(`Preview server exited unexpectedly (${signal ?? `code ${code}`}). Stopping hybrid watcher.`);
		stopping = true;
		process.exit(1);
	});
}

function collectSnapshot(path, entries = []) {
	if (!existsSync(path)) return entries;
	const stats = statSync(path);
	if (stats.isDirectory()) {
		for (const entry of readdirSync(path, { withFileTypes: true })) collectSnapshot(resolve(path, entry.name), entries);
	} else {
		entries.push(`${path}:${stats.mtimeMs}:${stats.size}`);
	}
	return entries;
}

function snapshotSources() {
	return watchPaths.flatMap((path) => collectSnapshot(path)).sort().join('\n');
}

function startWatching() {
	sourceSnapshot = snapshotSources();
	setInterval(() => {
		const nextSnapshot = snapshotSources();
		if (nextSnapshot === sourceSnapshot) return;
		sourceSnapshot = nextSnapshot;
		queueBuild();
	}, 750);
	console.log(`Polling ${watchPaths.length} Astro and Quarto source locations for hybrid rebuilds.`);
}

function stop() {
	stopping = true;
	clearTimeout(rebuildTimer);
	preview?.kill('SIGTERM');
	process.exit();
}

process.on('SIGINT', stop);
process.on('SIGTERM', stop);

if (!await build()) process.exit(1);
startPreview();
startWatching();
