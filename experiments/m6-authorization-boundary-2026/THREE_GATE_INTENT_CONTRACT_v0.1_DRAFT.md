# M6 — Three GO gates for intent-level idempotency

**Step 279AU | v0.1 DRAFT | DESIGN REVIEW ONLY | NOT IMPLEMENTED | NOT RUN**

Baseline: `CFC FROZEN | M6 HOLD | E2E 0/6 | T-M6 NOT RUN`.

This proposal follows the external reviewer’s fresh-nonce/same-intent counterexample and the provisional AB09–AB14 scenarios. It is not a new test result, implementation, independent custody claim, or change to the frozen controller.

## Decision

Do **not** activate the approval path or execute AB09–AB14 until the authority, executor and target each have a durable, observable and enforceable decision boundary. **All three gates are required together.**

### Gate A — authority intent-level approval ledger: OPEN

Proposed `intent_key = H(domain || unambiguous_encoding(authenticated_requester_id, intent_id))`. The requester identity must come from verified authentication, not a self-asserted field. The authority computes `action_digest` over specified canonical action bytes.

**Linearization point:** an atomic, durable unique insert/update for `intent_key`, binding `action_digest`, stable `approval_id`, policy/authority epoch and lifecycle state. “Read, then insert” is not sufficient. No approval may be returned unless the exact decision or signed artifact can be durably recovered.

A retry with a fresh nonce and identical key/digest should reuse the stable approval identity, subject to current validity. Same key/different digest => conflict. Concurrent or ambiguous durability outcome => HOLD. Revoked or expired approval must not be silently reissued as valid.

**Requested evidence:** authenticated requester provenance (publicly redacted), attempt correlation, durable ledger transactions and uniqueness constraints, and concurrent/crash observations.

### Gate B — current authority at executor/commit boundary: OPEN

**Linearization point:** enforceable ordering between the *effective* revocation boundary and the target effect. The executor must check the signed approval against the action actually about to be committed: `intent_key`, `action_digest`, scope, target/resource, evaluated evidence/state, policy epoch, expiry and trustworthy provenance. Caller-controlled matching identifiers are not an independent binding.

A preflight revocation check does not prevent a time-of-check/time-of-use race. A claim of no post-revocation effects requires an enforced target-side atomic/fencing rule and a preregistered cutoff. Uncertain clock, status or reachability => HOLD/INCONCLUSIVE, never ALLOW.

**Requested evidence:** raw executor validation, authority version/epoch, ordered revoke/commit observations with clock uncertainty, target outcome.

### Gate C — observable target effect, deduplication and recovery: OPEN

For a local target in the **same transactionally governed store**, bind intent state and effect in one atomic transaction with a unique intent key. The current separate filesystem `.claim` and `.event` operations do **not by themselves** demonstrate that property.

For an external target, local `RESERVED` alone cannot prove an exactly-once effect. The target itself needs an idempotency guarantee and a trustworthy, queryable receipt/reconciliation mechanism by `intent_key`. After crash or lost response, missing receipt != `NOT_EXECUTED`, and unknown effects must not be retried automatically.

**Proposed receipt fields:** target identity, intent key, action digest, approval ID, effect ID, commit outcome, target sequence/version, enforced authorization epoch (when applicable), observation window and provenance. Define completeness, retention and deletion rights. Mutable local hashes are not independent custody.

### Provisional test oracles (all NOT RUN)

| Case | Expected positive oracle | Important limitation |
| --- | --- | --- |
| **AB09** | Same intent, fresh nonces => one stable approval and exactly one observed target effect | A deny-all system cannot pass |
| **AB12** | Distinct valid intents, identical action => two approvals and exactly two target effects | False-block control |
| **AB13** | Concurrent retries and authority crash => recover one stable approval, no duplicate | Unknown durable state => HOLD |
| **AB14** | Executor crash after RESERVED => no second effect; reconcile uncertain target outcome | Missing receipt != NOT_EXECUTED |

AB10 and AB11 remain separately proposed and NOT RUN. AB09–AB14 do not alter the six historical E2E gates.

**Classification:** a positive scenario is NOT RUN if no valid positive authority path exists; INCONCLUSIVE if observed target evidence is incomplete; FAIL only when its preregistered positive preconditions and complete observation are established and the oracle is violated. Do not claim PASS for a returned DENY alone.

### Questions for independent review

1. Is the authority’s unique/atomic approval linearization point sufficient under concurrent retries and crashes? What minimal durable transaction/receipt would establish it?
2. What enforceable revocation ordering at commit is possible when the authority, executor and target do not share one transaction?
3. What minimum target-side idempotency/receipt/reconciliation contract supports AB09 and AB12 without falsely treating a missing file or receipt as no effect?
4. Which proposed observation would falsify this architecture, including the distinct-intent positive control?

**STOP/NO-GO:** no credible trustworthy claim/action binding; no independently accountable approval; no durable uniqueness; no enforceable revocation; no target idempotency/reconciliation; incomplete evidence framed as confirmed outcome; or common administration misrepresented as independent custody.

**Next decision:** obtain critical review, then freeze one preregistered test contract and oracles. Only if a harmless isolated target and credible authority/receipt boundaries become available should a narrow **LAB_ONLY** test be considered. No CFC modification, service start, ACL change or `APPROVAL_HOLD` removal is authorized by this draft.

`279AU DRAFT | A/B/C OPEN | AB09–AB14 NOT RUN | E2E 0/6 | M6 HOLD`
