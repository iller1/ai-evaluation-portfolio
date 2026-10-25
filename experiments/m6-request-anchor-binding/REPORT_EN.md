# M6 — Request-to-Anchor Claim Binding: A Synthetic Trust-Boundary Diagnostic

**Date:** 25 October 2026  
**Scope:** CFC Integration Layer v0.5.0 with frozen CFC Anchor 0.2.90rc1  
**Evidence assessment:** `PASS_WITH_SCOPE_LIMITATIONS`  
**Recorded experiment verdict:** `CALLER_BINDING_BOUNDARY_OBSERVED`

## Executive finding

In a local, deliberately misbound request, `PilotService` returned `ALLOW`, `source="ANCHOR"`, and `final_action_authorized=true` for `binding.resource_id="claim:c2"`, although its caller-provided Anchor callback evaluated claim `c1`. In a matching positive control, `claim:c1 → c1` also returned `ALLOW`. In a revocation-unknown control, host-policy returned `STOP` and did not invoke the callback.

The observation identifies a **caller-to-integration claim-identity binding boundary**: the v0.5.0 contract accepts an `AnchorProjection` containing `claim_status` and `control_closure` but no independently checkable claim/resource identity. The host-policy's resource matching concerns a host-context/attestation representation constructed from the request; it is not evidence that the callback's evaluated claim is the requested resource.

**This is not a demonstrated fault in the frozen Anchor's own evidence reasoning, not a production exploit, and not proof of an executed downstream action.** The caller deliberately supplied a mismatched callback; the experiment records the integrator's response to that misuse.

## Frozen test design and reference

The protocol (`PROTOCOL_FROZEN.json`) specifies three historical synthetic cases with `as_of=2026-09-03`, a positive frozen Anchor fixture, and predeclared interpretations. The test was authored internally and was **not externally preregistered or independently adjudicated**. The original integration archive's SHA-256, independently recalculated during this post-run review, is:

`93b9380680f67efca72ee579122552b8b3cb8c00617224435b6741b2e74cf2b5`

The runner's recorded frozen-wheel SHA-256 is:

`b3b1f11e060289afa4e7da61072f2c31be7f0da1786be90682ec307d4e1f5303`

Its recorded frozen engine SHA-256 is:

`77a7547c02ce4aac3d3abc759bbd266f4251de9149da2308454527c7f2dea5c0`

The wheel itself was **not included in the submitted review evidence**, so this audit confirms the recorded wheel identity agrees across protocol, setup/install record, and case files; it does not independently re-hash the wheel bytes.

## Observations

| Case | Requested resource | Claim passed to Anchor callback | `PilotService` decision / source | Callback invocations | `final_action_authorized` |
|---|---|---|---|---:|---|
| M6-01, matched positive control | `claim:c1` | `c1` | `ALLOW / ANCHOR` | 1 | `true` |
| M6-02, intentionally mismatched | `claim:c2` | `c1` | `ALLOW / ANCHOR` | 1 | `true` |
| M6-03, revocation unknown | `claim:c1` | No callback invocation | `STOP / HOST_POLICY` | 0 | `false` |

The M6-02 response includes `ANCHOR_VERIFIED_CLOSURE` as its reason code despite the recorded claim/resource mismatch. The M6-03 response includes `REVOCATION_UNKNOWN`. These are wire-response observations, not interpretations of unrecorded external effects.

## Code-path explanation

The post-run reviewer inspected the exact source archive. `PilotService.evaluate(request, anchor_evaluator)` parses the request and passes the parameterless callback to `IntegrationController.evaluate_with_ledger(...)`. `IntegrationController.evaluate()` first calls the host-policy gate. If it allows the request, the controller invokes the callback and returns `ALLOW` when the returned projection satisfies `anchor.control_closure and anchor.claim_status == "VERIFIED"`.

In v0.5.0, `AnchorProjection` has fields `claim_status`, `control_closure`, `stop_type`, and `raw`; there is no required, verified `evaluated_claim_id` or canonical claim/resource binding. `PilotService._response()` sets `final_action_authorized` to whether the integration decision equals `ALLOW`. This means a mismatch can be reflected in the returned authorization-shaped field without a demonstrated downstream action.

The controller also checks for changes in the *local lifecycle ledger commitment* during Anchor evaluation; that is a different invariant from binding the callback's evaluated claim to `request.binding.resource_id`.

## Evidence audit

Source: `CFC_M6_EVIDENCE_FOR_REVIEW.zip` (SHA-256 `c5150f436218534a579e919b1bf2fe8eff0f7448e7ebb7e885a50e5fe666d95a`).

- ZIP CRC/integrity: **PASS**; 15 members (14 items listed in `MANIFEST.json` plus the manifest itself).
- Manifest: **14/14 SHA-256 checks PASS** against the bytes of the archived files.
- Frozen protocol versus run-time `PREREGISTRATION.json`: **semantically equal**, although **not byte-identical**. The `M6_SUMMARY.preregistration_sha256` value refers to `PROTOCOL_FROZEN.json`, not the differently serialized `PREREGISTRATION.json`; this is a naming/serialization ambiguity, not an altered case definition.
- All three `request_fingerprint` values: **PASS** on independent recomputation using the published source's canonical JSON algorithm.
- All three response `audit_digest` values: **PASS** on independent recomputation.
- Requested resource, lifecycle event, callback count, response decision/source, and `final_action_authorized`: **consistent** with the archived protocol and case JSON.
- The source archive v0.5.0 SHA-256 was recomputed directly from the archived original available to the reviewer and matches the protocol.

These checks are an **internal post-run forensic consistency review**, not a second evaluator's independent execution of the frozen wheel.

## Evidence boundaries and limitations

1. The test is constructed to mismatch `claim:c2` and `c1` and therefore diagnoses the integration's **contract boundary**. It does not establish the prevalence of such mismatches in real callers.
2. The callback was caller-supplied; therefore the result does not prove that Anchor incorrectly verified claim `c2`. The Anchor output shown in the test pertains to `c1`.
3. The runner's fixture utility evaluated the real Anchor **during case preparation**, including M6-03. Consequently, `callback_invocations=0` in M6-03 means the `PilotService` callback was not invoked—not that zero Anchor operations occurred anywhere in that subprocess.
4. The case records contain SHA-256 values for raw Anchor JSON, **not the complete raw Anchor JSON**; those particular digests cannot be recomputed from this evidence archive alone.
5. The wheel bytes are not included. `INSTALL_RECORD.json` and setup output document verification, but are not an independently preserved copy of the tested binary.
6. The protocol was authored internally. Its `date_prepared` and checksum do not demonstrate independently witnessed preregistration before test execution.
7. All cases use a synthetic historical fixture and no actual external action, model A/B, HAWM, or independent third-party validation.
8. A true request-bound response requires a **trustworthy identity association**; merely copying the caller's resource string into an output field would not resolve the provenance problem.

## Disposition

**M6 — closed as `CALLER_BINDING_BOUNDARY_OBSERVED`, with bounded evidence.** No modification to frozen CFC Anchor is warranted by this finding. The next justified activity is a **contract/design review** of how an application binds request identity to the evaluated evidence/claim and how that binding can be checked at the integration boundary; it is not to manufacture more synthetic positive tests or to claim a production vulnerability.

An eventual proposed control could require a verifier-derived, auditable mapping of request resource to Anchor claim/evidence provenance before interpreting an Anchor projection as authorizing the specific requested action. This is a design proposal, **not an implemented or tested fix**.