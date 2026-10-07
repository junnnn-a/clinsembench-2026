#!/usr/bin/env python
"""
15_generate_omission_insertion.py — X1b: controlled OMISSION / INSERTION layer (MIMIC-CXR, local track).

Same-position substitution is impossible for these two error types, so P and C use the same
sentence-level operation instead (docs/3 §5.2, optional layer):

  omission   C: delete one finding-bearing sentence F (asserted finding)
             P: delete one non-clinical sentence N of similar length (technique / comparison statement:
                "PA and lateral views of the chest were obtained.")          -> both delete one sentence
  insertion  C: append a finding sentence taken from ANOTHER report whose finding is not mentioned
                in this section (unsupported finding)
             P: append a paraphrase of a sentence that is already in the section (redundant restatement)
                                                                              -> both append one sentence

Cells: identity, P0/C0 (minimal), P1/C1 (shared sentence permutation), P2/C2 (all other sentences paraphrased;
same paraphraser + NLI filter as 5_paraphrase_context.py).

Needs the vLLM env:  source scripts/env_llm.sh; $PY scripts/15_generate_omission_insertion.py --corpus mimic
Output: data/pairs/full_{corpus}oi_all.csv, full_{corpus}oi_targets.csv, full_{corpus}oi_paraphrase_log.csv
        (corpus tag "mimicoi" so that 6/7/8/9/10/11 scripts work unchanged)
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import random
import re
import time
from pathlib import Path

import pandas as pd

NEW = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("par", NEW / "scripts/5_paraphrase_context.py")
PAR = importlib.util.module_from_spec(spec); spec.loader.exec_module(PAR)

N_PATTERNS = [
    r"^(?:(?:PA|AP|Frontal|Portable|Upright|Semi-upright|Semiupright|Supine|Single|Two|Erect|Lateral)\b[^.]*\b(?:views?|radiographs?|films?|images?)\b(?: of the chest)?(?: (?:were|was|are|is))? (?:obtained|provided|performed|submitted|acquired)(?: [^.]{0,60})?\.)$",
    r"^(?:(?:PA and lateral|Frontal and lateral|AP(?: portable)?(?: upright)?(?: and lateral)?|Portable AP(?: upright)?|Single (?:AP|frontal|portable)[a-z ]*) (?:chest )?(?:views?|radiographs?)(?: of the chest)?\.)$",
    r"^(?:Comparison (?:is made )?(?:to|with) [^.]{0,80}\.)$",
    r"^(?:No (?:previous|prior) (?:images|studies|study|exams?|examinations?|films)(?: (?:are|is) available)?(?: for comparison)?\.)$",
]
N_RE = re.compile("|".join(N_PATTERNS), re.I)
FIND_RE = re.compile(r"\b(effusions?|pneumothorax|pneumothoraces|atelectasis|consolidations?|opacit(?:y|ies)|edema|pneumonia|infiltrates?|"
                     r"nodules?|mass(?:es)?|cardiomegaly|fractures?|congestion|emphysema|granulomas?|scarring|thickening|hernia)\b", re.I)
NEG_RE = re.compile(r"\b(?:no|not|without|negative|absent|nor|neither|clear|normal|unremarkable|resolved|resolution|removed|removal)\b", re.I)
DEID_RE = re.compile(r"XXXX|___")
BAD_INS = re.compile(r"\b(?:again|unchanged|stable|persistent|increased|decreased|improved|worsened|interval|prior|previous|new|"
                     r"compared|comparison|also|otherwise|however|this|these|there is also|additionally)\b", re.I)


def rng_for(*keys):
    return random.Random(int(hashlib.md5("|".join(map(str, keys)).encode()).hexdigest()[:12], 16))


def stem(term: str) -> str:
    t = term.lower()
    for a, b in [("effusions", "effusion"), ("pneumothoraces", "pneumothorax"), ("consolidations", "consolidation"),
                 ("opacities", "opacit"), ("opacity", "opacit"), ("infiltrates", "infiltrate"), ("nodules", "nodule"),
                 ("masses", "mass"), ("fractures", "fracture"), ("granulomas", "granuloma")]:
        if t == a:
            return b
    return t


def is_finding_sentence(s):
    n = len(s.split())
    return bool(FIND_RE.search(s)) and not NEG_RE.search(s) and not DEID_RE.search(s) and 4 <= n <= 22


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default="mimic")
    ap.add_argument("--n_per_type", type=int, default=150)
    ap.add_argument("--max_sections", type=int, default=40000)
    ap.add_argument("--seed", type=int, default=13)
    ap.add_argument("--model", default="Qwen/Qwen2.5-7B-Instruct")
    ap.add_argument("--k", type=int, default=4)
    ap.add_argument("--nli_thr", type=float, default=0.8)
    ap.add_argument("--gpu_mem", type=float, default=0.15)
    args = ap.parse_args()
    tagc = f"{args.corpus}oi"

    sec = pd.read_csv(NEW / f"data/corpus/{args.corpus}_sections.csv")
    sec = sec[sec.n_sent >= 4]
    if args.max_sections and len(sec) > args.max_sections:
        sec = sec.sample(n=args.max_sections, random_state=args.seed)
    # reports already used by the substitution layer are excluded (independent sample)
    used = set(pd.read_csv(NEW / f"data/pairs/full_{args.corpus}_targets.csv").report_id.astype(str))
    sec = sec[~sec.report_id.astype(str).isin(used)].reset_index(drop=True)

    # ---------------- candidate targets
    om, ins_cand, pool = [], [], []
    for r in sec.itertuples():
        sents = json.loads(r.sentences)
        rng = rng_for(args.seed, r.report_id, r.section)
        N = [i for i, s in enumerate(sents) if N_RE.match(s) and not FIND_RE.search(s)]
        F = [i for i, s in enumerate(sents) if is_finding_sentence(s)]
        if N and F:
            pairs = [(abs(len(sents[f].split()) - len(sents[n].split())), f, n) for f in F for n in N]
            d, f, n = min(pairs, key=lambda x: (x[0], rng.random()))
            if d <= 6:
                om.append({"report_id": str(r.report_id), "section": r.section, "sentences": sents, "f_idx": f, "n_idx": n, "len_diff": d})
        clean = [i for i, s in enumerate(sents) if not DEID_RE.search(s) and 4 <= len(s.split()) <= 15 and not N_RE.match(s)]
        if len(clean) >= 2 and not any(DEID_RE.search(s) for s in sents):
            ins_cand.append({"report_id": str(r.report_id), "section": r.section, "sentences": sents, "src_idx": rng.choice(clean)})
        for i in F:
            s = sents[i]
            if 5 <= len(s.split()) <= 14 and not BAD_INS.search(s) and s[0].isupper() and s.endswith("."):
                pool.append((s, sorted({stem(m) for m in FIND_RE.findall(s)}), str(r.report_id)))
    rng = rng_for(args.seed, "sample")
    rng.shuffle(om); rng.shuffle(ins_cand); rng.shuffle(pool)
    # balance sections for omission
    def take(items, n):
        out, per = [], {}
        for it in items:
            if per.get(it["section"], 0) < (n + 1) // 2:
                out.append(it); per[it["section"]] = per.get(it["section"], 0) + 1
            if len(out) == n:
                break
        return out
    om = take(om, args.n_per_type)
    om_reports = {o["report_id"] for o in om}
    ins_cand = take([c for c in ins_cand if c["report_id"] not in om_reports], int(args.n_per_type * 1.6))
    print(f"[{tagc}] omission targets={len(om)}  insertion candidates={len(ins_cand)}  finding-sentence pool={len(pool)}", flush=True)

    # ---------------- paraphrase everything we may need
    need = {}
    for o in om:
        for i, s in enumerate(o["sentences"]):
            if i not in (o["f_idx"], o["n_idx"]) and not DEID_RE.search(s):
                need[s] = None
    for c in ins_cand:
        for s in c["sentences"]:
            need[s] = None
    sents_all = list(need)
    from vllm import LLM, SamplingParams
    llm = LLM(model=args.model, gpu_memory_utilization=args.gpu_mem, max_model_len=2048, dtype="bfloat16", seed=0)
    tok = llm.get_tokenizer()
    sp = SamplingParams(n=args.k, temperature=0.8, top_p=0.95, max_tokens=120, seed=0)
    prompts = [tok.apply_chat_template([{"role": "user", "content": PAR.PROMPT.format(sent=s)}], tokenize=False, add_generation_prompt=True) for s in sents_all]
    t0 = time.time()
    outs = llm.generate(prompts, sp)
    print(f"  paraphrased {len(sents_all)} sentences in {time.time()-t0:.0f}s", flush=True)
    nli = PAR.NLI()
    src, cands = [], []
    for s, o in zip(sents_all, outs):
        seen = set()
        for c in o.outputs:
            t = PAR.clean(c.text)
            if t and t.lower() != s.lower() and t.lower() not in seen:
                seen.add(t.lower()); src.append(s); cands.append(t)
    fwd, bwd = nli.entail_prob(src, cands), nli.entail_prob(cands, src)
    acc, log = {}, []
    for s, c, f, b in zip(src, cands, fwd, bwd):
        et = PAR.edit_tokens(s, c)
        ok = f >= args.nli_thr and b >= args.nli_thr and PAR.lexical_guard(s, c) and et >= 2
        log.append({"source": s, "paraphrase": c, "nli_fwd": f, "nli_bwd": b, "edit_tokens": et, "accepted": ok})
        if ok:
            acc.setdefault(s, []).append((et, c))
    for s in acc:
        acc[s] = [c for _, c in sorted(acc[s], reverse=True)]
    pd.DataFrame(log).to_csv(NEW / f"data/pairs/full_{tagc}_paraphrase_log.csv", index=False)
    print(f"  sentences with >=1 accepted paraphrase: {len(acc)}/{len(sents_all)}", flush=True)

    # ---------------- assemble
    rows, targets = [], []

    def emit(tid, meta, ref_sents, p_sents, c_sents, ctx_map, perm_seed):
        ref = " ".join(ref_sents)
        r = rng_for(args.seed, tid, "perm")
        def reorder(ss):
            idx = list(range(len(ss)))
            for _ in range(20):
                r.shuffle(idx)
                if idx != list(range(len(ss))):
                    break
            return [ss[i] for i in idx]
        # one shared permutation: permute the union order by sorting on a random key per sentence string
        keyr = rng_for(args.seed, tid, "key")
        keys = {s: keyr.random() for s in set(p_sents) | set(c_sents)}
        p1 = sorted(p_sents, key=lambda s: keys[s]); c1 = sorted(c_sents, key=lambda s: keys[s])
        if p1 == p_sents and c1 == c_sents:
            p1, c1 = p1[::-1], c1[::-1]
        par = lambda ss: [ctx_map.get(s, s) for s in ss]
        cells = [("identity", ref_sents, 0), ("P0", p_sents, 0), ("C0", c_sents, 1), ("P1", p1, 0), ("C1", c1, 1),
                 ("P2", par(p_sents), 0), ("C2", par(c_sents), 1)]
        for cell, ss, ch in cells:
            rows.append({"uid": f"{tid}__{cell}", "target_id": tid, "corpus": tagc, **meta, "cell": cell,
                         "surface_layer": "identity" if cell == "identity" else "S" + cell[1], "is_changed": ch,
                         "reference": ref, "candidate": " ".join(ss)})
        targets.append({"target_id": tid, "corpus": tagc, **meta, "reference": ref,
                        "p0": " ".join(p_sents), "c0": " ".join(c_sents),
                        "n_context_paraphrased": sum(1 for s in set(p_sents) & set(c_sents) if s in ctx_map)})

    for o in om:
        s = o["sentences"]; f, n = o["f_idx"], o["n_idx"]
        tid = f"{tagc}_{o['report_id']}_{o['section']}_omission"
        meta = dict(report_id=o["report_id"], section=o["section"], edit_type="omission", subtype="finding_sentence_deleted",
                    pattern="delete F vs delete N", edit_detail=f"F={s[f]} || N={s[n]}", target_idx=f, needs_expert_review=False)
        ctx_map = {x: acc[x][0] for i, x in enumerate(s) if i not in (f, n) and x in acc}
        emit(tid, meta, s, [x for i, x in enumerate(s) if i != n], [x for i, x in enumerate(s) if i != f], ctx_map, 0)

    n_ins = 0
    for c in ins_cand:
        if n_ins >= args.n_per_type:
            break
        s = c["sentences"]; k = c["src_idx"]
        if s[k] not in acc:
            continue
        p_ins = acc[s[k]][0]
        section_stems = {stem(m) for x in s for m in FIND_RE.findall(x)}
        rr = rng_for(args.seed, c["report_id"], "ins")
        options = [(abs(len(g.split()) - len(p_ins.split())), rr.random(), g) for g, st, rid in pool
                   if rid != c["report_id"] and not (set(st) & section_stems) and g not in s]
        if not options:
            continue
        d, _, g = min(options[:4000])
        if d > 3:
            continue
        tid = f"{tagc}_{c['report_id']}_{c['section']}_insertion"
        meta = dict(report_id=c["report_id"], section=c["section"], edit_type="insertion", subtype="foreign_finding_appended",
                    pattern="append foreign F vs append restatement", edit_detail=f"C+={g} || P+={p_ins} (restates: {s[k]})",
                    target_idx=len(s), needs_expert_review=False)
        # in S2 the restated source sentence uses a different paraphrase (or stays verbatim) so that the appended
        # restatement is not an exact duplicate of its neighbour
        ctx_map = {x: acc[x][0] for i, x in enumerate(s) if i != k and x in acc}
        if len(acc[s[k]]) > 1:
            ctx_map[s[k]] = acc[s[k]][1]
        emit(tid, meta, s, s + [p_ins], s + [g], ctx_map, 0)
        n_ins += 1

    P = pd.DataFrame(rows); T = pd.DataFrame(targets)
    P.to_csv(NEW / f"data/pairs/full_{tagc}_all.csv", index=False)
    T.to_csv(NEW / f"data/pairs/full_{tagc}_targets.csv", index=False)
    print(f"[{tagc}] targets: {T.edit_type.value_counts().to_dict()}  rows={len(P)}")
    for et, g in T.groupby("edit_type"):
        e = g.sample(n=3, random_state=1)
        for x in e.itertuples():
            print(f"  [{et}] {x.edit_detail[:300]}")


if __name__ == "__main__":
    main()
