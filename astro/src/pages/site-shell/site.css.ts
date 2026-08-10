import css from '../../styles/shell.css?raw';

export const prerender = true;

export function GET() {
	return new Response(css, {
		headers: { 'Content-Type': 'text/css; charset=utf-8' },
	});
}
