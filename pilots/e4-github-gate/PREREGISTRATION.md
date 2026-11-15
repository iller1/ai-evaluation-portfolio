# E4 / GitHub Protected Environment — preregistration v0.1

**Frozen 2026-10-25 before any GitHub pilot run.** This is a review copy; no tests have been executed.

## Single research question

Can independent GitHub platform enforcement, using one protected environment configured with a **separate actual human reviewer**, block a harmless NOOP job without approval, let it proceed after that approval, and refuse it after rejection? This **does not** test atomic authorization-epoch CAS or the safety of downstream effects.

- Actor A: starts a GitHub `workflow_dispatch`.
- Actor B: preregistered reviewer, different real GitHub account, willing participant with only required privileges.
- Protected environment: `cfc-handoff-review-test` in a **new disposable public sandbox**, not in the production or existing CFC repositories.
- T1: run created with synthetic decision `DEMO-001`, SHA-256 `fb4755bb465c15e897548ba7b40997a0c548f83026b8147188a95cb7f8b26911`.
- T2: GitHub approves/rejects deployment through its own control plane; **not** a CP-15 receipt or epoch CAS.
- T3: runner executes **NOOP only**, a log message, not publication or mutation of external data.

## Required setup evidence before G1

1. Separate public sandbox and no secrets.
2. Exact environment `cfc-handoff-review-test`, with `Required reviewers` configured to named B.
3. `Prevent self-review` ON; admin bypass OFF if the platform supports it; otherwise **HOLD/INCONCLUSIVE** for a strong gate claim.
4. Record repo name, workflow hash, configuration screenshot/record and date.
5. B has explicitly agreed. Workflow has been reviewed by A before addition; Actions enabled.
6. Do not start the workflow before all rules are enabled.

## Frozen tests, in order

| Case | Sequence | PASS | FAIL | INCONCLUSIVE |
|---|---|---|---|---|
| G1_WAIT | A dispatches; B does not approve; inspect waiting; cancel | GitHub shows waiting, and NOOP log absent | NOOP executes without approval | Insufficient state/config evidence |
| G2_APPROVE | Separate run; B approves; job executes | Provider history identifies B approval before NOOP, and run log binds ID and T1 hash | NOOP runs without required B or with invalid recorded binding | Approval actor or log not established |
| G3_REJECT | Separate run; B rejects | GitHub records rejection, NOOP does not execute | NOOP executes despite rejection | Rejection evidence missing |

Do not alter configuration or expected results in response to outcomes; do not use administrator bypass. One run per case.

### Evidence to collect

Run URL, run ID and attempt, case, dates, job state, who approved/rejected according to GitHub, approval/rejection record, setup screenshots (captured **before** tests), workflow and fixture hashes, NOOP log for G2 and non-execution evidence for G1/G3.

### Final decision

- `EXTERNAL_GATE_OBSERVED_PASS`: G1/G2/G3 all meet documented criteria; **only provider gate behavior** in this setup.
- `FAIL`: observed execution without required B approval given verified correct configuration.
- `INCONCLUSIVE`: cannot determine approval actor, sequence, settings, or logs.
- `NOT_COMPLETED`: missing willing reviewer, configured sandbox or runs.

A participant acting as B is **not** automatically an independent security auditor of CFC. This pilot cannot prove safe post-approval revocation, time-consistent execution, signed authority, or T3 publication.
