// Dynamically show only the active content tab's headings in the table of contents (TOC)
document.addEventListener("DOMContentLoaded", () => {
  function syncTocWithActiveTabs() {
    // Find all content tab containers
    const tabContainers = document.querySelectorAll(".tabbed-set");
    if (!tabContainers.length) return;

    // Collect IDs of headings located inside inactive tabs
    const hiddenHeadingIds = new Set();
    const visibleHeadingIds = new Set();

    tabContainers.forEach(container => {
      const inputs = container.querySelectorAll("input");
      const blocks = container.querySelectorAll(".tabbed-block");

      inputs.forEach((input, index) => {
        const block = blocks[index];
        if (!block) return;

        const headings = block.querySelectorAll("[id]");
        if (input.checked) {
          headings.forEach(h => visibleHeadingIds.add(h.id));
        } else {
          headings.forEach(h => hiddenHeadingIds.add(h.id));
        }
      });
    });

    // Toggle corresponding TOC links in the right navigation bar
    const tocLinks = document.querySelectorAll(".md-sidebar--secondary .md-nav__link");
    tocLinks.forEach(link => {
      const href = link.getAttribute("href") || "";
      const hash = href.startsWith("#") ? href.slice(1) : href.split("#")[1];
      if (!hash) return;

      const listItem = link.closest(".md-nav__item");
      if (!listItem) return;

      if (hiddenHeadingIds.has(hash) && !visibleHeadingIds.has(hash)) {
        listItem.style.display = "none";
      } else if (visibleHeadingIds.has(hash)) {
        listItem.style.display = "";
      }
    });
  }

  // Initial sync
  syncTocWithActiveTabs();

  // Listen for tab switches
  document.addEventListener("change", (e) => {
    if (e.target && e.target.matches(".tabbed-set input")) {
      setTimeout(syncTocWithActiveTabs, 10);
    }
  });

  // Also support MkDocs instant navigation
  if (typeof location$ !== "undefined") {
    location$.subscribe(() => {
      setTimeout(syncTocWithActiveTabs, 50);
    });
  }
});
