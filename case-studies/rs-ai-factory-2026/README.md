# Case Study — RS AI Factory: Independent Offline Verifier Evaluation

**Evaluation date:** 22 November 2026  
**Evaluator:** Krzysztof Sliwka — Independent AI Evaluation Researcher  
**Project:** RS AI Factory (project name acknowledged by the owner for portfolio use)  
**Subject under test:** `rs-ai-minimal-offline-verifier/1.0`  
**Status:** INITIAL LIMITED-SCOPE EVALUATION COMPLETED — **PUBLICATION APPROVED BY PROJECT OWNER (23 November 2026)**  
**Assessment:** **LIMITED POSITIVE EVIDENCE**; not a general platform PASS or security certification.

> **Publication and attribution:** RS AI Factory’s owner reviewed the case study and approved its publication under the project name on 23 November 2026. This approval is permission to publish the case study, not an endorsement of the evaluation findings or a certification of the platform.

## Evaluation question

For an unchanged, supplier-provided offline evidence verifier, do the reported result categories and process exit codes match the specified expectations for reference cases and four evaluator-designed negative alterations?

This was a **bounded independent evaluator-run assessment** of a particular verifier package. It did not cover the full RS AI Factory platform, production deployment, or real downstream execution.

## Method

- Inspected the supplied offline-verifier package against the provider's reference archive digest and retained local test receipts.
- Ran the unchanged Python verifier under a restricted Ubuntu WSL2 environment, in fresh temporary package copies. This was not a hardened independent security sandbox.
- Exercised **three provider-supplied reference fixtures**, **three unchanged positive-control repeats**, and **four independently prepared negative alterations**.
- Checked observed `VALID`/`INVALID` classifications and exit codes against predeclared expectations. Reviewed stored check identifiers and the supplied failure-code references.
- Preserved six JSON receipts, an evidence manifest, and SHA-256 consistency records in the evaluation delivery package supplied to the project owner.

## Recorded observations

| Category | Observed outcomes | Interpretation |
|---|---:|---|
| Provider reference fixtures | 3/3 matched expected category and exit code | Two `VALID / 0`; one supplied tampered fixture `INVALID / 1` |
| Unchanged positive-control repeats | 3/3 matched | Three additional `VALID / 0` observations |
| Evaluator-created negative alterations | 4/4 matched | Four `INVALID / 1` observations for the specific changes made |
| **Total verifier invocations** | **10/10 expected category and exit-code matches** | **5 `VALID / 0`, 5 `INVALID / 1`**; not ten unique failure scenarios |

The four evaluator-designed negative alterations tested:

1. One changed hexadecimal character in the signed commit-grant `prepared_sha256` field (reported `F2`).
2. An incorrect command-line keyring SHA-256 pin (`K1`).
3. An incorrect command-line policy SHA-256 pin (`P1`).
4. A one-byte change to a decision-audit event signature (`E1`).

The provider-supplied tampered evidence fixture separately returned `INVALID / 1` with reported `A1` and `S1` checks. The check codes are **verifier-reported results**, not independently established proof of every internal cryptographic pathway.

## Crucial unresolved findings

**Every one of the ten verifier responses — including the five `VALID` responses — contained six `INCONCLUSIVE` items.** The provider's verifier identified these unresolved matters:

| Code | Unresolved assurance question |
|---|---|
| `U1` | Completeness of the decision-audit log |
| `U3` | Independent provenance/authenticity of public keys |
| `U4` | Full contents of underlying immutable-chain records |
| `U5` | Independently witnessed checkpoint authenticity and historical completeness |
| `U6` | Evidence of target-side execution or absence of effects |
| `U7` | Ability to reassess policy correctness without the underlying policy text |

A `VALID` response means the applicable mandatory checks passed **for the supplied evidence**. It does **not** establish authorization to act, independently verified execution, or closure of these unresolved assurance questions.

## Evidence and reproduction boundary

This case study summarizes the evaluator's recorded observations. The owner received the detailed evaluation report (reviewed v0.4) and supporting evidence package. The original provider verifier source, signed fixtures, altered input files, and complete mutation scripts are **not included in this public case study**.

Consequently, the case study supports inspection of the described method and findings, **not independent, bit-for-bit reproduction of the full experiment from this document alone**. Locally matching archive hashes and receipt manifests support artifact consistency, not independent attestation of execution chronology.

A separate set of **13 candidate test cases**, organised into **three groups (T01: 4, T02: 4, T03: 5)**, was prepared but **not executed** against this verifier. No general reliability rate, production readiness, key trust, log completeness, replay resistance, revocation-to-commit enforcement, or real-world action effects were established.

## Professional takeaway

The central lesson of this engagement was the separation of **successful mandatory-check outcomes** from **unresolved assurance claims**. The verifier rejected the four tested evaluator-created alterations as expected, while independently significant questions remained explicitly `INCONCLUSIVE` even in `VALID` cases.

**Disposition:** **LIMITED POSITIVE EVIDENCE** for the tested offline-verifier behavior. Initial evaluation closed within its recorded scope; further independent technical due diligence of the broader platform would require a separate, defined engagement. This is not a product endorsement, certification, or acquisition valuation.