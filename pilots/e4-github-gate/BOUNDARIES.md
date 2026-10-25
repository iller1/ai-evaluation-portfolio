# E4 — what can and cannot be concluded

**STATUS: proposal only; NOT RUN.**

A protected GitHub Actions environment can supply real provider-managed waiting, review and execution records, which are stronger external observations than a synthetic local signer alone.

Nevertheless, a successful G1/G2/G3 **does not** establish:

- atomic authorization-epoch compare-and-swap, or a linearizable policy-revocation-vs-execution order;
- a CP-15-authorized or enterprise-signed T2 receipt;
- real-world authority of the reviewer beyond the configured GitHub reviewer role;
- revocation safety between approval and execution;
- a real T3 effect: the sole execution step prints a NOOP record;
- exactly-once effect guarantees across crashes/retries;
- external certification of CFC, HAWM, or CP-15;
- independence of administrative domains; the repository owner still has authority over settings.

**STOP** if the protected environment lacks a real agreed reviewer, self-review is possible, admin bypass is not addressed, or evidence is incomplete. Do not state PASS from self-authored logs alone.

The workflow is kept outside `.github/workflows/` in this review branch so it does not become active.

**Open next question:** a genuine downstream system that atomically binds policy-epoch validation to accepting a concrete action, with separately evidenced effect at T3. This GitHub pilot is not that system.
