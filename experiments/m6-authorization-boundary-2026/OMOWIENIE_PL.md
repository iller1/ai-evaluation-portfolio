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
