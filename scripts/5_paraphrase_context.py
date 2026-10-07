#!/usr/bin/env python
"""
5_paraphrase_context.py  — S2 cells (P2 / C2): paraphrase every NON-target sentence with a local
LLM (vLLM), verify each paraphrase with bidirectional NLI, and assemble

    P2 = paraphrased context + P0 target sentence
    C2 = paraphrased context + C0 target sentence          (identical context for P2 and C2)

Sentences that contain de-identification tokens are copied unchanged.
For each sentence we sample K paraphrases and keep the one that
    (a) passes NLI both ways (entailment prob >= --nli_thr),
    (b) has no numbers / laterality / negation-cue changes (cheap lexical guard),
    (c) among those, changes the most tokens.
If none passes we keep the original sentence and record `kept_original=1`.

Run with the vLLM env:  envs/llm/bin/python scripts/5_paraphrase_context.py --tag pilot --corpus iu
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import time
from pathlib import Path

import pandas as pd
import torch

NEW = Path(__file__).resolve().parent.parent

PROMPT = (
    "You are rewriting one sentence from a chest X-ray radiology report.\n"
    "Rewrite the sentence so that it states EXACTLY the same clinical content with different wording "
    "(change the sentence structure and/or use synonyms). Rules:\n"
    "- Keep every finding, negation, laterality (left/right), anatomical location, severity, degree of certainty, "
    "measurement and comparison statement identical in meaning.\n"
    "- Do not add or remove information. Do not add explanations.\n"
    "- Keep any placeholder tokens (XXXX, ___) exactly as they are.\n"
    "- Output only the rewritten sentence.\n\n"
    "Sentence: {sent}\nRewritten sentence:"
)

NUM_RE = re.compile(r"\d+(?:\.\d+)?")
GUARD_RE = re.compile(r"\b(?:left|right|bilateral|no|not|without|negative|mm|cm)\b", re.I)


def edit_tokens(a, b):
    sm = difflib.SequenceMatcher(a=a.split(), b=b.split(), autojunk=False)
    return sum(max(i2 - i1, j2 - j1) for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag != "equal")


DEGREE_RE = re.compile(r"\b(?:trace|minimal|minimally|mild|mildly|slight|slightly|small|tiny|moderate|moderately|large|severe|severely|"
                       r"marked|markedly|extensive|massive|significant|significantly|substantial|prominent|subtle|gross|grossly)\b", re.I)
DEGREE_GUARD = False     # set by --degree_guard (10/7 review, point 5: "large" -> "significant" drift, defect D-11)


def lexical_guard(src, cand):
    if sorted(NUM_RE.findall(src)) != sorted(NUM_RE.findall(cand)):
        return False
    if DEGREE_GUARD and sorted(w.lower() for w in DEGREE_RE.findall(src)) != sorted(w.lower() for w in DEGREE_RE.findall(cand)):
        return False
    g1 = sorted(w.lower() for w in GUARD_RE.findall(src))
    g2 = sorted(w.lower() for w in GUARD_RE.findall(cand))
    # allow negation-cue re-expression (no <-> not/without) but not laterality/unit changes
    lat = lambda g: [w for w in g if w in ("left", "right", "bilateral", "mm", "cm")]
    if lat(g1) != lat(g2):
        return False
    neg1 = sum(w in ("no", "not", "without", "negative") for w in g1)
    neg2 = sum(w in ("no", "not", "without", "negative") for w in g2)
    if (neg1 == 0) != (neg2 == 0):
        return False
    return True


def clean(s):
    s = s.strip().strip('"').strip()
    s = re.sub(r"^(?:Rewritten sentence:|Rewritten:|Output:)\s*", "", s, flags=re.I)
    s = s.split("\n")[0].strip()
    if s and s[-1] not in ".!?":
        s += "."
    return s


class NLI:
    def __init__(self, model="cross-encoder/nli-deberta-v3-large", device="cuda"):
        from transformers import AutoModelForSequenceClassification, AutoTokenizer
        self.tok = AutoTokenizer.from_pretrained(model)
        self.model = AutoModelForSequenceClassification.from_pretrained(model).to(device).eval()
        self.device = device
        labels = {v.lower(): k for k, v in self.model.config.id2label.items()}
        self.ent = labels["entailment"]

    @torch.no_grad()
    def entail_prob(self, premises, hypotheses, bs=64):
        out = []
        for i in range(0, len(premises), bs):
            enc = self.tok(premises[i:i + bs], hypotheses[i:i + bs], padding=True, truncation=True, max_length=256, return_tensors="pt").to(self.device)
            probs = self.model(**enc).logits.softmax(-1)[:, self.ent]
            out.extend(probs.float().cpu().tolist())
        return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", nargs="+", default=["iu"])
    ap.add_argument("--tag", default="pilot")
    ap.add_argument("--model", default="Qwen/Qwen2.5-7B-Instruct")
    ap.add_argument("--k", type=int, default=4)
    ap.add_argument("--temperature", type=float, default=0.8)
    ap.add_argument("--nli_thr", type=float, default=0.8)
    ap.add_argument("--min_edit", type=int, default=2)
    ap.add_argument("--degree_guard", action="store_true")
    ap.add_argument("--gpu_mem", type=float, default=0.45)
    args = ap.parse_args()

    global DEGREE_GUARD
    DEGREE_GUARD = args.degree_guard
    from vllm import LLM, SamplingParams
    llm = LLM(model=args.model, gpu_memory_utilization=args.gpu_mem, enforce_eager=(__import__("os").environ.get("VLLM_EAGER", "1") == "1"), kv_cache_memory_bytes=(int(float(__import__("os").environ["KV_GB"]) * 2**30) if __import__("os").environ.get("KV_GB") else None), max_model_len=2048, dtype="bfloat16", seed=0)
    tok = llm.get_tokenizer()
    sp = SamplingParams(n=args.k, temperature=args.temperature, top_p=0.95, max_tokens=120, seed=0)
    nli = NLI()

    for corpus in args.corpus:
        tg = pd.read_csv(NEW / f"data/pairs/{args.tag}_{corpus}_targets.csv")
        sec = pd.read_csv(NEW / f"data/corpus/{corpus}_sections.csv")
        sec = sec.set_index(["report_id", "section"])
        sec.index = sec.index.map(lambda x: (str(x[0]), x[1]))
        # collect unique (report, section, sent_idx) context sentences
        jobs = {}
        for r in tg.itertuples():
            sents = json.loads(sec.loc[(str(r.report_id), r.section), "sentences"])
            deid = json.loads(sec.loc[(str(r.report_id), r.section), "sent_has_deid"])
            for i, s in enumerate(sents):
                if i == r.target_idx or deid[i]:
                    continue
                jobs[(str(r.report_id), r.section, i)] = s
        keys = list(jobs)
        print(f"[{corpus}] targets={len(tg)} context sentences to paraphrase={len(keys)}")
        prompts = [tok.apply_chat_template([{"role": "user", "content": PROMPT.format(sent=jobs[k])}], tokenize=False, add_generation_prompt=True) for k in keys]
        t0 = time.time()
        outs = llm.generate(prompts, sp)
        print(f"  generation done in {time.time()-t0:.0f}s")
        # NLI verification
        src, cands, owner = [], [], []
        for k, o in zip(keys, outs):
            seen = set()
            for c in o.outputs:
                txt = clean(c.text)
                if not txt or txt.lower() == jobs[k].lower() or txt.lower() in seen:
                    continue
                seen.add(txt.lower())
                src.append(jobs[k]); cands.append(txt); owner.append(k)
        fwd = nli.entail_prob(src, cands)
        bwd = nli.entail_prob(cands, src)
        best, log = {}, []
        for s, c, k, f, b in zip(src, cands, owner, fwd, bwd):
            ok = f >= args.nli_thr and b >= args.nli_thr and lexical_guard(s, c)
            et = edit_tokens(s, c)
            log.append({"report_id": k[0], "section": k[1], "sent_idx": k[2], "source": s, "paraphrase": c,
                        "nli_fwd": f, "nli_bwd": b, "guard_ok": lexical_guard(s, c), "edit_tokens": et, "accepted": ok and et >= args.min_edit})
            if ok and et >= args.min_edit and (k not in best or et > best[k][1]):
                best[k] = (c, et)
        pd.DataFrame(log).to_csv(NEW / f"data/pairs/{args.tag}_{corpus}_paraphrase_log.csv", index=False)
        kept = sum(1 for k in keys if k not in best)
        print(f"  accepted paraphrases: {len(best)}/{len(keys)}  (kept original: {kept})")

        # assemble S2 rows
        rows = []
        for r in tg.itertuples():
            sents = json.loads(sec.loc[(str(r.report_id), r.section), "sentences"])
            ctx = []
            n_par = 0
            for i, s in enumerate(sents):
                k = (str(r.report_id), r.section, i)
                if i == r.target_idx:
                    ctx.append(None)
                elif k in best:
                    ctx.append(best[k][0]); n_par += 1
                else:
                    ctx.append(s)
            def assemble(t):
                return " ".join(t if x is None else x for x in ctx)
            meta = dict(target_id=r.target_id, corpus=corpus, report_id=str(r.report_id), section=r.section, edit_type=r.edit_type,
                        subtype=r.subtype, pattern=r.pattern, edit_detail=r.edit_detail, target_idx=r.target_idx,
                        needs_expert_review=r.needs_expert_review, reference=r.reference,
                        n_context_sents=len(sents) - 1, n_context_paraphrased=n_par, paraphrase_model=args.model)
            rows.append({"uid": f"{r.target_id}__P2", **meta, "cell": "P2", "surface_layer": "S2", "is_changed": 0,
                         "candidate": assemble(r.p_sent), "edit_tokens_target": r.edit_tokens_p})
            rows.append({"uid": f"{r.target_id}__C2", **meta, "cell": "C2", "surface_layer": "S2", "is_changed": 1,
                         "candidate": assemble(r.c_sent), "edit_tokens_target": r.edit_tokens_c})
        out = pd.DataFrame(rows)
        out.to_csv(NEW / f"data/pairs/{args.tag}_{corpus}_S2.csv", index=False)
        full = pd.concat([pd.read_csv(NEW / f"data/pairs/{args.tag}_{corpus}_S0S1.csv"), out], ignore_index=True)
        full.to_csv(NEW / f"data/pairs/{args.tag}_{corpus}_all.csv", index=False)
        print(f"  wrote {len(out)} S2 rows; all cells -> {args.tag}_{corpus}_all.csv ({len(full)} rows)")
        print(f"  context paraphrase coverage: mean {out.n_context_paraphrased.mean():.2f}/{out.n_context_sents.mean():.2f} sentences")


if __name__ == "__main__":
    main()
