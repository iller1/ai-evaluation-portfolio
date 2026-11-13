# M6 — wprowadzenie dla polskiego czytelnika (14 listopada 2026)

**Start przeglądu po angielsku:** [REVIEW_START_HERE.md](REVIEW_START_HERE.md)  
**Dane kontrolne:** [PUBLIC_EVIDENCE_STEP278.json](PUBLIC_EVIDENCE_STEP278.json)  
**Bezpieczny, tylko odczytujący weryfikator:** [verify_step278.py](verify_step278.py)

## Po co to badanie?

M6 bada granicę pomiędzy **oceną uzasadnienia wniosku** a **niezależnym uprawnieniem do konkretnego działania**. Prawidłowy podpis żądania nie zastępuje odrębnej zgody na wykonanie operacji. CFC pozostaje zamrożone i nie jest przedstawiane jako gotowy moduł udzielający autoryzacji.

## Co obecnie mamy?

- Prywatne archiwum Kroku 278A zostało udostępnione do wtórnego przeliczenia hashy: **5/5 wpisów ZIP zgodnych z indeksowanymi hashami**, a cztery pliki wymienione w manifeście mają zgodne SHA-256. To dowód integralności *otrzymanych bajtów*, nie niezależnego pochodzenia.
- Według lokalnego `evidence.json` kompilacja zakończyła się kodem `0`, a test negatywny zwrócił `DENY_WRONG_PROCESS_IDENTITY`. Testu pozytywnego i ścieżki niezależnej akceptacji nie uruchomiono.
- Pokazany osobno fragment źródła zawiera bezwarunkowy `return "DENY_INDEPENDENT_APPROVAL_NOT_IMPLEMENTED";`, wyjaśniający nieosiągalny fragment kodu zgłoszony jako `CS0162`. Pełne źródła nie są obecnie publiczne.
- Przebudowana DLL **nie jest bajtowo identyczna** z historyczną DLL; przyczyna różnicy wymaga osobnego wyjaśnienia.
- **E2E 0/6** to **sześć otwartych bramek**, a nie sześć nieudanych testów lub sześć zaliczeń.

## Co sprawdzi zewnętrzny specjalista?

Może zweryfikować strukturę opublikowanego indeksu i podważyć logikę wniosków; jeśli otrzyma oryginalny ZIP w uzgodnionym, bezpiecznym trybie, może także sam przeliczyć jego SHA-256 bez uruchamiania DLL. Nie może obecnie potwierdzić pełnej niezależnej autoryzacji ani wykonania E2E.

**Prosimy szczególnie o:** kontrprzykład, rozbieżność między twierdzeniem a dowodem, sposób obejścia granicy wykonawcy, minimalny projekt niezależnej akceptacji oraz ocenę sześciu wymaganych testów.

**Status:** `CFC FROZEN | M6 HOLD | E2E 0/6`. Żadnej aktywacji systemu.


## Dodatkowy plan przeglądu — wiązanie działania i czas

**[Plan techniczny EN: ACTION_BINDING_AND_TIMING_REVIEW_PLAN.md](ACTION_BINDING_AND_TIMING_REVIEW_PLAN.md)**

W historycznym przypadku `M6-02` żądano `claim:c2`, lecz callback oceniał `c1`. Warstwa integracyjna zwróciła `ALLOW`, ale **nie wykonano działania**. Problemem jest wiarygodne powiązanie żądania z rzeczywiście ocenionym obiektem i dowodami, **nie** udowodniony błąd zamrożonego Anchor.

Nowe scenariusze `AB01–AB08` sprawdzą kiedyś zgodność obiektu, autentyczność źródła powiązania, cofnięcie zgody, replay, zmianę stanu, utratę łączności i ryzyko fałszywych STOP. **Żaden z tych testów nie został wykonany.** Etykiety `AB` celowo nie pokrywają się z sześcioma historycznymi bramkami E2E.

**`T-M6: DESIGN_OPEN / MEASUREMENT_NOT_RUN`** to osobna przyszła kontrola czasowa: czas decyzji, czas od decyzji do dowodu wyniku od executora, czas propagacji revocation **oraz osobno** skuteczność blokady przy wykonaniu, TTL/expiry i wpływ opóźnień/zegarów. Nie ustalono arbitralnego bezpiecznego progu. Najpierw trzeba uzgodnić ryzyko, pomiar, dopuszczalny margines i zamrożone kryteria.

Zapis z kontrolowanego laboratorium (`LAB_TARGET_RECEIPT`) nie jest tym samym co dowód z niezależnie zarządzanego systemu (`INDEPENDENT_TARGET_RECEIPT`).

**Status bez zmian:** `CFC FROZEN | M6 HOLD | E2E 0/6`. To **plan przeglądu**, nie nowe PASS ani prerejestracja wykonanego badania.
