# Assurance Card 01 — Paired Prompt Evaluation

Date: 19 October 2026
Assessment type: Author self-assessment
Status: LOCAL EVIDENCE ASSESSMENT — NOT EXTERNAL CERTIFICATION

## Scope

One Qwen3-0.6B model evaluated on 200 paired ARC-Easy questions.
Two prompt variants, A and B, with 400 recorded model responses.

## Claims and evidence

| Claim | Evidence | Assessment |
|---|---|---|
| A scored 80.5%; B scored 78.5% | 200 paired derived outcomes and statistical script | SUPPORTED BY PUBLIC DERIVED DATA |
| Variant B improves accuracy | Difference B-A = -2.0 pp; McNemar p = 0.38769531; bootstrap 95% CI [-5.5, +1.5] pp | NOT ESTABLISHED |
| A and B have equivalent performance | No prespecified equivalence margin or equivalence test | NOT ESTABLISHED |
| Public statistics can be reproduced | Local replay of the published calculation script: PASS | SUPPORTED FOR DERIVED STATISTICS ONLY |
| Original execution was independently verified | No completed external assessment documented | NOT VERIFIED |

## Evidence links

- [Study report](../reports/report_01/Report01_Qwen3_ARC_Easy_Evaluation_EN.pdf)
- [Study methodology](../reports/report_01/README.md)
- [Paired outcomes](../reports/report_01/paired_outcomes_200.csv)
- [Recalculation script](../reports/report_01/recompute_paired_statistics.py)
- [Reviewer checklist](../reports/report_01/REVIEWER_CHECKLIST.md)

## Limitations

The public dataset contains binary correctness outcomes, not original
questions, prompts or raw model responses.

Public recalculation does not establish original execution provenance,
sampling fidelity, or the correctness of the original response scoring.

The experiment covers one model, one benchmark and one fixed sample.
Its results do not establish performance in other applications.

## Decision

Do not claim that variant B improves accuracy.
Do not claim equivalence between A and B.
Do not use this study alone to authorize production deployment.

The evidence supports a limited statistical conclusion, not a
general operational approval.

## Open evidence requirement

An external reviewer may inspect the published calculations and
request additional artifacts for deeper verification.

Until a review is completed, no external validation is claimed.