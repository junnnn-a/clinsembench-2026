# 0_audit — automatic audit of the ARR-May experiment

## A. Pooled AUROC incl. trivial baselines (subset200, same rows as paper Table 3)

| metric | findings | impression |
|---|---|---|
| green | 0.896 | 0.903 |
| jaccard | 0.890 | 0.849 |
| token_f1 | 0.818 | 0.821 |
| neg_edit_tokens | 0.844 | 0.814 |
| bow_changed | 0.827 | 0.812 |
| ratescore | 0.804 | 0.768 |
| radgraph | 0.639 | 0.650 |
| temporal | 0.609 | 0.613 |
| f1chexbert | 0.581 | 0.572 |
| seqratio | 0.173 | 0.254 |
| bertscore | 0.165 | 0.221 |

### cluster(report)-bootstrap 95% CI

| section | metric | n | auroc | cluster_ci_low | cluster_ci_high |
|---|---|---|---|---|---|
| impression | green | 2400 | 0.903 | 0.893 | 0.913 |
| impression | ratescore | 2400 | 0.768 | 0.743 | 0.793 |
| impression | radgraph | 2400 | 0.650 | 0.624 | 0.675 |
| impression | temporal | 2400 | 0.613 | 0.604 | 0.622 |
| impression | f1chexbert | 2400 | 0.572 | 0.561 | 0.582 |
| impression | bertscore | 2400 | 0.221 | 0.204 | 0.236 |
| impression | token_f1 | 2400 | 0.821 | 0.798 | 0.844 |
| impression | jaccard | 2400 | 0.849 | 0.828 | 0.871 |
| impression | seqratio | 2400 | 0.254 | 0.233 | 0.273 |
| impression | bow_changed | 2400 | 0.812 | 0.795 | 0.831 |
| impression | neg_edit_tokens | 2400 | 0.814 | 0.798 | 0.834 |
| findings | green | 2400 | 0.896 | 0.884 | 0.908 |
| findings | ratescore | 2400 | 0.804 | 0.781 | 0.828 |
| findings | radgraph | 2400 | 0.639 | 0.610 | 0.663 |
| findings | temporal | 2400 | 0.609 | 0.600 | 0.619 |
| findings | f1chexbert | 2400 | 0.581 | 0.569 | 0.592 |
| findings | bertscore | 2400 | 0.165 | 0.150 | 0.181 |
| findings | token_f1 | 2400 | 0.818 | 0.795 | 0.843 |
| findings | jaccard | 2400 | 0.890 | 0.871 | 0.909 |
| findings | seqratio | 2400 | 0.173 | 0.158 | 0.191 |
| findings | bow_changed | 2400 | 0.827 | 0.809 | 0.845 |
| findings | neg_edit_tokens | 2400 | 0.844 | 0.828 | 0.858 |

## A2. Per-type AUROC (changed type vs pooled benign)

| section | changed_type | bertscore | bow_changed | f1chexbert | green | jaccard | neg_edit_tokens | radgraph | ratescore | seqratio | temporal | token_f1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| findings | anatomy_region_flip | 0.054 | 0.827 | 0.490 | 0.939 | 0.898 | 1.000 | 0.585 | 0.833 | 0.039 | 0.500 | 0.779 |
| findings | false_finding_insertion | 0.421 | 0.827 | 0.750 | 0.979 | 0.963 | 0.402 | 0.780 | 0.883 | 0.521 | 0.795 | 0.970 |
| findings | finding_deletion | 0.741 | 0.827 | 0.852 | 0.976 | 0.979 | 0.359 | 0.888 | 0.918 | 0.625 | 0.703 | 0.984 |
| findings | laterality_flip | 0.002 | 0.827 | 0.485 | 0.967 | 0.801 | 1.000 | 0.539 | 0.781 | 0.044 | 0.500 | 0.790 |
| findings | measurement_flip | 0.000 | 0.827 | 0.485 | 0.821 | 0.904 | 1.000 | 0.538 | 0.660 | 0.020 | 0.500 | 0.750 |
| findings | negation_flip | 0.150 | 0.827 | 0.696 | 0.945 | 0.782 | 0.837 | 0.642 | 0.799 | 0.216 | 0.500 | 0.811 |
| findings | severity_flip | 0.003 | 0.827 | 0.487 | 0.954 | 0.909 | 1.000 | 0.581 | 0.806 | 0.041 | 0.500 | 0.788 |
| findings | temporal_comparison_flip | 0.069 | 0.827 | 0.492 | 0.946 | 0.897 | 1.000 | 0.575 | 0.778 | 0.038 | 0.988 | 0.789 |
| findings | uncertainty_flip | 0.044 | 0.827 | 0.490 | 0.535 | 0.876 | 0.999 | 0.619 | 0.782 | 0.013 | 0.500 | 0.703 |
| impression | anatomy_region_flip | 0.066 | 0.812 | 0.490 | 0.951 | 0.842 | 0.976 | 0.631 | 0.787 | 0.139 | 0.500 | 0.795 |
| impression | false_finding_insertion | 0.640 | 0.812 | 0.728 | 0.986 | 0.945 | 0.339 | 0.807 | 0.853 | 0.588 | 0.810 | 0.958 |
| impression | finding_deletion | 0.868 | 0.812 | 0.820 | 0.985 | 0.974 | 0.301 | 0.881 | 0.914 | 0.728 | 0.710 | 0.980 |
| impression | laterality_flip | 0.030 | 0.812 | 0.487 | 0.974 | 0.790 | 0.977 | 0.577 | 0.754 | 0.150 | 0.500 | 0.805 |
| impression | measurement_flip | 0.005 | 0.812 | 0.487 | 0.792 | 0.831 | 0.977 | 0.520 | 0.619 | 0.060 | 0.500 | 0.744 |
| impression | negation_flip | 0.191 | 0.812 | 0.640 | 0.934 | 0.739 | 0.834 | 0.663 | 0.783 | 0.210 | 0.500 | 0.774 |
| impression | severity_flip | 0.023 | 0.812 | 0.487 | 0.981 | 0.850 | 0.977 | 0.611 | 0.770 | 0.174 | 0.500 | 0.810 |
| impression | temporal_comparison_flip | 0.083 | 0.812 | 0.507 | 0.944 | 0.849 | 0.977 | 0.599 | 0.701 | 0.137 | 0.995 | 0.792 |
| impression | uncertainty_flip | 0.082 | 0.812 | 0.497 | 0.585 | 0.823 | 0.967 | 0.561 | 0.730 | 0.097 | 0.500 | 0.736 |

## B. AUROC of ALL changed vs. each single benign type

| section | metric | benign_format | benign_paraphrase_rule | benign_sentence_order |
|---|---|---|---|---|
| findings | bertscore | 0.097 | 0.310 | 0.087 |
| findings | bow_changed | 0.980 | 0.500 | 1.000 |
| findings | f1chexbert | 0.576 | 0.591 | 0.576 |
| findings | green | 0.908 | 0.906 | 0.873 |
| findings | jaccard | 0.939 | 0.757 | 0.974 |
| findings | neg_edit_tokens | 0.806 | 0.743 | 0.983 |
| findings | radgraph | 0.576 | 0.805 | 0.535 |
| findings | ratescore | 0.662 | 0.864 | 0.887 |
| findings | seqratio | 0.228 | 0.275 | 0.016 |
| findings | temporal | 0.609 | 0.609 | 0.609 |
| findings | token_f1 | 0.966 | 0.489 | 1.000 |
| impression | bertscore | 0.160 | 0.346 | 0.156 |
| impression | bow_changed | 0.938 | 0.500 | 1.000 |
| impression | f1chexbert | 0.579 | 0.572 | 0.564 |
| impression | green | 0.909 | 0.916 | 0.885 |
| impression | jaccard | 0.883 | 0.686 | 0.979 |
| impression | neg_edit_tokens | 0.778 | 0.699 | 0.965 |
| impression | radgraph | 0.667 | 0.732 | 0.550 |
| impression | ratescore | 0.657 | 0.779 | 0.867 |
| impression | seqratio | 0.316 | 0.379 | 0.066 |
| impression | temporal | 0.613 | 0.613 | 0.613 |
| impression | token_f1 | 0.904 | 0.561 | 1.000 |

## B2. Edit magnitude by perturbation type

| section | perturbation_type | n | edit_tokens_mean | edit_tokens_median | len_diff_mean | ref_len_mean | token_f1_drop_mean | bow_unchanged_rate |
|---|---|---|---|---|---|---|---|---|
| impression | anatomy_region_flip | 200 | 1.00 | 1.00 | 0.00 | 48.04 | 0.03 | 0.00 |
| impression | benign_format | 200 | 4.12 | 4.00 | 4.09 | 38.72 | 0.01 | 0.88 |
| impression | benign_paraphrase_rule | 200 | 2.76 | 3.00 | -1.56 | 51.31 | 0.03 | 0.00 |
| impression | benign_sentence_order | 200 | 33.69 | 26.00 | 0.00 | 48.05 | 0.00 | 1.00 |
| impression | false_finding_insertion | 200 | 8.65 | 7.00 | 8.65 | 38.72 | 0.14 | 0.00 |
| impression | finding_deletion | 200 | 13.76 | 12.50 | -13.26 | 41.69 | 0.33 | 0.00 |
| impression | laterality_flip | 200 | 1.00 | 1.00 | 0.00 | 45.64 | 0.03 | 0.00 |
| impression | measurement_flip | 200 | 1.00 | 1.00 | 0.00 | 63.54 | 0.02 | 0.00 |
| impression | negation_flip | 200 | 1.95 | 1.00 | 0.77 | 43.34 | 0.04 | 0.00 |
| impression | severity_flip | 200 | 1.00 | 1.00 | 0.00 | 45.08 | 0.04 | 0.00 |
| impression | temporal_comparison_flip | 200 | 1.00 | 1.00 | 0.00 | 50.34 | 0.03 | 0.00 |
| impression | uncertainty_flip | 200 | 1.10 | 1.00 | 0.76 | 43.68 | 0.02 | 0.00 |
| findings | anatomy_region_flip | 200 | 1.01 | 1.00 | 0.00 | 62.09 | 0.02 | 0.00 |
| findings | benign_format | 200 | 5.56 | 5.00 | 5.51 | 57.27 | 0.00 | 0.96 |
| findings | benign_paraphrase_rule | 200 | 3.29 | 3.00 | -1.63 | 57.65 | 0.03 | 0.00 |
| findings | benign_sentence_order | 200 | 45.91 | 38.00 | 0.00 | 58.60 | 0.00 | 1.00 |
| findings | false_finding_insertion | 200 | 8.97 | 10.00 | 8.97 | 57.27 | 0.09 | 0.00 |
| findings | finding_deletion | 200 | 14.04 | 12.00 | -14.00 | 58.81 | 0.17 | 0.00 |
| findings | laterality_flip | 200 | 1.00 | 1.00 | 0.00 | 61.20 | 0.02 | 0.00 |
| findings | measurement_flip | 200 | 1.00 | 1.00 | 0.00 | 72.33 | 0.02 | 0.00 |
| findings | negation_flip | 200 | 2.48 | 3.00 | 0.91 | 55.97 | 0.02 | 0.00 |
| findings | severity_flip | 200 | 1.00 | 1.00 | 0.00 | 59.85 | 0.02 | 0.00 |
| findings | temporal_comparison_flip | 200 | 1.00 | 1.00 | 0.00 | 58.87 | 0.02 | 0.00 |
| findings | uncertainty_flip | 200 | 1.06 | 1.00 | 0.86 | 56.58 | 0.01 | 0.00 |

## B3. Spearman(metric penalty, #edited tokens)

| section | metric | spearman_penalty_vs_edit_tokens |
|---|---|---|
| impression | green | -0.139 |
| impression | ratescore | -0.030 |
| impression | radgraph | 0.219 |
| impression | temporal | 0.115 |
| impression | f1chexbert | 0.353 |
| impression | bertscore | 0.810 |
| findings | green | -0.167 |
| findings | ratescore | -0.052 |
| findings | radgraph | 0.289 |
| findings | temporal | 0.085 |
| findings | f1chexbert | 0.377 |
| findings | bertscore | 0.865 |

## C. Rule-quality heuristics

| section | split | perturbation_type | issue | n_type | n_flagged | rate |
|---|---|---|---|---|---|---|
| impression | full_clean_5k | identity | reference_has_duplicated_sentence | 4666 | 18 | 0.004 |
| impression | full_clean_5k | identity | reference_has_numbered_list | 4666 | 490 | 0.105 |
| impression | full_clean_5k | identity | reference_has_abbrev_split_risk(Dr./a.m./p.m.) | 4666 | 373 | 0.080 |
| impression | full_clean_5k | identity | reference_word_count<=5 | 4666 | 49 | 0.011 |
| impression | full_clean_5k | negation_flip | direction=present->negated(insert 'no') | 3581 | 2254 | 0.629 |
| impression | full_clean_5k | negation_flip | direction=negated->present | 3581 | 1327 | 0.371 |
| impression | full_clean_5k | negation_flip | inserted 'no' lands mid-phrase (e.g. 'left no pleural effusion') | 2254 | 2125 | 0.943 |
| impression | full_clean_5k | negation_flip | 'present' finding sits in a sentence that already has a negation cue | 2254 | 171 | 0.076 |
| impression | full_clean_5k | negation_flip | negated->present leaves coordinated remainder ('X is present or Y') | 1327 | 184 | 0.139 |
| impression | full_clean_5k | laterality_flip | source=bilateral (paper says bilateral is skipped) | 3229 | 295 | 0.091 |
| impression | full_clean_5k | laterality_flip | reference mentions BOTH left and right (first-match flip may create contradiction) | 3229 | 1115 | 0.345 |
| impression | full_clean_5k | laterality_flip | flipped token is non-anatomical candidate ('right heart', 'left in place', 'right IJ/PICC' device) | 3229 | 693 | 0.215 |
| impression | full_clean_5k | measurement_flip | unit swap only (cm<->mm); numeric value never edited | 322 | 322 | 1.000 |
| impression | full_clean_5k | uncertainty_flip | direction=asserted->possible (insert 'possible') | 3049 | 2471 | 0.810 |
| impression | full_clean_5k | uncertainty_flip | direction=hedged->definite | 3049 | 578 | 0.190 |
| impression | full_clean_5k | benign_format | prefix 'Report impression:' (single-sentence refs; also used for FINDINGS section) | 4666 | 661 | 0.142 |
| impression | full_clean_5k | benign_format | bullets break numbered list ('- 1. - ...') | 4666 | 489 | 0.105 |
| impression | full_clean_5k | benign_sentence_order | reference has discourse connective (However/Otherwise/This/These/Also ...) -> order-dependent | 3053 | 413 | 0.135 |
| impression | full_clean_5k | benign_sentence_order | reference has numbered list | 3053 | 485 | 0.159 |
| impression | full_clean_5k | finding_deletion | whole section replaced by 'No acute cardiopulmonary abnormality.' | 3108 | 353 | 0.114 |
| impression | full_clean_5k | false_finding_insertion | reference lacks terminal period before appended sentence | 4666 | 144 | 0.031 |
| impression | full_clean_5k | false_finding_insertion | inserted sentence carries laterality/severity/size (multi-factor, not minimal) | 4666 | 4666 | 1.000 |
| impression | full_clean_5k | temporal_comparison_flip | detail=stable/unchanged->increased | 1963 | 1156 | 0.589 |
| impression | full_clean_5k | temporal_comparison_flip | flipped word describes device/position ('tube|catheter|line|lead ... unchanged') | 1963 | 303 | 0.154 |
| impression | full_clean_5k | severity_flip | polarity flip (small/trace/mild/minimal <-> large/severe), not an adjacent grade | 2253 | 1789 | 0.794 |
| impression | subset200 | identity | reference_has_duplicated_sentence | 1741 | 10 | 0.006 |
| impression | subset200 | identity | reference_has_numbered_list | 1741 | 209 | 0.120 |
| impression | subset200 | identity | reference_has_abbrev_split_risk(Dr./a.m./p.m.) | 1741 | 146 | 0.084 |
| impression | subset200 | identity | reference_word_count<=5 | 1741 | 8 | 0.005 |
| impression | subset200 | negation_flip | direction=present->negated(insert 'no') | 200 | 131 | 0.655 |
| impression | subset200 | negation_flip | direction=negated->present | 200 | 69 | 0.345 |
| impression | subset200 | negation_flip | inserted 'no' lands mid-phrase (e.g. 'left no pleural effusion') | 131 | 120 | 0.916 |
| impression | subset200 | negation_flip | 'present' finding sits in a sentence that already has a negation cue | 131 | 14 | 0.107 |
| impression | subset200 | negation_flip | negated->present leaves coordinated remainder ('X is present or Y') | 69 | 11 | 0.159 |
| impression | subset200 | laterality_flip | source=bilateral (paper says bilateral is skipped) | 200 | 15 | 0.075 |
| impression | subset200 | laterality_flip | reference mentions BOTH left and right (first-match flip may create contradiction) | 200 | 70 | 0.350 |
| impression | subset200 | laterality_flip | flipped token is non-anatomical candidate ('right heart', 'left in place', 'right IJ/PICC' device) | 200 | 42 | 0.210 |
| impression | subset200 | measurement_flip | unit swap only (cm<->mm); numeric value never edited | 200 | 200 | 1.000 |
| impression | subset200 | uncertainty_flip | direction=asserted->possible (insert 'possible') | 200 | 161 | 0.805 |
| impression | subset200 | uncertainty_flip | direction=hedged->definite | 200 | 39 | 0.195 |
| impression | subset200 | benign_format | prefix 'Report impression:' (single-sentence refs; also used for FINDINGS section) | 200 | 25 | 0.125 |
| impression | subset200 | benign_format | bullets break numbered list ('- 1. - ...') | 200 | 23 | 0.115 |
| impression | subset200 | benign_sentence_order | reference has discourse connective (However/Otherwise/This/These/Also ...) -> order-dependent | 200 | 31 | 0.155 |
| impression | subset200 | benign_sentence_order | reference has numbered list | 200 | 29 | 0.145 |
| impression | subset200 | finding_deletion | whole section replaced by 'No acute cardiopulmonary abnormality.' | 200 | 25 | 0.125 |
| impression | subset200 | false_finding_insertion | reference lacks terminal period before appended sentence | 200 | 7 | 0.035 |
| impression | subset200 | false_finding_insertion | inserted sentence carries laterality/severity/size (multi-factor, not minimal) | 200 | 200 | 1.000 |
| impression | subset200 | temporal_comparison_flip | detail=stable/unchanged->increased | 200 | 108 | 0.540 |
| impression | subset200 | temporal_comparison_flip | flipped word describes device/position ('tube|catheter|line|lead ... unchanged') | 200 | 31 | 0.155 |
| impression | subset200 | severity_flip | polarity flip (small/trace/mild/minimal <-> large/severe), not an adjacent grade | 200 | 148 | 0.740 |
| findings | full_clean_5k | identity | reference_has_duplicated_sentence | 4667 | 20 | 0.004 |
| findings | full_clean_5k | identity | reference_has_numbered_list | 4667 | 92 | 0.020 |
| findings | full_clean_5k | identity | reference_has_abbrev_split_risk(Dr./a.m./p.m.) | 4667 | 178 | 0.038 |
| findings | full_clean_5k | identity | reference_word_count<=5 | 4667 | 7 | 0.001 |
| findings | full_clean_5k | negation_flip | direction=present->negated(insert 'no') | 3964 | 1642 | 0.414 |
| findings | full_clean_5k | negation_flip | direction=negated->present | 3964 | 2322 | 0.586 |
| findings | full_clean_5k | negation_flip | inserted 'no' lands mid-phrase (e.g. 'left no pleural effusion') | 1642 | 1552 | 0.945 |
| findings | full_clean_5k | negation_flip | 'present' finding sits in a sentence that already has a negation cue | 1642 | 141 | 0.086 |
| findings | full_clean_5k | negation_flip | negated->present leaves coordinated remainder ('X is present or Y') | 2322 | 626 | 0.270 |
| findings | full_clean_5k | laterality_flip | source=bilateral (paper says bilateral is skipped) | 3666 | 230 | 0.063 |
| findings | full_clean_5k | laterality_flip | reference mentions BOTH left and right (first-match flip may create contradiction) | 3666 | 1689 | 0.461 |
| findings | full_clean_5k | laterality_flip | flipped token is non-anatomical candidate ('right heart', 'left in place', 'right IJ/PICC' device) | 3666 | 1015 | 0.277 |
| findings | full_clean_5k | measurement_flip | unit swap only (cm<->mm); numeric value never edited | 465 | 465 | 1.000 |
| findings | full_clean_5k | uncertainty_flip | direction=asserted->possible (insert 'possible') | 3145 | 2596 | 0.825 |
| findings | full_clean_5k | uncertainty_flip | direction=hedged->definite | 3145 | 549 | 0.175 |
| findings | full_clean_5k | benign_format | prefix 'Report impression:' (single-sentence refs; also used for FINDINGS section) | 4667 | 96 | 0.021 |
| findings | full_clean_5k | benign_format | bullets break numbered list ('- 1. - ...') | 4667 | 91 | 0.019 |
| findings | full_clean_5k | benign_sentence_order | reference has discourse connective (However/Otherwise/This/These/Also ...) -> order-dependent | 4300 | 577 | 0.134 |
| findings | full_clean_5k | benign_sentence_order | reference has numbered list | 4300 | 92 | 0.021 |
| findings | full_clean_5k | finding_deletion | whole section replaced by 'No acute cardiopulmonary abnormality.' | 3198 | 23 | 0.007 |
| findings | full_clean_5k | false_finding_insertion | reference lacks terminal period before appended sentence | 4667 | 132 | 0.028 |
| findings | full_clean_5k | false_finding_insertion | inserted sentence carries laterality/severity/size (multi-factor, not minimal) | 4667 | 4667 | 1.000 |
| findings | full_clean_5k | temporal_comparison_flip | detail=stable/unchanged->increased | 2645 | 1729 | 0.654 |
| findings | full_clean_5k | temporal_comparison_flip | flipped word describes device/position ('tube|catheter|line|lead ... unchanged') | 2645 | 413 | 0.156 |
| findings | full_clean_5k | severity_flip | polarity flip (small/trace/mild/minimal <-> large/severe), not an adjacent grade | 2667 | 2150 | 0.806 |
| findings | subset200 | identity | reference_has_duplicated_sentence | 1727 | 10 | 0.006 |
| findings | subset200 | identity | reference_has_numbered_list | 1727 | 41 | 0.024 |
| findings | subset200 | identity | reference_has_abbrev_split_risk(Dr./a.m./p.m.) | 1727 | 83 | 0.048 |
| findings | subset200 | identity | reference_word_count<=5 | 1727 | 0 | 0.000 |
| findings | subset200 | negation_flip | direction=present->negated(insert 'no') | 200 | 78 | 0.390 |
| findings | subset200 | negation_flip | direction=negated->present | 200 | 122 | 0.610 |
| findings | subset200 | negation_flip | inserted 'no' lands mid-phrase (e.g. 'left no pleural effusion') | 78 | 76 | 0.974 |
| findings | subset200 | negation_flip | 'present' finding sits in a sentence that already has a negation cue | 78 | 6 | 0.077 |
| findings | subset200 | negation_flip | negated->present leaves coordinated remainder ('X is present or Y') | 122 | 32 | 0.262 |
| findings | subset200 | laterality_flip | source=bilateral (paper says bilateral is skipped) | 200 | 7 | 0.035 |
| findings | subset200 | laterality_flip | reference mentions BOTH left and right (first-match flip may create contradiction) | 200 | 93 | 0.465 |
| findings | subset200 | laterality_flip | flipped token is non-anatomical candidate ('right heart', 'left in place', 'right IJ/PICC' device) | 200 | 49 | 0.245 |
| findings | subset200 | measurement_flip | unit swap only (cm<->mm); numeric value never edited | 200 | 200 | 1.000 |
| findings | subset200 | uncertainty_flip | direction=asserted->possible (insert 'possible') | 200 | 176 | 0.880 |
| findings | subset200 | uncertainty_flip | direction=hedged->definite | 200 | 24 | 0.120 |
| findings | subset200 | benign_format | prefix 'Report impression:' (single-sentence refs; also used for FINDINGS section) | 200 | 8 | 0.040 |
| findings | subset200 | benign_format | bullets break numbered list ('- 1. - ...') | 200 | 3 | 0.015 |
| findings | subset200 | benign_sentence_order | reference has discourse connective (However/Otherwise/This/These/Also ...) -> order-dependent | 200 | 23 | 0.115 |
| findings | subset200 | benign_sentence_order | reference has numbered list | 200 | 5 | 0.025 |
| findings | subset200 | finding_deletion | whole section replaced by 'No acute cardiopulmonary abnormality.' | 200 | 2 | 0.010 |
| findings | subset200 | false_finding_insertion | reference lacks terminal period before appended sentence | 200 | 6 | 0.030 |
| findings | subset200 | false_finding_insertion | inserted sentence carries laterality/severity/size (multi-factor, not minimal) | 200 | 200 | 1.000 |
| findings | subset200 | temporal_comparison_flip | detail=stable/unchanged->increased | 200 | 136 | 0.680 |
| findings | subset200 | temporal_comparison_flip | flipped word describes device/position ('tube|catheter|line|lead ... unchanged') | 200 | 44 | 0.220 |
| findings | subset200 | severity_flip | polarity flip (small/trace/mild/minimal <-> large/severe), not an adjacent grade | 200 | 170 | 0.850 |

## D. Section provenance

| scope | n | has_IMPRESSION_header | has_FINDINGS_header | has_both_headers | findings_text==impression_text | impression_text==full_text | reference_is_true_section(header present & sections differ) |
|---|---|---|---|---|---|---|---|
| all_prepared_reports | 172171 | 0.771 | 0.574 | 0.412 | 0.581 | 0.066 |  |
| impression:5000_seed0_clean | 4666 | 0.825 | 0.623 | 0.448 | 0.546 | 0.000 | 0.447 |
| findings:5000_seed0_clean | 4667 | 0.825 | 0.623 | 0.448 | 0.546 | 0.000 | 0.454 |
| impression:clean_metric_subset_200 | 1741 | 0.799 | 0.553 | 0.352 | 0.640 | 0.000 | 0.351 |
| findings:clean_metric_subset_200 | 1727 | 0.823 | 0.642 | 0.465 | 0.529 | 0.000 | 0.471 |

| split | n_impression_reports | n_findings_reports | reports_in_both | identical_reference_text_in_both | identical_reference_any_report |
|---|---|---|---|---|---|
| 5000_seed0_clean | 4666 | 4667 | 4666 | 2548 | 2548 |
| clean_metric_subset_200 | 1741 | 1727 | 749 | 468 | 468 |

## E. Human annotation structure

| annotator | n | match_rule | yes | no | uncertain | comment_rate |
|---|---|---|---|---|---|---|
| annotator_A | 280 | 0.914 | 0.261 | 0.732 | 0.007 | 0.011 |
| annotator_B | 280 | 0.850 | 0.254 | 0.661 | 0.086 | 0.993 |
| annotator_C | 280 | 0.829 | 0.321 | 0.679 | 0.000 | 1.000 |

| n_labels | n_items | match_rule_incl_uncertain | uncertain_rate |
|---|---|---|---|
| 1 | 300 | 0.860 | 0.040 |
| 3 | 180 | 0.983 | 0.006 |

| perturbation_type | annotator_A | annotator_B | annotator_C |
|---|---|---|---|
| anatomy_region_flip | 0.89 | 0.95 | 1.00 |
| benign_format | 0.91 | 0.78 | 0.83 |
| benign_paraphrase_rule | 0.79 | 0.95 | 0.80 |
| benign_sentence_order | 0.86 | 0.96 | 0.77 |
| false_finding_insertion | 0.91 | 0.90 | 0.85 |
| finding_deletion | 0.96 | 0.92 | 0.83 |
| laterality_flip | 0.92 | 0.96 | 0.82 |
| measurement_flip | 1.00 | 0.92 | 0.78 |
| negation_flip | 1.00 | 0.96 | 0.68 |
| severity_flip | 0.91 | 0.95 | 0.85 |
| temporal_comparison_flip | 0.96 | 0.92 | 0.86 |
| uncertainty_flip | 0.91 | 0.08 | 0.87 |

| perturbation_type | size | mean |
|---|---|---|
| anatomy_region_flip | 25 | 0.880 |
| benign_format | 25 | 0.840 |
| benign_paraphrase_rule | 25 | 0.840 |
| benign_sentence_order | 25 | 0.880 |
| false_finding_insertion | 25 | 0.920 |
| finding_deletion | 25 | 0.920 |
| laterality_flip | 25 | 0.880 |
| measurement_flip | 25 | 0.880 |
| negation_flip | 25 | 0.920 |
| severity_flip | 25 | 0.840 |
| temporal_comparison_flip | 25 | 0.920 |
| uncertainty_flip | 25 | 0.600 |

| comment | count |
|---|---|
| Fact or wording altered | 75 |
| Sentence order shuffled only | 26 |
| New sentence or finding added | 25 |
| sentence order changed only | 23 |
| Formatting or punctuation change only | 22 |
| Changed 'cm' to 'mm' | 21 |
| Sentence or finding removed | 19 |
| bullet-point formatting only | 18 |
| Minor filler word changes only | 17 |
| Changed 'unchanged' to 'increased' | 12 |
| Negation introduced ('no') | 10 |
| Changed 'small' to 'large' | 9 |
| Changed 'right' to 'left' | 8 |
| Changed 'left' to 'right' | 7 |
| Changed 'bases' to 'apices' | 7 |
| Changed 'mild' to 'severe' | 6 |
| candidate adds 'New focal consolidation is present in the right lower lobe' | 5 |
| candidate adds 'A new 3 cm nodular opacity is seen in the left upper lobe' | 5 |
| Changed 'lower' to 'upper' | 5 |
| right pleural effusion → right possible pleural effusion | 4 |
| candidate adds 'There is a moderate left pleural effusion' | 4 |
| 4 cm → 4 mm above carina | 4 |
| candidate adds 'There is moderate pulmonary edema' | 4 |
| Changed 'upper' to 'lower' | 4 |
| candidate adds 'Report impression:' label only | 3 |
| No focal consolidation → Focal consolidation is present | 3 |
| Changed 'large' to 'small' | 3 |
| candidate adds 'There is a new right pneumothorax' | 2 |
| small → large right pleural effusion | 2 |
| 'There is no pneumothorax' → 'No pneumothorax' | 2 |
