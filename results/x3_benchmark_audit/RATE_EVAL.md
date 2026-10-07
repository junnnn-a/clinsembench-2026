# RaTE-Eval — surface-only probe (public suite)

## Task 3 (synthetic triplets)

| subset | n_triplets | surface_only_LR_auroc | auc_jaccard_drop | auc_edit_tokens | paired_acc_jaccard | paired_acc_token_f1 | paired_acc_edit_distance | mean_edit_frac_rewrite | mean_edit_frac_opposite |
|---|---|---|---|---|---|---|---|---|---|
| all aligned | 847 | 0.864 | 0.188 | 0.214 | 0.159 | 0.151 | 0.123 | 1.137 | 0.563 |
| confident alignment | 739 | 0.887 | 0.166 | 0.206 | 0.147 | 0.139 | 0.108 | 1.065 | 0.525 |
| rewrite and opposite pick the same original | 714 | 0.874 | 0.180 | 0.214 | 0.163 | 0.154 | 0.119 | 1.075 | 0.539 |

alignment: 739/847 confident; examples:

- ORIG: The ventricles and extra-axial CSF spaces are mildly prominent, which may relate to mild diffuse parenchymal volume loss.
  - REWRITE: The ventricles and surrounding CSF spaces are slightly enlarged, possibly due to mild, widespread reduction in brain tissue volume.
  - OPPOSITE: The ventricles and extra-axial CSF spaces are mildly decreased, which may indicate no significant diffuse parenchymal volume loss.
- ORIG: There is trace fluid at the attachment of right hamstring on the ischial tuberosity, unchanged.
  - REWRITE: At the attachment of the right hamstring, a minimal amount of fluid is present on the ischial tuberosity, with no change observed.
  - OPPOSITE: There is no trace of fluid at the attachment of the left hamstring on the ischial tuberosity, which has changed.
- ORIG: There is some minimal spurring at the superolateral aspects of both acetabula.
  - REWRITE: There is slight outgrowth present at the upper lateral portions of both acetabula.
  - OPPOSITE: There is no observable spurring at the superolateral aspects of either acetabulum.
- ORIG: The patient is status post left thyroidectomy.
  - REWRITE: The patient has a history of undergoing a left thyroidectomy.
  - OPPOSITE: The patient has not undergone left thyroidectomy.

## Tasks 1-2 (radiologist ratings): Kendall tau of surface statistics with the human rating (sign fixed so that positive = agrees)

| task | n_test | surface_only_ridge_tau | tau:jaccard_drop | tau:tokenf1_drop | tau:seq_ratio_drop | tau:char_ratio_drop | tau:edit_frac | tau:abs_len_diff |
|---|---|---|---|---|---|---|---|---|
| Task 1 (sentence, normalised error count) | 441 | 0.316 | 0.242 | 0.237 | 0.145 | 0.188 | 0.126 | 0.005 |
| Task 2 (paragraph, 0-5 score) | 370 | 0.448 | 0.453 | 0.409 | 0.326 | 0.357 | 0.224 | -0.067 |
