ClinSemBench: Stress-Testing Radiology Report Metrics with Meaning-Preserving and Meaning-Changing Minimal Pairs
Download PDF
Junah Jung, YeonGyu Han, Chang Min Park, Dongheon Lee 
25 May 2026 (modified: 29 Sept 2026)
ACL ARR 2026 May Submission
May, Senior Area Chairs, Area Chairs, Reviewers, Authors
Revisions
CC BY 4.0
Keywords: radiology report evaluation, clinical NLP, radiology report generation, evaluation metrics, minimal-pair benchmark, metric meta-evaluation, meaning preservation, semantic evaluation, sensitivity analysis, MIMIC-CXR
Abstract:
Radiology report generation is often evaluated by comparing a candidate report with a reference, but high reference-based similarity does not guarantee sensitivity to semantic changes in the stated findings. We introduce ClinSemBench, a controlled minimal-pair benchmark for stress-testing whether radiology report metrics distinguish meaning-preserving edits from meaning-changing edits in MIMIC-CXR report sections. Candidates preserve meaning through formatting, sentence-order, and rule-based paraphrase edits, or change meaning through negation, laterality, anatomy, severity wording, uncertainty, temporal comparison, finding omission, false finding insertion, and measurement edits. We validate 480 blinded pairs with 840 human judgments; aggregated labels agree with rule-derived labels in 93.1% of evaluable cases. Across representative metric families, GREEN performs best, reaching AUROC 0.903/0.896 on impression/findings rule labels and 0.814 on human labels. In contrast, BERTScore is directionally reversed, falling below random on rule-derived labels (0.221/0.165) and human-derived labels (0.274) because it often penalizes benign rewrites more than meaning-changing edits. Edit-type analysis shows that clinical-aware metrics improve over general similarity but retain blind spots, especially for laterality and measurement. We recommend sensitivity cards that report invariance to benign rewrites and sensitivity to specific meaning-changing edits.

Paper Type: Long
Research Area: Resources and Evaluation
Research Area Keywords: benchmarking, evaluation methodologies, evaluation, metrics, NLP datasets, statistical testing for evaluation
Contribution Types: Model analysis & interpretability, NLP engineering experiment, Data analysis
Languages Studied: English
Reassignment Request Area Chair: This is not a resubmission
Reassignment Request Reviewers: This is not a resubmission
A1 Limitations Section: This paper has a limitations section.
A2 Potential Risks: Yes
A2 Elaboration: Limitations; Ethical Considerations
B Use Or Create Scientific Artifacts: Yes
B1 Cite Creators Of Artifacts: Yes
B1 Elaboration: Sections 2, 3.2, and 5
B2 Discuss The License For Artifacts: Yes
B2 Elaboration: Ethical Considerations
B3 Artifact Use Consistent With Intended Use: Yes
B3 Elaboration: Ethical Considerations
B4 Data Contains Personally Identifying Info Or Offensive Content: Yes
B4 Elaboration: Ethical Considerations
B5 Documentation Of Artifacts: Yes
B5 Elaboration: Sections 3.2--3.4; Appendix A
B6 Statistics For Data: Yes
B6 Elaboration: Sections 3.2, 3.5, and 6; Appendices A and E
C Computational Experiments: Yes
C1 Model Size And Budget: Yes
C1 Elaboration: Section 5; Appendix F
C2 Experimental Setup And Hyperparameters: Yes
C2 Elaboration: Section 5; Appendix F
C3 Descriptive Statistics: Yes
C3 Elaboration: Sections 3.2 and 6.1--6.2; Appendices A and E
C4 Parameters For Packages: Yes
C4 Elaboration: Section 5; Appendix F
D Human Subjects Including Annotators: Yes
D1 Instructions Given To Participants: Yes
D1 Elaboration: Section 3.5; Appendix E
D2 Recruitment And Payment: Yes
D2 Elaboration: Appendix E
D3 Data Consent: Yes
D3 Elaboration: Appendix E
D4 Ethics Review Board Approval: No
D4 Elaboration: No formal ethics review board approval or exemption determination was sought. The study uses de-identified MIMIC-CXR reports under credentialed access and does not involve intervention, collection of private patient information, or patient contact. The human annotation task involved graduate-student annotators judging blinded text pairs for meaning preservation; no sensitive personal data about annotators was collected. We discuss this in Section 3.5, Appendix E, and Ethical Considerations.
E Ai Assistants In Research Or Writing: Yes
E1 Information About Use Of Ai Assistants: Yes
E1 Elaboration: AI assistants were used for editorial feedback, structural suggestions, and copy-editing support. All claims, references, experiments, numerical results, and final text were checked and finalized by the authors.
Author Submission Checklist: yes
EMNLP 2026 AI Reviewing Experiment: no
TLDR: ClinSemBench is a controlled minimal-pair benchmark showing that radiology report metrics need sensitivity cards: GREEN is strongest, while BERTScore is directionally reversed on meaning-change detection.
Preprint: no
Preprint Status: There is no non-anonymous preprint and we do not intend to release one. (this option is binding)
Preferred Venue: EMNLP
Visa Needs: no
Consent To Share Data: no
Consent To Share Submission Details: On behalf of all authors, we agree to the terms above to share our submission details.
Association For Computational Linguistics - Blind Submission License Agreement: On behalf of all authors, I agree
Submission Number: 7910
Discussion
Filter by reply type...
Filter by author...
Search keywords...

Sort: Newest First
7 / 7 replies shown
Add:
Meta Review of Submission7910 by Area Chair XnAy
Meta Reviewby Area Chair XnAy24 Jul 2026, 17:30 (modified: 31 Jul 2026, 17:53)Senior Area Chairs, Area Chairs, Authors, Reviewers Submitted, Program Chairs, Area Chair XnAyRevisions
Metareview:
This paper proposes a benchmark in the context of clinical reports by using semantic perturbation. It then compares existing automated metrics with human annotation, and discuss how well automated metrics can capture semantic perturbation. Overall, the novelty and impact of this work is pretty limited, and the finding that BERTScore is sensitive to surface changes is pretty well established already.

Summary Of Reasons To Publish:
It adds another resource in the context of evaluating report generation.
Summary Of Suggested Revisions:
Reviewers suggested more fine-grained analyses and it would be useful to incorporate those in the paper.
It would be useful to add more modern metrics as suggested by reviewer 38pP and also more modern models.
Overall Assessment: 2 = Resubmit next cycle: I think this paper needs substantial revisions that can be completed by the next ARR cycle.
Reported Issues: No
Publication Ethics Policy Compliance: I did not use any generative AI tools for this review
Add:
Official Review of Submission7910 by Reviewer jzA1
Official Reviewby Reviewer jzA102 Jul 2026, 17:28 (modified: 12 Jul 2026, 17:33)Program Chairs, Senior Area Chairs, Area Chairs, Reviewers Submitted, Authors, Reviewer jzA1Revisions
Paper Summary:
The authors have developed ClinSemBench, a paired report analysis benchmark for determining whether radiology report quality metrics distinguish semantic-preserving edits from meaning-changing edits in MIMIC-CXR reports.

Summary Of Strengths:
The dataset and the metric are useful additions to the available measures for evaluating the clinical quality/accuracy of radiology reports.

The authors propose valid methods to determine susceptibility of other metrics to misclassification errors.

It is useful to learn which semantic/clinical metrics are susceptible to unimportant changes in the report.

Summary Of Weaknesses:
Reports vary widely in length, style, nomenclature across radiology practices. This study is confined to MIMIC reports, which are derived from a single institution. There are many other publicly available radiology report corpora that could have been used to show generalizability.

The humans raters are asked to determine whether meaning is preserved. As mentioned under Limitations. not all changes in semantics have the same clinical impact. For example a change in measurement, severity, or uncertainty isn't typically as clinically important as a change in side, which could result in wrong-side surgery, or a negation error that could result in a misdiagnosis. Clinical significance is a much more important aspect of report quality.

This method correlates best with GREEN. An interesting question regarding construct validity: Would GREEN or the developed metric correlate most closely with the quality ratings of clinicians?

Grad student annotators don’t have clinical experience. Perhaps this is appropriate if the analysis is focused purely on semantic rather than clinical errors.

There is discussion of a trigger for the rules. More detail is needed on how other rules are applied. Presumably the sidedness rule is only applied when a side is mentioned. Uncertainty may be more difficult. For example, a wide variety of uncertainty words might be used. How were these captured in the trigger rule?

Rationale is needed for excluding UNCERTAIN ratings from interrater agreement analysis. UNCERTAIN could be grouped with YES or NO ratings (or analyzed both ways) to give a full sense of agreement. Or a multi-valued kappa could be calculated.

The low accuracy for uncertainty edits make sense. There is great variability in how even humans interpret uncertainty words in radiology reports. https://pubmed.ncbi.nlm.nih.gov/12809424/

The data access statement needs clarification. It appears the authors plan to release aggregate outputs rather than the ratings of each MIMIC report by each rating method and the human raters.

Comments Suggestions And Typos:
Line 251-252: best to italicize or capitalize impression and findings to indicate you are referring to section headings in the report.

Confidence: 4 = Quite sure. I tried to check the important points carefully. It's unlikely, though conceivable, that I missed something that should affect my ratings.
Soundness: 3 = Acceptable: This study provides sufficient support for its main claims. Some minor points may need extra support or details.
Excitement: 2 = Potentially Interesting: this paper does not resonate with me, but it might with others in the *ACL community.
Overall Assessment: 3 = Findings: I think this paper could be accepted to the Findings of the ACL.
Ethical Concerns:
There are no concerns with this submission

Needs Ethics Review: No
Reproducibility: 5 = They could easily reproduce the results.
Datasets: 2 = Documentary: The new datasets will be useful to study or replicate the reported research, although for other purposes they may have limited interest or limited usability. (Still a positive rating)
Software: 1 = No usable software released.
Knowledge Of Or Educated Guess At Author Identity: No
Knowledge Of Paper: N/A, I do not know anything about the paper from outside sources
Knowledge Of Paper Source: N/A, I do not know anything about the paper from outside sources
Impact Of Knowledge Of Paper: N/A, I do not know anything about the paper from outside sources
Reviewer Certification: I certify that the review I entered accurately reflects my assessment of the work. If you used any type of automated tool to help you craft your review, I hereby certify that its use was restricted to improving grammar and style, and the substance of the review is either my own work or the work of an acknowledged secondary reviewer.
Publication Ethics Policy Compliance: I did not use any generative AI tools for this review
Add:
Official Comment by Authors
Official Commentby Authors (YeonGyu Han, Junah Jung, Dongheon Lee, Chang Min Park)13 Jul 2026, 20:24Program Chairs, Senior Area Chairs, Area Chairs, Reviewers Submitted, Authors, Reviewer jzA1
Comment:
Thank you for the clinically grounded questions. We clarify the construct, add UNCERTAIN sensitivity analyses, expand rule details, clarify release, and add a cross-corpus transfer check.

1. Construct: semantic ≠ clinical significance

ClinSemBench is a meta-evaluation benchmark, not a new report-quality metric; there is no single ClinSemBench score. Because the benchmark provides diagnostic tests rather than a scalar, a GREEN-versus-ClinSemBench correlation is not defined; clinician quality ratings would instead serve as an external criterion against which each evaluated metric could be tested independently.

The benchmark validates whether a metric is invariant to meaning-preserving edits and sensitive to text-level meaning changes. This is a necessary but not sufficient property for clinically useful evaluation. A laterality flip, a negation error, and an uncertainty wording shift can have different clinical implications; ClinSemBench does not claim to validate image-grounded correctness, treatment impact, patient risk, or radiologist-adjudicated severity. We used graduate annotators because the task asks only whether two texts preserve the same stated meaning. Clinical-significance validation would require a separate radiologist-adjudicated study. We will sharpen this distinction throughout.

2. UNCERTAIN and agreement

We excluded aggregated UNCERTAIN items from the submitted AUROC only because that endpoint requires a binary preserved/changed target. We agree that UNCERTAIN should remain visible.

Of the 480 validation items, 13 received aggregated UNCERTAIN labels. Eleven of these 13 are uncertainty_flip perturbations, confirming that ambiguity is concentrated in the intended stress case. We completed the ten previously missing metric outputs, so both binary sensitivity analyses now cover all 480 validation items. Using the raw 
 judgment matrix and the full YES/NO/UNCERTAIN label space, three-category Fleiss' 
 = 0.430.

Treatment	n	changed / preserved	GREEN human AUROC
Exclude UNCERTAIN	467	337 / 130	0.814
UNCERTAIN → changed	480	350 / 130	0.802
UNCERTAIN → preserved	480	337 / 143	0.815
Metric rankings are unchanged under all three treatments. The maximum absolute AUROC change across all metrics is 0.023; for GREEN it is 0.012. We will report all three analyses.

3. Rule details

Rules are applied only when rule-specific triggers are present; otherwise the perturbation is skipped. Key rules:

Laterality: trigger = unilateral left/right; replacement = left↔right; skipped for bilateral/ambiguous.
Negation: trigger = No ..., There is no ..., without ...; replacement = absence↔presence.
Uncertainty: trigger = possible, probable, suspected, may represent, could represent, cannot exclude; replacement = hedged↔definite.
Severity: trigger = trace, small, mild, moderate, severe, large; replacement = grade shift.
Temporal comparison: trigger = stable, unchanged, improved, worsened, new, resolved; replacement = direction substitution.
Measurement: trigger = numeric with unit (cm, mm); replacement = value/unit change.
Finding deletion/insertion: deletion removes one finding-bearing sentence; insertion adds a templated finding absent from the reference. We will add a full table with triggers, replacements, exclusions, and coverage.
4. Data release

Subject to the MIMIC-CXR data-use terms, we will release the perturbation-generation and evaluation scripts, per-example rule IDs, edit parameters, anonymized individual human judgments, UNCERTAIN indicators, raw and oriented metric outputs, identity scores, and penalties. Fields that could expose source-report content will be provided through reconstruction scripts for credentialed users.

5. Cross-corpus transfer check and remaining

As a targeted cross-corpus rule-label transfer check, the unchanged pipeline yields the same broad pattern on IU X-Ray/OpenI: on their respective balanced subsets, GREEN reaches 0.925 on subset10, while RadGraph and BERTScore reach 0.715 and 0.270 on subset50. Because the labels are rule-derived and sample sizes differ, we interpret this as a transfer check, not a direct metric ranking or full cross-institution semantic validation.

Khorasani et al. (2003) provides clinical context for the elevated disagreement we observe on uncertainty phrasing. We will also make the requested Impression/Findings formatting correction.

Add:
Official Review of Submission7910 by Reviewer 84Wq
Official Reviewby Reviewer 84Wq01 Jul 2026, 20:49 (modified: 12 Jul 2026, 17:33)Program Chairs, Senior Area Chairs, Area Chairs, Reviewers Submitted, Authors, Reviewer 84WqRevisions
Paper Summary:
The goal of this paper is to study the behaviors of automated radiology report generation evaluation metrics. Specifically, when a reference report is minimally edited, do automated metrics penalize meaning-changing edits more than meaning-preserving ones? The authors introduce ClimSemBench, a benchmark designed to answer this question, as well as provide analysis of existing metrics.

Summary Of Strengths:
This work addresses an important challenge: the meta-evaluation of metrics designed to assess generated radiology reports
The provided benchmark covers a diverse and comprehensive set of perturbations
The authors provide insights into blindspots that existing metrics may have, revealing insights into when each metric should or should not be used
This work addresses an important gap in the current literature and is likely to be useful for the medical NLP community.
Summary Of Weaknesses:
Use of data from just one dataset: ClinSemBench is composed of samples obtained from just one chest X-ray dataset: MIMIC-CXR. This might limit generalizability of results, especially as some of the evaluated metrics (e.g. RadGraph) are developed using MIMIC-CXR and are likely to demonstrate better performance on this dataset than in the wild. Incorporating samples from multiple datasets would help improve the utility of the proposed benchmark.
Need for finer-grained analysis: The paper provides insufficient performance analysis of existing metrics on the benchmark. Specifically, Sections 6.2 and 6.3 provide a high-level summary of overall performance of each metric on the benchmark; however, comprehensive perturbation-level breakdowns are not provided. The paper could benefit from additional analysis into the blindspots / failure modes of each metric.
Ambiguity in dataset composition: There are multiple versions of the benchmark utilized in the paper: subset500 (L357), subset200 (L357), full clean 5k pair sets (L355), 2400 non-identity candidates (L360), and 36k impression pairs + 40k findings pairs (L251). It is not clear to me what all of these variations represent, and it would be useful to add further clarification on the composition of the benchmark.
Comments Suggestions And Typos:
Please see weaknesses above

Confidence: 4 = Quite sure. I tried to check the important points carefully. It's unlikely, though conceivable, that I missed something that should affect my ratings.
Soundness: 3 = Acceptable: This study provides sufficient support for its main claims. Some minor points may need extra support or details.
Excitement: 3.5
Overall Assessment: 3 = Findings: I think this paper could be accepted to the Findings of the ACL.
Limitations And Societal Impact:
Yes

Ethical Concerns:
There are no concerns with this submission

Needs Ethics Review: No
Reproducibility: 3 = They could reproduce the results with some difficulty. The settings of parameters are underspecified or subjectively determined, and/or the training/evaluation data are not widely available.
Datasets: 4 = Useful: I would recommend the new datasets to other researchers or developers for their ongoing work.
Software: 4 = Useful: I would recommend the new software to other researchers or developers for their ongoing work.
Knowledge Of Or Educated Guess At Author Identity: No
Knowledge Of Paper: N/A, I do not know anything about the paper from outside sources
Knowledge Of Paper Source: N/A, I do not know anything about the paper from outside sources
Impact Of Knowledge Of Paper: N/A, I do not know anything about the paper from outside sources
Reviewer Certification: I certify that the review I entered accurately reflects my assessment of the work. If you used any type of automated tool to help you craft your review, I hereby certify that its use was restricted to improving grammar and style, and the substance of the review is either my own work or the work of an acknowledged secondary reviewer.
Publication Ethics Policy Compliance: I did not use any generative AI tools for this review
Add:
Official Comment by Authors
Official Commentby Authors (YeonGyu Han, Junah Jung, Dongheon Lee, Chang Min Park)13 Jul 2026, 20:24Program Chairs, Senior Area Chairs, Area Chairs, Reviewers Submitted, Authors, Reviewer 84Wq
Comment:
Thank you for the constructive feedback. We agree that the submitted analysis needed a more complete perturbation-level breakdown and clearer benchmark composition. We add both, and we also add a cross-corpus rule-label transfer check on IU X-Ray/OpenI.

1. Complete perturbation-level analysis

We computed type-specific AUROC on subset200 for all six main metrics across both sections. For each meaning-changing type, AUROC compares that type's penalties against the pooled three meaning-preserving types; each cell compares 200 changed candidates against the pooled 600 meaning-preserving candidates within the same section. Results are Impression / Findings:

Type	GREEN	RaTE	RadGraph	F1CheX	Temporal	BERT
negation	.934/.945	.783/.799	.663/.642	.640/.696	.500/.500	.191/.150
laterality	.974/.967	.754/.781	.577/.539	.487/.485	.500/.500	.030/.002
finding del	.985/.976	.914/.918	.881/.888	.820/.852	.710/.703	.868/.741
false ins	.986/.979	.853/.883	.807/.780	.728/.750	.810/.795	.640/.421
measurement	.792/.821	.619/.660	.520/.538	.487/.485	.500/.500	.005/.000
severity	.981/.954	.770/.806	.611/.581	.487/.487	.500/.500	.023/.003
uncertainty	.585/.535	.730/.782	.561/.619	.497/.490	.500/.500	.082/.044
anatomy	.951/.939	.787/.833	.631/.585	.490/.490	.500/.500	.066/.054
temporal	.944/.946	.701/.778	.599/.575	.507/.492	.995/.988	.083/.069
This complete profile shows why aggregate AUROC alone is insufficient. Temporal is nearly perfect on temporal-comparison edits (0.995/0.988) but at chance on most other types. F1CheXbert is strong on finding deletion and false insertion but near chance on laterality, measurement, severity, and anatomy. GREEN is strongest overall, but uncertainty is a difficult residual case (0.585/0.535), where RaTEScore is stronger (0.730/0.782). BERTScore is sharply reversed on most compact semantic flips but remains above chance on finding deletion; this heterogeneous behavior is hidden by its aggregate below-random AUROC.

The submitted Figure 3 visualized only five of the nine meaning-changing types; we will replace it with the complete profile.

2. Benchmark composition

One row denotes one reference–candidate pair. The 2,400 count excludes identity baselines, whereas subset200 includes identity rows required to compute per-reference penalties. The hierarchy is:

5,000 source reports/section → all valid perturbation rules → filtering → 36,488 Impression / 40,941 Findings clean pairs.
subset500: up to 500 candidates from each of the 12 non-identity types, plus one deduplicated identity row per involved reference; 8,934 Impression and 9,183 Findings rows; used for BERTScore, F1CheXbert, RaTEScore, and Temporal.
subset200: analogously balanced with 2,400 non-identity candidates/section; the subset200 tables contain 4,141 Impression and 4,127 Findings rows including identity baselines for 
.
480-pair validation set: separately sampled and balanced; used for blinded human annotation and human-label metric evaluation. All six rule-label metrics in Table 3 use the same 2,400 non-identity candidates within each section; the human-label column uses the separately sampled validation set.
3. Cross-corpus rule-label transfer check

We applied the unchanged perturbation and metric pipeline to IU X-Ray/OpenI. From 3,955 reports, we extracted 7,241 sections and generated 18,159 external minimal pairs. Because the external labels are rule-derived without independent human adjudication, we treat this as a targeted transfer check rather than full semantic validation. GREEN is evaluated on subset10 due to runtime; other metrics on subset50.

Metric	OpenI/IU AUROC
GREEN	0.925*
RaTEScore	0.778
RadGraph	0.715
Temporal	0.577
F1CheXbert	0.552
BERTScore	0.270
*GREEN on subset10; others on subset50. Because sample sizes differ, these are not used for direct metric ranking.	
The qualitative pattern recurs outside MIMIC-CXR: clinical-aware metrics remain stronger, and BERTScore remains below random.

Add:
Official Review of Submission7910 by Reviewer 38pP
Official Reviewby Reviewer 38pP30 Jun 2026, 09:51 (modified: 17 Jul 2026, 09:01)Program Chairs, Senior Area Chairs, Area Chairs, Reviewers Submitted, Authors, Reviewer 38pPRevisions
Paper Summary:
This paper introduces ClinSemBench, a reference-anchored minimal-pair benchmark for stress-testing radiology report evaluation metrics. It constructs meaning-preserving and meaning-changing perturbations from MIMIC-CXR report sections, validates the labels with human judgments, and evaluates whether different metrics penalize clinically meaningful semantic changes more than benign rewrites.

Summary Of Strengths:
Controlled minimal-pair construction. The perturbation design isolates specific semantic factors such as negation, laterality, omissions, false findings, and measurement changes, making metric failures easier to interpret.

Human validation supports the benchmark labels. The reported human-rule agreement is high, suggesting that the rule-based perturbations largely match intuitive meaning-preservation judgments.

Summary Of Weaknesses:
Limited novelty relative to prior metric re-evaluation work. The paper overlaps with ReEvalMed and should clarify what new failure modes or conclusions ClinSemBench adds beyond existing medical metric stress tests.

The benchmark may be too simple for LLM-based evaluators. Most edits are local and explicit, such as negation, laterality, deletion, insertion, and measurement changes. Strong LLMs can already detect many of these, so the benchmark may not reveal deeper LLM-as-a-metric failures.

The metric suite is incomplete. BERTScore’s failure is unsurprising, and evaluating only GREEN as the main LLM-based metric is insufficient. The paper should include stronger baselines such as CRIMSON, FineRadScore, broader RadEval metrics, CheXbert variants, and comparisons across different LLM backbones or prompts.

Clinical interpretation is limited. The benchmark is reference-anchored and text-only, with mostly rule-derived labels and non-radiologist annotators. It should be framed as a text-level semantic sensitivity test, not evidence of real clinical evaluation reliability.

Comments Suggestions And Typos:
See in Weaknesses.

[Post-rebuttal Update:] My major concern remains unaddressed: the evaluation does not include a sufficiently broad and up-to-date set of LLMs. Given that modern LLMs can provide both strong performance and interpretable judgments, relying primarily on Meta-Llama-3-8B, released in 2024, limits the practical relevance of the conclusions. I believe the authors should conduct a more comprehensive benchmark evaluation covering current proprietary models, such as Gemini 3.1 Pro, Claude Opus, and GPT-5.5, as well as open-weight or domain-specific models, such as MedGemma and Qwen3.7. Such results would be important for assessing real-world clinical and engineering applicability and would provide a useful resource for the community.

Confidence: 4 = Quite sure. I tried to check the important points carefully. It's unlikely, though conceivable, that I missed something that should affect my ratings.
Soundness: 2.5
Excitement: 2 = Potentially Interesting: this paper does not resonate with me, but it might with others in the *ACL community.
Overall Assessment: 2 = Resubmit next cycle: I think this paper needs substantial revisions that can be completed by the next ARR cycle.
Ethical Concerns:
There are no concerns with this submission

Needs Ethics Review: No
Reproducibility: 5 = They could easily reproduce the results.
Datasets: 2 = Documentary: The new datasets will be useful to study or replicate the reported research, although for other purposes they may have limited interest or limited usability. (Still a positive rating)
Software: 1 = No usable software released.
Knowledge Of Or Educated Guess At Author Identity: No
Knowledge Of Paper: N/A, I do not know anything about the paper from outside sources
Knowledge Of Paper Source: N/A, I do not know anything about the paper from outside sources
Impact Of Knowledge Of Paper: N/A, I do not know anything about the paper from outside sources
Reviewer Certification: I certify that the review I entered accurately reflects my assessment of the work. If you used any type of automated tool to help you craft your review, I hereby certify that its use was restricted to improving grammar and style, and the substance of the review is either my own work or the work of an acknowledged secondary reviewer.
Publication Ethics Policy Compliance: I used a privacy-preserving tool exclusively for the use case(s) approved by PEC policy, such as language edits
Add:
Official Comment by Authors
Official Commentby Authors (YeonGyu Han, Junah Jung, Dongheon Lee, Chang Min Park)13 Jul 2026, 20:24Program Chairs, Senior Area Chairs, Area Chairs, Reviewers Submitted, Authors, Reviewer 38pP
Comment:
Thank you for the careful and critical feedback. We agree that the submitted version did not position ClinSemBench relative to ReEvalMed clearly enough, and that the scope of the benchmark should be stated more precisely. We have added new evidence and will revise the paper accordingly.

1. Relation to ReEvalMed

ReEvalMed and ClinSemBench are complementary, but they target different constructs. ReEvalMed evaluates clinically weighted discrimination, robustness, and monotonicity using LLM-generated, expert-validated rewrites. ClinSemBench evaluates a controlled text-semantic behavioral property: whether a reference-based metric is invariant to meaning-preserving edits and sensitive to meaning-changing edits under same-reference minimal pairs.

ReEvalMed also provides aspect-level analysis, so our novelty is not simply "per-type diagnosis." The contribution of ClinSemBench is the combination of: (i) deterministic, single-factor generation at scale across both Impression and Findings, (ii) per-reference identity-normalized penalties with benign-over-changed inversion and edit-type blindness diagnostics, and (iii) a separate 480-pair human text-semantic validation set. These enable controlled, factor-specific attribution of metric failures.

For example, F1CheXbert is near chance on laterality (0.487/0.485) and measurement (0.487/0.485), but substantially stronger on finding deletion (0.820/0.852). BERTScore is sharply reversed on compact semantic flips such as laterality (0.030/0.002) and measurement (0.005/0.000), although it remains above chance on finding deletion (0.868/0.741); this heterogeneous profile is obscured by aggregate AUROC alone. We will add a direct comparison table positioning ReEvalMed and ClinSemBench as complementary.

2. LLM-rubric ablation

Following the reviewer's suggestion, we additionally evaluate an open-weight LLM-rubric judge using Meta-Llama-3-8B-Instruct. The evaluator is prompted to classify whether the candidate preserves or changes the stated meaning of the reference, and we convert its output to the same agreement-oriented scoring direction used for the other metrics. The rule-label ablation uses a balanced subset50 per section. The primary human-label AUROC uses the same 467 non-UNCERTAIN validation pairs as the original metrics; we additionally report both binary mappings of all 13 UNCERTAIN items.

Evaluator	Rule AUROC I / F	Human AUROC
GREEN	0.903 / 0.896*	0.814
RaTEScore	0.768 / 0.804*	0.725
Llama-3-8B rubric	0.760 / 0.736	0.710
RadGraph	0.650 / 0.639*	0.587
F1CheXbert	0.572 / 0.581*	0.570
BERTScore	0.221 / 0.165*	0.274
*Rule AUROC from subset200; Llama rule AUROC from subset50, so rule-label values are not used for direct cross-evaluator ranking. Human AUROC uses the same 467 non-UNCERTAIN pairs for all.		
The Llama-rubric evaluator improves substantially over general contextual similarity but does not saturate ClinSemBench. Its perturbation profile is uneven: strong on negation (0.850/0.860), laterality (0.880/0.790), false insertion (0.890/0.960), and temporal comparison (0.880/0.890), but much weaker on measurement (0.550/0.530), uncertainty (0.600/0.500), and anatomy (0.640/0.570). On human labels, its AUROC is 0.710; treating UNCERTAIN as changed or preserved yields 0.705 and 0.703. Even an instruction-tuned LLM judge benefits from sensitivity-card reporting rather than only aggregate scores.

3. Benchmark non-saturation

The atomic edits are deliberate behavioral unit tests. Passing them is necessary but not sufficient for robustness to natural or clinically weighted errors. The benchmark is not saturated even by GREEN: its uncertainty-flip AUROC is 0.585/0.535, below RaTEScore's 0.730/0.782. BERTScore is reversed on rule labels (0.221/0.165) and human labels (0.274). F1CheXbert is stable under benign rewrites but near chance on laterality and measurement.

4. Clinical interpretation

We agree that ClinSemBench should not be framed as a clinical-significance benchmark. It does not adjudicate image-grounded correctness, patient safety, treatment impact, or radiologist-rated severity. CRIMSON, FineRadScore, and related severity-aware evaluators are complementary because they target clinical significance or severity-aware correction. ClinSemBench instead provides a controlled text-semantic behavioral test for reference-based metrics. We will revise the paper to make this scope explicit.

As a cross-corpus rule-label transfer check, the qualitative metric pattern also recurs on IU X-Ray/OpenI; we provide the detailed results in our response to Reviewer 84Wq.

Add:
