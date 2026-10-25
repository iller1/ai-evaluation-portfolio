# Case Study — TheChoiceLessChoice Alpha: evidence-bound black-box evaluation

**Evaluation dates:** 23–25 October 2026  
**Evaluator:** Krzysztof Sliwka (external operator; AI-assisted offline consistency checks)  
**Subject:** TheChoiceLessChoice Alpha  
**Status:** COMPLETE / CLOSED — within the authorized scope  
**Classification:** Practitioner case study, **not** Portfolio Study 02, a penetration test, a security certification, or an independent audit of production controls.

## Evaluation question

Can the observable Alpha interfaces reject stale or unregistered decision-state receipts in the specified scenarios, and does the public dry-run execution interface enforce the initially stated single-use expectation?

The developer authorized the relevant, bounded dry-run API exercises. The G0/G1 sequence followed a developer-supplied procedure. T1 and T2 used frozen, prospective expectations and fresh decision identifiers; no automatic retry was performed.

## Recorded outcomes

| Phase | Date | Observed result | Evidence boundary |
|---|---|---|---|
| P01–P04 Preflight | 23 Oct | 4/4 expected visual/simulator behaviors | UI observations only; **not** the state API or an executor test |
| G0/G1 state-version sequence | 23 Oct | **PASS_OBSERVED**: HTTP 201 / 200 / 201 / 409 / 200 / 422 | Developer-provided procedure; client-captured responses, local SHA-256 recomputation |
| T1 receipt reuse | 24 Oct | **FAIL_OBSERVED** against the pre-test single-use expectation: same current state/receipt accepted twice (HTTP 200, `accepted: true` on both executions) | A **dry-run contract mismatch**, not a demonstrated downstream replay exploit |
| T2 uncommitted state hash | 25 Oct | **PASS_OBSERVED**: correctly calculated but uncommitted successor hash rejected with HTTP 422 / `unknown_receipt` | Single recorded client-side sequence; no claim about all forged receipts |

The T1 record preserves the original `FAIL_OBSERVED` outcome without retrospective relabeling. The pre-test expectation was recorded in the 24 October T1/T2 preregistration following the developer's earlier single-use statement.

**Developer clarification, received after testing:** the public Alpha dry-run endpoint checked stored-state freshness without consuming a nonce. The developer first described downstream single-use enforcement as existing elsewhere, then **explicitly corrected that statement on 25 October**: downstream single-use enforcement was **not implemented in this Alpha project and remained unverified**. This is a developer-reported architectural clarification, **not** a property independently established by these tests. It explains the observed dry-run mismatch but does not alter the frozen T1 verdict.

## Evidence handling and reproducibility boundary

- Client-side JSON records were retained for the API steps; recorded state hashes were independently recalculated locally using the specified canonicalization.
- Offline checks included a first-pass 36/36 internal consistency assessment and a second-pass 26/26 verifier consistency check plus 8/8 intentionally modified-case detections. The T1/T2 runner had 12/12 offline self-tests.
- **These counts do not constitute third-party replication or independent server-side verification.** They describe internal, AI-assisted consistency checks of operator-side artifacts.
- The historical findings, preregistered expectations, and developer clarification were preserved in a consolidated private PDF dossier (v1.1, 25 October 2026), supplied to the project owner.
- Raw evidence archives and the dossier are retained outside this public repository; they are not presented here as publicly reproducible test fixtures. No credentials, access tokens, or raw authorized API requests are published.

## Not established

This exercise did **not** establish downstream single-use consumption, concurrency/atomicity, real action suppression, production policy enforcement, signatures or attestation, cross-account isolation, revocation semantics, or immutable server-side evidence custody. A SHA-256 digest is an integrity identifier, **not** a server signature.

## Professional takeaway

The value of this case lies in disciplined reporting: freeze expectations before tests, preserve unfavorable observations, separate owner explanations from independent evidence, disclose provenance and evidence limits, and stop at the agreed boundary.

**Disposition:** evaluation closed on 25 October 2026; no further access or testing requested. The recorded outcomes are specific to the tested Alpha interface and scenarios, not a product endorsement or security-assurance claim.
