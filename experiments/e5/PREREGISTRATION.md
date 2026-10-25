# E5 — Remote resource-version conditional update (2026-10-25)

**Frozen before executing any E5 remote update.** Separate from E4. This experiment uses only a synthetic resource on an isolated branch in `iller1/ai-evaluation-portfolio`, never `main` or CFC. No reviewer, workflows, secrets, deployment, publication, or external action required.

## Narrow question

Does GitHub's Contents API accept a file update conditioned on the current **file blob SHA**, reject a second update using the same stale blob SHA after the first update, and expose a persisted resulting artifact that can be read back independently of the write response?

This is **resource version control**, **not** an authorization-epoch CAS test. The GitHub API's Contents Update uses the existing file blob `sha`, required for updates. Its guarantees are scoped to the target content. It does not atomically couple an arbitrary revocation ledger to side effects, nor independently attest real user permission, timestamps, multiple process consistency, or the actual downstream effect of a decision.

## Fixed test data

- Branch: `experiment/e5-remote-file-cas-20261025`.
- Path: `experiments/e5/controlled_resource.json`.
- File data: JSON with `schema=CFC_E5_REMOTE_FILE_CAS_v0.1`, `decision_id=DEMO-E5-001`, `resource_id=E5-NOOP-RESOURCE`, `action=NOOP`, `authorization_epoch=NOT_TESTED`, and a `state`.
- Initial state: `READY`; positive update: `ACCEPTED`; stale attempt: `REJECTED_SHOULD_NOT_COMMIT`.
- All writes use the GitHub connected repository Contents API on the isolated experiment branch. No parallel invocations.

## Frozen cases

| Case | Execution | Expected | Acceptable decision |
|---|---|---|---|
| E5-P | Read initial file SHA; update `READY → ACCEPTED` with that SHA | Update succeeds with resulting commit ID | PASS if verified by separate readback |
| E5-S | Attempt an update to `REJECTED_SHOULD_NOT_COMMIT` using *old initial blob SHA* after E5-P | GitHub refuses as stale/conflict, no new file content | PASS only with explicit stale/mismatch failure and independent readback |
| E5-V | Fetch file again from the named branch | JSON state `ACCEPTED`, expected `decision_id`, no unintended content | PASS only if reads agree |

**STOP / INCONCLUSIVE** if a transport/authentication error, unclear refusal, or unverifiable readback occurs. **FAIL** if stale update succeeds and changes the tracked file despite the preconditions. Do not retry until a result is understood. Retain the original and current blob SHA, updated commit SHA, rejection reason, branch and path. A refusal without a clear stale-SHA reason cannot be counted as an E5-S PASS.

## Explicit limitations

1. Git blob SHA is content-addressed, so an `A→B→A` change can return to the old blob SHA (ABA); this is **not** a monotonic authorization epoch.
2. This test is authored and executed using the user's own account; GitHub provides external persisted state but no independent reviewer or auditor.
3. The test does **not** verify real revocation, cross-resource atomic authorization, signed T2 acceptance, or real T3 effects.
4. No claim of distributed transaction or exactly-once execution follows from these results.
5. The experiment branch is intentionally separate from the E4 draft PR and frozen CFC/HAWM/CP-15 artifacts.

**Release status before remote test:** PREREGISTERED / NOT EXECUTED.
