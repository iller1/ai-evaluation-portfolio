# M6 — Action-binding, executor outcome and timing: review plan

**Planning note · 13 November 2026 · DRAFT FOR DESIGN REVIEW — NOT A TEST RESULT**

**Baseline preserved:** `CFC FROZEN | M6 HOLD | E2E 0/6`. This note does **not** modify CFC Anchor, approve deployment, close an E2E gate, or claim an experimentally observed latency.

## Why this plan exists

The earlier [M6-02 diagnostic](../m6-request-anchor-binding/REPORT_EN.md) observed a synthetic mismatch: the caller requested `claim:c2`, while the supplied callback evaluated `c1`; Integration Layer v0.5.0 nevertheless returned `ALLOW` and `final_action_authorized=true`. No external action was executed. This is an **integration/caller identity-binding boundary**, not a proven defect in frozen CFC Anchor or an executed exploit.

A correct CFC assessment, valid request signature, or local `DENY` return alone does not prove that an **independent authority approved this exact action** or that a **real executor complied**. A matching pair of IDs both controlled by the caller is not an authenticated binding.

A reviewer should challenge the following *proposed* chain; it has **not** been demonstrated end to end:

`REQUEST -> VERIFIED BINDING + INDEPENDENT AUTHORIZATION -> EXECUTOR COMPARE/COMMIT -> TARGET-SIDE OUTCOME`

Each arrow needs its own source of trust and a separately inspectable observation. A successful control must show both **no unauthorized allow** and **no unjustified stop of a valid request**.

## Provenance, separation, and evidence classification

- **Requester (Laptop 1):** proposes exact action, resource, purpose, audience/target and intended state; must not self-attest the result.
- **Authority/Signer (Laptop 2 in the current lab):** cryptographic key-use can be demonstrated separately, but sharing administration/control with the executor does **not establish independent organizational authority**.
- **Executor (currently also Laptop 2):** must verify authorization **for the committed action**, using a trusted binding source and current relevant state; a decision returned earlier does not replace this check.
- **Target outcome:** a lab-local event written under lab control is a proposed `LAB_TARGET_RECEIPT`; a receipt from an independently administered target would be `INDEPENDENT_TARGET_RECEIPT`. Neither can be inferred from `executed=false` or a local response without direct observation.

Log the request digest, verified claim/evidence snapshot digest, binding-source identity and record digest, policy version, authorization decision, executor identity, target receipt, and unambiguous event correlation identifier. The integrity and trust level of each assertion must be stated separately; private account details or key material must not be published.

## Proposed scenario matrix — NEW IDs to avoid collisions with frozen E2E gates

These are **future oracle candidates only**. They do not rename or count toward `P01/B01/B02/B03/R01/F01` in the six-gate E2E table.

| Scenario | Setup | Expected high-level outcome | Status |
| --- | --- | --- | --- |
| **AB01** | Valid `c1` request, independently sourced exact `c1` binding and valid approval | Exactly one intended isolated target event, if all checks pass | NOT RUN |
| **AB02** | Requested `c2`; evaluated `c1` | No authorization, no event | NOT RUN |
| **AB03** | Both IDs match but originate only from an untrusted caller | No final authorization, no event | NOT RUN |
| **AB04** | Valid approval revoked **before** executor commit | No event after effective revocation check; timing/cutoff must be predeclared | NOT RUN |
| **AB05** | Reuse signed response/nonce | No second effect | NOT RUN |
| **AB06** | Resource or evidence snapshot changed between check and use | No commit on stale state | NOT RUN |
| **AB07** | Binding/approval authority cannot be reached or state unknown | HOLD/UNRESOLVED, no event | NOT RUN |
| **AB08** | Valid, current, independently approved request | No unjustified refusal; exactly one intended event | NOT RUN |

**AB08 is essential:** a deny-everything implementation passes many negative controls but fails the research objective. Fail-closed behavior is not enough.

## Required **timing and freshness review gate** (separate from historical E2E 0/6)

**Gate label: `T-M6` · status: `DESIGN_OPEN / MEASUREMENT_NOT_RUN`.** It is a required **future study condition**, **not** a newly closed E2E gate nor a retrospective addition to the six-gate denominator.

Before collection, the protocol must define:

1. **Decision latency:** request received by authorization verifier -> allow/stop decision issued; define `t_request_received`, `t_decision`.
2. **Executor latency:** decision received/executor entry -> target commit or explicit rejection; distinguish `t_executor_entry`, `t_commit`, `t_target_receipt`.
3. **Revocation propagation latency:** authority records revocation -> executor obtains/observes it; distinguish `t_revoke_accepted` from `t_revoke_observed`.
4. **Revocation enforcement at commit:** independent of propagation time, show whether an attempted action after the defined effective cutoff is denied. Record actual executor decision and target-side event count.
5. **TTL / expiry:** predeclare issue-time, not-before, expiry, clock source, timestamp units, comparison rule at exact boundary, skew allowance and policy on uncertainty.
6. **Network and clock disturbances:** deliberate delay, delayed replies, loss of authoritative status, out-of-order messages, clock skew and request retries; specify which default to HOLD.
7. **Measurement quality:** per-host monotonic elapsed times for local segments, correlated event IDs for cross-device ordering, wall-clock timestamps with sync/skew/uncertainty metadata, resolution, repetitions and raw logs. **Do not subtract unsynchronized laptop wall times as if they were precise latency measurements.**
8. **Safety/reliability criteria:** thresholds must follow a risk and threat model **before** any run. No arbitrary claim that 100 ms (or another number) is safe; specify permissible stale-authorization window and false-block/false-allow rules.

**Requested timing evidence:** raw timestamps, host/clock metadata, verified run configuration and target/executor receipts — not just duration printed by a PowerShell wrapper.

### Timing acceptance has not been decided

The reviewer should recommend an explicit criterion for:
- positive request latency and event receipt;
- zero post-cutoff unauthorized events under expiry/revocation;
- measurable propagation delay with uncertainty;
- absence of false STOP on valid current requests;
- conservative treatment of ambiguous/disconnected status.

Until the oracle, safety window and observations are defined and frozen **before execution**, do not report `T-M6: PASS`.

## Review questions and stop conditions

1. **Trusted binding:** what source can independently establish the mapping between `request.resource_id`, the actually evaluated Anchor claim, the **exact evidence snapshot**, and the action? If only the caller controls both strings: **STOP IMPLEMENTATION**.
2. **Independent authority:** is there a separate accountable approver and key custodian, not merely two devices? If not, label any result `LAB_ONLY`.
3. **Executor boundary:** can the requester or signer bypass the executor's validation or directly write the target event? If yes: **NO-GO**.
4. **TOCTOU and revocation:** is authorization rechecked or atomically bound to commit and current target state? What is the precise point at which revocation becomes effective?
5. **Evidence:** can anyone outside the operator independently confirm which operation actually happened, not only what a script claimed happened?
6. **Proportionality:** can a smaller, clearer isolated proof establish both an allowed and denied path before adding further complexity?

## Proposed sequence (no active execution)

1. Review trusted `REQUEST -> Anchor` binding source and separate approval authority **on paper first**.
2. Obtain criticism of action/commit boundary, intended lab target receipt and two-sided positive/negative oracle.
3. Freeze exact test cases and timing instrumentation, including TTL, revocation-effective cutoff, clock uncertainties and stop conditions.
4. Only then, if safety and independence conditions are met, perform **small, isolated, non-harmful LAB_ONLY** E2E tests and publish evidence with precise limits. The frozen CFC baseline must remain unchanged.

**No tests have been run under this new plan.** Neither the existing Step 277/278 evidence nor the earlier synthetic M6-02 results establish independent authorization, a production executor, or timing guarantees.

**Related:** [current review packet](REVIEW_START_HERE.md) · [earlier proposed claim-binding contract](../m6-request-anchor-binding/BOUNDARY_CONTRACT_PROPOSAL_v0.1.md) · [review discussion](https://github.com/iller1/ai-evaluation-portfolio/issues/3).
