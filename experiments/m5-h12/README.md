# M5-H12 portfolio review package

This package records a **completed and internally audited synthetic host-policy A/B pilot** (25 October 2026). It does **not** document a frozen CFC Anchor run, downstream authorization, independent blind evaluation or a production benchmark.

## Files

- `REPORT_EN.md` — publication-ready English audit report.
- `OMOWIENIE_PL.md` — Polish explanation and decision.
- `AUDIT_RECEIPT.json` — machine-readable per-case consistency check and summary.
- `verify_evidence.py` — read-only standalone Python 3 standard-library verifier (distributed in the downloadable review archive; not yet hosted in this repository).
- `FROZEN_CASES_AND_ORACLE.json` — unmodified pre-authored cases and oracle (in downloadable review archive; not yet hosted here).
- `evidence/CFC_M5_H12_EVIDENCE_FOR_REVIEW.zip` — unchanged 14-file evidence bundle from Windows (in downloadable review archive; not yet hosted here).

To verify locally:

```bash
python verify_evidence.py evidence/CFC_M5_H12_EVIDENCE_FOR_REVIEW.zip --frozen-file FROZEN_CASES_AND_ORACLE.json
```

The result should be `PASS_WITH_SCOPE_LIMITATIONS`.

**Archive SHA-256:** `e0fd85dbed3b1b605fc2fecfc1c1c425727b89f6beae102b0254b86b0e38a15c`.

No file in this package proves independent custody or independently re-executes the original CFC Integration Layer. Please retain the English limitations section when sharing the report.
## Current GitHub publication scope

The report, Polish commentary and `AUDIT_RECEIPT.json` are published here. The original 14-file evidence ZIP, frozen case source, and standalone verifier remain in the downloadable research archive and are **not yet available from this repository**. Consequently, GitHub visitors cannot independently run the posted verifier using only this repository. This is a documentation publication, not an independent reproduction or complete evidence release.
