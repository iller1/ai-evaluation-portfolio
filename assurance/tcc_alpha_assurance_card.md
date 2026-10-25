# Assurance Card — TCC Alpha External Black-Box Case Study

**Date closed:** 25 October 2026  
**Assessor:** Krzysztof Sliwka, authorized external operator with AI-assisted offline checks  
**Assessment status:** CLOSED / CLIENT-SIDE OBSERVATIONS ONLY — NOT EXTERNAL SECURITY CERTIFICATION

## Scope and claims

| Claim | Observed basis | Assessment |
|---|---|---|
| Preflight UI displays expected halt and re-arm sequence | P01–P04 operator observations | **OBSERVED IN SIMULATOR ONLY** |
| Alpha state API rejects use of superseded G0 after G1 commit | One developer-specified 201 / 200 / 201 / 409 / 200 / 422 sequence | **PASS_OBSERVED IN RECORDED SEQUENCE** |
| Dry-run execution consumes current receipt after one successful invocation | Pre-registered T1, repeated same decision/hash; both executions 200 and accepted=true | **FAIL_OBSERVED vs. PRE-TEST EXPECTATION** |
| Uncommitted, correctly computed successor hash is rejected | Pre-registered T2: 422 / unknown_receipt | **PASS_OBSERVED IN RECORDED SEQUENCE** |
| Downstream single-use/idempotency exists and is enforced | No downstream executor test; owner subsequently said it is not implemented in Alpha | **NOT ESTABLISHED; OWNER-REPORTED UNIMPLEMENTED** |
| System is secure or production ready | No production executor access, server logs, concurrency test, signed response or independent custody | **NOT ESTABLISHED** |

## Interpretive note on T1

The original negative result is frozen and should not be rewritten. The developer acknowledged a mismatch between an earlier statement and the dry-run behavior, and later corrected their own description: downstream single-use enforcement remained unimplemented and unverified in this Alpha. This disclosure narrows what can reasonably be inferred from T1; it does **not** turn a dry-run mismatch into proof of a downstream exploit or erase the original test outcome.

## Evidence and independence limits

- Records are **client-captured JSON** with locally recomputed hashes; historical UI images are observational, not server attestations.
- 36/36 and 26/26 consistency checks and 8/8 detected mutations describe **internal** evidence checking; they are not an independent third-party audit.
- The first G0/G1 sequence was developer-specified. T1/T2 were prospectively frozen and executed once each.
- Private source artifacts were supplied in the final PDF dossier to the project owner. They are not redistributed in this public repository.
- No general security claims follow from these limited API tests.

## Decision

Preserve both unfavorable and favorable results, keep the simulator, state API and downstream executor distinct, and **stop at the authorized evaluation boundary**.

[Full public case-study summary](../case-studies/tcc-alpha-2026/README.md)
