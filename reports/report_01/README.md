# Study 01 — Qwen3-0.6B paired prompt evaluation

**Date:** 19 October 2026
**State:** Study closed; local artifact checks completed; outside review requested but not yet received.
**Question:** Does asking the model to compare all choices before selecting its answer improve multiple-choice accuracy?

## Design and results

200 deterministic sampled ARC-Easy **test** questions; each evaluated once with A and once with B (400 model calls), alternating A/B and B/A order. Fixed model, generation parameters, question/option formatting, schema-constrained JSON label output, and strict exact-match scoring were used. Details and limitations are in the [five-page report](Report01_Qwen3_ARC_Easy_Evaluation_EN.pdf).

| | A: basic instruction | B: careful-comparison instruction |
|---|---:|---:|
| Correct answers | 161 / 200 | 157 / 200 |
| Accuracy | 80.5% | 78.5% |

Paired table: both correct 153, A only 8, B only 4, both wrong 35. Effect B − A: **−2.0 pp**; exact two-sided McNemar **p = 0.38769531**; paired bootstrap 95% CI **[−5.5, +1.5] pp**. The study did not demonstrate a benefit from B. Neither equivalence nor broadly generalizable superiority is supported.

## Public files and instructions

- `Report01_Qwen3_ARC_Easy_Evaluation_EN.pdf` — full report; note that its page 4 references a *separately retained* full evidence archive and a deeper verifier not included in this public subset.
- `paired_outcomes_200.csv` — 200 paired binary correctness outcomes, in fixed order, no item texts or raw answers.
- `recompute_paired_statistics.py` — exact McNemar and paired bootstrap recomputation; Python standard library only.
- `REVIEWER_CHECKLIST.md` — specific, scope-limited feedback requested from an external reviewer.

From this directory:

```bash
python recompute_paired_statistics.py paired_outcomes_200.csv
```

From repository root:

```bash
python reports/report_01/recompute_paired_statistics.py reports/report_01/paired_outcomes_200.csv
```

Expected output begins `RESULT: PASS`, followed by the paired table and statistics. The script checks the dataset SHA-256 before performing any calculations.

## Boundary of verification

The **public package can independently recalculate statistical results only**. It cannot independently establish raw model response fidelity, frozen request reconstruction, original sampling, execution provenance, or rerun the model. The private full evidence archive was reviewed locally, with matching internal hashes and 400 rescores; these checks are **not** third-party validation or independently witnessed execution. Request full artifacts separately if a deeper assessment is needed, subject to rights and privacy review.

**Original full-evidence ZIP SHA-256 (unpublished):** `360e867cdb6af2c0fec4d0712443dae4971bb198eec76a071b0f60f81ecbb8ca`.

## Benchmark credit and licensing

Dataset: [AI2 ARC / ARC-Easy](https://huggingface.co/datasets/allenai/ai2_arc), licensed CC BY-SA 4.0 per its dataset card; Clark et al. (2018), [paper](https://arxiv.org/abs/1803.05457). Benchmark questions and answer texts are not included here. No repository-wide license for the author's own material has been granted.
