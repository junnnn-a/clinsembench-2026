#!/usr/bin/env python
"""
3_generate_factorial_pairs.py  (X1: factorial minimal-pair set, S0 + S1 cells)   — v2 (shape-matched)

For every (report, section, edit type) we pick ONE target sentence s that carries a
type-specific trigger, and build a matched pair of rewritten sentences:

    P (meaning-preserving)  : s with a benign substitution at the trigger slot
    C (meaning-changing)    : s with a meaning flip at the SAME trigger slot

Shape matching (v2). A surface-only classifier must not separate P from C, so within a
variant P and C use the *same surface operation* (same number of edited tokens, same length
change) and differ only in the meaning slot.  Two mechanisms:
  (a) C := P's benign transformation + the flip   e.g. left pleural effusion
          P: left-sided pleural effusion       C: right-sided pleural effusion
          P: LLL                               C: RLL
  (b) both are single-token replacements       e.g. P: stable->unchanged  C: stable->increased
Where a residual asymmetry is unavoidable (negation, uncertainty), variants with opposite
asymmetry are provided and balanced by 4_sample_targets.py (`shape_sign`).

Cells written here (S2 = context paraphrase is filled by 5_paraphrase_context.py):
    identity : reference
    P0 / C0  : target sentence replaced, other sentences untouched          (S0, minimal)
    P1 / C1  : same but all sentences re-ordered with one shared permutation (S1, structure)

Rules fire only when the trigger occurs exactly once in the target sentence and the trigger
phrase occurs exactly once in the whole section. Sentences with de-id tokens are never targets.
`needs_expert_review` marks P lexicon entries we consider borderline (docs/3 §6.5).

Output: NEW/data/pairs/{corpus}_factorial_S0S1.csv (+ _targets.csv, _coverage.csv)
"""
from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import random
import re
from pathlib import Path

import pandas as pd

NEW = Path(__file__).resolve().parent.parent
MAX_EDIT_DIFF = 1

# ----------------------------------------------------------------------------- vocab
FINDING_TERMS = [
    "pleural effusions", "pleural effusion", "effusions", "effusion", "pneumothorax", "pneumothoraces",
    "atelectasis", "consolidation", "consolidations", "opacity", "opacities", "pulmonary edema", "edema",
    "pneumonia", "infiltrate", "infiltrates", "nodule", "nodules", "mass", "masses", "cardiomegaly",
    "fracture", "fractures", "airspace disease", "air space disease", "pleural thickening", "vascular congestion",
    "congestion", "emphysema", "hyperinflation", "lymphadenopathy", "adenopathy", "free air", "pneumoperitoneum",
    "interstitial markings", "interstitial opacities", "scarring", "granuloma", "granulomas", "calcification",
    "calcifications", "hiatal hernia", "hernia", "aspiration", "abnormality", "abnormalities", "process",
    "disease", "lesion", "lesions", "collapse", "volume loss", "fluid", "thickening", "widening", "enlargement",
    "displacement", "deformity", "blunting", "elevation", "acute cardiopulmonary process", "acute cardiopulmonary abnormality",
    "bronchiectasis", "fibrosis", "density", "densities", "opacification", "consolidative", "nodular opacity",
]
FINDING_RE = "(?:" + "|".join(re.escape(t) for t in sorted(FINDING_TERMS, key=len, reverse=True)) + ")"
DEVICE_RE = re.compile(r"\b(?:tube|tubes|catheter|catheters|line|lines|lead|leads|device|devices|pacemaker|pacer|"
                       r"wire|wires|hardware|stent|stents|port|port-a-cath|drain|drains|sheath|PICC|IJ|jugular|"
                       r"subclavian|sternotomy|valve|clip|clips|generator|position|positioned|placement|"
                       r"nasogastric|enteric|endotracheal|ETT|NG|tip|terminates|terminating|prosthesis|replacement)\b", re.I)
NEG_CUES = re.compile(r"\b(?:no|not|without|negative|absent|absence|free of|clear of|nor|neither|resolved|resolution|cleared)\b", re.I)
HEDGE_CUES = re.compile(r"\b(?:possible|possibly|probable|probably|likely|unlikely|may|might|could|cannot|can not|"
                        r"questionable|suspicious|suspected|suspect|concerning|worrisome|suggestive|suggesting|"
                        r"versus|vs\.?|or|equivocal|potential|potentially|presumably|presumed|favored|favor)\b", re.I)
TEMPORAL_CUES = re.compile(r"\b(?:unchanged|stable|improved|improving|improvement|worsened|worsening|worse|better|"
                           r"increased|increasing|increase|decreased|decreasing|decrease|resolved|resolution|new|newly|"
                           r"persistent|persists|persisting|progressed|progression|interval|prior|previous|previously|compared|"
                           r"comparison|since|again|similar|constant|redemonstrated|re-demonstrated)\b", re.I)
SEVERITY_WORDS = ["trace", "minimal", "mild", "small", "moderate", "large", "severe", "marked", "extensive", "massive", "tiny", "slight"]
SEVERITY_CUES = re.compile(r"\b(?:" + "|".join(SEVERITY_WORDS) + r"|mildly|moderately|severely|markedly|minimally|slightly)\b", re.I)
STRICT_NEG = re.compile(r"\b(?:no|not|without|negative|absent|absence|nor|neither)\b", re.I)
ANATOMY_CUES = re.compile(r"\b(?:lobe|lobes|base|bases|basilar|basal|bibasilar|apex|apices|apical|biapical|zone|zones|"
                          r"perihilar|parahilar|retrocardiac|hilar|hilum|hila)\b", re.I)


def _cap(src: str, repl: str) -> str:
    return repl[:1].upper() + repl[1:] if src[:1].isupper() and repl[:1].islower() else repl


def count_in(text: str, phrase: str) -> int:
    return len(re.findall(r"(?<![\w-])" + re.escape(phrase) + r"(?![\w-])", text, flags=re.I))


def edit_tokens(a: str, b: str) -> int:
    sm = difflib.SequenceMatcher(a=a.split(), b=b.split(), autojunk=False)
    return sum(max(i2 - i1, j2 - j1) for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag != "equal")


def rng_for(*keys) -> random.Random:
    h = hashlib.md5("|".join(str(k) for k in keys).encode()).hexdigest()
    return random.Random(int(h[:12], 16))


class Edit:
    def __init__(self, p_sent, c_sent, pattern, subtype="", detail="", needs_expert_review=False):
        self.p_sent, self.c_sent, self.pattern, self.subtype, self.detail = p_sent, c_sent, pattern, subtype, detail
        self.needs_expert_review = needs_expert_review


def one_sub(sent, span, repl):
    return sent[:span[0]] + repl + sent[span[1]:]


def _has_finding(np_text):
    return re.search(r"\b" + FINDING_RE + r"\b", np_text, flags=re.I) is not None


# ----------------------------------------------------------------------------- 1. laterality  (C = P-op + side flip)
LAT_SIDED_NOUNS = r"(?:pleural effusions?|effusions?|pneumothorax|atelectasis|opacit(?:y|ies)|consolidation|infiltrates?|nodules?|mass|airspace disease|pleural thickening|pleural fluid|densit(?:y|ies)|opacification)"
LAT_LOBE = r"(?:lower|upper|middle) lobe"


def rule_laterality(sent, section, rng):
    if len(re.findall(r"\b(?:left|right)\b", sent, flags=re.I)) != 1:
        return None
    if re.search(r"\b(?:bilateral|bilaterally|both|bibasilar|biapical|unilateral|left-sided|right-sided)\b", sent, flags=re.I):
        return None
    if DEVICE_RE.search(sent) or re.search(r"\b(?:left|right)\s+(?:heart|atri\w*|ventric\w*|main|hilum|hilar|paratracheal|neck|shoulder|humer\w*|breast|arm|hand|greater|more|than)\b", sent, flags=re.I):
        return None
    m = re.search(r"\b(left|right)\b(\s+(?:\w+\s+){0,2}?)(" + LAT_SIDED_NOUNS + r"|" + LAT_LOBE + r")\b", sent, flags=re.I)
    if not m:
        return None
    side, gap, head = m.group(1), m.group(2), m.group(3)
    other = "right" if side.lower() == "left" else "left"
    phrase = sent[m.start():m.end()]
    if count_in(section, phrase) != 1 or count_in(section, side) != 1:
        return None
    hl = head.lower()
    span_side = (m.start(1), m.end(1))
    span_head = (m.start(3), m.end(3))
    span_all = (m.start(), m.end())
    if re.fullmatch(LAT_SIDED_NOUNS, hl) and gap.strip() == "" and rng.random() < 0.5 \
            and re.search(r"\b(?:the|a|an|small|large|moderate|mild|trace|minimal|new|tiny)\s+$", sent[:m.start()], flags=re.I) \
            and sent[m.end():].lstrip()[:1] in (".", ",", ";", ""):
        # reorder variant: "<det/adj> left X" -> "<det/adj> X on the left"
        tail = sent[m.end():]
        p = sent[:m.start()] + f"{head} on the {side.lower()}" + tail
        c = sent[:m.start()] + f"{head} on the {other}" + tail
        pat = "side->on the side"
    elif re.fullmatch(LAT_SIDED_NOUNS, hl):
        p = one_sub(sent, span_side, _cap(side, side.lower() + "-sided"))
        c = one_sub(sent, span_side, _cap(side, other + "-sided"))
        pat = "side->sided"
    elif re.fullmatch(LAT_LOBE, hl) and gap.strip() == "":
        part = hl.split()[0][0].upper()
        p = one_sub(sent, span_all, side[0].upper() + part + "L")
        c = one_sub(sent, span_all, other[0].upper() + part + "L")
        pat = "lobe->abbrev"
    else:
        return None
    return Edit(p, c, pat, "lesion_laterality", f"{side.lower()}->{other}")


# ----------------------------------------------------------------------------- 2. negation  (shape-matched variants)
NP = r"((?:(?!\b(?:is|are|was|were)\b)[\w,/\-]+\s?){1,7}?)"


def _plural(x: str) -> bool:
    w = x.split()[-1].lower()
    return w.endswith(("s", "es")) and not w.endswith(("thorax", "mass", "atelectasis", "process", "disease", "sis", "us", "ss"))


def rule_negation(sent, section, rng):
    s = sent.rstrip()
    body = s[:-1] if s.endswith(".") else s
    n_neg = len(NEG_CUES.findall(body))
    # N1: "No X is seen."
    m = re.fullmatch(r"(No )(evidence of |signs? of |focal |definite |significant |new )?(.+?) (is|are) (seen|identified|noted|present|visualized|appreciated|evident|demonstrated|detected)", body, flags=re.I)
    if m and n_neg == 1 and _has_finding(m.group(3)):
        lead, x, be, v = (m.group(2) or ""), m.group(3), m.group(4), m.group(5)
        X = _cap("X", lead + x)
        v1 = rng.choice(["a", "b"])
        if v1 == "a":     # both delete one token
            p, c = f"No {lead}{x} {v}.", f"{X} {be} {v}."
        else:             # P replaces verb, C deletes 'No'   (shape_sign: C shorter)
            syn = {"seen": "identified", "identified": "seen", "noted": "identified", "present": "evident", "visualized": "seen",
                   "appreciated": "seen", "evident": "present", "demonstrated": "seen", "detected": "seen"}[v.lower()]
            p, c = f"No {lead}{x} {be} {syn}.", f"{X} {be} {v}."
        return Edit(p, c, f"N1{v1}:No X is seen", "negated->present", "drop No")
    # N2: "There is no X ..."
    m = re.match(r"(There (is|are) no )(evidence of |signs? of |focal |definite |significant |new )?(.+)", body, flags=re.I)
    if m and n_neg == 1 and _has_finding(m.group(4)):
        be, lead, rest = m.group(2), (m.group(3) or ""), m.group(4)
        v1 = rng.choice(["a", "b"])
        if v1 == "a":     # P: "No X."(-2)   C: "There is X."(-1)
            p, c = f"No {lead}{rest}.", f"There {be} {lead}{rest}."
        else:             # P: "There is no evidence of X"(+2)  C: "There is evidence of X"(+1)
            if lead:
                p, c = f"There {be} no {lead}{rest}.".replace(f"no {lead}", "no definite " + lead if "definite" not in lead else "no " + lead), f"There {be} {lead}{rest}."
            else:
                p, c = f"There {be} no evidence of {rest}.", f"There {be} evidence of {rest}."
        return Edit(p, c, f"N2{v1}:There is no X", "negated->present", "drop no")
    # N3: "No X."  (fragment)
    m = re.fullmatch(r"No ((?:[\w,/-]+ ?){1,7})", body, flags=re.I)
    # (v6, after full sets were frozen) "No X identified." must not be treated as a bare fragment: it produced
    # "X identified is absent." in 1.7% (IU) / 4.0% (MIMIC) of the frozen negation targets (docs/9 §known defects).
    if m and n_neg == 1 and _has_finding(m.group(1)) and not re.search(r"\b(?:change|interval|comparison|prior|significant|acute cardiopulmonary)\b", body, flags=re.I) \
            and not re.search(r"\b(?:identified|seen|noted|present|visualized|detected|appreciated|demonstrated|evident)$", body, flags=re.I):
        x = m.group(1).strip()
        be = "are" if _plural(x) else "is"
        X = _cap("X", x)
        v1 = rng.choice(["a", "b", "c"])
        if v1 == "a":     # identical shape
            p, c = f"{X} {be} absent.", f"{X} {be} present."
        elif v1 == "b":   # P: "No X seen."(+1)  C: "X seen."(0)
            p, c = f"No {x} seen.", f"{X} seen."
        else:             # P: "X absent."(0)   C: "X is present."(+1)
            p, c = f"{X} absent.", f"{X} {be} present."
        return Edit(p, c, f"N3{v1}:No X.", "negated->present", "fragment")
    # N4: "... without X"
    m = re.search(r"\bwithout (evidence of |signs? of )?(" + NP + r")", body, flags=re.I)
    if m and n_neg == 1 and _has_finding(m.group(2)):
        lead, x = (m.group(1) or ""), m.group(2)
        if lead:
            p = one_sub(body, (m.start(), m.end()), f"without {'signs of' if 'evidence' in lead else 'evidence of'} {x}") + "."
            c = one_sub(body, (m.start(), m.end()), f"with {lead}{x}") + "."
        else:
            p = one_sub(body, (m.start(), m.end()), f"with no {x}") + "."
            c = one_sub(body, (m.start(), m.end()), f"with new {x}") + "."
        return Edit(p, c, "N4:without X", "negated->present", "without->with")
    # N5: mid-sentence "no evidence of X"
    m = re.search(r"\bno evidence of (" + NP + r")", body, flags=re.I)
    if m and n_neg == 1 and _has_finding(m.group(1)) and not body.lower().startswith("there is no"):
        p = one_sub(body, (m.start(), m.end()), f"no sign of {m.group(1)}") + "."
        c = one_sub(body, (m.start(), m.end()), f"new evidence of {m.group(1)}") + "."
        return Edit(p, c, "N5:no evidence of X", "negated->present", "no->new")
    # N7: "negative for X"
    m = re.search(r"\bnegative for (" + NP + r")", body, flags=re.I)
    if m and n_neg == 1 and _has_finding(m.group(1)):
        p = one_sub(body, (m.start(), m.end()), f"negative for any {m.group(1)}") + "."
        c = one_sub(body, (m.start(), m.end()), f"positive for {m.group(1)}") + "."
        return Edit(p, c, "N7:negative for X", "negated->present", "negative->positive")
    # N6: positive "X is seen/present" -> negated
    if n_neg == 0 and not HEDGE_CUES.search(body):
        m = re.fullmatch(r"(?:There (?:is|are) )?(a |an |the )?((?:[\w,/-]+ ?){1,7}?) ?(?:(is|are) (seen|present|identified|noted|visualized|evident|demonstrated))", body, flags=re.I)
        if m and _has_finding(m.group(2)):
            be, v, x = m.group(3), m.group(4), m.group(2).strip()
            X = _cap("X", x)
            v1 = rng.choice(["a", "b"])
            if v1 == "a":   # P: "X seen."(-1)   C: "X not seen."(0)
                p, c = f"{X} {v}.", f"{X} not {v}."
            else:           # P: "X is visualized."(0)  C: "X is not seen."(+1)
                syn = {"seen": "visualized", "present": "evident", "identified": "seen", "noted": "identified",
                       "visualized": "seen", "evident": "present", "demonstrated": "seen"}[v.lower()]
                p, c = f"{X} {be} {syn}.", f"{X} {be} not {v}."
            return Edit(p, c, f"N6{v1}:X is seen->not", "present->negated", f"{v}->not {v}")
    return None


# ----------------------------------------------------------------------------- 3. measurement (shape-matched)
MEAS_RE = re.compile(r"(?<![\d.])(\d+(?:\.\d+)?)\s?(cm|mm)\b", re.I)


def _fmt(v: float) -> str:
    return f"{v:.1f}".rstrip("0").rstrip(".") if v != int(v) else str(int(v))


def rule_measurement(sent, section, rng):
    ms = list(MEAS_RE.finditer(sent))
    if len(ms) != 1 or len(MEAS_RE.findall(section)) != 1:
        return None
    m = ms[0]
    val, unit = float(m.group(1)), m.group(2).lower()
    if val <= 0 or val > 40:
        return None
    other = "mm" if unit == "cm" else "cm"
    conv = val * 10 if unit == "cm" else val / 10
    factor = rng.choice([2.0, 0.5])
    variant = rng.choice(["value", "magnitude"])
    p_txt = f"{_fmt(conv)} {other}"                       # P: same quantity in the other unit
    if variant == "value":                                # C: quantity doubled/halved, other unit
        c_txt = f"{_fmt(conv * factor)} {other}"
        detail = f"{_fmt(val)}{unit}->{_fmt(conv * factor)}{other}(={_fmt(val * factor)}{unit})"
        sub = "value"
    else:                                                 # C: converted digits with the original unit (10x error)
        c_txt = f"{_fmt(conv)} {unit}"
        detail = f"{_fmt(val)}{unit}->{_fmt(conv)}{unit}"
        sub = "unit"
    return Edit(one_sub(sent, m.span(), p_txt), one_sub(sent, m.span(), c_txt), f"measurement_{variant}", sub, detail)


# ----------------------------------------------------------------------------- 4. temporal (single-token replacements)
TEMPORAL_TABLE = {
    "unchanged": (["stable"], ["increased", "worsened", "improved"]),
    "stable": (["unchanged"], ["increased", "worsened", "improved"]),
    "improved": (["better"], ["worsened"]),
    "worsened": (["worse"], ["improved"]),
    "has increased": (["has progressed"], ["has decreased"]),
    "have increased": (["have progressed"], ["have decreased"]),
    "has decreased": (["has diminished"], ["has increased"]),
    "have decreased": (["have diminished"], ["have increased"]),
    "decreased": (["diminished"], ["increased"]),
    "has resolved": (["has cleared"], ["has persisted", "has worsened"]),
    "have resolved": (["have cleared"], ["have persisted", "have worsened"]),
    "new": (["newly identified"], ["previously seen"]),
}
_TEMP_KEYS = sorted(TEMPORAL_TABLE, key=len, reverse=True)
_TEMP_RE = re.compile(r"\b(" + "|".join(re.escape(k) for k in _TEMP_KEYS) + r")\b", re.I)


def rule_temporal(sent, section, rng):
    if DEVICE_RE.search(sent) or re.search(r"\b(?:hemodynamically|stable position|in position)\b", sent, flags=re.I):
        return None
    ms = list(_TEMP_RE.finditer(sent))
    if len(ms) != 1:
        return None
    m = ms[0]
    cue = m.group(1).lower()
    cue_words = set(cue.split())
    others = [w for w in TEMPORAL_CUES.findall(sent) if w.lower() not in cue_words]
    if others:
        return None
    if count_in(section, m.group(1)) != 1:
        return None
    if cue == "new" and not re.match(r"\s+(?:\w+[\s-]+){0,2}?" + FINDING_RE, sent[m.end():m.end() + 50], flags=re.I):
        return None
    p_alts, c_alts = TEMPORAL_TABLE[cue]
    c_word = rng.choice(c_alts)
    p = one_sub(sent, m.span(), _cap(m.group(1), rng.choice(p_alts)))
    c = one_sub(sent, m.span(), _cap(m.group(1), c_word))
    return Edit(p, c, f"temporal:{cue}", "comparison_direction", f"{cue}->{c_word}")


# ----------------------------------------------------------------------------- 5. severity (single-token replacements)
SIZE_NOUNS = re.compile(r"\b(?:pleural effusions?|effusions?|pneumothorax|hiatal hernia|hiatus hernia|hernia|nodules?|mass|masses|opacit(?:y|ies)|consolidation|infiltrates?|pneumothoraces|densit(?:y|ies))\b", re.I)
SEV_TABLE = {
    "trace": (["minimal"], ["small"], ["large", "moderate"], False),
    "minimal": (["trace"], ["mild", "small"], ["severe", "large"], False),
    "mild": (["slight"], ["moderate"], ["severe"], False),
    "small": (["small-sized"], ["moderate"], ["large"], True),
    "moderate": (["moderate-sized"], ["mild", "small", "large", "severe"], ["severe", "large"], True),
    "large": (["large-volume"], ["moderate"], ["small", "trace"], True),
    "severe": (["marked"], ["moderate"], ["mild"], False),
    "marked": (["severe"], ["moderate"], ["mild", "minimal"], False),
}
_SEV_RE = re.compile(r"\b(" + "|".join(SEV_TABLE) + r")\b", re.I)


def rule_severity(sent, section, rng):
    ms = list(_SEV_RE.finditer(sent))
    if len(ms) != 1 or len(SEVERITY_CUES.findall(sent)) != 1:
        return None
    if NEG_CUES.search(sent):
        return None
    m = ms[0]
    w = m.group(1).lower()
    if count_in(section, m.group(1)) != 1:
        return None
    after = sent[m.end():m.end() + 60]
    if not re.match(r"\s+(?:\w+[\s-]+){0,3}?" + FINDING_RE + r"\b", after, flags=re.I):
        return None
    p_alts, adj, ext, size_only = SEV_TABLE[w]
    size_ctx = SIZE_NOUNS.search(after[:45]) is not None
    if size_only and not size_ctx:
        return None
    if size_ctx:
        adj = [a for a in adj if a not in ("mild", "severe")] or adj
        ext = [a for a in ext if a not in ("mild", "severe")] or ext
    else:
        adj = [a for a in adj if a not in ("small", "large")] or adj
        ext = [a for a in ext if a not in ("small", "large")] or ext
    sub = rng.choice(["adjacent", "extreme"])
    c_word = rng.choice(adj if sub == "adjacent" else ext)
    p_word = rng.choice(p_alts)
    if w == "large" and not re.search(r"effusion", after[:40], flags=re.I):
        p_word = "large-sized"
    p = one_sub(sent, m.span(), _cap(m.group(1), p_word))
    c = one_sub(sent, m.span(), _cap(m.group(1), c_word))
    return Edit(p, c, f"severity:{w}->{p_word}", sub, f"{w}->{c_word}",
                needs_expert_review=p_word in {"small-sized", "large-volume", "large-sized", "moderate-sized", "minimal", "trace"})


# ----------------------------------------------------------------------------- 6. uncertainty
UNC_TABLE = {
    # cue: (P alternatives, C alternatives, subtype)   -- shapes are matched where possible
    "may represent": (["might represent", "may reflect"], ["clearly represents", "represents"], "hedged->definite"),
    "could represent": (["may represent", "might represent"], ["clearly represents", "represents"], "hedged->definite"),
    "may reflect": (["might reflect", "may represent"], ["clearly reflects", "reflects"], "hedged->definite"),
    "could reflect": (["may reflect", "might reflect"], ["clearly reflects", "reflects"], "hedged->definite"),
    "likely represents": (["probably represents"], ["clearly represents", "definitely represents"], "hedged->definite"),
    "likely reflects": (["probably reflects"], ["clearly reflects", "definitely reflects"], "hedged->definite"),
    "possibly representing": (["potentially representing"], ["clearly representing", "representing"], "hedged->definite"),
    "possibly reflecting": (["potentially reflecting"], ["clearly reflecting", "reflecting"], "hedged->definite"),
    "cannot be excluded": (["cannot be ruled out"], ["is excluded", "can be excluded"], "hedged->definite"),
    "can not be excluded": (["cannot be ruled out"], ["is excluded", "can be excluded"], "hedged->definite"),
    "cannot exclude": (["cannot rule out"], ["can exclude"], "hedged->definite"),
    "suspicious for": (["concerning for"], ["consistent with", "diagnostic of"], "hedged->definite"),
    "worrisome for": (["concerning for"], ["consistent with", "diagnostic of"], "hedged->definite"),
    "suggestive of": (["suggesting"], ["diagnostic of", "indicative of"], "hedged->definite"),
    "questionable": (["equivocal"], ["definite"], "hedged->definite"),
    "probable": (["likely"], ["definite"], "hedged->definite"),
    "possible": (["potential"], ["definite"], "hedged->definite"),
    "consistent with": (["compatible with"], ["suspicious for", "suggestive of"], "definite->hedged"),
    "compatible with": (["consistent with"], ["suspicious for", "suggestive of"], "definite->hedged"),
    "represents": (["reflects"], ["may represent"], "definite->hedged"),
    "reflects": (["represents"], ["may reflect"], "definite->hedged"),
    "diagnostic of": (["indicative of"], ["suspicious for", "suggestive of"], "definite->hedged"),
}
_UNC_KEYS = sorted(UNC_TABLE, key=len, reverse=True)
_UNC_RE = re.compile(r"\b(" + "|".join(re.escape(k) for k in _UNC_KEYS) + r")\b", re.I)
_UNC_FINDING_AFTER = {"questionable", "probable", "possible", "consistent with", "compatible with", "suggestive of",
                      "suspicious for", "worrisome for", "diagnostic of"}


def rule_uncertainty(sent, section, rng):
    ms = list(_UNC_RE.finditer(sent))
    if len(ms) != 1:
        return None
    m = ms[0]
    cue = m.group(1).lower()
    cue_words = set(cue.split())
    if [h for h in HEDGE_CUES.findall(sent) if h.lower() not in cue_words]:
        return None
    if count_in(section, m.group(1)) != 1:
        return None
    if NEG_CUES.search(sent) and cue not in ("cannot be excluded", "can not be excluded", "cannot exclude"):
        return None
    if cue in _UNC_FINDING_AFTER and not re.match(r"\s+(?:\w+[\s-]+){0,3}?" + FINDING_RE, sent[m.end():m.end() + 60], flags=re.I):
        return None
    p_alts, c_alts, sub = UNC_TABLE[cue]
    p_word, c_word = rng.choice(p_alts), rng.choice(c_alts)
    p = one_sub(sent, m.span(), _cap(m.group(1), p_word))
    c = one_sub(sent, m.span(), _cap(m.group(1), c_word))
    return Edit(p, c, f"uncertainty:{cue}", sub, f"{cue}->{c_word}",
                needs_expert_review=cue in {"probable", "possible", "questionable", "suggestive of", "represents", "reflects", "diagnostic of"})


# ----------------------------------------------------------------------------- 7. anatomy (C = P-op + region flip)
def rule_anatomy(sent, section, rng):
    if DEVICE_RE.search(sent):
        return None
    cands = []
    for m in re.finditer(r"\b(left|right) (lower|upper|middle) lobe\b", sent, flags=re.I):
        side, part = m.group(1), m.group(2).lower()
        flip = {"lower": "upper", "upper": "lower", "middle": rng.choice(["upper", "lower"])}[part]
        cands.append((m.span(), side[0].upper() + part[0].upper() + "L", side[0].upper() + flip[0].upper() + "L", "lobe->abbrev", f"{part}->{flip}"))
    for m in re.finditer(r"\blung bases\b", sent, flags=re.I):
        cands.append((m.span(), "bases of the lungs", "apices of the lungs", "lung bases->bases of the lungs", "bases->apices"))
    for m in re.finditer(r"\b(left|right) (?:lung )?base\b", sent, flags=re.I):
        cands.append((m.span(), f"base of the {m.group(1)} lung", f"apex of the {m.group(1)} lung", "base->base of the lung", "base->apex"))
    for m in re.finditer(r"\bbibasilar\b", sent, flags=re.I):
        cands.append((m.span(), "bilateral basilar", "bilateral apical", "bibasilar->bilateral basilar", "bibasilar->biapical"))
    for m in re.finditer(r"\bbasilar\b", sent, flags=re.I):
        cands.append((m.span(), "basal", "apical", "basilar->basal", "basilar->apical"))
    for m in re.finditer(r"\bperihilar\b", sent, flags=re.I):
        cands.append((m.span(), "parahilar", "peripheral", "perihilar->parahilar", "perihilar->peripheral"))
    if len(cands) != 1 or len(ANATOMY_CUES.findall(sent)) > 2:
        return None
    span, p_txt, c_txt, pat, detail = cands[0]
    phrase = sent[span[0]:span[1]]
    if count_in(section, phrase) != 1:
        return None
    if re.search(r"\b(?:bilateral|both)\b", sent, flags=re.I) and "lobe" in phrase.lower():
        return None
    p = one_sub(sent, span, _cap(phrase, p_txt))
    c = one_sub(sent, span, _cap(phrase, c_txt))
    return Edit(p, c, f"anatomy:{pat}", "region", detail, needs_expert_review=pat in {"perihilar->parahilar", "basilar->basal"})


RULES = {
    "laterality": rule_laterality, "negation": rule_negation, "measurement": rule_measurement,
    "temporal": rule_temporal, "severity": rule_severity, "uncertainty": rule_uncertainty, "anatomy": rule_anatomy,
}


# ----------------------------------------------------------------------------- assembly
def shared_permutation(n, rng):
    idx = list(range(n))
    for _ in range(20):
        rng.shuffle(idx)
        if idx != list(range(n)):
            return idx
    return idx[::-1]


def process_section(args):
    """One (report, section): returns (rows, targets). Top-level so multiprocessing can pickle it."""
    corpus, seed, report_id, section, sentences_json, deid_json = args
    sents = json.loads(sentences_json)
    deid = json.loads(deid_json)
    section_text = " ".join(sents)
    rows, targets = [], []
    for etype, rule in RULES.items():
        rng = rng_for(seed, corpus, report_id, section, etype)
        options = []
        for i, s in enumerate(sents):
            if deid[i] or len(s.split()) < 3:
                continue
            e = rule(s, section_text, rng_for(seed, corpus, report_id, section, etype, i))
            if e is None or e.p_sent == s or e.c_sent == s or e.p_sent == e.c_sent:
                continue
            ep, ec = edit_tokens(s, e.p_sent), edit_tokens(s, e.c_sent)
            if abs(ep - ec) > MAX_EDIT_DIFF or ep == 0 or ec == 0:
                continue
            options.append((i, e, ep, ec))
        if not options:
            continue
        i, e, ep, ec = rng.choice(options)
        perm = shared_permutation(len(sents), rng)
        tid = f"{corpus}_{report_id}_{section}_{etype}"
        ref = " ".join(sents)

        def assemble(target_sent, order=None):
            ss = sents[:i] + [target_sent] + sents[i + 1:]
            if order is not None:
                ss = [ss[j] for j in order]
            return " ".join(ss)

        lp, lc = len(e.p_sent.split()), len(e.c_sent.split())
        meta = dict(target_id=tid, corpus=corpus, report_id=str(report_id), section=section, edit_type=etype,
                    subtype=e.subtype, pattern=e.pattern, edit_detail=e.detail, target_idx=i, n_sent=len(sents),
                    target_sent=sents[i], p_sent=e.p_sent, c_sent=e.c_sent, edit_tokens_p=ep, edit_tokens_c=ec,
                    shape_sign=("C_longer" if lc > lp else "P_longer" if lp > lc else "equal"),
                    target_negated=bool(STRICT_NEG.search(sents[i])),
                    needs_expert_review=e.needs_expert_review, reference=ref, permutation=json.dumps(perm))
        targets.append(meta)
        cells = [("identity", ref, 0), ("P0", assemble(e.p_sent), 0), ("C0", assemble(e.c_sent), 1),
                 ("P1", assemble(e.p_sent, perm), 0), ("C1", assemble(e.c_sent, perm), 1)]
        for cell, cand, changed in cells:
            rows.append({"uid": f"{tid}__{cell}",
                         **{k: meta[k] for k in ("target_id", "corpus", "report_id", "section", "edit_type", "subtype", "pattern", "edit_detail", "target_idx", "needs_expert_review")},
                         "cell": cell, "surface_layer": "S0" if cell in ("P0", "C0") else ("S1" if cell in ("P1", "C1") else "identity"),
                         "is_changed": changed, "reference": ref, "candidate": cand,
                         "edit_tokens_target": (ep if cell.startswith("P") else ec if cell.startswith("C") else 0)})
    return rows, targets


def build(corpus_csv: Path, corpus: str, min_sents: int, out_dir: Path, seed: int, max_sections: int = 0, workers: int = 32):
    from multiprocessing import Pool
    df = pd.read_csv(corpus_csv)
    df = df[df.n_sent >= min_sents]
    if max_sections:
        df = df.sample(n=min(max_sections, len(df)), random_state=seed)
    jobs = [(corpus, seed, r.report_id, r.section, r.sentences, r.sent_has_deid) for r in df.itertuples()]
    rows, targets = [], []
    with Pool(workers) as pool:
        for k, (rw, tg) in enumerate(pool.imap_unordered(process_section, jobs, chunksize=64)):
            rows.extend(rw); targets.extend(tg)
            if k % 5000 == 0:
                print(f"  [{corpus}] {k}/{len(jobs)} sections, targets so far {len(targets)}", flush=True)
    out_dir.mkdir(parents=True, exist_ok=True)
    pairs, tg = pd.DataFrame(rows), pd.DataFrame(targets)
    pairs.to_csv(out_dir / f"{corpus}_factorial_S0S1.csv", index=False)
    tg.to_csv(out_dir / f"{corpus}_targets.csv", index=False)
    cov = tg.groupby(["section", "edit_type"]).agg(
        n_targets=("target_id", "size"), n_patterns=("pattern", "nunique"),
        top_pattern_share=("pattern", lambda x: x.value_counts(normalize=True).iloc[0]),
        edit_p=("edit_tokens_p", "mean"), edit_c=("edit_tokens_c", "mean"),
        c_longer=("shape_sign", lambda x: (x == "C_longer").mean()), p_longer=("shape_sign", lambda x: (x == "P_longer").mean()),
        review_share=("needs_expert_review", "mean")).reset_index()
    cov.to_csv(out_dir / f"{corpus}_coverage.csv", index=False)
    print(f"[{corpus}] sections={len(df)} targets={len(tg)} rows={len(pairs)}")
    print(cov.round(3).to_string(index=False))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", nargs="+", default=["iu", "mimic"])
    ap.add_argument("--min_sents", type=int, default=3)
    ap.add_argument("--seed", type=int, default=13)
    ap.add_argument("--max_sections", type=int, default=0, help="subsample sections (MIMIC is large)")
    ap.add_argument("--out_dir", default=str(NEW / "data/pairs"))
    ap.add_argument("--workers", type=int, default=32)
    args = ap.parse_args()
    for c in args.corpus:
        build(NEW / f"data/corpus/{c}_sections.csv", c, args.min_sents, Path(args.out_dir), args.seed, args.max_sections, args.workers)


if __name__ == "__main__":
    main()
