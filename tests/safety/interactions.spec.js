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
    await expect(first.locator(".bibtex")).toBeVisible();

    const copy = first.locator(".copy-citation");
    await copy.click();
    await expect(copy).toHaveText("Copied");
    await expect.poll(() => page.evaluate(() => navigator.clipboard.readText())).toContain("@article");
  });

  test("news disclosure opens from its summary", async ({ page }) => {
    await page.goto("/");

    const item = page.locator("details.news-item").first();
    await item.locator("summary").click();
    await expect(item).toHaveAttribute("open", "");
  });
});
