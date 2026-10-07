#!/usr/bin/env python
"""
7_score_metrics.py — score (reference, candidate) rows with reference-based metrics.

Run in the `clinsev` env (radeval 2.2.1) for RadEval metrics:
    /opt/conda/envs/clinsev/bin/python scripts/7_score_metrics.py --pairs data/pairs/pilot_iu_all.csv \
        --out results/1_pilot_iu/scores --metrics lexical,bertscore,f1chexbert,radgraph,ratescore,temporal,green,radcliq

Each metric group is written to its own CSV  {out}/{group}.csv  (uid + score columns) so that
runs are resumable and can be merged later (8_analyze_factorial.py).

Groups
  lexical        : bleu, rougeL, token_f1, jaccard                       (own implementation, copied from v1)
  bertscore      : RadEval bertscore (distilbert-base-uncased, L5, rescaled)  + bert_score roberta-large (L17, rescaled)
                   + bert_score microsoft/deberta-xlarge-mnli
  f1chexbert / radgraph / ratescore / temporal / green / radcliq / srrbert / radeval_bertscore : RadEval per-sample
All metric outputs are oriented "higher = closer to reference" here EXCEPT radcliq (lower = better); the
orientation is fixed in the analysis script via ORIENT.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
import time
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

NEW = Path(__file__).resolve().parent.parent
TOKEN_RE = re.compile(r"\b\w+\b")


def norm(t):
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9\. ]+", " ", str(t or "").lower())).strip()


def toks(t):
    return TOKEN_RE.findall(norm(t))


def token_f1(r, h):
    a, b = Counter(toks(r)), Counter(toks(h))
    if not a and not b:
        return 1.0
    inter = sum((a & b).values())
    if not inter:
        return 0.0
    p, rc = inter / sum(b.values()), inter / sum(a.values())
    return 2 * p * rc / (p + rc)


def jaccard(r, h):
    a, b = set(toks(r)), set(toks(h))
    return len(a & b) / len(a | b) if a | b else 1.0


def score_lexical(df):
    import sacrebleu
    from rouge_score import rouge_scorer
    R = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=True)
    out = pd.DataFrame({"uid": df.uid})
    out["bleu"] = [sacrebleu.sentence_bleu(str(h), [str(r)], smooth_method="exp").score / 100 for r, h in zip(df.reference, df.candidate)]
    out["rougeL"] = [R.score(str(r), str(h))["rougeL"].fmeasure for r, h in zip(df.reference, df.candidate)]
    out["token_f1"] = [token_f1(r, h) for r, h in zip(df.reference, df.candidate)]
    out["jaccard"] = [jaccard(r, h) for r, h in zip(df.reference, df.candidate)]
    return out


def score_bertscore(df, batch_size=64):
    from bert_score import score as bscore
    out = pd.DataFrame({"uid": df.uid})
    refs, hyps = df.reference.astype(str).tolist(), df.candidate.astype(str).tolist()
    for name, model_type, layers, rescale in [
        ("bertscore_distilbert", "distilbert-base-uncased", 5, True),     # = RadEval default (v1 paper)
        ("bertscore_roberta_large", "roberta-large", 17, True),           # bert_score default for English
        ("bertscore_deberta_mnli", "microsoft/deberta-xlarge-mnli", 40, False),
    ]:
        t0 = time.time()
        _, _, f = bscore(hyps, refs, model_type=model_type, num_layers=layers, lang="en",
                         rescale_with_baseline=rescale, batch_size=batch_size, verbose=False)
        out[name] = f.numpy()
        print(f"  [{name}] {time.time()-t0:.0f}s", flush=True)
    return out


def _radeval_alias():
    import importlib
    import radeval as _r
    sys.modules.setdefault("RadEval", _r)
    for sub in ["radeval", "rewards", "utils", "validate_rewards"]:
        try:
            sys.modules.setdefault(f"RadEval.{sub}", importlib.import_module(f"radeval.{sub}"))
        except Exception:
            pass


def score_radeval(df, metric, batch_size):
    _radeval_alias()
    from radeval import RadEval
    ev = RadEval(metrics=[metric], per_sample=True, show_progress=False)
    refs, hyps = df.reference.astype(str).tolist(), df.candidate.astype(str).tolist()
    vals = []
    t0 = time.time()
    for st in range(0, len(df), batch_size):
        res = ev(refs=refs[st:st + batch_size], hyps=hyps[st:st + batch_size])
        key = metric if metric in res else next((k for k, v in res.items() if isinstance(v, list)), None)
        v = res[key]
        vals.extend(v if isinstance(v, list) else [v] * len(refs[st:st + batch_size]))
        if (st // batch_size) % 20 == 0:
            print(f"  [{metric}] {st+batch_size}/{len(df)} {time.time()-t0:.0f}s", flush=True)
    return pd.DataFrame({"uid": df.uid, metric: vals})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pairs", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--metrics", default="lexical,bertscore,f1chexbert,radgraph,ratescore,temporal")
    ap.add_argument("--batch_size", type=int, default=16)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    df = pd.read_csv(args.pairs)
    if args.limit:
        df = df.head(args.limit)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    for m in [x for x in args.metrics.split(",") if x]:
        target = out / f"{m}.csv"
        if target.exists() and not args.force:
            prev = pd.read_csv(target)
            if set(prev.uid) >= set(df.uid):
                print(f"[skip] {m} already scored"); continue
        t0 = time.time()
        try:
            if m == "lexical":
                res = score_lexical(df)
            elif m == "bertscore":
                res = score_bertscore(df)
            else:
                res = score_radeval(df, m, args.batch_size)
        except Exception as e:
            print(f"[FAILED] {m}: {type(e).__name__}: {e}", flush=True)
            continue
        res.to_csv(target, index=False)
        print(f"[done] {m} n={len(res)} {time.time()-t0:.0f}s -> {target}", flush=True)


if __name__ == "__main__":
    main()
