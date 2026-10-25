# M5-H12 · Synthetic paired host-policy conformance pilot

**Run date:** 25 October 2026 · **Audit:** internal post-run technical consistency · **Outcome:** `PASS_WITH_SCOPE_LIMITATIONS`.

Qwen3 0.6B returned `HOST_ALLOW` for all twelve constructed cases (**6/12 correct; 6 false allows**); the deterministic host-policy v0.5.0 gate matched all twelve pre-authored labels (**12/12; no false allow or false stop**). This is a narrow test of **permission to invoke an Anchor callback**, not final authorization. The frozen CFC Anchor, HAWM, downstream executor, and independent review were **not executed**.

## Repository contents

- [REPORT_EN.md](REPORT_EN.md) — full English methods, case-level results and limitations.
- [OMOWIENIE_PL.md](OMOWIENIE_PL.md) — Polish explanation.
- [AUDIT_RECEIPT.json](AUDIT_RECEIPT.json) — per-case internal consistency report.
- [FROZEN_CASES_AND_ORACLE.json](FROZEN_CASES_AND_ORACLE.json) — original pre-authored case set. SHA-256: `4ad7adf13c6d93543fac09d05221f0737c15810b5d7a77e2044e0f947b35a86a`.
- [evidence/PRIMARY_EVIDENCE_EXPORT.json](evidence/PRIMARY_EVIDENCE_EXPORT.json) — **verbatim UTF-8 contents of all 14 original JSON evidence members** and per-member SHA-256 checksums, as a public text export. This is **not** the original ZIP byte stream.
- [verify_public_export.py](verify_public_export.py) — checks every public member's SHA-256, reconstructs a temporary ZIP for inspection, and recomputes the audit using the accompanying [verify_evidence.py](verify_evidence.py).

## Recompute from public source files

Requires Python 3.9+ and the standard library; no local model or GitHub login is needed.

```bash
python verify_public_export.py evidence/PRIMARY_EVIDENCE_EXPORT.json --frozen-file FROZEN_CASES_AND_ORACLE.json
```

Expected lines include `PUBLIC_EXPORT_AUDIT: PASS_WITH_SCOPE_LIMITATIONS`, `VERBATIM_JSON_MEMBERS: 14`, model A correct = 6, gate B correct = 12 and paired outcomes both_correct = 6, B_only = 6.

**Important boundary:** the original evidence container, `CFC_M5_H12_EVIDENCE_FOR_REVIEW.zip`, has a reported SHA-256 of `e0fd85dbed3b1b605fc2fecfc1c1c425727b89f6beae102b0254b86b0e38a15c`. Its raw binary ZIP bytes are **not hosted** in this repository. The public export independently checks *member contents*, not the original ZIP envelope hash. The original Windows run and v0.5.0 Integration Layer were **not rerun** by the post-run audit; this does not prove independent source custody, external preregistration, or actual frozen CFC execution.

**Research disposition:** M5-H12 closed; do not fold new tests into its 12-case denominator. Any frozen-Anchor identity-binding test is a separate, preregistered study.
