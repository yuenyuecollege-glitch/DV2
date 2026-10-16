#!/usr/bin/env python3
"""Step 2: build slim chart-ready files from downloaded ABS / secondary sources."""

from __future__ import annotations

import csv
import json
import math
import random
import subprocess
import zipfile
from pathlib import Path

import openpyxl
import pandas as pd
import shapefile
from shapely.geometry import MultiPolygon, Point, Polygon, mapping, shape
from shapely.ops import unary_union

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "_raw"
OUT = ROOT / "data"
OUT.mkdir(parents=True, exist_ok=True)

STE_NAMES = {
    "1": "New South Wales",
    "2": "Victoria",
    "3": "Queensland",
    "4": "South Australia",
    "5": "Western Australia",
    "6": "Tasmania",
    "7": "Northern Territory",
    "8": "Australian Capital Territory",
    "9": "Other Territories",
}


def write_csv(path: Path, rows: list[dict], fieldnames: list[str] | None = None) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames = fieldnames or list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {path.relative_to(ROOT)} ({len(rows)} rows, {path.stat().st_size} bytes)")


def sheet_rows(path: Path, sheet: str) -> list[list]:
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb[sheet]
    return [[c for c in row] for row in ws.iter_rows(values_only=True)]


def build_gss_csvs() -> dict:
    claims = {}

    # --- age rates (C5) from Table 10.3 Persons ---
    rows10 = sheet_rows(RAW / "GSSDC10.xlsx", "Table 10.3 Proportion")
    age_rows = []
    in_persons = False
    for row in rows10:
        label = row[0]
        if label == "Persons(a)":
            in_persons = True
            continue
        if in_persons:
            if label in {
                "15-24",
                "25-34",
                "35-44",
                "45-54",
                "55-64",
                "65 years and over",
            }:
                age_rows.append(
                    {
                        "age_group": label,
                        "formal_rate_pct": float(row[1]),
                        "informal_rate_pct": float(row[3]),
                    }
                )
            elif label == "Labour force status":
                break
    write_csv(OUT / "gss_formal_rate_by_age.csv", age_rows)
    claims["age_45_54"] = next(r["formal_rate_pct"] for r in age_rows if r["age_group"] == "45-54")
    claims["age_25_34"] = next(r["formal_rate_pct"] for r in age_rows if r["age_group"] == "25-34")

    # national rate Table 10.3
    for row in rows10:
        if row[0] and "Persons aged 15 years and over" in str(row[0]):
            claims["formal_rate_2025"] = float(row[1])
            claims["informal_rate_2025"] = float(row[3])
            break

    # --- remoteness (C4) from Table 7.3 ---
    rows7 = sheet_rows(RAW / "GSSDC07.xlsx", "Table 7.3 Proportion")
    rem_rows = []
    for row in rows7:
        if row[0] and "unpaid voluntary work through an organisation" in str(row[0]).lower():
            labels = ["Major cities", "Inner regional", "Outer regional", "Remote", "Total"]
            for lab, val in zip(labels, row[1:6]):
                rem_rows.append({"remoteness": lab, "formal_rate_pct": float(val)})
            break
    write_csv(OUT / "gss_formal_rate_by_remoteness.csv", rem_rows)
    claims["major_cities"] = next(r["formal_rate_pct"] for r in rem_rows if r["remoteness"] == "Major cities")
    claims["remote"] = next(r["formal_rate_pct"] for r in rem_rows if r["remoteness"] == "Remote")

    # --- org types (C7) Table 11.3 ---
    rows11 = sheet_rows(RAW / "GSSDC11.xlsx", "Table 11.3 Proportion ")
    org_rows = []
    in_org = False
    for row in rows11:
        if row[0] and "Type of organisation" in str(row[0]):
            in_org = True
            continue
        if in_org:
            if row[0] == "Number of organisations did unpaid voluntary work for in last 12 months":
                break
            if row[0] and row[3] is not None:
                org_rows.append(
                    {
                        "organisation_type": str(row[0]).strip(),
                        "share_of_volunteers_pct": float(row[3]),
                    }
                )
    write_csv(OUT / "gss_org_types.csv", org_rows)
    claims["org_sport"] = next(
        r["share_of_volunteers_pct"] for r in org_rows if r["organisation_type"].startswith("Sport")
    )
    claims["org_faith"] = next(
        r["share_of_volunteers_pct"] for r in org_rows if r["organisation_type"].startswith("Religious")
    )
    claims["org_community"] = next(
        r["share_of_volunteers_pct"] for r in org_rows if r["organisation_type"].startswith("Community")
    )

    # reasons for (C12) from Table 11.3
    reason_for = []
    in_r = False
    for row in rows11:
        if row[0] and "Reasons for being a volunteer" in str(row[0]):
            in_r = True
            continue
        if in_r:
            if row[0] and "Whether incurred" in str(row[0]):
                break
            if row[0] and row[3] is not None:
                reason_for.append({"reason": str(row[0]).strip(), "pct": float(row[3]), "polarity": "for"})

    # reasons against (C12) Table 13.3 Total persons column = last numeric before footnotes
    rows13 = sheet_rows(RAW / "GSSDC13.xlsx", "Table 13.3 Proportion")
    reason_against = []
    in_ra = False
    for row in rows13:
        if row[0] and "Reasons for not doing" in str(row[0]):
            in_ra = True
            continue
        if in_ra:
            if row[0] and "Persons aged 15" in str(row[0]):
                break
            if row[0] and row[9] is not None:
                reason_against.append(
                    {"reason": str(row[0]).strip(), "pct": float(row[9]), "polarity": "against"}
                )
    # keep top reasons for diverging chart
    top_for = sorted(reason_for, key=lambda r: -r["pct"])[:6]
    top_against = sorted(reason_against, key=lambda r: -r["pct"])[:6]
    write_csv(OUT / "gss_reasons_diverging.csv", top_for + top_against)
    claims["reason_help"] = next(r["pct"] for r in reason_for if "Help others" in r["reason"])
    claims["reason_satisfaction"] = next(
        r["pct"] for r in reason_for if "Personal satisfaction" in r["reason"]
    )
    claims["reason_no_time"] = next(r["pct"] for r in reason_against if r["reason"] == "No time")
    claims["reason_not_interested"] = next(
        r["pct"] for r in reason_against if "Not interested" in r["reason"]
    )

    # --- hours heatmap (C9) Table 12.3 Persons ---
    rows12p = sheet_rows(RAW / "GSSDC12.xlsx", "Table 12.3 Proportion")
    heat = []
    in_p = False
    for row in rows12p:
        if row[0] == "Persons(a)":
            in_p = True
            continue
        if in_p:
            if row[0] and "Persons aged 15" in str(row[0]):
                break
            if row[0] in {
                "15-24",
                "25-34",
                "35-44",
                "45-54",
                "55-64",
                "65 years and over",
            }:
                for band, val in zip(
                    ["1-20 hours", "21-99 hours", "100 hours or more"],
                    [row[1], row[2], row[3]],
                ):
                    heat.append(
                        {
                            "age_group": row[0],
                            "hours_band": band,
                            "share_pct": float(val),
                        }
                    )
    write_csv(OUT / "gss_hours_by_age_heatmap.csv", heat)

    # total hours (C10) — 2025 from Table 12.1; 2019/2020 from ABS GSS release narrative
    rows12e = sheet_rows(RAW / "GSSDC12.xlsx", "Table 12.1 Estimate")
    hours_2025 = None
    for row in rows12e:
        if row[0] and "Persons aged 15 years and over who have undertaken unpaid voluntary work" in str(
            row[0]
        ):
            hours_2025 = float(row[6])  # millions
            break
    claims["hours_2025_m"] = hours_2025
    hours_2019, hours_2020 = 596.0, 490.0
    hours_trend = [
        {
            "year": 2019,
            "total_hours_million": hours_2019,
            "note": "ABS GSS release narrative (prior comparable survey)",
            "insight": "",
            "tone": "other",
            "observed": 1,
        },
        {
            "year": 2020,
            "total_hours_million": hours_2020,
            "note": "ABS GSS release narrative (COVID-affected)",
            "insight": "Pandemic impact: −106M hours\\n(−17.8% vs 2019)",
            "tone": "dip",
            "observed": 1,
        },
    ]
    # Fill 2021–2024 so the C10 axis is yearly (linear bridge 2020 → 2025).
    for year in range(2021, 2025):
        t = (year - 2020) / 5
        hours_trend.append(
            {
                "year": year,
                "total_hours_million": round(hours_2020 + (hours_2025 - hours_2020) * t, 1),
                "note": "Linear interpolate (2020→2025)",
                "insight": "",
                "tone": "other",
                "observed": 0,
            }
        )
    hours_trend.append(
        {
            "year": 2025,
            "total_hours_million": hours_2025,
            "note": "ABS GSS 2025 Table 12.1",
            "insight": "Above 2019: +22M hours\\n(+3.7%)",
            "tone": "peak",
            "observed": 1,
        }
    )
    write_csv(OUT / "gss_formal_hours_trend.csv", hours_trend)

    # --- formal rate time series (C6) ---
    # Pre-2019: ABS Measuring What Matters (18+ comparable series quoted on Social connections page)
    # 2019–2025: ABS GSS Table 1.3 (15+); 2021–2024 linearly interpolated for yearly axis
    rows01 = sheet_rows(RAW / "GSSDC01.xlsx", "Table 1.3 Proportion")
    gss_rates = {}
    for row in rows01:
        if row[0] and "unpaid voluntary work through an organisation" in str(row[0]).lower():
            # cols: 2019 M/F/T, 2020 M/F/T, 2025 Men/Women/T -> indices 3,6,9 are totals
            gss_rates[2019] = float(row[3])
            gss_rates[2020] = float(row[6])
            gss_rates[2025] = float(row[9])
            break
    slope = [
        {"year": 2006, "formal_rate_pct": 34.1, "series": "ABS MWM (18+)", "observed": 1},
        {"year": 2010, "formal_rate_pct": 36.2, "series": "ABS MWM (18+)", "observed": 1},
        {"year": 2014, "formal_rate_pct": 30.9, "series": "ABS MWM (18+)", "observed": 1},
        {
            "year": 2019,
            "formal_rate_pct": gss_rates[2019],
            "series": "ABS GSS (15+)",
            "observed": 1,
        },
        {
            "year": 2020,
            "formal_rate_pct": gss_rates[2020],
            "series": "ABS GSS (15+)",
            "observed": 1,
        },
    ]
    for year in range(2021, 2025):
        t = (year - 2020) / 5
        slope.append(
            {
                "year": year,
                "formal_rate_pct": round(
                    gss_rates[2020] + (gss_rates[2025] - gss_rates[2020]) * t, 1
                ),
                "series": "Linear interpolate (2020→2025)",
                "observed": 0,
            }
        )
    slope.append(
        {
            "year": 2025,
            "formal_rate_pct": gss_rates[2025],
            "series": "ABS GSS (15+)",
            "observed": 1,
        }
    )
    write_csv(OUT / "gss_formal_rate_trend.csv", slope)
    claims["formal_rate_2019"] = gss_rates[2019]
    claims["formal_rate_2020"] = gss_rates[2020]

    # waffle (C11)
    rate = claims["formal_rate_2025"]
    write_csv(
        OUT / "waffle_formal_2025.csv",
        [
            {"cell": i, "status": "volunteer" if i < round(rate) else "not"}
            for i in range(100)
        ],
    )

    return claims


def build_snapshot_and_acnc() -> None:
    # Snapshot 2023 — population shares as published (see PLAN risks for union vs 64.3%)
    formal = 31.8
    informal = 42.7
    both = 24.5
    formal_only = round(formal - both, 1)
    informal_only = round(informal - both, 1)
    neither = round(100 - (formal_only + informal_only + both), 1)
    write_csv(
        OUT / "snapshot_formal_informal_sankey.csv",
        [
            {"source": "Australian adults (15+)", "target": "Formal only", "value": formal_only},
            {"source": "Australian adults (15+)", "target": "Informal only", "value": informal_only},
            {"source": "Australian adults (15+)", "target": "Both formal & informal", "value": both},
            {"source": "Australian adults (15+)", "target": "Neither (implied)", "value": neither},
        ],
    )
    write_csv(
        OUT / "snapshot_key_stats.csv",
        [
            {"metric": "any_volunteer_pct", "value": 64.3, "unit": "percent", "year": 2023},
            {"metric": "formal_pct", "value": 31.8, "unit": "percent", "year": 2023},
            {"metric": "informal_pct", "value": 42.7, "unit": "percent", "year": 2023},
            {"metric": "both_pct", "value": 24.5, "unit": "percent", "year": 2023},
            {"metric": "total_hours_billion", "value": 3.2, "unit": "billion_hours", "year": 2023},
            {
                "metric": "modelled_benefits_billion_aud",
                "value": 565.6,
                "unit": "AUD_billion",
                "year": 2023,
            },
        ],
    )
    # ACNC Charities Report 11th ed (2023 AIS)
    write_csv(
        OUT / "acnc_volunteers_by_size.csv",
        [
            {"charity_size": "Extra small", "volunteers": 222356},
            {"charity_size": "Small", "volunteers": 604008},
            {"charity_size": "Medium", "volunteers": 541983},
            {"charity_size": "Large", "volunteers": 1332352},
            {"charity_size": "Very large", "volunteers": 619674},
            {"charity_size": "Extra large", "volunteers": 166125},
            {"charity_size": "Unknown - BRC", "volunteers": 278721},
        ],
    )
    write_csv(
        OUT / "acnc_key_stats.csv",
        [
            {"metric": "charity_volunteers", "value": 3765219, "year": 2023},
            {"metric": "volunteers_per_employee", "value": 2.4, "year": 2023},
            {"metric": "volunteer_run_charities", "value": 22629, "year": 2023},
            {"metric": "volunteer_run_volunteers", "value": 581971, "year": 2023},
        ],
    )


def extract_zip_member(zip_path: Path, member_substr: str, dest: Path) -> Path:
    with zipfile.ZipFile(zip_path) as z:
        matches = [n for n in z.namelist() if member_substr in n]
        if not matches:
            raise FileNotFoundError(f"{member_substr} not in {zip_path}")
        name = matches[0]
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(z.read(name))
        return dest


def build_census_tables() -> dict:
    claims = {}
    sa4_csv = extract_zip_member(
        RAW / "2021_GCP_SA4_AUS.zip",
        "2021Census_G23_AUST_SA4.csv",
        RAW / "sa4_gcp" / "G23_SA4.csv",
    )
    ste_csv = extract_zip_member(
        RAW / "2021_GCP_STE_AUS.zip",
        "2021Census_G23_AUST_STE.csv",
        RAW / "ste_gcp" / "G23_STE.csv",
    )
    geog = RAW / "sa4_gcp" / "Metadata" / "2021Census_geog_desc_1st_2nd_3rd_release.xlsx"
    if not geog.exists():
        extract_zip_member(
            RAW / "2021_GCP_SA4_AUS.zip",
            "2021Census_geog_desc",
            geog,
        )

    # SA4 names
    wb = openpyxl.load_workbook(geog, data_only=True)
    sa4_names = {}
    for sn in wb.sheetnames:
        ws = wb[sn]
        headers = None
        for i, row in enumerate(ws.iter_rows(values_only=True)):
            if i == 0:
                headers = [str(c).upper() if c else "" for c in row]
                continue
            rec = {headers[j]: row[j] for j in range(len(headers)) if j < len(row)}
            code = rec.get("SA4_CODE_2021") or rec.get("CODE")
            name = rec.get("SA4_NAME_2021") or rec.get("NAME")
            if code and name and str(code).isdigit():
                sa4_names[str(int(code))] = str(name)

    # fallback: read from ASGS shp DBF after extract
    df = pd.read_csv(sa4_csv)
    sa4_out = []
    for _, r in df.iterrows():
        code = str(int(r["SA4_CODE_2021"]))
        if code.endswith("97") or int(r["P_Tot_Tot"]) == 0:
            continue  # migratory / no usual address / empty
        volunteers = int(r["P_Tot_Volunteer"])
        total = int(r["P_Tot_Tot"])
        stated = volunteers + int(r["P_Tot_N_a_volunteer"])
        rate = round(100.0 * volunteers / stated, 2) if stated else None
        sa4_out.append(
            {
                "sa4_code": code,
                "sa4_name": sa4_names.get(code, code),
                "volunteers": volunteers,
                "not_volunteer": int(r["P_Tot_N_a_volunteer"]),
                "not_stated": int(r["P_Tot_Voluntary_work_ns"]),
                "population_15plus": total,
                "rate_pct": rate,
            }
        )
    write_csv(OUT / "census_volunteering_sa4.csv", sa4_out)

    ste = pd.read_csv(ste_csv)
    ste_out = []
    national_vol = 0
    national_stated = 0
    for _, r in ste.iterrows():
        code = str(int(r["STE_CODE_2021"]))
        if code == "9":
            continue
        volunteers = int(r["P_Tot_Volunteer"])
        stated = volunteers + int(r["P_Tot_N_a_volunteer"])
        rate = round(100.0 * volunteers / stated, 2) if stated else None
        national_vol += volunteers
        national_stated += stated
        ste_out.append(
            {
                "ste_code": code,
                "state": STE_NAMES.get(code, code),
                "volunteers": volunteers,
                "not_volunteer": int(r["P_Tot_N_a_volunteer"]),
                "not_stated": int(r["P_Tot_Voluntary_work_ns"]),
                "population_15plus": int(r["P_Tot_Tot"]),
                "rate_pct": rate,
            }
        )
    write_csv(OUT / "census_volunteering_ste.csv", ste_out)
    claims["census_volunteers"] = national_vol
    claims["census_rate"] = round(100.0 * national_vol / national_stated, 1) if national_stated else None
    return claims


def unzip_shp(zip_path: Path, dest_dir: Path) -> Path:
    dest_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path) as z:
        z.extractall(dest_dir)
    shps = list(dest_dir.rglob("*.shp"))
    if not shps:
        raise FileNotFoundError(f"no shp in {zip_path}")
    return shps[0]


def mapshaper_simplify(shp: Path, out_geojson: Path, percent: str) -> None:
    # mapshaper wants: -simplify 8% keep-shapes  (percent and flag as separate tokens)
    cmd = [
        "npx",
        "--yes",
        "mapshaper",
        str(shp),
        "-simplify",
        percent,
        "keep-shapes",
        "-clean",
        "-o",
        "format=geojson",
        str(out_geojson),
    ]
    print("running", " ".join(cmd))
    subprocess.run(cmd, check=True, cwd=str(ROOT))


def _ring_signed_area(ring) -> float:
    a = 0.0
    for i in range(len(ring) - 1):
        x1, y1 = ring[i][0], ring[i][1]
        x2, y2 = ring[i + 1][0], ring[i + 1][1]
        a += x1 * y2 - x2 * y1
    return a / 2.0


def rewind_ring(ring, want_positive_area: bool):
    """Force planar winding. d3-geo expects CW exteriors for south-hemisphere fills."""
    is_pos = _ring_signed_area(ring) > 0
    if is_pos != want_positive_area:
        return list(reversed(ring))
    return ring


def rewind_geom_for_d3(geom: dict) -> dict:
    """Rewind so Vega/d3-geo fills Australia, not the rest of the sphere."""
    if geom["type"] == "Polygon":
        geom["coordinates"] = [
            rewind_ring(ring, want_positive_area=(i != 0))
            for i, ring in enumerate(geom["coordinates"])
        ]
    elif geom["type"] == "MultiPolygon":
        geom["coordinates"] = [
            [
                rewind_ring(ring, want_positive_area=(i != 0))
                for i, ring in enumerate(poly)
            ]
            for poly in geom["coordinates"]
        ]
    return geom


def drop_tiny_islands(geom: dict, min_area: float = 0.05) -> dict:
    """Keep mainland (+ large islands). Tiny islets make Vega projection.fit world-sized."""
    if geom["type"] != "MultiPolygon":
        return geom
    kept = [poly for poly in geom["coordinates"] if abs(_ring_signed_area(poly[0])) >= min_area]
    if not kept:
        kept = [max(geom["coordinates"], key=lambda p: abs(_ring_signed_area(p[0])))]
    if len(kept) == 1:
        return {"type": "Polygon", "coordinates": kept[0]}
    return {"type": "MultiPolygon", "coordinates": kept}


def attach_props_and_filter(geojson_path: Path, join_csv: Path, code_field: str, out_path: Path, drop_other=True):
    gj = json.loads(geojson_path.read_text())
    df = pd.read_csv(join_csv, dtype=str)
    # normalize join keys
    lookup = {}
    for _, r in df.iterrows():
        if code_field == "sa4_code":
            lookup[str(int(r["sa4_code"]))] = r.to_dict()
        else:
            lookup[str(int(r["ste_code"]))] = r.to_dict()

    feats = []
    for f in gj["features"]:
        props = f.get("properties") or {}
        raw_code = props.get("SA4_CODE21") or props.get("STE_CODE21") or props.get("SA4_CODE_2021") or props.get("STE_CODE_2021")
        if raw_code is None:
            continue
        code = str(int(float(raw_code)))
        if drop_other and code == "9":
            continue
        if code_field == "sa4_code" and (code.endswith("97") or code not in lookup):
            continue
        if code not in lookup:
            continue
        joined = lookup[code]
        new_props = {k: (float(v) if k in {"volunteers", "rate_pct", "population_15plus", "not_volunteer", "not_stated"} and v not in (None, "") else v) for k, v in joined.items()}
        # cast ints
        for k in ("volunteers", "not_volunteer", "not_stated", "population_15plus"):
            if k in new_props and new_props[k] not in (None, ""):
                new_props[k] = int(float(new_props[k]))
        if "rate_pct" in new_props and new_props["rate_pct"] not in (None, ""):
            new_props["rate_pct"] = float(new_props["rate_pct"])
        feats.append(
            {
                "type": "Feature",
                "properties": new_props,
                "geometry": drop_tiny_islands(rewind_geom_for_d3(f["geometry"])),
            }
        )

    out = {"type": "FeatureCollection", "features": feats}
    out_path.write_text(json.dumps(out, separators=(",", ":")))
    print(f"wrote {out_path.relative_to(ROOT)} ({len(feats)} features, {out_path.stat().st_size} bytes)")


def random_points_in_polygon(poly, n: int, rng: random.Random) -> list[Point]:
    minx, miny, maxx, maxy = poly.bounds
    pts = []
    tries = 0
    while len(pts) < n and tries < n * 500:
        tries += 1
        p = Point(rng.uniform(minx, maxx), rng.uniform(miny, maxy))
        if poly.contains(p):
            pts.append(p)
    return pts


def build_dot_density(ste_geojson: Path, ste_csv: Path, out_path: Path, per_dot: int = 10000) -> None:
    gj = json.loads(ste_geojson.read_text())
    df = pd.read_csv(ste_csv)
    by_code = {str(int(r.ste_code)): r for r in df.itertuples()}
    rng = random.Random(3179)
    dots = []
    for f in gj["features"]:
        code = str(f["properties"]["ste_code"])
        row = by_code[code]
        n = int(round(row.volunteers / per_dot))
        geom = shape(f["geometry"])
        if geom.geom_type == "Polygon":
            poly = geom
        else:
            poly = unary_union(geom)
        pts = random_points_in_polygon(poly, n, rng)
        for i, p in enumerate(pts):
            dots.append(
                {
                    "type": "Feature",
                    "properties": {
                        "ste_code": code,
                        "state": row.state,
                        "dot_value": per_dot,
                    },
                    "geometry": mapping(p),
                }
            )
    out = {"type": "FeatureCollection", "features": dots}
    out_path.write_text(json.dumps(out, separators=(",", ":")))
    print(f"wrote {out_path.relative_to(ROOT)} ({len(dots)} dots, {out_path.stat().st_size} bytes)")


def build_centroids(ste_geojson: Path, out_csv: Path) -> None:
    gj = json.loads(ste_geojson.read_text())
    rows = []
    for f in gj["features"]:
        geom = shape(f["geometry"])
        c = geom.representative_point()  # guaranteed inside
        p = f["properties"]
        rows.append(
            {
                "ste_code": p["ste_code"],
                "state": p["state"],
                "volunteers": p["volunteers"],
                "rate_pct": p["rate_pct"],
                "longitude": round(c.x, 5),
                "latitude": round(c.y, 5),
            }
        )
    write_csv(out_csv, rows)


def main() -> None:
    print("=== GSS / Snapshot / ACNC tables ===")
    claims = build_gss_csvs()
    build_snapshot_and_acnc()
    print("=== Census ===")
    claims.update(build_census_tables())

    print("=== Geometries ===")
    ste_shp = unzip_shp(RAW / "STE_2021_AUST_SHP_GDA2020.zip", RAW / "ste_shp")
    sa4_shp = unzip_shp(RAW / "SA4_2021_AUST_SHP_GDA2020.zip", RAW / "sa4_shp")

    # Always enrich SA4 names from shapefile DBF
    sa4_csv = OUT / "census_volunteering_sa4.csv"
    df = pd.read_csv(sa4_csv, dtype={"sa4_code": str})
    r = shapefile.Reader(str(sa4_shp))
    fields = [f[0] for f in r.fields[1:]]
    name_map = {}
    for rec in r.records():
        d = dict(zip(fields, rec))
        raw = str(d.get("SA4_CODE21") or d.get("SA4_CODE_2021") or "").strip()
        if not raw.isdigit():
            continue
        name_map[str(int(raw))] = d.get("SA4_NAME21") or d.get("SA4_NAME_2021") or raw
    df["sa4_code"] = df["sa4_code"].astype(int).astype(str)
    df["sa4_name"] = df["sa4_code"].map(lambda c: name_map.get(c, c))
    df.to_csv(sa4_csv, index=False)
    print("updated SA4 names from shapefile")

    ste_raw_gj = RAW / "ste_simplified_raw.geojson"
    sa4_raw_gj = RAW / "sa4_simplified_raw.geojson"
    # Aggressive simplify to keep payload in the low-MB range
    mapshaper_simplify(ste_shp, ste_raw_gj, "2%")
    mapshaper_simplify(sa4_shp, sa4_raw_gj, "1.5%")

    attach_props_and_filter(
        ste_raw_gj, OUT / "census_volunteering_ste.csv", "ste_code", OUT / "australia_states.geojson"
    )
    attach_props_and_filter(
        sa4_raw_gj, OUT / "census_volunteering_sa4.csv", "sa4_code", OUT / "australia_sa4.geojson"
    )
    build_centroids(OUT / "australia_states.geojson", OUT / "state_volunteer_centroids.csv")
    build_dot_density(
        OUT / "australia_states.geojson",
        OUT / "census_volunteering_ste.csv",
        OUT / "volunteer_dots.geojson",
        per_dot=10000,
    )

    # claims dump
    (OUT / "verified_claims.json").write_text(json.dumps(claims, indent=2))
    print("\nVerified claims:", json.dumps(claims, indent=2))

    # size summary
    print("\n=== data/ payload (excluding _raw) ===")
    total = 0
    for p in sorted(OUT.iterdir()):
        if p.name.startswith("_") or p.is_dir():
            continue
        total += p.stat().st_size
        print(f"  {p.name:40s} {p.stat().st_size/1024:8.1f} KB")
    print(f"TOTAL slim payload: {total/1024:.1f} KB ({total/1024/1024:.2f} MB)")


if __name__ == "__main__":
    main()
