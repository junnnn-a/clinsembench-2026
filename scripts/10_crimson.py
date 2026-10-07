#!/usr/bin/env python
"""
10_crimson.py — CRIMSON (Rajpurkar lab) with the open MedGemma-4B CRIMSON model.

Prompt construction and score computation come from radeval.metrics.crimson (v2.2.1);
generation is done with vLLM (batched) instead of radeval's sequential HF pipeline, which
needed >30 min for 40 pairs on this machine.  Decoding matches radeval's HF path: greedy,
repetition_penalty 1.1.

Output: {out}/crimson.csv with uid, crimson (0..1, higher = better), per-category error counts, raw JSON.

    source scripts/env_llm.sh; $PY scripts/10_crimson.py --pairs data/pairs/pilot_iu_all.csv --out results/1_pilot_iu/scores_all
"""
from __future__ import annotations

import argparse
import time
from pathlib import Path

import numpy as np
import pandas as pd


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pairs", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--model", default=str(Path(__file__).resolve().parent.parent / "envs/models/medgemma-4b-it-crimson"))
    ap.add_argument("--gpu_mem", type=float, default=0.2)
    ap.add_argument("--max_tokens", type=int, default=3072)
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    df = pd.read_csv(args.pairs)
    if args.limit:
        df = df.head(args.limit)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    target = out / "crimson.csv"
    done = pd.read_csv(target) if target.exists() else pd.DataFrame(columns=["uid"])
    todo = df[~df.uid.isin(set(done.uid))].reset_index(drop=True)
    print(f"[crimson] total={len(df)} done={len(done)} todo={len(todo)}", flush=True)
    if todo.empty:
        return

    from radeval.metrics.crimson import crimson as C
    C.CRIMSON._init_hf_pipeline = lambda self: None          # no HF pipeline; vLLM does generation
    scorer = C.CRIMSON(provider="hf", model_name=args.model)
    prompts_txt = [scorer._build_request(r, h)["prompt"] for r, h in zip(todo.reference.astype(str), todo.candidate.astype(str))]

    from vllm import LLM, SamplingParams
    llm = LLM(model=args.model, gpu_memory_utilization=args.gpu_mem, enforce_eager=(__import__("os").environ.get("VLLM_EAGER", "1") == "1"), kv_cache_memory_bytes=(int(float(__import__("os").environ["KV_GB"]) * 2**30) if __import__("os").environ.get("KV_GB") else None), max_model_len=8192, seed=0, trust_remote_code=True)
    tok = llm.get_tokenizer()
    prompts = [tok.apply_chat_template([{"role": "system", "content": C._SYSTEM_MSG}, {"role": "user", "content": p}],
                                       tokenize=False, add_generation_prompt=True) for p in prompts_txt]
    sp = SamplingParams(temperature=0.0, max_tokens=args.max_tokens, repetition_penalty=1.1, seed=0)
    t0 = time.time()
    outs = llm.generate(prompts, sp)
    print(f"[crimson] generated {len(outs)} in {time.time()-t0:.0f}s", flush=True)

    rows, n_fail = [], 0
    for uid, o in zip(todo.uid, outs):
        raw = o.outputs[0].text
        try:
            res = scorer._parse_response(raw)
            counts = res.get("error_counts", {})
            rows.append({"uid": uid, "crimson": res.get("crimson_score", np.nan), **{f"crimson_{k}": v for k, v in counts.items()},
                         "crimson_raw": raw[:4000]})
        except Exception as e:
            n_fail += 1
            rows.append({"uid": uid, "crimson": np.nan, "crimson_raw": raw[:4000], "crimson_parse_error": str(e)[:200]})
    res = pd.DataFrame(rows)
    allres = pd.concat([done, res], ignore_index=True) if len(done) else res
    allres.to_csv(target, index=False)
    print(f"[crimson] parse failures {n_fail}/{len(res)}; mean={res.crimson.mean():.3f} -> {target}", flush=True)


if __name__ == "__main__":
    main()
