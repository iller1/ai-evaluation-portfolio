# E5 — External GitHub resource-version conditional update: observed result

**Status: CLOSED / PROVIDER-OBSERVED LOCAL-OPERATOR PASS (3/3).**
**Date: 2026-10-25.** Run performed through the connected GitHub account, **without independent reviewer or reproducer**. Pre-registration was committed before running E5-P/E5-S/E5-V.

- [Frozen preregistration](PREREGISTRATION.md)
- [Actual remote controlled resource](controlled_resource.json)
- [Positive update commit](https://github.com/iller1/ai-evaluation-portfolio/commit/347e9ce44da7ca530d0ff7bc9b38926ac2267082)

## Evidence chronology

| Step | Observation | Result |
|---|---|---|
| PRE | Pre-registration commit `4004d126bf41411a62c7210618fdae2373ec9a61` | Recorded before any positive/stale write |
| INIT | Created the synthetic file on isolated branch; original blob SHA `4279da5b4c98b6eee3f1d81f43d7332ddfe41edb` | READY |
| E5-P | Updated file with the original blob SHA | GitHub accepted update; commit `347e9ce44da7ca530d0ff7bc9b38926ac2267082`; current blob SHA `d1ebb92bcd60a17226383ffbc96e1405614f6505` |
| E5-S | Sent a **different** update (`REJECTED_SHOULD_NOT_COMMIT`) using the **old** blob SHA `4279da5b4c98b6eee3f1d81f43d7332ddfe41edb` | GitHub responded **HTTP 409 CONFLICT** with a file/sha mismatch |
| E5-V | Fetched the file again by the isolated branch ref | Observed state `ACCEPTED`; blob SHA remained `d1ebb92bcd60a17226383ffbc96e1405614f6505` |

**Recorded rejection** (diagnostic excerpt; no tokens or secrets):
```
GitHub API error 409:
"experiments/e5/controlled_resource.json does not match
4279da5b4c98b6eee3f1d81f43d7332ddfe41edb"
```

The test used GitHub's `Create or update file contents` endpoint, where the `sha` parameter for an update identifies the file blob being replaced, not the entire repository commit or an authorization policy epoch.

## Claim ceiling

The observations support this narrow claim:

> For this particular remote file and sequential test, GitHub accepted an update conditioned on the then-current **file blob SHA**, rejected a stale-SHA update with a specific 409 mismatch, and exposed the committed `ACCEPTED` state on a subsequent read.

They **do not prove**:

- authorization revocation safety, genuine epoch compare-and-swap, or an atomic check against a separate revocation registry;
- real T2 acceptance by an independent executor or an independently signed acceptance receipt;
- real T3 business execution (the only change was to an inert synthetic file);
- linearizability across arbitrary resources/processes, exactly-once external execution, or independent replication;
- independence of the user's own account from the operator who designed and ran the test.

**ABA caveat:** a Git blob SHA is content-derived. If content changes `A → B → A`, the blob SHA for `A` returns. An old `A` hash is not a monotonic policy revision counter. Thus this GitHub file SHA cannot simply be relabeled as `authorization_epoch`.

## Research decision

**E5 CLOSED / 3 cases observed as preregistered.** Do not repeat just to accumulate pass counts. **HOLD** on claims about a genuine independent external authorization actor and cross-system revocation/execution atomicity. E4 remains a separate draft review proposal; `main`, frozen CFC Anchor 0.2.90rc1, CP-15, HAWM, and Operator Wrapper v1.23 were not changed.
