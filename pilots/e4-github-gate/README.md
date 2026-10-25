# E4 — External decision-handoff gate (review request)

**Status: REVIEW ONLY · NOT RUN · No independent replication.**

This is a small, preregistered experiment proposal testing whether GitHub Actions' **protected environment** can prevent a harmless NOOP job from starting until a **separate, named human reviewer** approves it. The test distinguishes (T1) making a decision, (T2) an external provider accepting/approving a job, and (T3) the actual effect. It does **not** equate any of these.

**Research question:** With a correctly configured GitHub environment, does the provider block a job without another human's approval, permit it after approval, and prevent it after rejection?

**No action has run.** The workflow is intentionally stored as [`t2-protected-noop.yml`](t2-protected-noop.yml) **outside** `.github/workflows/`. Merely viewing this review branch cannot enable or execute the workflow. Do not move it into an active workflow path until a separate disposable public sandbox repository, the required reviewer, and its environment protections are configured and checked.

## Three preregistered cases

| Case | Procedure | Expected observation |
|---|---|---|
| G1_WAIT | Dispatch, withhold approval, inspect waiting state, cancel | Job does not execute NOOP |
| G2_APPROVE | New run; separate reviewer approves | Provider records approval before NOOP runs |
| G3_REJECT | New run; separate reviewer rejects | NOOP does not run |

**Preconditions:** separate public sandbox repository; one named reviewer with a separate GitHub account who has agreed to participate; required reviewer enabled; prevent self-review ON; administrator bypass disabled where supported; setup evidence recorded before first run. Otherwise **HOLD/NOT COMPLETED**. Do not change the criteria after seeing results.

Synthetic T1: [`synthetic_decision.json`](synthetic_decision.json), canonical JSON SHA-256 `fb4755bb465c15e897548ba7b40997a0c548f83026b8147188a95cb7f8b26911`.

### Review correction: T1 runtime binding (2026-10-25)

The original proposal merely compared a `workflow_dispatch` string with the expected digest; this did **not** prove that a real fixture was present on the run's source commit. That review finding has been fixed in the **inactive workflow source**:

- The runner checks out the exact `github.sha` with a pinned `actions/checkout` revision and no persisted credentials.
- It requires `git rev-parse HEAD == GITHUB_SHA`.
- It reads `pilots/e4-github-gate/synthetic_decision.json` **from that checkout**, rejects duplicate JSON keys/unexpected fixture content, recomputes SHA-256 over canonical sorted compact JSON, and compares this with both the pre-registered hash and dispatch input.
- The runner observation includes `github_sha`, `checkout_sha`, `fixture_canonical_sha256`, and `fixture_raw_sha256`. Only the canonical SHA-256 is compared with the frozen expected value.
- **For the future sandbox:** place the fixture at the *same repository-relative path* and activate the workflow in `.github/workflows/` **only after** all required human environment protections are configured. The G1/G2/G3 criteria stay unchanged. The fixture binding is observed only when a runner actually starts; GitHub approval metadata must still be examined separately.

This closes one **runtime artifact-binding issue in the proposed runner**, not the gap between approval and execution. No live run, cryptographic authorization receipt, or independent audit is claimed.

## Please review

1. Is the setup sufficient to separate the requester's approval from the human reviewer's decision?
2. Do the three cases correctly distinguish WAIT, APPROVE, and REJECT?
3. What evidence from GitHub run/deployment history would establish the observed ordering?
4. Where would a revocation **after** approval but **before** execution still be able to slip through?
5. Would you agree to participate as the second reviewer, **after inspecting the design**?

Full criteria: [Preregistration](PREREGISTRATION.md) · [Limits](BOUNDARIES.md) · [Workflow source for inspection](t2-protected-noop.yml)

## Prior evidence — not independent validation

Earlier, isolated Windows fixtures reported **13/13** local decision-handoff tests and **8/8** local signed T2 tests. Those runs were synthetic, on the project owner's machine, with no real enterprise IAM or externally proven T3. This GitHub experiment remains **NOT EXECUTED**. Even three passing GitHub runs would demonstrate only the provider's review gate **under the selected configuration**.

**Out of scope:** linearizable compare-and-swap on an authorization epoch; enterprise authorization, mid-flight revocation, signed authorization receipts, proof of real publication, fault-tolerant exactly-once execution, and external security certification.

The frozen CFC Anchor 0.2.90rc1, Operator Wrapper v1.23, CP-15, and HAWM are not modified by this proposal. No business data, secrets, tokens, or publishing credentials are required.

### Polski — krótko

To **publiczny materiał do oceny**, nie wykonany eksperyment. Badamy, czy GitHub zatrzymuje zadanie testowe bez zgody **drugiej osoby**, uruchamia je po zgodzie i nie uruchamia po odmowie. Repozytorium do właściwego testu ma być osobne; workflow w tym PR jest celowo nieaktywny. Wynik nie udowodni atomowej autoryzacji ani wykonania działania po cofnięciu uprawnień.

**Feedback welcome:** comment on the pull request with concrete counterexamples or missing evidence. Participation in live runs is optional and requires explicit agreement.
