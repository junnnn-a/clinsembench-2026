#!/usr/bin/env python
"""
2_prepare_corpora.py  (E1: data rebuild)

Builds clean, sentence-split report sections for the two corpora.

  IU X-Ray / OpenI : OLD/data/external_reports/openi_iu_xray_reports.csv (already section-level)
  MIMIC-CXR        : OLD/data/processed/reports_mimic_txt_dir.csv -> re-parse the `text` column
                     WITHOUT the v1 fallback (findings<-impression<-text).

Fixes relative to v1 (docs/2 Audit C, D):
  * no section fallback: a section exists only if its header exists and the body is non-empty,
    and impression != findings
  * administrative headers (EXAMINATION/INDICATION/TECHNIQUE/COMPARISON/...) never leak into a section
  * sentence splitter protects abbreviations (Dr., a.m., p.m., e.g., vs., No.), decimals (4.7 cm)
    and numbered-list markers ("1. No acute ...")
  * IU: sentences containing the de-identification token XXXX are flagged (not usable as targets)
  * MIMIC: sentences containing ___ are flagged likewise

Outputs (NEW/data/corpus/):
  {corpus}_sections.csv   one row per (report_id, section) with cleaned text + JSON sentence list
  {corpus}_stats.json
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import pandas as pd

OLD = Path("/home/irteam/junah-data-1/2_ClinSevBench/ClinSevBench_v2")
NEW = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------- sentence splitting
ABBREV = ["Dr", "Drs", "Mr", "Mrs", "Ms", "vs", "e.g", "i.e", "No", "approx", "St", "Jr", "Sr", "Prof", "Fig", "et al"]
_ABBR_RE = re.compile(r"\b(" + "|".join(re.escape(a) for a in ABBREV) + r")\.", flags=re.I)
_AMPM_RE = re.compile(r"\b([ap])\.m\.", flags=re.I)
_DEC_RE = re.compile(r"(\d)\.(\d)")
_LIST_RE = re.compile(r"(^|\s)(\d{1,2})\.\s+(?=[A-Z])")
_ENUM_RE = re.compile(r"(^|\s)([a-z])\)\s+")
PLACEHOLDER = "․"  # one-dot leader, restored afterwards


def protect(text: str) -> str:
    t = _AMPM_RE.sub(lambda m: f"{m.group(1)}{PLACEHOLDER}m{PLACEHOLDER}", text)
    t = _ABBR_RE.sub(lambda m: m.group(1) + PLACEHOLDER, t)
    t = _DEC_RE.sub(lambda m: m.group(1) + PLACEHOLDER + m.group(2), t)
    # "1. Text" list markers -> keep the number attached to its item
    t = _LIST_RE.sub(lambda m: f"{m.group(1)}{m.group(2)}{PLACEHOLDER} ", t)
    return t


def unprotect(text: str) -> str:
    return text.replace(PLACEHOLDER, ".")


def clean_text(text: str) -> str:
    t = str(text or "").replace("\r", "\n")
    t = re.sub(r"\s+", " ", t)
    t = re.sub(r"\s+([,.;:])", r"\1", t)
    t = re.sub(r"\.\s*\.(\s*\.)*", ".", t)          # ".." / ". ." artefacts (IU)
    t = re.sub(r"\s{2,}", " ", t)
    return t.strip()


def split_sentences(text: str) -> list[str]:
    t = protect(clean_text(text))
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'(\[-])", t)
    out = []
    for p in parts:
        p = unprotect(p).strip()
        if not p:
            continue
        # strip a leading list marker that ended up alone ("1." or "2)")
        if re.fullmatch(r"\d{1,2}[.)]", p):
            continue
        out.append(p)
    return out


def strip_list_marker(sent: str) -> str:
    return re.sub(r"^\s*\d{1,2}[.)]\s+", "", sent).strip()


# ---------------------------------------------------------------- MIMIC section parsing
SECTION_HEADERS = ["FINDINGS", "IMPRESSION", "CONCLUSION"]
OTHER_HEADERS = ["FINAL REPORT", "WET READ", "EXAMINATION", "EXAM", "INDICATION", "HISTORY", "CLINICAL HISTORY",
                 "CLINICAL INDICATION", "REASON FOR EXAMINATION", "REASON FOR EXAM", "TECHNIQUE", "COMPARISON",
                 "COMPARISONS", "NOTIFICATION", "RECOMMENDATION", "RECOMMENDATIONS", "ADDENDUM", "PROVISIONAL FINDINGS",
                 "PFI", "STUDY", "VIEWS", "REFERENCE EXAM", "CHEST RADIOGRAPH", "CHEST", "PORTABLE CHEST",
                 "PORTABLE AP CHEST", "AP CHEST", "PA AND LATERAL CHEST"]
_HDR_RE = re.compile(
    r"(?:(?<=\s)|^)(" + "|".join(re.escape(h) for h in sorted(SECTION_HEADERS + OTHER_HEADERS, key=len, reverse=True)) + r")\s*:",
)
_FINAL_RE = re.compile(r"\bFINAL REPORT\b")
_WET_RE = re.compile(r"\bWET READ\b.*?(?=\bFINAL REPORT\b|$)", flags=re.S)


def parse_mimic_sections(text: str) -> dict[str, str]:
    t = clean_text(text)
    t = _WET_RE.sub(" ", t)              # drop wet-read preamble entirely
    t = _FINAL_RE.sub(" ", t)
    t = re.sub(r"\s+", " ", t).strip()
    hits = list(_HDR_RE.finditer(t))
    out: dict[str, str] = {}
    for i, m in enumerate(hits):
        name = m.group(1).upper()
        start = m.end()
        end = hits[i + 1].start() if i + 1 < len(hits) else len(t)
        body = clean_text(t[start:end])
        if name in SECTION_HEADERS and body:
            key = "impression" if name in ("IMPRESSION", "CONCLUSION") else "findings"
            # keep the first occurrence; later duplicates (addenda) are ignored
            out.setdefault(key, body)
    return out


# ---------------------------------------------------------------- shared row builder
def make_row(corpus, report_id, section, text, deid_pat):
    sents = split_sentences(text)
    flags = [bool(re.search(deid_pat, s)) for s in sents]
    return {
        "corpus": corpus,
        "report_id": str(report_id),
        "section": section,
        "text": clean_text(" ".join(sents)),
        "n_sent": len(sents),
        "n_words": len(text.split()),
        "sentences": json.dumps(sents),
        "sent_has_deid": json.dumps(flags),
        "n_sent_clean": int(sum(not f for f in flags)),
        "any_deid": any(flags),
    }


def build_iu():
    df = pd.read_csv(OLD / "data/external_reports/openi_iu_xray_reports.csv")
    rows = [make_row("iu", r.report_id, r.section, r.reference, r"XXXX") for r in df.itertuples()]
    return pd.DataFrame(rows)


def build_mimic(max_reports: int):
    df = pd.read_csv(OLD / "data/processed/reports_mimic_txt_dir.csv", usecols=["report_id", "text"])
    rows, stats = [], {"reports": len(df), "with_findings": 0, "with_impression": 0, "both": 0, "identical_dropped": 0}
    for r in df.itertuples():
        sec = parse_mimic_sections(r.text)
        f, i = sec.get("findings", ""), sec.get("impression", "")
        if f:
            stats["with_findings"] += 1
        if i:
            stats["with_impression"] += 1
        if f and i:
            stats["both"] += 1
            if f.strip().lower() == i.strip().lower():
                stats["identical_dropped"] += 1
                continue
        for name, body in (("findings", f), ("impression", i)):
            if body and len(body.split()) >= 5:
                rows.append(make_row("mimic", r.report_id, name, body, r"___"))
    out = pd.DataFrame(rows)
    if max_reports:
        keep = out.report_id.drop_duplicates().head(max_reports)
        out = out[out.report_id.isin(keep)]
    return out, stats


def summarize(df: pd.DataFrame) -> dict:
    s = {}
    for sec, g in df.groupby("section"):
        s[sec] = {
            "n_sections": int(len(g)),
            "n_reports": int(g.report_id.nunique()),
            "words_mean": round(float(g.n_words.mean()), 1),
            "sent_mean": round(float(g.n_sent.mean()), 2),
            "ge3_sent_rate": round(float((g.n_sent >= 3).mean()), 3),
            "any_deid_rate": round(float(g.any_deid.mean()), 3),
            "ge3_clean_sent_rate": round(float((g.n_sent_clean >= 3).mean()), 3),
        }
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out_dir", default=str(NEW / "data/corpus"))
    ap.add_argument("--mimic_max_reports", type=int, default=0)
    args = ap.parse_args()
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    iu = build_iu()
    iu.to_csv(out / "iu_sections.csv", index=False)
    st_iu = summarize(iu)
    json.dump(st_iu, open(out / "iu_stats.json", "w"), indent=2)
    print("[iu]", json.dumps(st_iu, indent=1))

    mimic, st = build_mimic(args.mimic_max_reports)
    mimic.to_csv(out / "mimic_sections.csv", index=False)
    st_m = {"parse": st, "sections": summarize(mimic)}
    json.dump(st_m, open(out / "mimic_stats.json", "w"), indent=2)
    print("[mimic]", json.dumps(st_m, indent=1))


if __name__ == "__main__":
    main()
