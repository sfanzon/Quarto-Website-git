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
    await page.goto("/index.html");

    const layout = await page.evaluate(() => {
      const bounds = (selector) => {
        const rect = document.querySelector(selector).getBoundingClientRect();
        return { left: rect.left, right: rect.right };
      };

      return {
        navbar: bounds(".navbar-container"),
        footer: bounds(".site-footer-inner"),
        brand: bounds(".navbar-title")
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

test("desktop search icon aligns with the navbar shell", async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 1000 });
  await page.goto("/index.html");

  const layout = await page.evaluate(() => {
    const navbar = document.querySelector(".navbar-container").getBoundingClientRect();
    const icon = document.querySelector("#quarto-search svg").getBoundingClientRect();
    return { navbarRight: navbar.right, iconRight: icon.right };
  });

  expectAligned(layout.iconRight, layout.navbarRight, "desktop: search icon right edge");
});
