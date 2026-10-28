# Qwen3 1.7B — błędy w analizie spójności dokumentów (9 przypadków)

**Data:** 28 października 2026  
**Status:** zakończony eksperyment diagnostyczny, wewnętrzna ocena z pomocą AI, **bez niezależnego recenzenta**. Nie jest to Raport #2 portfolio ani test pełnej aplikacji CFC × HAWM.

## Co sprawdziliśmy?

Lokalny model `qwen3:1.7b` otrzymał dziewięć **fikcyjnych** dokumentów po polsku. Trzy zawierały sprzeczności, trzy były zgodne, a trzy miały celowo brakujący kontekst. Oczekiwane etykiety zapisano lokalnie przed uruchomieniem. Model nie widział tych etykiet.

**Parametry:** Ollama `/api/chat`, `think=false`, `temperature=0`, `seed=42`, `num_predict=512`, jeden przebieg na dokument.

## Wyniki

| Miernik | Wynik |
|---|---|
| Ukończone odpowiedzi modelu | **9/9** |
| Zgodność początkowej etykiety z kluczem autora | **5/9** |
| Pełna poprawność semantyczna: werdykt + spójne wyjaśnienie + właściwa niepewność | **4/9 PASS, 5/9 FAIL** |
| Rozpoznanie niejednoznaczności | **0/3** |
| Dosłowne pełne cytaty w trzech zadaniach konfliktowych | **2/6** |

**Wykryte typy błędów:** (1) odpowiedź przeczy własnemu uzasadnieniu; (2) model dopowiada warunek, którego nie ma w dokumencie; (3) rozstrzyga mimo brakującego kontekstu; (4) nie cytuje dokładnie całych zdań, np. pomija końcową kropkę.

Najbardziej czytelny przypadek to `C01`: model napisał `SPOJNE`, a później sam opisał, dlaczego zasady są sprzeczne. To przykład niebezpiecznej rozbieżności między etykietą a uzasadnieniem, nawet gdy każde wywołanie technicznie zakończyło się sukcesem.

## Co jest, a czego nie ma w dowodach?

Pełny [raport angielski](README.md) oraz [teksty dziewięciu przypadków i zapisane odpowiedzi](RAW_OBSERVATIONS.md) są publiczne do inspekcji. Oryginalne archiwum ZIP wraz z `RESULTS.json`, sumami SHA-256 żądań i metadanymi Ollama pozostaje poza GitHubem. Dostępne tutaj przepisy tekstowe **nie są niezależnym odtworzeniem oryginalnych wywołań**.

Ocena została wykonana wewnętrznie z pomocą asystenta, a zwłaszcza etykiety trzech niejednoznacznych przykładów wymagają **zewnętrznego przeglądu**. Dziewięć dobranych przykładów nie pozwala oszacować ogólnej skuteczności modelu. Brak testu wielu seedów, promptów i wersji modelu.

**Nie uruchomiono CFC Anchor; nie testowano natywnego HAWM ani interfejsu aplikacji.** Ten eksperyment pokazuje problemy w odpowiedziach modelu, **nie dowodzi**, że CFC × HAWM automatycznie je wykrywa. Granica M6 pozostaje otwarta; produkt nie jest zatwierdzony do publicznego wydania.

## Znaczenie dla portfolio

Pokazujemy projektowanie przypadków testowych, zapis oczekiwań przed testem, oddzielenie transportu od poprawności semantycznej, zachowanie negatywnych wyników i precyzyjne ograniczenie twierdzeń. To materiał do rozmowy z recenzentem, nie certyfikat jakości modelu lub produktu.

**Repozytorium:** [AI Evaluation & Assurance Portfolio](https://github.com/iller1/ai-evaluation-portfolio). Zasady praw i ponownego użycia opisano w [RIGHTS_AND_REUSE.md](../../RIGHTS_AND_REUSE.md).
