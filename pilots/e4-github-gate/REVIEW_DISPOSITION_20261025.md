# E4 — external technical feedback: disposition and evidence plan

**2026-10-25 · Review-only addendum · NOT EXECUTED · no new preregistered cases.**

Source: [Mo-eid200 GitHub comment (2026-10-25T01:38:05Z)](https://github.com/iller1/ai-evaluation-portfolio/pull/1#issuecomment-6392031897).

This is **technical feedback on the design**, not an independent execution or certification, and is not acceptance by the commenter to act as the required reviewer B. All three E4 cases remain on HOLD until a distinct, explicitly consenting B is configured in a separate sandbox.

## Disposition — no retroactive editing of outcomes

| Reviewer observation | Disposition | Reason / evidence rule |
|---|---|---|
| Repo owner A attempts approval as a negative control | **DEFER to separately labelled optional control**; do not silently count as G1/G2/G3 | Useful separation check, but requires real sandbox and B; record result separately if ever executed |
| Capture protection configuration by GitHub API, incl. deployment branch policy and allowed dispatch refs | **ACCEPT as additional setup evidence** for any future run | Store raw, dated provider responses before/after each case; absent/conflicting configuration = INCONCLUSIVE/HOLD |
| For G1/G3 record no executed job steps, not simply no log lines | **ACCEPT as stronger supporting evidence** | Use job status/conclusion plus step list from provider; missing records are NOT proof of non-execution |
| If `case_id` label disagrees with actual reviewer action | **ACCEPT: INCONCLUSIVE** | Case labels and run names are requests/metadata, never an authorization source |
| Include a SHA-256 prefix in `run-name` | **DEFER workflow-source change** | Sensible reviewer UX, not needed to establish bound artifact after runner starts; keep frozen workflow unchanged for now |
| For ordering use GitHub approvals and jobs REST provider timestamps, archive raw JSON | **ACCEPT for evidence plan** | Collect approval actor/time and job start/steps; timestamps are observations, not proof of distributed linearizability |
| Describe canonical fixture hash algorithm in prose | **ACCEPT** | UTF-8; `json.dumps(data, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')`; SHA-256 of resulting bytes. Raw file SHA-256 intentionally differs |
| Make original freeze/amendment chronology explicit | **ACCEPT** | See below; no history rewrite or reassignment of version 0.1 |
| Reviewer removal, configuration edits, queued start after approval, and re-run reuse | **OPEN, OUT OF SCOPE**; potential *future* G4 | These are real TOCTOU/authorization questions, but were not preregistered G1–G3 and must not be smuggled into their score |
| `one run per case` is procedural rather than enforced | **ACKNOWLEDGE** | A second run cannot be treated as satisfying original preregistration; report deviations honestly |

## Amendment ledger — exact recorded commits

1. Original preregistration first added in commit [`9afb69f32f90c38f6309f174202c973c9af0b5ca`](https://github.com/iller1/ai-evaluation-portfolio/commit/9afb69f32f90c38f6309f174202c973c9af0b5ca).
2. Initial inactive workflow included in commit [`4eb62435bfc9d636867da8f5ab371418042fcef3`](https://github.com/iller1/ai-evaluation-portfolio/commit/4eb62435bfc9d636867da8f5ab371418042fcef3).
3. Runtime T1 artifact binding correction committed as [`a74025c402668dbd6342a679b4c6047b1b1f8571`](https://github.com/iller1/ai-evaluation-portfolio/commit/a74025c402668dbd6342a679b4c6047b1b1f8571), before a live run. Changed only inactive workflow code: checkout exact `GITHUB_SHA`, validate checked-out HEAD, hash actual committed fixture, compare expected/input, log commit and two digest variants.
4. README explanation committed as [`b631281d98a1f1adb49e53292d47d6462202a2c1`](https://github.com/iller1/ai-evaluation-portfolio/commit/b631281d98a1f1adb49e53292d47d6462202a2c1).
5. This addendum follows Mohamed's review. **No test has been run on GitHub.**

The original `PREREGISTRATION.md` and its G1_WAIT, G2_APPROVE, G3_REJECT criteria are **not modified**. The original preregistration file blob SHA was `d604c51bcc5da5069e3865ff965d11c6b5405e0d`; Git history and this explicit ledger provide a traceable sequence. **A signed or immutable Git tag has not been created. Do not claim one exists.**

## Minimum evidence per future G1/G2/G3

**Preflight:** GitHub owner/repository/branch/commit and action workflow exact content hash; `GET /repos/{owner}/{repo}/environments/{environment_name}` response + captured allowed-ref policy before any dispatch; named, consenting reviewer B distinct from initiator; self-review disabled; bypass rules documented; no tokens or secrets published.

**Per run:** raw JSON/API copies and links for run ID, run attempt, selected ref/sha, deployment review/approval records, job status/started_at/steps/conclusion, reviewer login, and exact `decision_id` and canonical fixture digest. Gather environment settings again after run. Interpret GitHub records, not self-written `runner_started_at_utc`, as primary time evidence.

- **G1_WAIT:** pending required review while B intentionally withholds approval, then canceled. No executed steps in the gated job. Missing evidence => INCONCLUSIVE.
- **G2_APPROVE:** B approves in GitHub provider records before gated job begins. Runtime evidence includes the actual committed fixture hash and `GITHUB_SHA`. If no B consent or actor evidence => NOT_COMPLETED/INCONCLUSIVE as applicable.
- **G3_REJECT:** B rejects in provider records, gated job has zero executed steps. Missing job/steps evidence => INCONCLUSIVE.

**Discrepancy handling:** `case_id` is just a label. Any mismatch between intended case and provider review event => INCONCLUSIVE, not success. No post-result threshold changes, no silent reruns.

## Claim ceiling and decision

**Review feedback RECEIVED; external live-provider gate experiment NOT COMPLETED.** We have an external **technical design review**, not independent replay, and a volunteer to read later results, **not** a consenting B approver. No new PASS claims about epoch-CAS, revocation timing, enterprise IAM, or real T3.

**GO:** preserve evidence clarity and try to obtain B's informed consent for a separate sandbox. **HOLD:** any live dispatch/merge until the preregistered setup conditions actually hold. **STOP:** changes solely intended to increase the local PASS count. Keep frozen CFC Anchor, HAWM, CP-15 and Operator Wrapper unchanged.

Research north star: reduce **false closures** and **unnecessary false blocks** under a clearly scoped decision-evidence contract. E4 supports only a narrow subquestion about provider review gates and must not replace comparative research on that north star.
