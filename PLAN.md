# PLAN.md — FIT3179 DV2

**Topic:** Volunteer Organisations  
**Audience:** Average Australian (Clayton) — presentation / storytelling, not an explorer  
**Status:** Step 6 checklist ready — see `PUBLISH.md`. **Part A/D still need your live GitHub Pages URL.**

---

## 1. Working title, dek, hero stats

**Working title:** Who still shows up?  
**Subtitle / dek:** Formal volunteering through organisations has slipped since before COVID — but Australians still give hundreds of millions of hours, and regional communities lean on volunteers more than the big cities.

**Hero stats** (verified Step 2 against downloaded files — see `data/verified_claims.json`):

| Stat | Claim | Source |
| --- | --- | --- |
| **22.6%** (~**23 in 100**) | Share of Australians 15+ who did unpaid voluntary work *through an organisation* in the prior 12 months | ABS GSS 2025 Table 10.3 / 1.3 |
| **618.2 million** | Formal volunteer hours in the prior 12 months (up from **490M** in 2020; **596M** in 2019) | ABS GSS 2025 Table 12.1; 2019/2020 from GSS release narrative |
| **34.0% vs 20.9%** | Remote Australia vs major cities formal volunteering rate | ABS GSS 2025 Table 7.3 |

*Optional footnote hero (contribution act, different definition):* Snapshot of Volunteering 2023 estimates **3.2 billion** hours including informal help, and models ~**$566 billion** in benefits — label as a broader/modelled figure, not ABS official.

---

## 2. Story sections (5)

Spine adapted from the suggested prompt + GSS/Census/ACNC evidence.

| # | Section | Core claim | Charts |
| --- | --- | --- | --- |
| 1 | **Where people still volunteer** | Participation is uneven across Australia: Census rates vary by region; remote/regional GSS rates beat major cities; raw volunteer *counts* pile into populous states. | C1–C3 maps, C4 |
| 2 | **Who steps forward** | Peak formal rates sit in mid-life (45–54 = **28.0%**); youngest adults lag (25–34 = **13.1%**). | C5, C6 |
| 3 | **What they do** | Sport/recreation orgs lead (**33.3%**), then faith (**22.9%**) and community/cultural (**17.6%**). Formal vs informal split matters for organisations. | C7, C8 |
| 4 | **Hours and contribution** | Hours recovered after 2020 even while the *rate* stayed soft; charities report **3.77M** volunteers (ACNC). | C9, C10, C11 |
| 5 | **Why people don’t — and what orgs face** | “No time” (**47%**) and “not interested” (**35.5%**) dominate non-volunteering; volunteer-run charities are the organisational backbone. | C12 |

Footer on page: author, date, source URLs, AI acknowledgement.

---

## 3. Chart list (≥11 charts; ★ = advanced; MAP = map idiom)

**Count:** 12 charts · **Advanced ★:** 10 · **Distinct map idioms:** 3  
**Basic idioms used:** multi-line, sorted horizontal bar (≤2) — HD asks ≥8 advanced across >10 charts.

### Maps (exactly 3 distinct idioms — same AU projection)

All three Australia maps use **Albers / conic equal-area** tuned for Australia (Course Notes: equal-area for magnitude/rate comparison; conic for mid-latitude countries; **no Web Mercator/Mercator** for AU thematic maps). Same projection parameters across all three AU maps.

| ID | ★ / MAP | Idiom | Data → question | Projection / Course Notes justification |
| --- | --- | --- | --- | --- |
| **C1** | ★ MAP | **Choropleth** | Census 2021 volunteering *rate* (%) by **SA4** (VOLWP) — where is participation high relative to population? | Equal-area Albers AU. Choropleth encodes **rates** (Course Notes + standing rules), not raw counts. Area marks + sequential colour. |
| **C2** | ★ MAP | **Proportional symbol** | Census 2021 volunteer *counts* by **state/territory** (centroids) — which jurisdictions hold the largest absolute volunteer pools? | Same Albers AU. Prop symbols encode **counts** (size channel); Course Notes: circles OK for ≤ few dozen items (8 states/territories). |
| **C3** | ★ MAP | **Dot density** | Same state volunteer counts as dots (e.g. 1 dot ≈ 10,000 volunteers) placed within state polygons — denser dots where more people volunteer (counts, not rates). | Same Albers AU. Dot maps need equal-area (Course Notes Dot Maps). Point marks; unit value chosen for readability. |

*Why not three choropleths / Mercator / flow?* Distinct idioms only. No natural origin–destination volunteer flows in public ABS tables — flow map deferred unless a credible OD source appears in Step 2.

### Non-map charts

| ID | ★ | Idiom | Story beat | Primary source |
| --- | --- | --- | --- | --- |
| **C4** | ★ | **Dumbbell / connected-dot** | Major cities (20.9%) vs remote (34.0%) formal rate 2025 — the geography gap in one glance | GSS 2025 Table 7.3 |
| **C5** | ★ | **Lollipop** | Formal volunteering rate by age (15–24 … 65+) | GSS 2025 age table / Table 10 |
| **C6** | ★ | **Slope chart** | Formal volunteering rate over time (≈2006–2025; include 2019→2020 COVID drop) | ABS Measuring What Matters “Social connections” + GSS releases |
| **C7** | ★ | **Treemap** | Share of volunteers by organisation type (sport 33%, faith 23%, community/cultural 18%, …) | GSS 2025 Table 11 |
| **C8** | ★ | **Sankey / alluvial** | Formal / informal / both (Snapshot 2023 population shares) — how “volunteering” splits beyond formal orgs | Snapshot of Volunteering in Australia 2023 |
| **C9** | ★ | **Heatmap** | Annual hours band × age among formal volunteers | GSS 2025 Table 12 |
| **C10** | basic | **Multi-line** | Total formal hours: 2019 (596M) → 2020 (490M) → 2025 (618M) | GSS releases |
| **C11** | ★ | **Unit / waffle chart** | “About 23 in 100 adults volunteer formally” (2025) — optional second row for Census 2021 ≈14 in 100 with caption explaining COVID-timing difference | GSS 2025 + Census 2021 headline |
| **C12** | ★ | **Diverging bar** | Top reasons *for* volunteering vs top reasons *for not* volunteering | GSS 2025 narrative / Tables 11 & 13 |

**Interactivity (light, purposeful):** hover tooltips on maps (area name, rate/count); optional highlight of sport tile on treemap; no section-swapping UI.

**Fallback idioms if a source fails in Step 2** (still ★ / still ≥8 advanced):

- Replace C8 Sankey with ★ **stacked area** of formal vs informal rates over years (ABS Social connections) — stacked area is *basic*; prefer ★ **bump** of top org types if multi-year Table 11 exists, else ★ **radial bar** of Snapshot activity types (sport/recreation 21.8%, etc.).
- Replace C3 dot density with ★ **bin (hex) map** of SA2 rates if SA4 choropleth + state dots feel redundant (Course Notes Bin Maps: equal-area tessellation).
- Replace C11 waffle with ★ **isotype** of ACNC volunteers by charity size (extra-small → extra-large).

---

## 4. Candidate data URLs → charts

### Primary statistical sources (≥2 required)

| # | Source | What it gives | Charts | URL |
| --- | --- | --- | --- | --- |
| A | **ABS General Social Survey: Summary Results, Australia, 2025** | Formal volunteering rates (age, sex, remoteness), org types, hours, reasons; Tables 10–13 XLSX | C4–C7, C9–C12, hero stats | https://www.abs.gov.au/statistics/people/people-and-communities/general-social-survey-summary-results-australia/latest-release |
| B | **ABS Measuring What Matters — Social connections (voluntary work)** | Longer formal (+ informal) rate time series CSV/XLSX | C6, optional informal series | https://www.abs.gov.au/statistics/measuring-what-matters/measuring-what-matters-themes-and-indicators/cohesive/social-connections |
| C | **ABS Census 2021 — Unpaid work and care** + **VOLWP** | National count 2,933,646; rate ~14.1%; DataPacks for STE/SA4 rates & counts | C1–C3, C11 footnote | https://www.abs.gov.au/statistics/people/people-and-communities/unpaid-work-and-care-census/latest-release · Dictionary: https://www.abs.gov.au/census/guide-census-data/census-dictionary/2021/variables-topic/unpaid-work-and-care/voluntary-work-organisation-or-group-volwp · DataPacks: https://www.abs.gov.au/census/find-census-data/datapacks |
| D | **ACNC Australian Charities Report — 11th edition** (2023 AIS) | ~3.77M charity volunteers; volunteers per employee; size breakdown; volunteer-run charities companion | C11 alt / contribution annotations; Section 5 text | https://www.acnc.gov.au/tools/reports/australian-charities-report-11th-edition · Volunteer-run companion: https://www.acnc.gov.au/tools/reports/charity-numbers-volunteer-effect · AIS open data via data.gov.au |

### Secondary / contextual (use carefully; label definitions)

| # | Source | What it gives | Charts | URL |
| --- | --- | --- | --- | --- |
| E | **Snapshot of Volunteering in Australia 2023** (State & Territory peak bodies / TCfV) | Formal 31.8% / informal 42.7% / both; 3.2B hours; activity mix; modelled $566B benefits | C8, contribution callouts | https://www.volunteering.com.au/wp-content/uploads/2025/04/04058-TCfV-Snapshot-of-Volunteering-2023-FULL-Report-Final.pdf |
| F | **Volunteering Australia — GSS 2025 commentary PDF** | Plain-language bridge of ABS GSS (useful for narrative tone, not a third primary cube) | Text only | https://www.volunteeringaustralia.org/wp-content/uploads/VA-GSS-Report-EXPANDED.pdf |

### Geography

| # | Source | Use | URL |
| --- | --- | --- | --- |
| G | **ABS ASGS Ed. 3 digital boundaries** (STE, SA4 shapefile/GeoPackage → slim GeoJSON/TopoJSON in Step 2) | Map base geometries | https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs/edition-3-july-2021-june-2026/access-and-downloads/digital-boundary-files |
| H | Optional: **Natural Earth** admin-1 Australia if ASGS too heavy | Fallback state polygons | https://www.naturalearthdata.com/ |

**Minimum two sources for the page:** A + C (GSS + Census). ACNC (D) and/or Snapshot (E) strengthen “organisations / contribution” without replacing ABS for rates.

---

## 5. Open risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| **GSS vs Census rates disagree** (GSS 2025 **22.6%** formal vs Census 2021 **14.1%** incl. not stated / **15.1%** excl.) | Reader confusion; interview trap | Always name the source, year, and definition. Prefer GSS for national “today” story; Census for geography. |
| **Snapshot formal rate (31.8%) ≠ GSS (22.6%)** | Mixing series looks like fabrication | Keep Snapshot for formal/informal/both structure (C8); never splice into GSS time series. |
| **Snapshot union math** (formal+informal−both ≈ 50% vs headline 64.3% any) | Sankey “Neither” is implied, not published | Caption C8 as “implied from published formal/informal/both shares”; do not claim ABS. |
| **GSS has no state volunteering cube** | Confirmed Step 2 — Table 10 has no STE | Maps use **Census SA4/STE**; GSS for remoteness/age/org/hours (Table 7, 10–13). |
| **Vega-Lite projection limits** | Albers AU needs custom `rotate` / `parallels` | Use Vega `projection`; avoid Web Mercator. |
| **SA4 GeoJSON size** | Was ~5MB @ 5% simplify | Re-simplified to **~1.7MB SA4 + ~1.5MB STE**; slim payload **~3.2MB**. Further TopoJSON optional in Step 3–4. |
| **Dot density placement** | Random dots in polygons | Unit = **10,000 volunteers/dot**; seed fixed (3179); state-level only. |
| **Table 11 org types** | Resolved — full 15 types in `gss_org_types.csv` | Treemap ready. |
| **ACNC AIS full dump** | Avoided | Used published Charities Report 11th ed aggregates only. |
| **Economic $566B is modelled** | Stats-jargon / overclaim | Plain language: “researchers estimate…”; optional callout. |
| **2019/2020 hours not in 2025 Table 12** | Only 2025 hours in cube | 2019=596M, 2020=490M taken from ABS GSS release narrative (same publication family); labelled in CSV. |
| **Sketch already done** | Layout may differ | If you share the sketch later, reorder sections to match. |

---

## 6. Data inventory (Step 2)

Rebuild: `scripts/build_data.py` (reads `data/_raw/`, writes slim files below).  
Licence: ABS / ACNC / Snapshot publications — CC attribution on page; ABS Creative Commons as per DataPacks readme.

### Slim files in `data/` (page payload ≈ **3.2 MB**)

| Local file | Charts | Source |
| --- | --- | --- |
| `australia_sa4.geojson` | C1 | ASGS SA4 2021 + Census G23 rates |
| `australia_states.geojson` | C2 base / C3 | ASGS STE 2021 + Census G23 |
| `state_volunteer_centroids.csv` | C2 | Derived centroids + Census STE counts |
| `volunteer_dots.geojson` | C3 | 1 dot = 10,000 Census volunteers |
| `census_volunteering_sa4.csv` | C1 | Census 2021 GCP G23 SA4 |
| `census_volunteering_ste.csv` | C2, C3 | Census 2021 GCP G23 STE |
| `gss_formal_rate_by_remoteness.csv` | C4 | GSS 2025 Table 7.3 |
| `gss_formal_rate_by_age.csv` | C5 | GSS 2025 Table 10.3 |
| `gss_formal_rate_trend.csv` | C6 | MWM 2006–2014 + GSS Table 1.3 2019–2025 |
| `gss_org_types.csv` | C7 | GSS 2025 Table 11.3 |
| `snapshot_formal_informal_sankey.csv` | C8 | Snapshot of Volunteering 2023 |
| `gss_hours_by_age_heatmap.csv` | C9 | GSS 2025 Table 12.3 |
| `gss_formal_hours_trend.csv` | C10 | GSS Table 12.1 (2025) + release narrative (2019/2020) |
| `waffle_formal_2025.csv` | C11 | Derived from GSS 22.6% |
| `gss_reasons_diverging.csv` | C12 | GSS Tables 11.3 + 13.3 |
| `acnc_volunteers_by_size.csv` / `acnc_key_stats.csv` | annotations / alt | ACNC Charities Report 11th ed |
| `snapshot_key_stats.csv` | annotations | Snapshot 2023 |
| `verified_claims.json` | QA | Machine-checked hero numbers |

### Raw downloads (not shipped to GitHub Pages — in `data/_raw/`, gitignored)

| Raw file | URL |
| --- | --- |
| `GSSDC01.xlsx`, `07`, `10`–`13`, `20.xlsx` | `https://www.abs.gov.au/statistics/people/people-and-communities/general-social-survey-summary-results-australia/2025/GSSDC##.xlsx` |
| `2021_GCP_SA4_AUS.zip`, `2021_GCP_STE_AUS.zip` | `https://www.abs.gov.au/census/find-census-data/datapacks/download/2021_GCP_{SA4\|STE}_for_AUS_short-header.zip` |
| `STE_2021_AUST_SHP_GDA2020.zip`, `SA4_2021_AUST_SHP_GDA2020.zip` | ABS ASGS Ed. 3 digital boundary files |
| `unpaid_work_summary.xlsx` | ABS Unpaid work and care Census 2021 summary |

Snapshot/ACNC figures transcribed from published reports (URLs in §4); not re-downloaded as bulk microdata.

---

## 7. Stop condition

**Step 6 complete (instructions + polish).** Publish steps in `PUBLISH.md`. Part A/D wait on your live URL.

### Rubric self-check (HD-oriented)

| Requirement | Status |
| --- | --- |
| Vega-Lite/Vega for maps/diagrams | Yes — 12 human-readable specs in `specs/` |
| Single scrolling GitHub Page, no section-swap UI | Yes — sticky nav anchors only |
| No horizontal scroll (small laptop) | Mitigated — `overflow-x: hidden` + responsive grids |
| ≥3 distinct map idioms + Albers AU (no Mercator thematic) | Yes — choropleth, prop symbols, dot density; same projection |
| >10 charts (≥11) | Yes — 12 |
| ≥8 advanced idioms | Yes — 10 advanced + 1 basic (hours line) |
| ≥2 real public sources | Yes — ABS GSS + Census (+ Snapshot/ACNC labelled) |
| Slim downloads | ~3.6 MB slim `data/` files; `_raw` gitignored |
| Author, date, sources, **AI acknowledgement** on page | Yes — footer + `AI_ACKNOWLEDGEMENT.txt` + write-up |
| Story / annotations / layout | Five acts in `index.html` |
| Sketch | Student-owned — Part C note only |
| Part A URL / Part D screenshot | **You** after Pages is live |

### Moodle paste list

1. **Part A** — live GitHub Pages visualisation URL (incognito-tested)
2. **Part C** — URL + screenshot of **your** existing sketch (not generated here)
3. **Part D** — full-page screenshot of the **live** visualisation
4. **Part B** — from `ASSIGNMENT_WRITEUP.md` (fill Name / Student ID / Studio first)
5. Replace `[Your name]` in `index.html` footer before final push
