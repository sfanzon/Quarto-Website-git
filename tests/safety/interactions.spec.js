const { test, expect } = require("@playwright/test");

test.describe("critical interactions", () => {
  test("desktop navbar dropdown opens", async ({ page }) => {
    await page.setViewportSize({ width: 1440, height: 1000 });
    await page.goto("/index.html");

    const toggle = page.locator("#nav-menu-more");
    await toggle.click();

    await expect(toggle).toHaveAttribute("aria-expanded", "true");
    await expect(
      page.getByLabel("More").getByRole("link", {
        name: "Contact",
        exact: true
      })
    ).toBeVisible();
  });

  test("mobile navbar expands and exposes navigation", async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto("/index.html");

    const toggle = page.locator(".navbar-toggler");
    await toggle.click();

    await expect(toggle).toHaveAttribute("aria-expanded", "true");
    await expect(page.locator("#navbarCollapse")).toHaveClass(/\bshow\b/);
    await expect(page.getByRole("link", { name: "About", exact: true })).toBeVisible();
  });

  test("theme toggle changes and persists the color scheme", async ({ page }) => {
    await page.goto("/index.html");

    const before = await page.locator("body").getAttribute("class");
    await page.locator(".quarto-color-scheme-toggle").first().click();
    await expect
      .poll(() => page.locator("body").getAttribute("class"))
      .not.toBe(before);

    const stored = await page.evaluate(() =>
      window.localStorage.getItem("quarto-color-scheme")
    );
    expect(stored).not.toBeNull();

    const changed = await page.locator("body").getAttribute("class");
    await page.reload();
    await expect(page.locator("body")).toHaveAttribute("class", changed);
  });

  test("site search returns a Teaching result", async ({ page }) => {
    await page.goto("/index.html");
    await page.locator("#quarto-search").click();

    const input = page.locator(".aa-DetachedContainer .aa-Input");
    await expect(input).toBeVisible();
    await input.fill("teaching");

    await expect(page.locator(".aa-DetachedContainer .aa-Item").first()).toBeVisible();
    await expect(page.locator(".aa-DetachedContainer")).toContainText(/Teaching/i);
  });

  test("publication abstract and citation panels are mutually exclusive", async ({
    page
  }) => {
    await page.goto("/publications.html");

    const entry = page.locator(".publication-entry").filter({
      has: page.locator(".abstract-toggle")
    }).first();
    const abstractToggle = entry.locator(".abstract-toggle");
    const citationToggle = entry.locator(".bibtex-toggle");

    await abstractToggle.click();
    await expect(abstractToggle).toHaveAttribute("aria-expanded", "true");
    await expect(entry.locator(".abstract")).toHaveClass(/\bopen\b/);

    await citationToggle.click();
    await expect(citationToggle).toHaveAttribute("aria-expanded", "true");
    await expect(entry.locator(".bibtex")).toHaveClass(/\bopen\b/);
    await expect(entry.locator(".abstract")).not.toHaveClass(/\bopen\b/);
  });

  test("news search filters entries and reports an empty result", async ({
    page
  }) => {
    await page.goto("/news.html");

    const input = page.locator("[data-news-search]");
    const items = page.locator("[data-news-item]");
    expect(await items.count()).toBeGreaterThan(0);

    await input.fill("query-that-cannot-match-any-news-entry");
    await expect(page.locator("[data-news-item]:visible")).toHaveCount(0);
    await expect(page.locator(".news-search-empty")).toBeVisible();
  });

  test("news disclosure opens from its summary", async ({ page }) => {
    await page.goto("/news.html");

    const item = page.locator("[data-news-item]").first();
    await item.locator("summary").click();
    await expect(item).toHaveAttribute("open", "");
  });
});
