# M6 — Authorization Boundary Laboratory Note (November 2026)

**Status:** DESIGN HOLD · **End-to-end acceptance:** 0/6 gates closed · **Product readiness:** HOLD

> This is an experimental authorization-boundary study. It is **not** an operational AI action-control product, a completed end-to-end security evaluation, or an independent security certification.

## Independent review entry point — Step 277/278 (14 November 2026)

**[START HERE — Reviewer packet](REVIEW_START_HERE.md)** · **[Evidence index (JSON)](PUBLIC_EVIDENCE_STEP278.json)** · **[Read-only verification script](verify_step278.py)** · **[Polish overview](OMOWIENIE_PL.md)** · **[Open review issue #3](https://github.com/iller1/ai-evaluation-portfolio/issues/3)**

This new packet records a **locally reported negative identity control** (`DENY_WRONG_PROCESS_IDENTITY`), compilation with an `APPROVAL_HOLD` source excerpt, and a SHA-256 checked **private** Step 278A archive. A byte-identical historical DLL rebuild was **not** established. **No positive independent approval was executed and no E2E gate was closed.**

**Review scope:** public claims, digests, static HOLD reasoning and falsifiable design questions. **Reproduction limit:** original ZIP, full source, and laboratory host environment are *not* publicly included; anyone claiming independent full replication from this page would be overstating the evidence.

## The question

A justified AI conclusion is not the same thing as permission to act on it.

M6 explores how a request, a cryptographic authorization decision, a restricted Windows execution identity, and an eventual action could be bound together without silently granting authority merely because an upstream assessment looks correct.

This work is related to my **Comparative Feedback Control (CFC)** research, but does not modify the frozen CFC Anchor and does **not** demonstrate an integrated CFC → M6 → executor authorization chain.

## What was exercised in the laboratory

The work used two Windows laptops in separate requester and authority/execution roles, with local, synthetic test data.

| Area | Observed or reported evidence | Boundary |
| --- | --- | --- |
| Cryptographic signatures | Local tests accepted an original signature and rejected a forged signature. | A bounded signature test, not proof of independent approving authority. |
| Windows service identity | A temporary service probe was reported to run under **LocalService**, with the expected Windows service identity present and read access to its intended policy/certificate materials. | This was a token/read-access probe, **not** an authorized executor run. |
| Windows access restrictions | A restricted non-administrator lab account was tested against protected storage and access restrictions. | The result does not prove resistance to administrator compromise or all bypass paths. |
| Experimental request/commit logic | Draft code and synthetic checks cover nonce-claiming, audit events and a proposed atomic event path. | Full nonce replay, commit safety and recovery have **not** been verified end-to-end. |
| Evidence handling | A dated checkpoint and file-hash records were preserved for later inspection. | Local operator-controlled records are not independent custody or a signed attestation. |

The Windows token test is referenced in the private laboratory record as **Step 439**. The private **Step 448** checkpoint records the hold state. The full source tree, executable candidates, raw operator records and host configuration are **not** distributed with this note. Therefore, this public page does **not** enable independent reproduction of those original test executions.

## Why development was placed on hold

Several controls can behave as expected individually while the overall authorization boundary remains unproven.

The unresolved questions include:

1. **Independent approval:** Who controls the approving key and authority, separately from the requester and executor?
2. **Exact binding:** Is each approval cryptographically bound to the specific request, action, resource, scope, purpose, policy version, executor identity and validity window?
3. **Revocation and freshness:** What happens to expired, revoked or superseded approvals?
4. **Replay and crash recovery:** Can retries or interrupted commits ever cause a second effect?
5. **Evidence integrity:** Can execution and audit records be modified by a party that should not be trusted to attest to its own actions?

An approval contract and an approval-HOLD source candidate exist privately. The HOLD candidate was checked at source/compile level only; it has **not** been established as a deployed runtime control. An older, not-approved executable candidate must not be confused with that later source.

## Mandatory end-to-end gates — all open

| Gate | Required observation | Status |
| --- | --- | --- |
| **P01** | Valid, independently approved request produces exactly one intended test event | OPEN |
| **B01** | Restricted caller cannot bypass the execution boundary or write the protected event | OPEN |
| **B02** | Missing or invalid authorization signature produces no event | OPEN |
| **B03** | Incorrect scope/resource produces no event | OPEN |
| **R01** | Reusing an authorization nonce produces no second event | OPEN |
| **F01** | Interrupted commit and recovery do not create a duplicate effect | OPEN |

**Closed: 0/6.** Earlier focused or synthetic tests are not counted as completed end-to-end gates.

## Relationship to CFC, HAWM and Information Passport

These are distinct concerns, not a claimed finished integration:

- **HAWM:** preserves structured working state, including open issues and evidence.
- **CFC:** evaluates whether a bounded conclusion/closure is justified by the represented evidence.
- **Information Passport:** a separate research concept for information provenance, scope, freshness and revocation; **not integrated into M6**.
- **M6:** investigates whether a specific action has independent, valid authorization before any executor is allowed to act.

A CFC decision, even if valid, would **not itself grant action authority**. No live downstream action authorization is claimed here.

## What this note does not claim

- No full CFC × HAWM × M6 × Information Passport integration.
- No completed production action execution.
- No independently verified approving authority or key custody.
- No completed mandatory end-to-end security gates.
- No claim that a successful signature check proves an approved business action.
- No independent reproduction or independent chain of custody.

## Next evidence threshold

Work should resume only with a separately reviewed approval boundary, an explicit authorization-to-action binding contract, a defined crash-recovery rule and an executable, preregistered negative/positive E2E test plan. Until those conditions are met, the correct disposition is **DESIGN HOLD / PRODUCT HOLD**, not an unconditional PASS.

**Publication scope:** research summary and limitations only. Implementation details and private test evidence are withheld pending a separate intellectual-property, safety and disclosure review.

**Rights:** published for reading and evaluation; no additional code or reuse license is granted by this note. Refer to the repository's [rights and reuse statement](../../RIGHTS_AND_REUSE.md).
