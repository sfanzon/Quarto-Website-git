import { existsSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { load } from 'js-yaml';

export interface Project {
	id: string;
	title: string;
	eyebrow: string;
	labels: string[];
	summary: string;
	image: string;
	href: string;
	code?: string;
	archived?: boolean;
}

const source = [
	resolve(process.cwd(), '../data/projects.yml'),
	resolve(process.cwd(), 'data/projects.yml'),
].find(existsSync);

if (!source) throw new Error('Unable to locate canonical data/projects.yml');
const parsed = load(readFileSync(source, 'utf8'));

if (!Array.isArray(parsed)) throw new Error('data/projects.yml must contain a project list');

export const projects = parsed as Project[];
