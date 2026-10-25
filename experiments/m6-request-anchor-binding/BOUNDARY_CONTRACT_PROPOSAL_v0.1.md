# M6 — Request-to-Anchor Binding Contract (Design Proposal v0.1)

**Date:** 25 October 2026  
**Status:** `DESIGN_PROPOSAL_NOT_IMPLEMENTED` — not an amendment to, or a fix for, the frozen CFC Anchor 0.2.90rc1.  
**Evidence:** [M6 report](REPORT_EN.md) and [post-run audit receipt](AUDIT_RECEIPT.json).

## Problem and observed boundary

The M6-02 synthetic run intentionally supplied `binding.resource_id="claim:c2"` while the caller-provided Anchor callback evaluated `c1`. Integration Layer v0.5.0 returned `decision=ALLOW`, `source=ANCHOR`, and `final_action_authorized=true`. No downstream action was performed. The result is a **caller/integration boundary observation**, not evidence that Anchor reasoned incorrectly about `c1` or that a production exploit occurred.

The actual v0.5.0 callback type is `Callable[[], AnchorProjection]`. `AnchorProjection` contains `claim_status`, `control_closure`, `stop_type`, and `raw`, but **no required authenticated claim/resource identity**. Host-policy and local lifecycle-ledger checks cannot by themselves prove that the callback evaluated the requested claim.

## Desired invariant

For a particular request `R`, let `r(R)` be its canonical resource identity; let `c(E)` be the claim actually evaluated by the frozen Anchor on evidence snapshot `E`; and let `B` be a **verifier-established**, purpose- and time-scoped mapping from resource identity to claim identity.

The integration **must not represent final authorization as true** unless:

1. The host-policy gate allows the request and its lifecycle checks hold.
2. A *trusted, independently checkable binding source* verifies `B(r(R)) = c(E)` for this exact request/purpose/audience/resource and time scope.
3. The frozen Anchor actually evaluates that bound claim/evidence snapshot and returns its ordinary positive closure result.
4. The identity and evidence snapshot used for the check remain valid through the final decision (and are rechecked/committed transactionally by the downstream executor if an external action is subsequently attempted).

A resource string copied from the request into callback output is **not** a binding proof. Two matching strings are insufficient if they originate solely from the same untrusted caller.

## Proposed minimal application-level envelope (illustrative, not runtime schema)

```json
{
  "request_fingerprint": "<canonical-request-digest>",
  "resource_id": "claim:c1",
  "anchor_claim_id": "c1",
  "evidence_snapshot_digest": "<digest-of-exact-input>",
  "attestation_payload_fingerprint": "<fingerprint>",
  "as_of": "2026-09-03",
  "purpose_id": "<purpose>",
  "audience_id": "<audience>",
  "binding_verifier_id": "<trusted-resolver-identity>",
  "binding_record_digest": "<digest-of-verifiable-mapping-record>",
  "binding_policy_version": "PROPOSAL_ONLY"
}
```

**Trust requirement:** a configured authoritative verifier/resolver must establish these associations from authenticated source records. The caller may submit candidates but must not be able to self-certify `binding_verifier_id`, `anchor_claim_id` or the evidence digest. The integration must check their provenance and validity; merely adding fields does not mitigate M6-02.

## Response behavior (proposed, not observed)

- **Verified exact binding + positive host gate + positive Anchor:** `ALLOW` is *eligible*, subject to downstream authorization and any other required checks.
- **Proven mismatch:** fail closed, e.g. `STOP / REQUEST_ANCHOR_BINDING_MISMATCH`; `final_action_authorized=false`.
- **Binding missing, untrusted, expired or indeterminate:** no final authorization; the policy owner must predeclare `STOP` versus `UNRESOLVED` and reason codes.
- **Binding/provenance/snapshot changes during evaluation:** no final authorization; refresh from the authoritative source and reevaluate instead of silently reusing prior closure.
- **Anchor response concerns a different claim/snapshot:** ignore that closure for this request; preserve audit evidence.

This is a check-to-use risk. A read-time binding check alone does **not** establish a safe atomic downstream action. Executor-side compare-and-commit or an equivalent transaction boundary must be evaluated separately.

## Proposed acceptance criteria before any implementation

Freeze the fixture/oracle **before execution** and obtain independent design criticism. At a minimum:

| Case | Request vs Anchor evidence | Required high-level property |
|---|---|---|
| Matched / authenticated | `c1` ↔ `c1` with verified binding | No new false block attributable to identity mismatch |
| Mismatched | `c2` ↔ `c1` | No final authorization |
| Matching but caller-self-asserted | `c1` ↔ `c1` with no independent binding record | No final authorization |
| Stale/revoked binding | Previously valid mapping no longer current | No final authorization |
| Evidence changed during check | Snapshot `E0` vs `E1` | No action on `E0` closure |
| Missing claim identity in projection | No verifiable statement about evaluated claim | No final authorization |

Log raw request, provenance/binding record, exact snapshot digest, versioned policy, host gate decision, Anchor callback invocation, frozen runtime identity, final decision, and downstream execution outcome **separately**. Redact secrets but retain a verifiable chain of digests.

## Explicit nonclaims and decision gate

This is **not implemented or validated**. It neither changes frozen CFC, nor proves that a future binding check is unbypassable, nor establishes a general improvement in AI decision quality. The M6 evidence is internally authored and audited, without independent execution of the wheel from the preserved evidence bundle.

**Next action:** request one independent design review to challenge the provenance trust root and executor boundary. If no trustworthy binding source can be identified, **STOP implementation** rather than introducing a decorative `evaluated_claim_id` field.
