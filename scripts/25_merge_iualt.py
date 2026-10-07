#!/usr/bin/env python
"""
25_merge_iualt.py — assemble results/2_full_iualt/scores for scorers that were run on the S2 cells only.

In the `iualt` set (10/7 review, S2 robustness) only the P2 / C2 candidates differ from the frozen IU set; identity, S0 and S1
rows are byte-identical (checked when data/pairs/full_iualts2_all.csv was written). To save compute on the shared machine the
slow scorers (GREEN, RadCliQ, temporal F1, CRIMSON) are run on the 602 S2 rows only (results/2_full_iualts2/scores) and the
remaining rows are copied from results/2_full_iu/scores. Scorers already present in results/2_full_iualt/scores are left alone.
"""
from pathlib import Path

import pandas as pd

NEW = Path(__file__).resolve().parent.parent
alt = pd.read_csv(NEW / "data/pairs/full_iualt_all.csv")[["uid", "cell"]]
keep_old = set(alt[~alt.cell.isin(["P2", "C2"])].uid)
out = NEW / "results/2_full_iualt/scores"
for f in sorted((NEW / "results/2_full_iualts2/scores").glob("*.csv")):
    if (out / f.name).exists():
        print("[skip]", f.name); continue
    new = pd.read_csv(f)
    old = pd.read_csv(NEW / "results/2_full_iu/scores" / f.name)
    old = old[old.uid.isin(keep_old)]
    m = pd.concat([old, new], ignore_index=True)
    missing = set(alt.uid) - set(m.uid)
    m.to_csv(out / f.name, index=False)
    print(f"[merged] {f.name}: {len(old)} rows from IU + {len(new)} new S2 rows; missing uids: {len(missing)}")
