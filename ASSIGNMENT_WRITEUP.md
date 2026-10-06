# FIT3179 Data Visualisation 2 — Assignment write-up

| Field | |
| --- | --- |
| Name | |
| Student ID | |
| Studio Session | |

---

## Part A: URL of the Visualisation

**Pending your GitHub Pages URL.** Follow `PUBLISH.md`, then paste the live URL below and test it in an incognito window. (Or send me the URL and I will fill this box.)

```
[GitHub Pages URL — pending — see PUBLISH.md]
```

Tip: Test your URL in incognito mode to ensure it is a working URL.

---

## Part B: Domain Description

### 1. Overall description

#### Domain

Volunteer organisations and unpaid voluntary work in Australia — who participates formally through organisations, where participation is higher or lower geographically, which organisation types attract volunteers, how rates and hours have changed since before COVID, and what barriers keep people from volunteering.

#### Who

The average Australian reader (Clayton campus audience). No specialist statistics knowledge is assumed. Terms such as *formal volunteering* (unpaid help given through an organisation), *informal volunteering* (unpaid help outside an organisation), *SA4* (Statistical Area Level 4 — a regional Census geography), and *Albers / equal-area map projection* are introduced in plain language on the page when first used.

#### Why (overall goal)

Australians hear that “volunteering is down” and that clubs and charities are short of helpers, but they rarely see participation, geography, organisation type, hours, and barriers in one guided story. The visualisation is explanatory (**presentation, not an expert exploration tool**). It walks a general reader through five linked acts: (1) where people still volunteer, (2) who steps forward by age and over time, (3) what organisation types they join and how formal/informal roles overlap, (4) how hours and contribution recovered even when the rate stayed soft, and (5) why people do or do not volunteer — with implications for volunteer-involving organisations.

#### What (overall data)

Public tables from multiple Australian sources, combined across datasets (not fabricated). Main sources:

- **ABS General Social Survey: Summary Results, Australia, 2025** (Tables 1, 7, 10–13) — national formal/informal rates by age and remoteness, organisation types, hours bands, reasons for/against volunteering.
- **ABS Census 2021** unpaid voluntary work (**VOLWP** / GCP table **G23**) at **SA4** and **state/territory** — geographic rates and counts.
- **ABS ASGS Edition 3** digital boundaries (STE, SA4) — map geometries, simplified for web size.
- **ABS Measuring What Matters — Social connections** — longer formal volunteering rate series used for context in planning (2019–2025 slope on the page uses GSS Table 1.3).
- **Snapshot of Volunteering in Australia 2023** — formal / informal / both population shares for the Sankey structure view (different definition from ABS; labelled on the page).
- **ACNC Australian Charities Report, 11th edition** — charity-reported volunteer totals (~3.77 million) for contribution context.

Keys identify year, age group, remoteness, organisation type, SA4/state, hours band, or reason; values are percentages, person counts, and hours (millions). Slim CSV/GeoJSON files live under `data/`; human-readable Vega-Lite/Vega specs under `specs/`.

#### How (overall idioms)

**Twelve charts.** Advanced idioms: choropleth map, proportional symbol map, dot density map, dumbbell (connected-dot), lollipop, slope chart, treemap, Sankey/alluvial, heatmap, unit/waffle chart, and diverging bar chart. Supporting basic idiom: multi-line/line chart of total formal hours. Each idiom is chosen so position, length, area, or size answers a specific locate / compare / summarise / present task for a general reader.

**Note on marks:** Following Munzner, only three mark types are used — **point**, **line**, and **area**. Map fills, treemap tiles, heatmap cells, waffle cells, bars, and Sankey bands are area (or area-like) marks; lollipop stems, dumbbell connectors, slope lines, and hours trend are line marks; symbols, dots, and waffle “on” cells as discrete units use point or small area marks depending on the idiom.

**Maps / projections:** All three Australia maps share the same **Albers / conic equal-area** projection (`conicEqualArea`, rotate `[-132, 0]`, parallels `[-18, -36]`). Course Notes: equal-area for comparing magnitudes/rates across regions; conic for mid-latitude landscape countries such as Australia; **no Web Mercator/Mercator** for national thematic maps. Choropleth encodes **rates**; proportional symbols and dots encode **counts**.

---

### 2. Chart-by-chart What / Why / How

---

#### Chart 1 — Choropleth map: Census volunteering rate by SA4

**What?**

| Field | Detail |
| --- | --- |
| Dataset type | Geographic table joined to polygons. Each row is one SA4 with a volunteering rate and volunteer count. |
| Sources / relevance / URL | ABS Census 2021 GCP G23 (VOLWP) + ASGS Ed. 3 SA4 boundaries. Rate = volunteers ÷ (volunteers + not volunteer), excluding not-stated. Files: `data/australia_sa4.geojson`, `data/census_volunteering_sa4.csv`. DataPacks: https://www.abs.gov.au/census/find-census-data/datapacks · Boundaries: https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs/edition-3-july-2021-june-2026/access-and-downloads/digital-boundary-files |
| Keys / values | Key: SA4 code/name. Values: rate (%), volunteer count. |
| Data type — qualitative (categorical) | SA4 region name. |
| Data type — ordered (quantitative) | Volunteering rate (%), ratio scale; volunteer count. |

**Why?**

| Field | Detail |
| --- | --- |
| Goal | Show that formal volunteering *rates* vary across Australia — e.g. Wheat Belt ~26.8% vs Sydney – South West ~6.8% — so the story starts with geography, not a single national headline. |
| Munzner — actions + targets | Query + locate → which regions have high/low rates. Query + compare → regional vs metro bands. Analyse + consume (present) → uneven participation map. |
| Function / form | Explanatory choropleth; hover for region name, rate, and count. |

**How?**

| Field | Detail |
| --- | --- |
| Idiom | Choropleth map |
| Marks | Area marks (filled SA4 polygons) |
| Projection | Albers / `conicEqualArea` for Australia (see overall How). Equal-area so colour comparisons of rates are not distorted by inflated northern areas. |

| Channel | Attribute encoded | Attribute type |
| --- | --- | --- |
| Spatial region (geographic) | SA4 polygon | Categorical |
| Colour (sequential teal) | Volunteering rate (%) | Quantitative |
| Text annotation | Highest / lowest named regions | Categorical |

Spec: `specs/map_c1_choropleth.vl.json`

---

#### Chart 2 — Proportional symbol map: volunteer counts by state

**What?**

| Field | Detail |
| --- | --- |
| Dataset type | State polygons + centroid table of volunteer counts. |
| Sources / relevance / URL | ABS Census 2021 G23 STE + ASGS STE boundaries. Files: `data/australia_states.geojson`, `data/state_volunteer_centroids.csv`. Same Census/DataPack URLs as Chart 1. |
| Keys / values | Key: state/territory. Value: volunteer count; rate shown in tooltip. |
| Data type — qualitative | State/territory name. |
| Data type — ordered (quantitative) | Volunteer count (ratio). |

**Why?**

| Field | Detail |
| --- | --- |
| Goal | Show that **counts** pile into NSW and Victoria even where some regional SA4s lead on **rates** — rates and counts must not be confused. |
| Munzner — actions + targets | Query + compare → which states hold the largest volunteer pools. Query + summarise → headcount concentrated in two states. |
| Function / form | Explanatory prop-symbol map; hover for count and rate. |

**How?**

| Field | Detail |
| --- | --- |
| Idiom | Proportional symbol map |
| Marks | Area marks (state outlines) + point marks (circles) |
| Projection | **Same** Albers AU parameters as Chart 1 (Course Notes: keep projection consistent across AU thematic maps). Size encodes **counts** (Course Notes: prop symbols for totals). |

| Channel | Attribute encoded | Attribute type |
| --- | --- | --- |
| Longitude / latitude | Representative point in state | Quantitative |
| Size (area of circle, sqrt scale) | Volunteer count | Quantitative |
| Text | State abbreviation | Categorical |

Spec: `specs/map_c2_prop_symbols.vl.json`

---

#### Chart 3 — Dot density map: volunteer counts as dots

**What?**

| Field | Detail |
| --- | --- |
| Dataset type | Point set derived from state volunteer counts (1 dot ≈ 10,000 volunteers), randomly placed inside state polygons with a fixed seed. |
| Sources / relevance / URL | Same Census STE counts as Chart 2. File: `data/volunteer_dots.geojson`. |
| Keys / values | Key: state. Value: each dot represents 10,000 volunteers. |
| Data type — qualitative | State/territory. |
| Data type — ordered (quantitative) | Dot count proportional to volunteers. |

**Why?**

| Field | Detail |
| --- | --- |
| Goal | Give a intuitive sense of absolute scale: denser dots where more people volunteered — without encoding a rate. |
| Munzner — actions + targets | Query + summarise → density of contribution by state. Query + compare → east-coast concentration vs sparse interiors. |
| Function / form | Explanatory dot density; hover shows state and unit value. |

**How?**

| Field | Detail |
| --- | --- |
| Idiom | Dot density map |
| Marks | Area marks (state outlines) + point marks (dots) |
| Projection | **Same** Albers AU as Charts 1–2. Course Notes Dot Maps: continent-scale dot maps need equal-area so polar/area inflation does not fake density. |

| Channel | Attribute encoded | Attribute type |
| --- | --- | --- |
| Position (lon/lat of dot) | Location within state | Quantitative |
| Number of dots | Volunteer count / 10,000 | Quantitative |

Spec: `specs/map_c3_dot_density.vl.json`

---

#### Chart 4 — Dumbbell: major cities vs remote formal rate

**What?**

| Field | Detail |
| --- | --- |
| Dataset type | Tiny table with two rates for one comparison. |
| Sources / relevance / URL | ABS GSS 2025 Table 7.3 (social experiences by remoteness). File: `data/dumbbell_remoteness.csv`. https://www.abs.gov.au/statistics/people/people-and-communities/general-social-survey-summary-results-australia/latest-release |
| Keys / values | Keys: place type. Values: formal rate (%) — major cities 20.9, remote 34.0. |
| Data type — qualitative | Place (major cities vs remote). |
| Data type — ordered (quantitative) | Formal volunteering rate (%). |

**Why?**

| Field | Detail |
| --- | --- |
| Goal | Make the remoteness gap impossible to miss: remote Australia’s formal rate is about 13 percentage points above major cities. |
| Munzner — actions + targets | Query + compare → cities vs remote on one axis. Analyse + consume → regional communities lean harder on formal volunteering. |
| Function / form | Explanatory connected-dot / dumbbell. |

**How?**

| Field | Detail |
| --- | --- |
| Idiom | Dumbbell / connected-dot chart |
| Marks | Line mark (connector) + point marks (dots) |

| Channel | Attribute encoded | Attribute type |
| --- | --- | --- |
| Position on aligned scale (x) | Formal rate (%) | Quantitative |
| Colour hue | Major cities vs remote | Categorical |

Spec: `specs/chart_c4_dumbbell.vl.json`

---

#### Chart 5 — Lollipop: formal rate by age

**What?**

| Field | Detail |
| --- | --- |
| Dataset type | Table of age groups with formal (and informal) rates. |
| Sources / relevance / URL | ABS GSS 2025 Table 10.3. File: `data/gss_formal_rate_by_age.csv`. Same GSS release URL as Chart 4. |
| Keys / values | Key: age group. Value: formal rate (%) — e.g. 45–54 = 28.0; 25–34 = 13.1. |
| Data type — qualitative | Age group (ordered categories). |
| Data type — ordered (quantitative) | Formal rate (%). |

**Why?**

| Field | Detail |
| --- | --- |
| Goal | Show mid-life peak vs soft young-adult participation — who “still shows up” by age. |
| Munzner — actions + targets | Query + compare → age bands on rate. Query + summarise → 45–54 highest among working ages; 25–34 lowest. |
| Function / form | Explanatory lollipop; peak and trough ages highlighted. |

**How?**

| Field | Detail |
| --- | --- |
| Idiom | Lollipop chart (horizontal) |
| Marks | Line marks (stems) + point marks (dots) |

| Channel | Attribute encoded | Attribute type |
| --- | --- | --- |
| Spatial region (y) | Age group | Categorical (ordered) |
| Size (length on x) | Formal rate (%) | Quantitative |
| Colour | Highlight vs other ages | Categorical |

Spec: `specs/chart_c5_lollipop.vl.json`

---

#### Chart 6 — Slope chart: formal vs informal rates, 2019→2025

**What?**

| Field | Detail |
| --- | --- |
| Dataset type | Long table: series × year × rate. |
| Sources / relevance / URL | ABS GSS 2025 Table 1.3 (2019 and 2025 proportions). File: `data/slope_formal_informal.csv`. Formal: 29.5% → 22.6%; informal: 33.4% → 29.5%. |
| Keys / values | Keys: series (formal/informal), year. Value: rate (%). |
| Data type — qualitative | Series name; year as ordinal. |
| Data type — ordered (quantitative) | Participation rate (%). |

**Why?**

| Field | Detail |
| --- | --- |
| Goal | Show the post-2019 softening: formal volunteering fell more sharply than informal help, but both eased. |
| Munzner — actions + targets | Query + compare → 2019 vs 2025 within each series. Query + compare → formal vs informal slopes. |
| Function / form | Explanatory slope chart (two time points). |

**How?**

| Field | Detail |
| --- | --- |
| Idiom | Slope chart |
| Marks | Line marks (slopes) + point marks (endpoints) |

| Channel | Attribute encoded | Attribute type |
| --- | --- | --- |
| Position on x (ordinal) | Year (2019, 2025) | Categorical ordered |
| Position on y | Rate (%) | Quantitative |
| Colour hue | Formal vs informal series | Categorical |

Spec: `specs/chart_c6_slope.vl.json`

---

#### Chart 7 — Treemap: organisation types among formal volunteers

**What?**

| Field | Detail |
| --- | --- |
| Dataset type | Table of organisation types with share of formal volunteers (%). Precomputed squarified layout in CSV. |
| Sources / relevance / URL | ABS GSS 2025 Table 11.3. File: `data/treemap_org_types.csv` (from `gss_org_types.csv`). Sport/recreation 33.3%; faith 22.9%; community/cultural 17.6%. People may name more than one type — shares need not sum to 100. |
| Keys / values | Key: organisation type. Value: share of volunteers (%). |
| Data type — qualitative | Organisation type. |
| Data type — ordered (quantitative) | Share (%); tile area. |

**Why?**

| Field | Detail |
| --- | --- |
| Goal | Show which organisation sectors dominate formal volunteering — sport first, then faith and community. |
| Munzner — actions + targets | Query + compare → relative size of org types. Query + summarise → sport is the largest tile. |
| Function / form | Explanatory treemap; sport highlighted. |

**How?**

| Field | Detail |
| --- | --- |
| Idiom | Treemap |
| Marks | Area marks (tiles) |

| Channel | Attribute encoded | Attribute type |
| --- | --- | --- |
| Size (area of tile) | Share of volunteers (%) | Quantitative |
| Colour hue | Sport vs other types | Categorical |
| Text | Short type label (large tiles) | Categorical |

Spec: `specs/chart_c7_treemap.vl.json`

---

#### Chart 8 — Sankey / alluvial: formal, informal, both, neither

**What?**

| Field | Detail |
| --- | --- |
| Dataset type | Flow table of population shares from Snapshot 2023; precomputed node/link geometry for Vega. |
| Sources / relevance / URL | Snapshot of Volunteering in Australia 2023 (formal 31.8%, informal 42.7%, both 24.5%; formal-only / informal-only / neither implied). Files: `data/sankey_nodes.json`, `data/sankey_links.json`. **Not ABS** — labelled as a structure view; Snapshot’s “any volunteering” headline (64%) uses a broader framing. |
| Keys / values | Keys: source/target categories. Value: % of adults. |
| Data type — qualitative | Volunteer-role category. |
| Data type — ordered (quantitative) | Population share (%). |

**Why?**

| Field | Detail |
| --- | --- |
| Goal | Show that “volunteering” is not only formal organisational work — informal help and overlap matter for organisations recruiting helpers. |
| Munzner — actions + targets | Query + summarise → part-to-whole of adult population across roles. Query + compare → band widths. |
| Function / form | Explanatory Sankey; hover for destination share. |

**How?**

| Field | Detail |
| --- | --- |
| Idiom | Sankey / alluvial diagram (Vega) |
| Marks | Area marks (flow bands and node bars) |

| Channel | Attribute encoded | Attribute type |
| --- | --- | --- |
| Size (band height / width) | Population share (%) | Quantitative |
| Colour | Destination category | Categorical |
| Spatial region | Left (all adults) → right (roles) | Categorical |

Spec: `specs/chart_c8_sankey.vg.json`

---

#### Chart 9 — Heatmap: hours band × age among formal volunteers

**What?**

| Field | Detail |
| --- | --- |
| Dataset type | Matrix table: age group × hours band → share of that age’s formal volunteers (%). |
| Sources / relevance / URL | ABS GSS 2025 Table 12.3. File: `data/gss_hours_by_age_heatmap.csv`. |
| Keys / values | Keys: age group, hours band (1–20; 21–99; 100+). Value: share (%). |
| Data type — qualitative | Age group; hours band. |
| Data type — ordered (quantitative) | Share within age (%). |

**Why?**

| Field | Detail |
| --- | --- |
| Goal | Show that older formal volunteers are more likely to give 100+ hours, while younger volunteers cluster in fewer hours. |
| Munzner — actions + targets | Query + compare → cells across ages and bands. Query + summarise → where “heavy” hours sit. |
| Function / form | Explanatory heatmap with numeric labels. |

**How?**

| Field | Detail |
| --- | --- |
| Idiom | Heatmap |
| Marks | Area marks (cells) |

| Channel | Attribute encoded | Attribute type |
| --- | --- | --- |
| Spatial region (row) | Age group | Categorical |
| Spatial region (column) | Hours band | Categorical |
| Colour | Share of age group (%) | Quantitative |
| Text | Share value | Quantitative |

Spec: `specs/chart_c9_heatmap.vl.json`

---

#### Chart 10 — Line chart: total formal volunteer hours 2019–2025

**What?**

| Field | Detail |
| --- | --- |
| Dataset type | Time series of national formal hours (millions). |
| Sources / relevance / URL | ABS GSS 2025 Table 12.1 (2025 = **618.2** million hours); 2019 = 596M and 2020 = 490M from the ABS GSS release narrative. File: `data/gss_formal_hours_trend.csv`. |
| Keys / values | Key: year. Value: total hours (millions). |
| Data type — qualitative | Year (ordinal). |
| Data type — ordered (quantitative) | Hours (millions), ratio. |

**Why?**

| Field | Detail |
| --- | --- |
| Goal | Show that total hours recovered after the 2020 dip even while the *participation rate* stayed soft — contribution is not the same as prevalence. |
| Munzner — actions + targets | Query + compare → years on hours. Query + summarise → 2025 above 2019 after the COVID trough. |
| Function / form | Explanatory line chart (**basic** idiom supporting the advanced set). |

**How?**

| Field | Detail |
| --- | --- |
| Idiom | Single-line chart with points |
| Marks | Line mark + point marks |

| Channel | Attribute encoded | Attribute type |
| --- | --- | --- |
| Position on x | Year | Categorical ordered |
| Position on y | Total hours (millions) | Quantitative |

Spec: `specs/chart_c10_hours_line.vl.json`

---

#### Chart 11 — Unit / waffle: ~23 in 100 vs ~14 in 100

**What?**

| Field | Detail |
| --- | --- |
| Dataset type | Two 10×10 grids of unit cells (volunteer vs not). |
| Sources / relevance / URL | Left panel: GSS 2025 formal rate **22.6%** ≈ 23 cells. Right panel: Census 2021 national rate **~14%** (14.1% including not-stated). File: `data/waffle_compare.csv`. GSS and Census differ in timing, definition, and COVID conditions — shown side by side, not spliced into one trend. |
| Keys / values | Key: panel + cell. Value: status (volunteer / not). |
| Data type — qualitative | Panel; status. |
| Data type — ordered (quantitative) | Implied count of filled cells / 100. |

**Why?**

| Field | Detail |
| --- | --- |
| Goal | Give an intuitive “out of 100 adults” reading of today’s GSS formal rate, and warn that Census 2021 is a different, lower snapshot. |
| Munzner — actions + targets | Query + summarise → part-to-whole of 100 units. Query + compare → GSS vs Census panels. |
| Function / form | Explanatory unit / waffle chart. |

**How?**

| Field | Detail |
| --- | --- |
| Idiom | Unit / waffle chart (faceted) |
| Marks | Area marks (small squares) |

| Channel | Attribute encoded | Attribute type |
| --- | --- | --- |
| Spatial region (row/col) | Cell position in 10×10 grid | Categorical |
| Colour | Volunteer vs not | Categorical |
| Facet | Survey/source panel | Categorical |

Spec: `specs/chart_c11_waffle.vl.json`

---

#### Chart 12 — Diverging bars: reasons for vs against volunteering

**What?**

| Field | Detail |
| --- | --- |
| Dataset type | Top reasons among formal volunteers (GSS Table 11.3) and among non-volunteers (Table 13.3), signed for diverging layout. |
| Sources / relevance / URL | ABS GSS 2025. File: `data/reasons_diverging.csv`. Examples: help others 65.2%; personal satisfaction 62.8%; no time 47.0%; not interested 35.5%. Multiple responses allowed. |
| Keys / values | Key: reason text. Value: share (%); polarity for/against. |
| Data type — qualitative | Reason; polarity. |
| Data type — ordered (quantitative) | Share (%). |

**Why?**

| Field | Detail |
| --- | --- |
| Goal | Close the story with motivations and barriers organisations actually face — time and interest on one side; helping others and satisfaction on the other. |
| Munzner — actions + targets | Query + compare → reasons within each polarity. Query + summarise → “no time” and “help others” dominate their sides. |
| Function / form | Explanatory diverging bar chart. |

**How?**

| Field | Detail |
| --- | --- |
| Idiom | Diverging bar chart |
| Marks | Area marks (bars) |

| Channel | Attribute encoded | Attribute type |
| --- | --- | --- |
| Spatial region (y) | Reason | Categorical |
| Size (length on x, signed) | Share (%) | Quantitative |
| Colour hue | For vs against volunteering | Categorical |

Spec: `specs/chart_c12_diverging.vl.json`

---

### AI acknowledgement (Part B / page)

Generative AI (Cursor) assisted with dataset discovery, cleaning scripts, Vega-Lite/Vega specifications, page layout, narrative drafting, and this write-up’s structure. All plotted statistics were taken from the public ABS, Snapshot, and ACNC sources listed above and checked against downloaded tables (`data/verified_claims.json`). See also `AI_ACKNOWLEDGEMENT.txt` in the repository and the footer on the visualisation page.

---

## Part C: Sketch

**Sketch already completed by me.** I will paste the sketch PDF URL and/or screenshot into Moodle myself.

Do **not** create sketch assets in this repository for Part C.

```
[Sketch PDF URL on GitHub — student to paste in Moodle]
```

---

## Part D: Full-size screenshot of your DV II

**TODO after GitHub Pages publish (Step 6).**  
Paste a full-page screenshot of the live visualisation from the Part A URL.

```
[Full-size screenshot — pending publish]
```

---

*End of write-up draft for Moodle Part B. Fill Name / Student ID / Studio Session and Parts A & D when the site is live.*
