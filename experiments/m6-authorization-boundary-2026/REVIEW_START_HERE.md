# M6 — Independent reviewer entry point (Step 277/278 snapshot)

**14 November 2026 · two-laptop local experiment · public challenge packet v1**

**Decision:** `GO_FOR_INDEPENDENT_DESIGN_AND_EVIDENCE_REVIEW` · `NO_GO_FOR_ACTION_ACTIVATION`  
**Frozen state:** `CFC FROZEN | M6 HOLD | E2E 0/6`

> **What you can do today:** inspect specific claims, inspect a privacy-minimized evidence index, verify its internal structure, and try to falsify the architecture or interpretation. **What you cannot do from this public repository:** independently replay the original Step 277 Windows execution, compile the withheld original source, establish custody of the operator logs, or demonstrate a working executor boundary.

## Research problem

A justified or CFC-verified conclusion must **not** be mistaken for permission to take an action. M6 asks whether a requester, an independent approving authority, and a restricted executor can enforce *one precisely defined action*, with valid scope, purpose, freshness, anti-replay state, and evidence that the action did or did not occur.

This November 2026 two-laptop **authorization-to-action** lab is distinct from the [October 2026 M6 request-to-Anchor claim-binding diagnostic](../m6-request-anchor-binding/README.md).

## Inspect the actual evidence boundary

| Public item | What it supports | What it does NOT support |
| --- | --- | --- |
| [PUBLIC_EVIDENCE_STEP278.json](PUBLIC_EVIDENCE_STEP278.json) | Review of recorded build state, exact SHA-256 digests, reported negative outcome, hold state and source excerpt | Authenticity of the original run; the raw redacted fields cannot be re-hashed into the private original evidence file |
| [verify_step278.py](verify_step278.py) | Stdlib-only structural checks on public JSON; optionally computes original ZIP/member hashes **if a reviewer separately has the private archive** | Re-execution of DLL, verification of source code behavior, or establishment of independent custody |
| [Original lab overview](README.md) | Earlier scope, architecture, private Step 439/448 references, and six mandatory E2E gates | Closed E2E gates |
| [Open review discussion](https://github.com/iller1/ai-evaluation-portfolio/issues) | Route to raise counterexamples or evidence questions | Any claim that an external review has already occurred |

The private, operator-origin Step 278A ZIP was provided to an assistant for secondary byte-level checking. SHA-256 was recalculated against the received ZIP and its entries; the reported ZIP digest is:

`E90D48D9F307FEC0D7025924EF97993D3DAB01BF4EA75433719A71ED022D58CE`

Its five files were present. The four payload hashes agreed with `SHA256SUMS.txt`; the manifest file itself was additionally hashed. **This does not establish who originally generated the evidence.** Full private `evidence.json` includes workstation, account/SID and absolute paths, so neither that raw file nor the DLL/ZIP is published in this packet.

### Step 277: bounded observations

- **Operator-recorded:** C# compilation completed with exit code `0`, a `CS0162` warning at source line 145, a DLL hash of `8A00AB6BBCFEC6EAE01206DA144F00B40DB829265D78DD05F197BBA4C618CAF7`.
- **Operator-recorded:** negative case `263A_REBUILT_WRONG_IDENTITY_ONLY` returned `DENY_WRONG_PROCESS_IDENTITY`. No positive control and no independent approval path were executed.
- **Operator-recorded:** `service_installed_or_started=false`; no executor event was independently inspected here.
- **Comparison:** rebuilt DLL is **not byte-identical** to historical reference; root cause of byte difference not established.
- **Separately displayed source excerpt:** the approval-HOLD candidate contains an unconditional `return "DENY_INDEPENDENT_APPROVAL_NOT_IMPLEMENTED";` before the source's nonce claim path. That explains the nearby `CS0162` warning on **that shown path**, but is not a full source audit or proof about any other process/build.

The complete source files whose hashes appear in the public index were **not provided in this packet** and their hash assertions are operator-origin. The source excerpt is from a later console display, not from within Step 278A ZIP.

## Six mandatory E2E gates — **all open**

| Gate | What a genuine independent test must show | Status |
| --- | --- | --- |
| P01 | Valid independent approval causes **exactly one** intended isolated test event | OPEN |
| B01 | Restricted caller cannot bypass executor or write protected event | OPEN |
| B02 | Missing/bad approval signature yields **zero** events | OPEN |
| B03 | Wrong scope/resource yields **zero** events | OPEN |
| R01 | Reused nonce yields **no second** effect | OPEN |
| F01 | Interrupted commit/recovery yields **no duplicate** effect | OPEN |

`0/6` means **zero gates closed**, not six tests failed and not a passing E2E experiment.

## Independent reviewer path

1. Read [the lab README](README.md) and identify exactly which claim you are challenging.
2. Inspect [the public evidence index](PUBLIC_EVIDENCE_STEP278.json) and run **Python 3.9+**, stdlib only:  
   `python verify_step278.py`  
   Expected: `PUBLIC_RECORD: PASS_WITH_LIMITATIONS`, `PRIVATE_ARCHIVE: NOT_SUPPLIED`, and `E2E: 0/6 OPEN`. This only validates public structure and conservative interpretation.
3. **If privately provided the original ZIP by its owner, and only after an independent source/disclosure review:** run `python verify_step278.py --archive /path/to/private.zip`. This verifies ZIP/member bytes and selected recorded fields **without executing the DLL**. It does not prove the original Windows execution.
4. For a real replication request the minimum missing materials are: full four reviewed C# sources, pinned toolchain/build recipe, isolated test fixtures and accounts, expected outputs, exact nonce/policy/approval contract, event-store inspection method, and custody/attestation method. These are **not** public yet.
5. Comment with a falsifiable finding: **claim → contradictory evidence/counterexample → reproducer or review method → severity → requested evidence**. A technical `NO-GO`, a bypass hypothesis, or a simpler alternative design is explicitly welcome.

## Questions most worth answering

1. Does the design actually separate key custody, approving authority, requester identity, and executor identity, or can one actor impersonate them?
2. What canonical representation must the authority sign, and how does the executor compare the **exact** action, resource, purpose, scope, target, policy version and expiry?
3. Where could time-of-check/time-of-use, replay, concurrency, crash recovery, or account/ACL overlap defeat an otherwise valid signature?
4. How would you prove a real **allow** and **deny** at the *executor boundary*, rather than just observing a simulator or a C# method return?
5. Is the unconditional approval-HOLD return appropriate for the current candidate? Could an older binary or alternate entry point escape it?
6. Is the current evidence sufficient to justify any claim stronger than a **local negative-control report plus a static HOLD excerpt**? If not, what minimum new evidence would change that?

## Citation / disclosure / status

**Refer to this as:** *M6 authorization-boundary laboratory, public reviewer packet (2026-11-14), operator-origin evidence and limited public verification.* Do **not** call it an independently replicated security control or an externally certified M6 implementation.

This is a frozen evidence snapshot. New review findings should be dated and linked; do not rewrite the historical E2E denominator or alter the frozen CFC baseline. The original Step 278A ZIP, DLL, full source and Windows host-specific metadata remain private. Review rights are described in [RIGHTS_AND_REUSE.md](../../RIGHTS_AND_REUSE.md).
