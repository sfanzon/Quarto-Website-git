const { test, expect } = require("@playwright/test");

const responsiveViewports = [
  { name: "mobile", width: 390, height: 844 },
  { name: "iPad", width: 820, height: 1180 },
  { name: "desktop", width: 1440, height: 1000 }
];

function expectAligned(actual, expected, label) {
  expect(Math.abs(actual - expected), label).toBeLessThanOrEqual(0.5);
}

test("navbar and footer share their responsive shell edges", async ({ page }) => {
  for (const viewport of responsiveViewports) {
    await page.setViewportSize(viewport);
    await page.goto("/");

    const layout = await page.evaluate(() => {
      const bounds = (selector) => {
        const rect = document.querySelector(selector).getBoundingClientRect();
        return { left: rect.left, right: rect.right };
      };

      return {
        navbar: bounds(".site-navbar"),
        footer: bounds(".site-footer-inner"),
        brand: bounds(".site-brand")
      };
    });

    expectAligned(
      layout.navbar.left,
      layout.footer.left,
      `${viewport.name}: left shell edge`
    );
    expectAligned(
      layout.navbar.right,
      layout.footer.right,
      `${viewport.name}: right shell edge`
    );
    expectAligned(
      layout.brand.left,
      layout.navbar.left,
      `${viewport.name}: brand text edge`
    );
  }
});

test("desktop navbar controls align with the navbar shell", async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 1000 });
  await page.goto("/");

  const layout = await page.evaluate(() => {
    const navbar = document.querySelector(".site-navbar").getBoundingClientRect();
    const controls = document.querySelector(".navbar-controls").getBoundingClientRect();
    return { navbarRight: navbar.right, controlsRight: controls.right };
  });

  expectAligned(layout.controlsRight, layout.navbarRight, "desktop: controls right edge");
});

test("project card grids retain their responsive column counts", async ({ page }) => {
  const targets = [
    { path: "/", selector: ".home-project-grid" },
    { path: "/projects/", selector: ".projects-card-grid" }
  ];
  const expectedColumns = { mobile: 1, iPad: 2, desktop: 3 };

  for (const viewport of responsiveViewports) {
    await page.setViewportSize(viewport);
    for (const target of targets) {
      await page.goto(target.path);
      const grid = page.locator(target.selector);
      await expect(grid).toBeVisible();

      const layout = await grid.evaluate((element) => {
        const columns = getComputedStyle(element).gridTemplateColumns
          .trim()
          .split(/\s+/)
          .filter(Boolean).length;
        const cardsFitViewport = [...element.querySelectorAll(".home-project-card")]
          .every((card) => {
            const rect = card.getBoundingClientRect();
            return rect.left >= -0.5 && rect.right <= window.innerWidth + 0.5;
          });
        return { columns, cardsFitViewport };
      });

      expect(layout.columns, `${viewport.name}: ${target.path} columns`)
        .toBe(expectedColumns[viewport.name]);
      expect(layout.cardsFitViewport, `${viewport.name}: ${target.path} overflow`)
        .toBe(true);
    }
  }
});

test("homepage alternating sections use viewport-wide tinted backgrounds", async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 1000 });
  await page.goto("/");

  const sections = page.locator([
    ".home-expertise-preview",
    ".home-approach-section",
    ".selected-publications-section",
    ".home-background-section"
  ].join(", "));
  const fullBleed = await sections.evaluateAll((sections) =>
    sections.map((section) => {
      const background = getComputedStyle(section, "::before");
      return {
        width: Math.round(Number.parseFloat(background.width)),
        color: background.backgroundColor
      };
    })
  );

  expect(fullBleed).toHaveLength(4);
  for (const background of fullBleed) {
    expect(background.width).toBe(1440);
    expect(background.color).not.toBe("rgba(0, 0, 0, 0)");
  }
});

test("migrated ordinary pages fit representative viewports", async ({ page }) => {
  for (const viewport of responsiveViewports) {
    await page.setViewportSize(viewport);
    for (const path of ["/teaching/", "/news/", "/contact/", "/presentations/", "/supervision/", "/cv/"]) {
      await page.goto(path);
      const dimensions = await page.evaluate(() => ({
        documentWidth: document.documentElement.scrollWidth,
        viewportWidth: window.innerWidth
      }));
      expect(dimensions.documentWidth, `${viewport.name}: ${path} overflow`)
        .toBeLessThanOrEqual(dimensions.viewportWidth);
    }
  }
});
