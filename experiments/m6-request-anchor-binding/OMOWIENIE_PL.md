# M6 — omówienie audytu (25 października 2026)

**Ocena dowodów:** `PASS_WITH_SCOPE_LIMITATIONS`.  
**Wynik eksperymentu:** `CALLER_BINDING_BOUNDARY_OBSERVED`.

### Co zaobserwowaliśmy?

W M6-02 żądanie dotyczyło `claim:c2`, ale funkcja przekazana do integracji oceniałą w frozen Anchor twierdzenie `c1`. Mimo tego `PilotService` zwrócił `ALLOW / ANCHOR`, a pole `final_action_authorized` miało wartość `true`.

Kontrole zachowały się zgodnie z protokołem: prawidłowo powiązane `c1 → c1` otrzymało `ALLOW`, a nieznany status odwołania zatrzymał wywołanie callbacka (`STOP / HOST_POLICY`, 0 wywołań callbacka).

**Wniosek:** integracja v0.5.0 nie zapewnia w tym kontrakcie niezależnie sprawdzalnego związania tożsamości żądania z twierdzeniem ocenionym przez przekazany callback. To granica odpowiedzialności integracji i aplikacji wywołującej, **nie udowodniony błąd oceny frozen Anchor** i nie przykład rzeczywistego wykonania nieuprawnionej operacji.

### Co zweryfikowano?

- Oryginalne archiwum integracji: SHA-256 zgodny z protokołem.
- ZIP M6: poprawne CRC, 15 plików, w tym manifest.
- Manifest: 14/14 hashy zgodnych.
- Odciski trzech żądań oraz trzech odpowiedzi (`audit_digest`): przeliczone i zgodne.
- `final_action_authorized`: w M6-01 i M6-02 `true`; w M6-03 `false`.
- Zamrożony protokół i dołączona prerejestracja są zgodne semantycznie, choć nie identyczne bajtowo; pole `preregistration_sha256` wskazuje na hash pliku `PROTOCOL_FROZEN.json`.

### Istotne ograniczenia

W paczce nie ma pełnego surowego JSON Anchor ani samego pliku wheel, więc nie mogliśmy ponownie policzyć hashy tych danych. Dla M6-03 liczba wywołań callbacka wyniosła zero, **ale** skrypt wcześniej oceniał Anchor, przygotowując stan testowy. Nie wolno więc twierdzić, że w całym przebiegu M6-03 nigdy nie uruchomiono Anchor.

To badanie jest syntetyczne, wewnętrzne, bez niezależnego eksperta, modelowego A/B, HAWM i wykonania działania zewnętrznego.

### Decyzja

**Zamknąć M6 jako obserwację granicy kontraktu.** Nie modyfikować frozen CFC. Następnym uzasadnionym krokiem jest omówienie kontraktu i bezpiecznego wiązania tożsamości żądania z dowodami ocenianymi przez Anchor. Nie powtarzać już tego samego syntetycznego testu.