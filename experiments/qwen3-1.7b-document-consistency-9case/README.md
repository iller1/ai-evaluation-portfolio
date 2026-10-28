# Qwen3 1.7B — document consistency and uncertainty: nine-case diagnostic

**Date:** 28 October 2026  
**Evaluator:** Krzysztof Sliwka, with AI-assisted internal review  
**Status:** COMPLETED LOCAL DIAGNOSTIC / INTERNAL SCORING / NOT INDEPENDENTLY REPLICATED  
**Scope:** nine self-authored, fictional Polish two-statement documents evaluated through **direct local Ollama**, **not** through the CFC × HAWM product. This is **not Portfolio Study 02**.

## Research question

When a small language model is asked to identify conflicting, consistent, or underspecified document rules, does it (a) select the expected class, (b) keep its explanation consistent with that class, (c) acknowledge missing conditions, and (d) quote source sentences exactly?

## Protocol and evidence boundary

- **Nine cases:** three author-labelled `CONFLICT`, three `CONSISTENT`, three `INCONCLUSIVE`. Expected labels and rationales were recorded locally before execution; **not** externally timestamped or independently validated.
- **Model:** local `qwen3:1.7b`, Ollama `/api/chat`. The provider-reported model name was checked; a specific model digest was **not recorded in this result**.
- **Common parameters:** `think=false`, `temperature=0`, `seed=42`, `num_predict=512`, `stream=false`; one response for each case. The expected label/rationale was not sent to the model.
- **Prompt:** inspect an unverified document and answer in Polish with one of `SPRZECZNE`, `SPOJNE` or `NIEJEDNOZNACZNE`, precise supporting quotes and brief reasoning, withholding a decisive conclusion when context is missing.
- **Scoring:** initial label agreement was distinguished from **strict semantic PASS** (compatible label, internally consistent reasoning and appropriate uncertainty). Exact quotation required the full original sentence, including punctuation, to appear in the reply. Semantic judgments were reviewed by an assistant, **not an independent human assessor**.
- **Primary evidence:** locally retained `CFC_HAWM_AI_QA_20261028T184200Z.zip`, SHA-256 `b1ae83de69b0669624c5f5339b246f4bd6d429baac8a8fe6b68e2187a5491b2f`. ZIP CRC and four manifest-listed SHA-256 checks passed in the internal review. The original ZIP is **not** deposited in this repository.
- **Source dataset digest:** original `CASES.json` SHA-256 `aa658881f96c8691c4dfca004980da10920d7fc401bbdacfd73521f848a0072c`. The text transcription published here is for inspection and is **not evidence of independently verified original model calls**.

## Observed results

| Measure | Observation |
|---|---:|
| Completed local model requests | **9/9** |
| Headline class matched self-authored reference | **5/9** |
| Strict semantic assessment (class + consistent explanation + uncertainty) | **4/9 PASS; 5/9 FAIL** |
| Correctly signalled `INCONCLUSIVE` on three author-labelled ambiguous cases | **0/3** |
| Exact complete source quotations on three conflicting cases | **2/6 sentences** |

The model finished all nine requests, but the outputs contained several defects. In **C01**, it wrote `SPOJNE` ('consistent') twice while explaining that the two rules were contradictory. In **N03**, it labelled compatible rules `SPOJNE` but then said the question could not be resolved without further context. In **A01**, it inferred that an accelerated emergency procedure waived written approval, although the document did not state that. **A02** and **A03** gave decisive conclusions despite unresolved questions about account creation versus access and the effective dates of instruction versions. Four of six required quotations missed at least the final full stop; this is an **exact-string** defect, not necessarily a change in meaning.

### Per-case disposition

| Case | Author reference | Model headline / behavior | Strict review |
|---|---|---|---|
| `C01_ACCESS_POSITIVE` | CONFLICT | `SPOJNE`; explanation says the rules conflict | **FAIL** |
| `C02_SATURDAY_POSITIVE` | CONFLICT | `SPRZECZNE` | PASS (quotes non-exact) |
| `C03_RETURNS_POSITIVE` | CONFLICT | `SPRZECZNE` | PASS (quotes non-exact) |
| `N01_NEGATION_CONTROL` | CONSISTENT | `SPOJNE` | PASS |
| `N02_WEEKEND_CONTROL` | CONSISTENT | `SPOJNE` | PASS |
| `N03_RECEIPT_CONTROL` | CONSISTENT | `SPOJNE`, then 'cannot determine' | **FAIL** |
| `A01_EMERGENCY_AMBIGUOUS` | INCONCLUSIVE | `SPORZECZNE` [intended `SPRZECZNE`]; unsupported assumption | **FAIL** |
| `A02_ACCOUNT_AMBIGUOUS` | INCONCLUSIVE | `SPOJNE`; missing scope caveat | **FAIL** |
| `A03_VERSIONS_AMBIGUOUS` | INCONCLUSIVE | `SPORZECZNE` [intended `SPRZECZNE`]; ignores effective dates | **FAIL** |

**Label-only matrix** (raw headline, ignoring conflicting justifications and accepting the misspelling `SPORZECZNE` as `SPRZECZNE`):

| Author reference \ model | SPRZECZNE | SPOJNE | NIEJEDNOZNACZNE |
|---|---:|---:|---:|
| CONFLICT | 2 | 1 | 0 |
| CONSISTENT | 0 | 3 | 0 |
| INCONCLUSIVE | 2 | 1 | 0 |

## Inspect the recorded examples

**[Nine source texts and verbatim response transcriptions](RAW_OBSERVATIONS.md)** · **[Polish summary](OMOWIENIE_PL.md)**

The source passages are fictional and self-authored. These pages publish the failure cases, including responses that conflict with their own reasoning. The transcript is a **text transcription of local evidence** rather than independently witnessed model output. The original `RESULTS.json` and ZIP, including request hashes and provider token counts, are retained by the evaluator outside this repository.

## Interpretation and next checks

This limited pilot documents **observed model failure modes**—self-contradictory verdicts, unsupported assumptions, poor uncertainty handling, and non-verbatim citations—under the stated conditions. It does **not** establish a population accuracy rate, cross-seed reliability, robustness to changed prompts, or performance on real corporate documents. The three `INCONCLUSIVE` references especially need independent review before extrapolation.

A practical product requirement follows: **a model's verdict must remain visibly unverified**; it should not silently authorize a document, update evidence, or imply that CFC approved the content. A proposed model-answer consistency checker would itself require adversarial evaluation; **it has not been demonstrated by this test**.

**No CFC Anchor run; no native HAWM state or product end-to-end run; no action authorization.** The known CFC × HAWM M6 integration boundary remains open. Publication of this **portfolio diagnostic report** is not publication, certification or release approval of the CFC × HAWM application.

**Rights:** public for inspection, with no repository-wide reuse licence; see [rights and reuse](../../RIGHTS_AND_REUSE.md).
