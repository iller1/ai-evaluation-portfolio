# M6 — Independent research review handoff (279DS)

**Prepared:** 14 November 2026 (UK)  
**Status:** REVIEW-READY RESEARCH NOTE — NOT A PRODUCT, NOT A PASSED E2E ASSESSMENT  
**Control state:** `CFC FROZEN | M6 HOLD | E2E 0/6 | AB09–AB14 NOT RUN | T-M6 NOT RUN`  
**Review only:** this handoff requests critique. It does not amend, activate, or unfreeze an implementation.

## One research question

Can an evidence-supported AI conclusion remain separate from *independently authorized permission to perform a specific action*—with that permission bound to the exact action, current state, and observable target effect?

## What the available evidence supports

1. **Caller / evaluated-claim binding gap (earlier M6-02).** In a deliberately synthetic mismatch, a request for `claim:c2` was paired with a callback evaluating `c1`; the integration returned `ALLOW` and `final_action_authorized=true`. This is an observed caller/integration contract boundary, **not** a defect proven in frozen CFC Anchor, a production exploit, or an executed external action.
2. **Windows HOLD candidate (277/278).** A negative wrong-process-identity outcome was recorded; the approval path remained on HOLD. Neither an independently authorized positive effect nor an E2E gate was demonstrated. Operator-derived source/build/evidence checks do **not** establish independent custody or complete runtime-path coverage.
3. **Gate C v0.2 reference (279DK–279DO).** Original ZIP SHA-256 and four member hashes matched the author's published checksums. One unmodified Windows run (Python 3.14.7, SQLite 3.50.4) yielded **13/14 reported PASS**. GC-5d failed its *both-race-orderings* coverage check: **200 commit-won, 0 fence-won**. The deterministic GC-5a/GC-5b ordering controls passed. No duplicate target effect was reported in GC-5d, but randomized Windows coverage was **not reproduced**. This is a synthetic reference implementation, not the protected M6 executor, a functioning authorization chain, or independent custody.

**Operator-held evidence digests (not independent attestation):**
- Gate C reference ZIP SHA-256: `33ecba1bfac5e7ec995a331f189e01180c68e153f3c0f9fa4b4b397a4a9a937a`
- Windows stdout SHA-256: `68cbba7a21be9d09a8b8dace8cb41b4fbf9bdb71885bde16863bf8997df2661d`
- Exact receipt digest: `19B26ECFDDBE004FE9923FA0CC229FC2BCE33FDEDB6CE56FF6FF6BA4FB844B94`

The reviewer has been asked to classify the GC-5d result and recommend whether further concurrency testing would change any decision; no response has been received as of preparation.

## The three remaining blockers

| Boundary | Minimum necessary evidence | Present status |
|---|---|---|
| A — independent authorization | Authenticated requester, accountable separate authority/key control, durable unique approval per intent under retries and crashes | **OPEN**: no independently approved, enforceable positive path shown |
| B — exact binding and freshness at commit | Trusted binding between request, actually assessed CFC claim/evidence, action digest, scope/purpose/target, policy, expiry/revocation; enforceable ordering at target | **OPEN**: not demonstrated by signed-message or caller-asserted IDs |
| C — target effect/receipt | Atomic target-side effect-or-fence uniqueness, recovery and independently observable positive/negative effects; no unjustified false blocks | **OPEN for M6 integration**: synthetic v0.2 reference only, with one Windows ordering-coverage failure |

**The six historical E2E gates** (`P01`, `B01`, `B02`, `B03`, `R01`, `F01`) are **0/6 closed**, not six failed trials. A lab-only PASS or a return value `DENY` does not close them.

## Focused request for independent reviewer

1. **Trust root:** What minimum *independently checkable* authority and claim/evidence binding could make Gate A/B meaningful without relying on IDs self-attested by the caller or merely sharing administration between two laptops?
2. **Commit/revocation ordering:** Is there a credible minimal executor/target contract for exact-action authorization and revocation cutoff when the authority and target are not in one transaction? If not, should this research branch STOP rather than build decorative controls?
3. **Stop threshold:** Is the current Gate C reference package review adequate to record a bounded result—13/14 on Windows, GC-5d randomized ordering coverage OPEN—or would **one** deterministically scheduled minimal test materially alter the assessment? Please specify a falsifiable oracle before recommending any run.

Please challenge assertions with concrete counterexamples and propose the **smallest** evidence-changing test, if one exists. A justified `NO-GO` is an acceptable outcome.

## GO / NO-GO / STOP disposition

- **GO:** independent critical research review and a bounded evidence report.
- **NO-GO:** enabling approval, changing protected ACLs/services or `APPROVAL_HOLD`, declaring product readiness, or claiming successful integrated enforcement.
- **STOP unnecessary testing:** do not repeat the same 200-trial race or add new test suites unless the specific missing observation could change a stated research or deployment decision.

**Research closure is distinct from product closure.** A limited study may close with unresolved gates and accurately characterized evidence. The M6 authorization product cannot be claimed complete while A/B/C and all six integrated E2E gates remain open.

## Public review sources

- [M6 review entry point](https://github.com/iller1/ai-evaluation-portfolio/blob/main/experiments/m6-authorization-boundary-2026/REVIEW_START_HERE.md)
- [M6 three-gate intent contract — unfrozen design draft](https://github.com/iller1/ai-evaluation-portfolio/blob/main/experiments/m6-authorization-boundary-2026/THREE_GATE_INTENT_CONTRACT_v0.1_DRAFT.md)
- [M6-02 caller/claim binding diagnostic](https://github.com/iller1/ai-evaluation-portfolio/blob/main/experiments/m6-request-anchor-binding/REPORT_EN.md)
- [Issue #3: external Gate C design and review](https://github.com/iller1/ai-evaluation-portfolio/issues/3)
- [Issue #3: our Windows reproduction report](https://github.com/iller1/ai-evaluation-portfolio/issues/3#issuecomment-6884836256)

---

## Podsumowanie dla autora (PL)

**Celem jest ocena badania, nie udawanie gotowego produktu.** Wynik Windows 13/14 pozostaje niezmieniony, GC-5d nie uzyskał obu kolejności wyścigu, nie dowiedziono podwójnego wykonania. A i B nie mają wiarygodnego, wdrożonego źródła autoryzacji/powiązania; C to prototyp syntetyczny, a w prawdziwym M6 nadal jest OPEN. Wszystkie sześć bramek E2E pozostaje otwarte. Nie wykonujemy kolejnych testów bez pytania, którego rozstrzygnięcie zmieni decyzję. Dokument nadaje się do przesłania recenzentowi jako *research handoff*, ale nie zastępuje surowego, niezależnie weryfikowalnego pakietu wykonawczego.
