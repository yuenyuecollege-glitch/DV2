const THEME = {
  background: null,
  font: "Source Sans 3",
  title: {
    font: "Literata",
    fontSize: 20,
    fontWeight: 650,
    color: "#0d1b24",
    subtitleFont: "Source Sans 3",
    subtitleFontSize: 15,
    subtitleColor: "#4a5863",
    offset: 8,
  },
  axis: {
    labelFont: "Source Sans 3",
    titleFont: "Source Sans 3",
    labelColor: "#4a5863",
    titleColor: "#4a5863",
    domainColor: "#cfd6d0",
    gridColor: "#e8ecea",
    tickColor: "#cfd6d0",
    labelFontSize: 15,
    titleFontSize: 15,
  },
  legend: {
    labelFont: "Source Sans 3",
    titleFont: "Source Sans 3",
    labelColor: "#4a5863",
    titleColor: "#0d1b24",
    labelFontSize: 15,
    titleFontSize: 15,
    symbolSize: 120,
  },
  header: {
    labelFont: "Source Sans 3",
    titleFont: "Literata",
    labelColor: "#0d1b24",
    labelFontSize: 15,
    titleFontSize: 16,
  },
  view: { stroke: "transparent" },
};

const SPEC_VERSION = "20261009ad";

const CHARTS = [
  ["#map-c1", "specs/map_c1_choropleth.vl.json"],
  ["#map-c2", "specs/map_c2_prop_symbols.vl.json"],
  ["#map-c3", "specs/map_c3_dot_density.vl.json"],
  ["#chart-c4", "specs/chart_c4_radial.vg.json"],
  ["#chart-c5", "specs/chart_c5_lollipop.vl.json"],
  ["#chart-c6", "specs/chart_c6_rate_bar.vl.json"],
  ["#chart-c7", "specs/chart_c7_treemap.vg.json"],
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

function sizeFor(el) {
  const styles = getComputedStyle(el);
  const padX =
    (parseFloat(styles.paddingLeft) || 0) + (parseFloat(styles.paddingRight) || 0);
  const padY =
    (parseFloat(styles.paddingTop) || 0) + (parseFloat(styles.paddingBottom) || 0);
  const width = Math.max(320, Math.floor((el.clientWidth || el.offsetWidth) - padX));
  const height = Math.max(
    320,
    Math.floor((el.clientHeight || el.offsetHeight || 640) - padY)
  );
  return { width, height };
}

function prepareSpec(selector, spec, width, height) {
  const next = JSON.parse(JSON.stringify(spec));

  if (selector === "#chart-c7") {
    next.width = width;
    next.height = height;
    next.autosize = { type: "none" };
    if (next.data && next.data[0] && next.data[0].transform) {
      const treemap = next.data[0].transform.find((t) => t.type === "treemap");
      if (treemap) treemap.size = [width, height];
    }
  }

  if (selector === "#chart-c11" && next.spec) {
    const panelW = Math.floor((width - 56) / 2);
    const panelH = Math.max(300, Math.min(height - 96, panelW));
    next.spec.width = Math.max(300, panelW);
    next.spec.height = panelH;
  }

  if (selector === "#chart-c4") {
    const side = Math.min(width, height);
    const chart = Math.max(400, Math.min(500, side - 100));
    next.width = chart;
    next.height = chart;
  }

  if (selector === "#chart-c9") {
    const plotW = Math.max(400, Math.min(480, width - 320));
    const plotH = Math.max(300, Math.min(380, height - 100));
    next.width = plotW;
    next.height = plotH;
    next.padding = { left: 24, right: 118, top: 12, bottom: 12 };
  }

  return next;
}

function embedAll() {
  return Promise.all(
    CHARTS.map(([selector, specPath]) => {
      const el = document.querySelector(selector);
      if (!el) return Promise.resolve();
      const { width, height } = sizeFor(el);
      const bust = `${specPath}?v=${SPEC_VERSION}`;
      const embedOpts = { ...options };

      if (selector === "#chart-c7") {
        embedOpts.width = width;
        embedOpts.height = height;
      }

      return fetch(bust)
        .then((res) => {
          if (!res.ok) throw new Error(`Failed to load ${specPath}`);
          return res.json();
        })
        .then((spec) =>
          vegaEmbed(el, prepareSpec(selector, spec, width, height), embedOpts)
        )
        .then((result) => {
          if (selector === "#chart-c7" && result && result.view) {
            result.view.width(width).height(height).runAsync();
          }
          return result;
        })
        .catch((err) => {
          el.textContent =
            "This chart could not be loaded. Open the page over http://, not as a local file.";
          console.error(specPath, err);
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
