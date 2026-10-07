# X3 — surface-only predictability of benchmark labels

| benchmark | n | surface_only_LR_auroc | jaccard_drop_auroc | edit_tokens_auroc | strongest_single_feature | direction |
|---|---|---|---|---|---|---|
| ClinSemBench v1 (impression, rule labels) | 2400 | 0.917 | 0.849 | 0.186 | jaccard_drop=0.849 | larger surface change => benign |
| ClinSemBench v1 (findings, rule labels) | 2400 | 0.964 | 0.890 | 0.156 | jaccard_drop=0.890 | larger surface change => benign |
| ClinSemBench v1 (480-pair set, human labels) | 467 | 0.827 | 0.811 | 0.238 | jaccard_drop=0.811 | larger surface change => benign |
| factorial IU — confound v1-type (C0 vs P1) | 1780 | 1.000 | 0.586 | 0.001 | char_ratio_drop=0.000 | larger surface change => benign |
| factorial IU — confound ReEvalMed-type (C0 vs P2) | 1780 | 0.983 | 0.053 | 0.017 | edit_tokens=0.017 | larger surface change => benign |
| factorial IU — controlled S0 (C0 vs P0) | 1780 | 0.643 | 0.586 | 0.508 | tokenf1_drop=0.588 | ≈ none |
| factorial IU — controlled S2 (C2 vs P2) | 1780 | 0.540 | 0.521 | 0.501 | tokenf1_drop=0.521 | ≈ none |
| factorial MIMIC — confound v1-type (C0 vs P1) | 2100 | 1.000 | 0.558 | 0.000 | char_ratio_drop=0.000 | larger surface change => benign |
| factorial MIMIC — confound ReEvalMed-type (C0 vs P2) | 2100 | 0.996 | 0.011 | 0.005 | char_ratio_drop=0.003 | larger surface change => benign |
| factorial MIMIC — controlled S0 (C0 vs P0) | 2100 | 0.622 | 0.558 | 0.508 | tokenf1_drop=0.568 | ≈ none |
| factorial MIMIC — controlled S2 (C2 vs P2) | 2100 | 0.523 | 0.513 | 0.501 | tokenf1_drop=0.515 | ≈ none |

## ReEvalMed (published per-metric means; data not available locally)

| metric | mean_score_significant_error_pairs | mean_score_insignificant_pairs | score_gap(sig - insig) | rewards_the_erroneous_candidate |
|---|---|---|---|---|
| BLEU | 78.48 | 41.89 | 36.59 | True |
| ROUGE-L | 87.90 | 65.95 | 21.95 | True |
| RadGraph | 81.35 | 58.56 | 22.79 | True |
| BERT-F1 | 97.31 | 92.99 | 4.32 | True |
| GREEN | 74.30 | 74.76 | -0.46 | False |
