const { test, expect } = require("@playwright/test");

test.describe("critical interactions", () => {
  test("desktop navbar dropdown opens", async ({ page }) => {
    await page.setViewportSize({ width: 1440, height: 1000 });
    await page.goto("/");

    const dropdown = page.locator("[data-navbar-dropdown]").filter({
      has: page.locator("summary", { hasText: "More" })
    });
    const toggle = dropdown.locator("summary");
    await toggle.click();

    await expect(dropdown).toHaveAttribute("open", "");
    await expect(
      dropdown.getByRole("link", { name: "Contact", exact: true })
    ).toBeVisible();
  });

  test("mobile navbar expands and exposes navigation", async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto("/");

    const toggle = page.locator(".menu-toggle");
    await toggle.click();

    await expect(toggle).toHaveAttribute("aria-expanded", "true");
    await expect(page.locator("#navbar-links")).toHaveClass(/\bis-open\b/);
    await expect(page.getByRole("link", { name: "About", exact: true })).toBeVisible();
  });

  test("mobile navbar covers project navigation without moving it", async ({
    page
  }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto("/projects/f1-time-rank-duality/index.html");

    const projectNavigation = page.locator(".project-chapter-rail");
    const projectToggle = page.locator(".project-chapter-toggle");
    const navbarToggle = page.locator(".menu-toggle");
    const navbarMenu = page.locator("#navbar-links");

    await expect(projectNavigation).toBeAttached();
    const topBefore = await projectNavigation.evaluate((element) =>
      element.getBoundingClientRect().top
    );

    await navbarToggle.click();
    await expect(navbarMenu).toHaveClass(/\bis-open\b/);
    await expect
      .poll(() =>
        projectNavigation.evaluate((element) =>
          element.getBoundingClientRect().top
        )
      )
      .toBe(topBefore);

    const navbarCoversProjectToggle = await projectToggle.evaluate((element) => {
      const rect = element.getBoundingClientRect();
      const coveringElement = document.elementFromPoint(
        rect.left + rect.width / 2,
        rect.top + rect.height / 2
      );
      return Boolean(coveringElement?.closest(".site-header"));
    });
    expect(navbarCoversProjectToggle).toBe(true);
  });

  test("theme toggle changes and persists the color scheme", async ({ page }) => {
    await page.goto("/");

    const before = await page.locator("html").getAttribute("data-theme");
    await page.locator(".theme-toggle").click();
    await expect
      .poll(() => page.locator("html").getAttribute("data-theme"))
      .not.toBe(before);

    const stored = await page.evaluate(() =>
      window.localStorage.getItem("theme")
    );
    expect(stored).toMatch(/^(light|dark)$/);

    const changed = await page.locator("html").getAttribute("data-theme");
    await page.reload();
    await expect(page.locator("html")).toHaveAttribute("data-theme", changed);
  });

  test("site search returns a Projects result", async ({ page }) => {
    await page.goto("/");
    await page.locator(".search-toggle").click();

    const input = page.locator("#site-search-input");
    await expect(input).toBeVisible();
    await input.fill("projects");

    const results = page.locator(".site-search-result-list");
    await expect(results).toContainText(/Projects/i);

		await input.fill("Portable Rule System");
		await expect(results).toContainText("A Portable Rule System for Working with AI");
  });

  test("publication details and citation copy work", async ({
    context,
    page
  }) => {
    await context.grantPermissions(["clipboard-read", "clipboard-write"]);
    await page.goto("/publications/");

    const first = page.locator(".publication-entry").first();
    const abstractToggle = first.locator(".abstract-toggle");
    const bibtexToggle = first.locator(".bibtex-toggle");

    await abstractToggle.click();
    await expect(abstractToggle).toHaveAttribute("aria-expanded", "true");
    await expect(first.locator(".abstract")).toBeVisible();

    await bibtexToggle.click();
    await expect(abstractToggle).toHaveAttribute("aria-expanded", "false");
    await expect(first.locator(".abstract")).toBeHidden();
    await expect(bibtexToggle).toHaveAttribute("aria-expanded", "true");
    await expect(first.locator(".bibtex")).toBeVisible();

    await bibtexToggle.click();
    await expect(bibtexToggle).toHaveAttribute("aria-expanded", "false");
    await expect(first.locator(".bibtex")).toBeHidden();

    await abstractToggle.click();
    await expect(abstractToggle).toHaveAttribute("aria-expanded", "true");
    await expect(first.locator(".abstract")).toBeVisible();

    await bibtexToggle.click();

    const copy = first.locator(".copy-citation");
    await copy.click();
    await expect(copy).toHaveText("Copied");
    await expect.poll(() => page.evaluate(() => navigator.clipboard.readText())).toContain("@article");

    await expect(first.locator(".publication-primary-action"))
      .toHaveAttribute("target", "_blank");
    await expect(first.getByRole("link", { name: "arXiv" }))
      .toHaveAttribute("target", "_blank");

    const mathEntry = page.locator('[id="2024-Bre-Car-Fan-Wal"]');
    await mathEntry.locator(".abstract-toggle").click();
    await expect(mathEntry.locator(".abstract .katex").first()).toBeVisible();

    const internalExplainer = page.locator('[id="2024-Fry-Bri-Fan"]')
      .getByRole("link", { name: "Explainer" });
    await expect(internalExplainer).not.toHaveAttribute("target", "_blank");
  });

  test("publication journal fragments retain canonical and legacy targets", async ({ page }) => {
    for (const fragment of ["journal", "journal-publications"]) {
      await page.goto(`/publications/#${fragment}`);
      await expect(page.locator('#journal-publications > h2')).toBeInViewport();
    }
  });

  test("back to top works on Astro and injected Quarto pages", async ({ page }) => {
    for (const path of ["/", "/projects/f1-time-rank-duality/technical.html"]) {
      await page.goto(path);
      const button = page.getByRole("button", {
        name: "Back to top",
        includeHidden: true
      });
      await expect(button).toHaveAttribute("aria-hidden", "true");

      await page.evaluate(() => window.scrollTo(0, 800));
      await expect(button).toHaveClass(/is-visible/);
      await expect(button).toHaveAttribute("tabindex", "0");
      await expect(button).not.toHaveClass(/is-docked/);
      await expect(button).toHaveCSS("position", "fixed");

      await page.evaluate(() => {
        const footer = document.querySelector(".site-footer");
        window.scrollTo(0, footer.getBoundingClientRect().top + window.scrollY - window.innerHeight + 1);
      });
      await expect(button).toHaveClass(/is-visible/);
      await expect(button).toHaveAttribute("tabindex", "0");
      await expect(button).toHaveClass(/is-docked/);
      await expect(button).toHaveCSS("position", "absolute");
      await expect.poll(() => page.evaluate(() => {
        const button = document.querySelector(".back-to-top").getBoundingClientRect();
        const footer = document.querySelector(".site-footer").getBoundingClientRect();
        return button.bottom <= footer.top;
      })).toBe(true);
      const dockedTop = await button.evaluate((element) => element.style.top);
      await page.evaluate(() => window.scrollBy(0, 40));
      expect(await button.evaluate((element) => element.style.top)).toBe(dockedTop);
      await expect(button).toHaveCSS("width", "40px");
      await expect(button).toHaveCSS("height", "40px");
      await expect(button).toHaveCSS("border-radius", "50%");
      await page.evaluate(() => window.scrollTo(0, 800));
      await expect(button).toHaveClass(/is-visible/);
      await expect(button).not.toHaveClass(/is-docked/);
      await expect(button).toHaveCSS("position", "fixed");
      await button.focus();
      await page.keyboard.press('Enter');
      await expect.poll(() => page.evaluate(() => window.scrollY)).toBeLessThan(10);
    }
  });

  test("news disclosure opens from its summary", async ({ page }) => {
    await page.goto("/");

    const homepageRows = await page.locator("[data-news-item]").evaluateAll((items) => items.map((item) => item.outerHTML));
    const item = page.locator("details.news-item").first();
    await item.locator("summary").click();
    await expect(item).toHaveAttribute("open", "");

    await page.goto("/news/");
    const archiveRows = await page.locator("[data-news-item]").evaluateAll((items) => items.slice(0, 8).map((item) => item.outerHTML));
    expect(homepageRows).toEqual(archiveRows);
  });

  test("Teaching About disclosures and News archive search work", async ({ page }) => {
    await page.goto("/teaching/#lecturer");
    await expect(page.locator("#lecturer > h2")).toBeInViewport();
    await expect(page.locator("#tutor > h2")).toHaveText("Teaching assistant");
    const about = page.locator(".teaching-course .abstract-toggle").first();
    const teachingStyle = await about.evaluate((element) => {
      const style = getComputedStyle(element);
      return [style.color, style.fontSize, style.fontWeight, style.backgroundColor, style.borderWidth, style.padding];
    });
    await about.click();
    await expect(about).toHaveAttribute("aria-expanded", "true");
    await expect(about).toHaveAttribute("aria-controls", /.+-abstract$/);
    const teachingPanel = page.locator(".teaching-course .abstract").first();
    await expect(teachingPanel).toBeVisible();
    const teachingPanelStyle = await teachingPanel.evaluate((element) => {
      const style = getComputedStyle(element);
      return [style.marginTop, style.padding, style.borderTopWidth, style.borderBottomWidth, style.backgroundColor, style.color, style.fontSize, style.lineHeight];
    });
    await about.click();
    await expect(about).toHaveAttribute("aria-expanded", "false");
    await expect(teachingPanel).toBeHidden();
    await page.goto("/publications/");
    const publicationAbstract = page.locator(".publication-entry .abstract-toggle").first();
    const publicationStyle = await publicationAbstract.evaluate((element) => {
      const style = getComputedStyle(element);
      return [style.color, style.fontSize, style.fontWeight, style.backgroundColor, style.borderWidth, style.padding];
    });
    expect(teachingStyle).toEqual(publicationStyle);
    await publicationAbstract.click();
    const publicationPanel = page.locator(".publication-entry .abstract").first();
    const publicationPanelStyle = await publicationPanel.evaluate((element) => {
      const style = getComputedStyle(element);
      return [style.marginTop, style.padding, style.borderTopWidth, style.borderBottomWidth, style.backgroundColor, style.color, style.fontSize, style.lineHeight];
    });
    expect(teachingPanelStyle).toEqual(publicationPanelStyle);

    await page.goto("/news/");
    const items = page.locator("[data-news-item]");
    const total = await items.count();
    expect(total).toBeGreaterThan(1);
    await page.locator("[data-news-search]").fill("curling");
    const visible = items.filter({ visible: true });
    await expect(visible.first()).toBeVisible();
    expect(await visible.count()).toBeLessThan(total);
    await visible.first().locator("summary").click();
    await expect(visible.first()).toHaveAttribute("open", "");
  });

  test("Notes index and merged Quarto articles preserve their contracts", async ({ page }) => {
    await page.goto("/notes/");
    await expect(page.locator(".notes-list .note-row")).toHaveCount(4);
    await expect(page.locator(".note-row h2").first()).toHaveText("A Portable Rule System for Working with AI");
    await expect(page.locator(".note-row").first().locator(".note-categories")).toHaveCount(0);
    await expect(page.locator(".note-row").first()).toContainText("How I moved from long, messy chats to concise, version-controlled instructions");
    const hrefs = await page.locator(".note-row h2 a").evaluateAll((links) => links.map((link) => link.getAttribute("href")));
    expect(hrefs).toEqual(expect.arrayContaining([
      "/notes/ai-agents-practical-stack-2026-qwen9-128k-copilot-opencode-no-gemini-free.html",
      "/notes/ai-real-project-lessons.html",
      "/notes/how-i-use-ai.html",
      "/notes/portable-ai-rules-workflow.html"
    ]));
    expect(hrefs.every((href) => href?.endsWith(".html"))).toBe(true);
    await expect(page.locator(".note-row img")).toHaveCount(4);
    await expect(page.locator(".note-row time")).toHaveCount(4);

    for (const path of ["/notes/how-i-use-ai.html", "/notes/portable-ai-rules-workflow.html"]) {
      await page.goto(path);
      await expect(page.locator(".site-header")).toHaveCount(1);
      await expect(page.locator(".site-footer")).toHaveCount(1);
      await expect(page.locator("#quarto-header")).toHaveCount(0);
      await expect(page.locator("main h1")).toBeVisible();
      await expect(page.locator("pre").first()).toBeVisible();
      await expect(page.getByRole("button", { name: "Back to top", includeHidden: true })).toBeAttached();
    }
  });

  test("migrated record archives preserve sections and disclosures", async ({ page }) => {
    await page.goto("/presentations/#talk");
    await expect(page.locator("#talk + .archive-year")).toBeAttached();
    await expect(page.locator("#poster")).toBeAttached();
    await expect(page.locator("#institutional")).toBeAttached();
    const presentationAbstract = page.locator(".record-archive .abstract-toggle").first();
    await presentationAbstract.click();
    await expect(presentationAbstract).toHaveAttribute("aria-expanded", "true");

    await page.goto("/supervision/#master");
    await expect(page.locator("#undergraduate")).toBeAttached();
    await expect(page.getByRole("link", { name: "Email me" })).toHaveAttribute("href", "mailto:silvio.fanzon.work@gmail.com");
    const supervisionAbstract = page.locator(".record-archive .abstract-toggle").first();
    await supervisionAbstract.click();
    await expect(supervisionAbstract).toHaveAttribute("aria-expanded", "true");
  });
});
