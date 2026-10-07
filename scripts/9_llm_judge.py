#!/usr/bin/env python
"""
9_llm_judge.py — LLM-as-judge scoring of (reference, candidate) rows with local open-weight models (vLLM).

Prompt A ("rubric"): does the candidate preserve the stated meaning of the reference?
    -> JSON {"label": "PRESERVED"|"CHANGED", "confidence": 0-100}
    score = confidence/100 if PRESERVED else 1 - confidence/100   (higher = closer to reference)
Prompt B ("errors"): GREEN-style — list clinically meaningful discrepancies, then "ERROR_COUNT: n"
    score = 1 / (1 + n)
Identity rows ARE sent to the model (v1 hard-coded them; we do not).

Output: {out}/{model_tag}__{prompt}.csv with columns uid, <model_tag>__<prompt> (score), label, confidence, raw

Run:  LD_LIBRARY_PATH=envs/llm/lib PATH=envs/llm/bin:$PATH HF_HOME=/home/irteam/hf_cache \
      envs/llm/bin/python scripts/9_llm_judge.py --pairs data/pairs/pilot_iu_all.csv --out results/1_pilot_iu/judges \
          --model Qwen/Qwen3-32B --tag qwen3_32b --prompt rubric
"""
from __future__ import annotations

import argparse
import json
import re
import time
from pathlib import Path

import pandas as pd

RUBRIC = """You are comparing two versions of the same section of a chest X-ray radiology report.

Reference:
{ref}

Candidate:
{cand}

Question: Does the candidate state exactly the same clinical findings as the reference?
Treat differences in wording, sentence order, formatting, abbreviations and synonyms as NOT changing the meaning.
Treat any change in a finding's presence/absence, laterality (left/right), anatomical location, severity or size, degree of certainty, measurement value or unit, or comparison with prior studies as CHANGING the meaning.
Judge only the relationship between the two texts; do not judge whether either is correct for the patient.

Answer with a single JSON object and nothing else:
{{"label": "PRESERVED" or "CHANGED", "confidence": <integer 0-100>}}"""

ERRORS = """You are evaluating a candidate chest X-ray report section against a reference section written by a radiologist.

Reference:
{ref}

Candidate:
{cand}

List every clinically meaningful discrepancy between the candidate and the reference (a finding that is present in one but absent or negated in the other; wrong laterality or location; different severity or size; different degree of certainty; different measurement; different comparison with prior studies). Ignore differences that do not change clinical meaning (wording, order, formatting, abbreviations, synonyms).
Write one line per discrepancy starting with "- ". If there is none, write "- none".
Finish with a final line exactly in the form:
ERROR_COUNT: <number of discrepancies>"""

# rubric_unit (10/7 review, point 6): the original rubric lists "measurement value or unit" among meaning changes, which
# may itself induce false alarms on unit conversions. This variant says explicitly that a converted quantity is the same.
RUBRIC_UNIT = RUBRIC.replace(
    "Treat differences in wording, sentence order, formatting, abbreviations and synonyms as NOT changing the meaning.",
    "Treat differences in wording, sentence order, formatting, abbreviations and synonyms as NOT changing the meaning. "
    "The same quantity expressed in another unit (for example 2.5 cm and 25 mm) is NOT a change.").replace(
    "measurement value or unit", "the measured quantity")
assert RUBRIC_UNIT != RUBRIC
PROMPTS = {"rubric": RUBRIC, "rubric_unit": RUBRIC_UNIT, "errors": ERRORS}


def parse_rubric(text):
    ms = re.findall(r"\{[^{}]*\}", text, flags=re.S)
    label, conf = None, None
    if ms:
        try:
            obj = json.loads(ms[-1])
            label = str(obj.get("label", "")).strip().upper()
            conf = float(obj.get("confidence", 50))
        except Exception:
            pass
    if label not in ("PRESERVED", "CHANGED"):
        up = text.upper()
        label = "CHANGED" if "CHANGED" in up else ("PRESERVED" if "PRESERVED" in up else "UNPARSED")
        conf = 50.0 if conf is None else conf
    conf = max(0.0, min(100.0, conf if conf is not None else 50.0))
    if label == "PRESERVED":
        score = conf / 100
    elif label == "CHANGED":
        score = 1 - conf / 100
    else:
        score = 0.5
    return label, conf, score


def parse_errors(text):
    m = re.findall(r"ERROR_COUNT:\s*(\d+)", text)
    if m:
        n = int(m[-1])
    else:
        n = len([l for l in text.splitlines() if l.strip().startswith("- ") and "none" not in l.lower()])
    return f"n={n}", float(n), 1.0 / (1.0 + n)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pairs", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--prompt", default="rubric", choices=list(PROMPTS))
    ap.add_argument("--gpu_mem", type=float, default=0.85)
    ap.add_argument("--max_model_len", type=int, default=4096)
    ap.add_argument("--max_tokens", type=int, default=64)
    ap.add_argument("--tp", type=int, default=1)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--reasoning", default="", help="e.g. 'low' for gpt-oss; empty = default")
    ap.add_argument("--no_think", action="store_true", help="disable thinking for Qwen3-style templates")
    args = ap.parse_args()

    df = pd.read_csv(args.pairs)
    if args.limit:
        df = df.head(args.limit)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    col = f"{args.tag}__{args.prompt}"
    target = out / f"{col}.csv"
    done = pd.read_csv(target) if target.exists() else None
    if done is not None and set(done.uid) >= set(df.uid):
        print("[skip] already scored", target)
        return

    from vllm import LLM, SamplingParams
    llm = LLM(model=args.model, gpu_memory_utilization=args.gpu_mem, enforce_eager=(__import__("os").environ.get("VLLM_EAGER", "1") == "1"), kv_cache_memory_bytes=(int(float(__import__("os").environ["KV_GB"]) * 2**30) if __import__("os").environ.get("KV_GB") else None), max_model_len=args.max_model_len,
              tensor_parallel_size=args.tp, seed=0, trust_remote_code=True)
    tok = llm.get_tokenizer()
    tmpl = PROMPTS[args.prompt]
    kw = {}
    if args.no_think:
        kw["enable_thinking"] = False
    sys_msg = []
    if args.reasoning:
        sys_msg = [{"role": "system", "content": f"Reasoning: {args.reasoning}"}]
    prompts = []
    for r in df.itertuples():
        msgs = sys_msg + [{"role": "user", "content": tmpl.format(ref=r.reference, cand=r.candidate)}]
        try:
            prompts.append(tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True, **kw))
        except TypeError:
            prompts.append(tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True))
    max_tokens = args.max_tokens if args.prompt.startswith("rubric") else max(args.max_tokens, 400)
    if args.reasoning or "gpt-oss" in args.model.lower():
        max_tokens = max(max_tokens, 4096)      # reasoning channel + final answer (1024 truncated ~1-10% of items)
    sp = SamplingParams(temperature=0.0, max_tokens=max_tokens, seed=0)
    t0 = time.time()
    outs = llm.generate(prompts, sp)
    print(f"[gen] {len(prompts)} prompts in {time.time()-t0:.0f}s", flush=True)
    rows = []
    for r, o in zip(df.itertuples(), outs):
        text = o.outputs[0].text
        finish = o.outputs[0].finish_reason
        # strip <think> blocks if any survived
        text_clean = re.sub(r"<think>.*?</think>", "", text, flags=re.S).strip()
        # harmony-format models (gpt-oss): "analysis...assistantfinal<answer>" -> judge ONLY the final channel.
        no_final = False
        if text_clean.startswith("analysis"):
            if "assistantfinal" in text_clean:
                answer = text_clean.split("assistantfinal")[-1].strip()
            else:                      # reasoning ran out of tokens before the final answer
                answer, no_final = "", True
        else:
            answer = text_clean
        if no_final:
            label, conf, score = "UNPARSED", float("nan"), float("nan")
        elif args.prompt.startswith("rubric"):
            label, conf, score = parse_rubric(answer)
        else:
            label, conf, score = parse_errors(answer)
        rows.append({"uid": r.uid, col: score, f"{col}__label": label, f"{col}__conf": conf,
                     f"{col}__finish": finish, f"{col}__raw": text_clean[:20000]})
    res = pd.DataFrame(rows)
    res.to_csv(target, index=False)
    print(res[f"{col}__label"].value_counts().to_string())
    print("[wrote]", target)


if __name__ == "__main__":
    main()
