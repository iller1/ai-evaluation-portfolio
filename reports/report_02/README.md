# Study 02 — Cross-seed stability of evidence–claim labels

**Preparation date:** 25 October 2026  
**Status:** `FROZEN LOCALLY / NOT RUN / NO RESULTS`  
**Planned execution and reporting window:** 2–15 November 2026  
**Review status:** internal author-led review only; no independent annotation or independent run.

## Research question

How stable are three-way evidence–claim classifications from **one fixed local model** when the evidence, claim, rubric, prompt, response schema and common generation settings remain unchanged, but the predefined random seed differs?

This is a **cross-seed label-stability study**, not a test of identical-seed replay, model accuracy, agreement between independent human raters, truth verification or production safety.

## Prespecified design

| Feature | Frozen specification |
|---|---|
| Model | `qwen3:0.6b` (Ollama 0.40.11) |
| Model digest | `7df6b6e09427a769808717c0a93cadc4ae99ed4eb8bf5ca557c90846becea435` |
| Inputs | 45 author-created fictional evidence–claim pairs |
| Author reference labels | 15 `SUPPORTED`, 15 `CONTRADICTED`, 15 `NOT_ESTABLISHED` |
| Case types | 12 direct facts; 12 numbers/dates; 12 conditions/exceptions; 9 compound claims |
| Pass A | seed 101 |
| Pass B | seed 202 |
| Common generation settings | temperature 0.2, context 2048, prediction cap 64, `think: false`, `stream: false` |
| Planned primary observations | 45 paired classifications (90 case/pass responses) |
| Output | JSON object with **exactly one** `label` field and one of the three enumerated values |

The model sees only the **evidence**, **claim** and **rubric**; it is not given author reference labels or rationales.

**Rubric precedence:** (1) `CONTRADICTED` if any material claim component is directly contradicted; otherwise (2) `SUPPORTED` only if *all* material components are supported; otherwise (3) `NOT_ESTABLISHED`. No external knowledge or inference of missing facts is permitted.

Six separate calibration examples (`CAL-01`–`CAL-06`) were internally reviewed and excluded from the 45-item main dataset.

## Frozen decision criteria

- **Primary metric:** strict matching label pairs out of all 45 cases; invalid outputs count as nonmatches.
- **Secondary metrics:** both-valid pairs, invalid counts by pass, 3×3 agreement/disagreement table and Cohen's κ computed **only on pairs with two valid labels**.
- **PASS:** 90 case/pass results recorded; at least **43/45** pairs have two valid labels; at least **40/45** pairs have two matching valid labels; and **κ ≥ 0.70**.
- **FAIL:** a completed, otherwise valid run fails any threshold, including undefined κ.
- **INCONCLUSIVE:** serious protocol/integrity error or unresolved transport failure.
- **NOT_COMPLETED:** no complete main experiment by the 15 November deadline.

Thresholds are **project-specific pilot criteria**, not established safety or production acceptance levels. The finite sample and exactly two predefined seeds limit generalization; κ is prevalence-sensitive. Agreement can be high even when both passes are wrong. Author reference labels were not independently validated.

The logger is designed to retain requests, raw responses, parameters, timestamps, hashes, final classifications, transport errors and retry attempts. At most one retry is permitted for a transport-only failure using the identical request bytes. The main run must not silently resume a partial attempt.

## Freeze evidence (local, 25 October 2026)

The following seven files were checked byte-for-byte and recorded in a local freeze manifest. The original names containing `REVIEW` are historical filenames; the manifest freezes those *exact* bytes.

| Frozen file | SHA-256 |
|---|---|
| `main_dataset_45_v0_2_REVIEW.json` | `74086847af27fbaffa38f0d794da7cff579d18f41fdb14afd2f8c10abebf6190` |
| `model_contract_v0_1_REVIEW.json` | `1b9c3d2c05a8785283b2bb30dab1d09dc3c47403f5bf4b8c99a2029d2a5f7beb` |
| `report02_score_v0_1.py` | `8797504a9c4080ea35ae28c192a04122502258935a8d46e5d4fc566d2cb747a2` |
| `model_environment_v0_1_REVIEW.json` | `bce603a748b03ee232ef35c65d2010665b91e42be0db4b9fdb7f2fc5c000d893` |
| `protocol_v0_2_REVIEW.md` | `91831de4bf4c389a79245373fed9e19bff8e73d1f8150354465ae979bb96ed73` |
| `calibration_review_v0_1.md` | `79a7ce46016690a92c222507fbb5cadd84b859d3538aa5b58ce751c395627544` |
| `report02_runner_v0_1.py` | `520584798d6f2cc9bb5097a727cdc6dfd3311391e69656754cc54658d2c44018` |

**Local `freeze_manifest_v0_1.json` SHA-256:** `85183e9ac9dde1d5d5f5a107bc150967647acf212e24fafd5210d7b983d9c6bd`.

This records the **author's local checks**; posting hashes here is not independently witnessed custody or validation.

## What is public now?

- [Frozen scorer code](report02_score_v0_1.py) — nine offline self-tests reported `PASS` locally.
- [Frozen runner code](report02_runner_v0_1.py) — five offline self-tests and a read-only local preflight reported `PASS`.
- This preregistration/plan and the frozen file hashes.

To run the *offline* self-tests from the repository root:

```bash
python reports/report_02/report02_score_v0_1.py --self-test
python reports/report_02/report02_runner_v0_1.py --self-test
```

**Publication boundary:** The exact frozen dataset, original protocol, model contract, local environment record, calibration audit, freeze manifest and actual run receipts are **not yet published here**. The full main experiment therefore **cannot currently be reproduced from this public subset**; do not claim that it has been run or externally verified. Publishing the full reproducibility package and report is planned after the study, subject to review.

## Outcome

**None yet.** As of 25 October 2026 the freeze verification reported `FROZEN`, seven locked files and **zero main model-generation calls**. Regardless of outcome, the study will report negative or inconclusive findings without changing the frozen thresholds.
