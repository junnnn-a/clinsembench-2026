#!/usr/bin/env python
"""
16_generate_monotonicity.py — X1c: monotonicity at FIXED surface.

For a section that admits three shape-matched edits of three different types in three different
sentences (e1, e2, e3; each with a meaning-preserving version p_i and a meaning-changing version c_i),
we build candidates that all contain exactly three edits and differ only in HOW MANY of them change meaning:

    M0 = p1 p2 p3      M1 = c1 p2 p3      M2 = c1 c2 p3      M3 = c1 c2 c3

Surface distance to the reference is (by construction of the matched edits) the same in all four cells, so a
metric that tracks meaning should give  D(M0) < D(M1) < D(M2) < D(M3).  Existing monotonicity tests
(ReEvalMed, RadSEM) add errors and surface change together.

Also written: K1 = c1 only, K2 = c1 c2 only (the uncontrolled "more errors = more edits" ladder, for contrast
with K3 = M3), and identity.

Output: data/pairs/full_{corpus}mono_all.csv, full_{corpus}mono_targets.csv   (corpus tag "<corpus>mono")
Run (CPU):  /opt/conda/envs/clinsev/bin/python scripts/16_generate_monotonicity.py --corpus iu mimic
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from multiprocessing import Pool
from pathlib import Path

import pandas as pd

NEW = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("gen", NEW / "scripts/3_generate_factorial_pairs.py")
G = importlib.util.module_from_spec(spec); spec.loader.exec_module(G)


def process(args):
    corpus, seed, report_id, section, sentences_json, deid_json = args
    sents = json.loads(sentences_json)
    deid = json.loads(deid_json)
    text = " ".join(sents)
    found = {}                       # etype -> (sent_idx, Edit)
    for etype, rule in G.RULES.items():
        opts = []
        for i, s in enumerate(sents):
            if deid[i] or len(s.split()) < 3:
                continue
            e = rule(s, text, G.rng_for(seed, corpus, report_id, section, etype, i))
            if e is None or e.p_sent == s or e.c_sent == s or e.p_sent == e.c_sent:
                continue
            ep, ec = G.edit_tokens(s, e.p_sent), G.edit_tokens(s, e.c_sent)
            if ep != ec or len(e.p_sent.split()) != len(e.c_sent.split()):     # strict: identical edit size and length
                continue
            if G.STRICT_NEG.search(s) and etype in ("laterality", "anatomy", "measurement"):
                continue
            opts.append((i, e))
        if opts:
            found[etype] = opts
    rng = G.rng_for(seed, corpus, report_id, section, "mono")
    types = list(found)
    rng.shuffle(types)
    chosen, used_sents = [], set()
    for t in types:
        cands = [(i, e) for i, e in found[t] if i not in used_sents]
        if not cands:
            continue
        i, e = rng.choice(cands)
        chosen.append((t, i, e)); used_sents.add(i)
        if len(chosen) == 3:
            break
    if len(chosen) < 3:
        return None
    ref = " ".join(sents)

    def build(flags):                 # flags[j] in {None, "p", "c"} for the j-th chosen edit
        ss = list(sents)
        for (t, i, e), f in zip(chosen, flags):
            if f == "p":
                ss[i] = e.p_sent
            elif f == "c":
                ss[i] = e.c_sent
        return " ".join(ss)

    tid = f"{corpus}mono_{report_id}_{section}"
    cells = {"identity": [None, None, None], "M0": ["p", "p", "p"], "M1": ["c", "p", "p"], "M2": ["c", "c", "p"],
             "M3": ["c", "c", "c"], "K1": ["c", None, None], "K2": ["c", "c", None]}
    meta = dict(target_id=tid, corpus=f"{corpus}mono", report_id=str(report_id), section=section,
                edit_type="+".join(t for t, _, _ in chosen), subtype="mono", pattern=" | ".join(e.pattern for _, _, e in chosen),
                edit_detail=" | ".join(f"{t}:{e.detail}" for t, _, e in chosen), target_idx=chosen[0][1], needs_expert_review=any(e.needs_expert_review for _, _, e in chosen))
    rows = [{"uid": f"{tid}__{c}", **meta, "cell": c, "n_flips": sum(x == "c" for x in f), "n_edits": sum(x is not None for x in f),
             "is_changed": int(any(x == "c" for x in f)), "reference": ref, "candidate": build(f)} for c, f in cells.items()]
    target = {**meta, "reference": ref, "n_sent": len(sents), "first_type": chosen[0][0],
              "edits": json.dumps([{"type": t, "sent": sents[i], "p": e.p_sent, "c": e.c_sent} for t, i, e in chosen])}
    return rows, target


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", nargs="+", default=["iu", "mimic"])
    ap.add_argument("--n", type=int, default=300)
    ap.add_argument("--max_sections", type=int, default=40000)
    ap.add_argument("--seed", type=int, default=13)
    ap.add_argument("--workers", type=int, default=48)
    args = ap.parse_args()
    for corpus in args.corpus:
        df = pd.read_csv(NEW / f"data/corpus/{corpus}_sections.csv")
        df = df[df.n_sent >= 4]
        if len(df) > args.max_sections:
            df = df.sample(n=args.max_sections, random_state=args.seed)
        jobs = [(corpus, args.seed, r.report_id, r.section, r.sentences, r.sent_has_deid) for r in df.itertuples()]
        res = []
        with Pool(args.workers) as pool:
            for out in pool.imap_unordered(process, jobs, chunksize=64):
                if out is not None:
                    res.append(out)
        res.sort(key=lambda x: x[1]["target_id"])
        rng = G.rng_for(args.seed, corpus, "mono-sample")
        rng.shuffle(res)
        # balance the type of the FIRST flipped edit (it defines M1) as evenly as supply allows
        per, keep = {}, []
        cap = max(1, args.n // 7 + 5)
        for rows, t in res:
            if per.get(t["first_type"], 0) >= cap:
                continue
            keep.append((rows, t)); per[t["first_type"]] = per.get(t["first_type"], 0) + 1
            if len(keep) >= args.n:
                break
        P = pd.DataFrame([r for rows, _ in keep for r in rows])
        T = pd.DataFrame([t for _, t in keep])
        P.to_csv(NEW / f"data/pairs/full_{corpus}mono_all.csv", index=False)
        T.to_csv(NEW / f"data/pairs/full_{corpus}mono_targets.csv", index=False)
        print(f"[{corpus}mono] candidates={len(res)} kept={len(T)} rows={len(P)} first-type={per}")
        e = json.loads(T.edits.iloc[0])
        for x in e:
            print(f"   {x['type']:12s} T: {x['sent']}\n                P: {x['p']}\n                C: {x['c']}")


if __name__ == "__main__":
    main()
