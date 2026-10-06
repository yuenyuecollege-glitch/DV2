const THEME = {
  background: null,
  font: "Source Sans 3",
  title: {
    font: "Literata",
    fontSize: 15,
    fontWeight: 650,
    color: "#15202b",
    subtitleFont: "Source Sans 3",
    subtitleFontSize: 12,
    subtitleColor: "#5a6670",
  },
  axis: {
    labelFont: "Source Sans 3",
    titleFont: "Source Sans 3",
    labelColor: "#5a6670",
    titleColor: "#5a6670",
    domainColor: "#d5d8cc",
    gridColor: "#e8ecea",
    tickColor: "#d5d8cc",
    labelFontSize: 12,
    titleFontSize: 12,
  },
  legend: {
    labelFont: "Source Sans 3",
    titleFont: "Source Sans 3",
    labelColor: "#5a6670",
    titleColor: "#15202b",
    labelFontSize: 12,
    titleFontSize: 12,
  },
  header: {
    labelFont: "Source Sans 3",
    titleFont: "Literata",
    labelColor: "#15202b",
  },
  view: { stroke: "transparent" },
};

const CHARTS = [
  ["#map-c1", "specs/map_c1_choropleth.vl.json"],
  ["#map-c2", "specs/map_c2_prop_symbols.vl.json"],
  ["#map-c3", "specs/map_c3_dot_density.vl.json"],
  ["#chart-c4", "specs/chart_c4_dumbbell.vl.json"],
  ["#chart-c5", "specs/chart_c5_lollipop.vl.json"],
  ["#chart-c6", "specs/chart_c6_slope.vl.json"],
  ["#chart-c7", "specs/chart_c7_treemap.vl.json"],
  ["#chart-c8", "specs/chart_c8_sankey.vg.json"],
  ["#chart-c9", "specs/chart_c9_heatmap.vl.json"],
  ["#chart-c10", "specs/chart_c10_hours_line.vl.json"],
  ["#chart-c11", "specs/chart_c11_waffle.vl.json"],
  ["#chart-c12", "specs/chart_c12_diverging.vl.json"],
];

const options = {
  actions: false,
  renderer: "svg",
  config: THEME,
};

function embedAll() {
  return Promise.all(
    CHARTS.map(([selector, spec]) => {
      const el = document.querySelector(selector);
      if (!el) return Promise.resolve();
      return vegaEmbed(el, spec, options).catch((err) => {
        el.textContent =
          "This chart could not be loaded. Open the page over http://, not as a local file.";
        console.error(spec, err);
      });
    })
  );
}

function watchSections() {
  const links = [...document.querySelectorAll(".sections a")];
  const sections = links
    .map((link) => document.querySelector(link.getAttribute("href")))
    .filter(Boolean);
  if (!sections.length || !("IntersectionObserver" in window)) return;
  const observer = new IntersectionObserver(
    (entries) => {
      const visible = entries
        .filter((e) => e.isIntersecting)
        .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
      if (!visible) return;
      links.forEach((link) => {
        link.toggleAttribute(
          "aria-current",
          link.getAttribute("href") === `#${visible.target.id}`
        );
      });
    },
    { rootMargin: "-20% 0px -65% 0px", threshold: [0.1, 0.25, 0.5] }
  );
  sections.forEach((section) => observer.observe(section));
}

embedAll();
watchSections();
