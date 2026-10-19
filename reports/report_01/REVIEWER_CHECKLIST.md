# External review checklist: Report 01

Suggested review time: 15–30 minutes for this public subset.

Please note **exactly** which of the following you did and return PASS / FAIL /
NOT_CHECKED plus any concrete discrepancies:

1. Run the public `recompute_paired_statistics.py` script in an empty directory.
   Does the reported paired 2x2 table, effect, exact McNemar test and bootstrap CI reproduce?
2. Assess whether conclusions avoid claiming prompt equivalence from a nonsignificant test.
3. Identify one meaningful limitation or alternative explanation not adequately addressed in the PDF.
4. If deeper review is needed, request the original evidence archive separately.
   The present package cannot establish fidelity of raw model responses or original sampling.

Do not label your assessment as *independent model validation* unless you have
actually performed the relevant independent work. A public-only statistical
recalculation is narrower than a full reproducibility assessment.
