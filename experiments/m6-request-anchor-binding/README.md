# M6 — Request-to-Anchor Claim Binding

**25 October 2026 · synthetic diagnostic · internally audited**

The frozen CFC Anchor 0.2.90rc1 was used through Integration Layer v0.5.0 in three local tests. In the deliberately mismatched case, a request for `claim:c2` was paired with a callback evaluating `c1`, yet `PilotService` returned `ALLOW` and `final_action_authorized=true`. This is an **integration/caller trust-boundary observation**, not a flaw shown inside the frozen Anchor and not a production exploit.

| Case | Request | Callback claim | Decision/source | `final_action_authorized` |
|---|---|---|---|---|
| M6-01 | `claim:c1` | `c1` | `ALLOW / ANCHOR` | `true` |
| M6-02 | `claim:c2` | `c1` | `ALLOW / ANCHOR` | `true` |
| M6-03 | `claim:c1` | Callback skipped | `STOP / HOST_POLICY` | `false` |

**Read:** [English report](REPORT_EN.md) · [Polish overview](OMOWIENIE_PL.md) · [machine-readable audit](AUDIT_RECEIPT.json) · [proposed binding contract](BOUNDARY_CONTRACT_PROPOSAL_v0.1.md).

**Evidence availability:** the original `CFC_M6_EVIDENCE_FOR_REVIEW.zip` is not hosted in this repository. Its SHA-256 is `c5150f436218534a579e919b1bf2fe8eff0f7448e7ebb7e885a50e5fe666d95a`; the audit receipt describes its 15 members and verification results. Raw frozen Anchor JSON and the wheel bytes were not preserved in that bundle, so a third party **cannot fully reproduce the Anchor execution from this GitHub publication alone**.

**Status:** `M6_CLOSED_CALLER_BINDING_BOUNDARY_OBSERVED`. The contract is **proposal only**. No changes to frozen CFC, no production mitigation claim, and no downstream executor authorization test.
