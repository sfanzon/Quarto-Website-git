-- Shared long-form project renderer.
--
-- Every project article declares only `project-id`; F1 subpages additionally
-- declare `project-view`. The content itself comes from data/projects.yml,
-- converted to JSON by scripts/build-content.py before Quarto renders.

local project_index = nil
local current_project = nil
local current_view = nil

local function html_escape(value)
  local text = tostring(value or "")
  text = text:gsub("&", "&amp;")
  text = text:gsub("<", "&lt;")
  text = text:gsub(">", "&gt;")
  text = text:gsub('"', "&quot;")
  text = text:gsub("'", "&#39;")
  return text
end

local function read_file(path)
  local handle = assert(io.open(path, "r"))
  local contents = handle:read("*a")
  handle:close()
  return contents
end

local function load_projects()
  if project_index then return project_index end
  if not quarto.project.directory then return {} end
  local path = pandoc.path.join({
    quarto.project.directory,
    "data",
    "projects.generated.json"
  })
  local decoded = quarto.json.decode(read_file(path))
  project_index = {}
  for _, project in ipairs(decoded or {}) do
    project_index[project.id] = project
  end
  return project_index
end

local function absolute_project_href(href)
  href = tostring(href or "")
  if href:match("^https?://") or href:match("^mailto:") or href:match("^#") then
    return href
  end
  if href:sub(1, 1) == "/" then return href end
  return "/" .. href
end

local function render_primary_links(resources)
  local links = {}
  for _, item in ipairs(resources or {}) do
    table.insert(
      links,
      '<a href="' .. html_escape(item.href) .. '">' ..
      html_escape(item.label) .. '</a>'
    )
  end
  return table.concat(links)
end

local function render_hero(project)
  local article = project.article
  if not article then return "" end
  local title = article.title or project.title or "Project"
  local eyebrow = article.eyebrow or project.eyebrow or "Project"
  local lead = article.lead or project.summary or ""
  local author = article.author or "Silvio Fanzon"
  local published = article.published or ""
  local resources = render_primary_links(article.resources)
  local resources_block = ""
  if resources ~= "" then
    resources_block = [[
    <div class="project-meta-resources">
      <span class="project-meta-label">Resources</span>
      <nav class="project-primary-links" aria-label="Primary project links">]] .. resources .. [[</nav>
    </div>]]
  end

  local hero_class = "project-detail-hero"
  if project.at_a_glance and #project.at_a_glance > 0 then
    hero_class = hero_class .. " has-at-a-glance"
  end

  return [[<header class="]] .. hero_class .. [[">
  <p class="project-category">]] .. html_escape(eyebrow) .. [[</p>
  <h1>]] .. html_escape(title) .. [[</h1>
  <p class="project-detail-lead">]] .. html_escape(lead) .. [[</p>
  <div class="project-meta" aria-label="Project metadata">
    <div class="project-meta-item">
      <span class="project-meta-label">Author</span>
      <span class="project-meta-value project-author-list"><span class="project-author-name">]] .. html_escape(author) .. [[</span></span>
    </div>
    <div class="project-meta-item">
      <span class="project-meta-label">Published</span>
      <time class="project-meta-value">]] .. html_escape(published) .. [[</time>
    </div>]] .. resources_block .. [[
  </div>
</header>]]
end

local function render_at_a_glance(project)
  local items = project.at_a_glance or {}
  if #items == 0 then return "" end

  local rendered = {}
  for _, item in ipairs(items) do
    table.insert(rendered, [[<div class="project-glance-item">
    <span class="project-glance-label">]] .. html_escape(item.label) .. [[</span>
    <p>]] .. html_escape(item.text) .. [[</p>
  </div>]])
  end

  return [[<section class="project-at-a-glance project-at-a-glance-]] .. tostring(#items) .. [[" aria-label="Project at a glance">
  ]] .. table.concat(rendered, "\n  ") .. [[
</section>]]
end

local function render_resource_map(project, view_id, completed)
  local article = project.article
  if not article or not article.views or not view_id then return "" end
  local classes = completed and "project-resource-map project-resource-map-end" or "project-resource-map"
  local intro_label = completed and "Section complete" or "Explore project"
  local intro_copy = completed and "Explore another view." or "Choose the level of detail you need."
  local links = {}

  for _, view in ipairs(article.views) do
    local is_current = view.id == view_id
    local link_classes = "project-resource-link"
    if is_current then link_classes = link_classes .. " is-current" end
    if is_current and completed then link_classes = link_classes .. " is-finished" end
    local aria = (is_current and not completed) and ' aria-current="page"' or ""
    local status = ""
    if is_current then
      status = '<span class="project-resource-status">' ..
        (completed and "✓ Finished" or "Current") .. '</span>'
    end
    table.insert(links, [[<a class="]] .. link_classes .. [[" href="]] ..
      html_escape(view.href) .. [["]] .. aria .. [[>
    <span class="project-resource-number">]] .. html_escape(view.number) .. [[</span>
    <span class="project-resource-copy"><strong>]] .. html_escape(view.title) ..
      [[</strong><small>]] .. html_escape(view.description) .. [[</small></span>
    ]] .. status .. [[
  </a>]])
  end

  return [[<nav class="]] .. classes .. [[" aria-label="Ways to explore this project">
  <div class="project-resource-intro">
    <span>]] .. intro_label .. [[</span>
    <strong>]] .. intro_copy .. [[</strong>
  </div>
  ]] .. table.concat(links) .. [[
</nav>]]
end

local function render_related(project)
  local all = load_projects()
  local cards = {}
  for i, project_id in ipairs(project.related or {}) do
    if i > 3 then break end
    local item = all[project_id]
    if item then
      local article = item.article or {}
      local label = article.eyebrow or item.eyebrow or "Project"
      local title = article.title or item.title or "Project"
      local summary = item.summary or ""
      local href = absolute_project_href(item.href)
      table.insert(cards, [[<a class="project-related-card" href="]] .. html_escape(href) .. [[">
      <span class="project-related-label">]] .. html_escape(label) .. [[</span>
      <strong>]] .. html_escape(title) .. [[</strong>
      <small>]] .. html_escape(summary) .. [[</small>
      <span class="project-related-action">Read project <span aria-hidden="true">→</span></span>
    </a>]])
    end
  end
  if #cards == 0 then return "" end

  return [[<section class="project-related column-page" aria-labelledby="project-related-heading">
  <div class="project-related-heading">
    <p class="project-category">Continue exploring</p>
    <h2 id="project-related-heading" data-nav-exclude>Related projects</h2>
  </div>
  <div class="project-related-grid">
    ]] .. table.concat(cards, "\n    ") .. [[
  </div>
</section>]]
end

local function render_end(project, view_id)
  local parts = {'<div class="project-page-end">'}
  local end_map = render_resource_map(project, view_id, true)
  if end_map ~= "" then table.insert(parts, end_map) end
  table.insert(parts, '</div>')

  local related = render_related(project)
  if related ~= "" then table.insert(parts, related) end

  table.insert(parts, [[<div class="project-end-footer">
  <a class="project-end-back-link" href="/projects.html">← Back to all projects</a>
</div>]])
  return table.concat(parts, "\n")
end

function Meta(meta)
  local id = meta["project-id"] and pandoc.utils.stringify(meta["project-id"]) or nil
  current_view = meta["project-view"] and pandoc.utils.stringify(meta["project-view"]) or nil
  if not id or id == "" then
    current_project = nil
    return meta
  end

  current_project = load_projects()[id]
  if not current_project then
    quarto.log.warning("Unknown project-id: " .. id)
    return meta
  end

  -- Project YAML is authoritative for the visible/document title of long-form
  -- project articles. Keeping this in Meta also sets the HTML page title.
  if current_project.article and current_project.article.title then
    meta.title = pandoc.MetaString(current_project.article.title)
    meta.pagetitle = pandoc.MetaString(current_project.article.title)
  end

  return meta
end

function Pandoc(doc)
  if not current_project then return doc end

  if current_project.article then
    local top = render_hero(current_project)
    local glance = render_at_a_glance(current_project)
    if glance ~= "" then top = top .. "\n" .. glance end
    local resource_map = render_resource_map(current_project, current_view, false)
    if resource_map ~= "" then top = top .. "\n" .. resource_map end
    table.insert(doc.blocks, 1, pandoc.RawBlock("html", top))
  end

  table.insert(doc.blocks, pandoc.RawBlock("html", render_end(current_project, current_view)))
  return doc
end
