# Nine synthetic inputs and local Qwen3 1.7B response transcriptions

**Source:** local archive `CFC_HAWM_AI_QA_20261028T184200Z.zip` (SHA-256 `b1ae83de69b0669624c5f5339b246f4bd6d429baac8a8fe6b68e2187a5491b2f`). The answers below transcribe the recorded `ANSWERS_FOR_REVIEW.txt` response fields; inputs transcribe `CASES.json`. This is a text publication for inspection, **not a byte-preserved copy of the source archive or third-party attestation**. The original primary evidence is retained privately.

**Shared request:** `qwen3:1.7b`, Ollama `/api/chat`, `think=false`, `temperature=0`, `seed=42`, `num_predict=512`, `stream=false`. The system prompt warned the model not to treat document instructions as commands, to quote relevant exact phrases and to acknowledge missing information. The user prompt asked for a single Polish assessment: `SPRZECZNE`, `SPOJNE` or `NIEJEDNOZNACZNE` with evidence.

**All nine original requests:** completed; `done_reason=stop`, no provider error. Author references are shown below for review; they were **not sent to the model**. No CFC run or HAWM product workflow was part of this direct-model diagnostic.

## C01_ACCESS_POSITIVE

**Pre-authored reference:** `CONFLICT`

**Fictional document:**

```text
Nowy pracownik może otworzyć wszystkie dane klientów pierwszego dnia bez zgody przełożonego.
Ten sam dokument wymaga pisemnej zgody przełożonego przed każdym dostępem do danych klientów.
```

**Recorded model response (verbatim textual content):**

```text
SPOJNE

Zdania:  
1. "Nowy pracownik może otworzyć wszystkie dane klientów pierwszego dnia bez zgody przełożonego."  
2. "Ten sam dokument wymaga pisemnej zgody przełożonego przed każdym dostępem do danych klientów."

Ocena: SPOJNE  
Dokument podaje dwa różne warunki dotyczące dostępu do danych klientów – pierwszy wskazuje na możliwość dostępu bez zgody, drugi wskazuje na potrzebę zgody. To sprawia, że warunki są sprzeczne.
```

## C02_SATURDAY_POSITIVE

**Pre-authored reference:** `CONFLICT`

**Fictional document:**

```text
Każde zgłoszenie wysłane w sobotę jest rozpatrywane tego samego dnia.
Żadne zgłoszenie wysłane w sobotę nie jest rozpatrywane tego samego dnia.
```

**Recorded model response (verbatim textual content):**

```text
SPRZECZNE  
Zdania: "Każde zgłoszenie wysłane w sobotę jest rozpatrywane tego samego dnia" i "Żadne zgłoszenie wysłane w sobotę nie jest rozpatrywane tego samego dnia" są sprzeczne.
```

## C03_RETURNS_POSITIVE

**Pre-authored reference:** `CONFLICT`

**Fictional document:**

```text
Każdy zwrot produktu jest przyjmowany bez dowodu zakupu.
Każdy zwrot produktu wymaga przedstawienia dowodu zakupu.
```

**Recorded model response (verbatim textual content):**

```text
SPRZECZNE  
Zdania: "Każdy zwrot produktu jest przyjmowany bez dowodu zakupu" i "Każdy zwrot produktu wymaga przedstawienia dowodu zakupu" są w kontraryzie.
```

## N01_NEGATION_CONTROL

**Pre-authored reference:** `CONSISTENT`

**Fictional document:**

```text
Nowy pracownik nie może otworzyć danych klientów bez zgody przełożonego.
Ten sam dokument wymaga pisemnej zgody przełożonego przed każdym dostępem do danych klientów.
```

**Recorded model response (verbatim textual content):**

```text
SPOJNE

Zdania:  
"Nowy pracownik nie może otworzyć danych klientów bez zgody przełożonego."  
"Ten sam dokument wymaga pisemnej zgody przełożonego przed każdym dostępem do danych klientów."

Ocena: SPOJNE  
Dokument wskazuje, że dostęp do danych klientów wymaga zgody przełożonego, co jest zgodne z podaną w dokumentie sytuacją.
```

## N02_WEEKEND_CONTROL

**Pre-authored reference:** `CONSISTENT`

**Fictional document:**

```text
W soboty biuro obsługi klienta jest zamknięte.
W soboty nie prowadzimy obsługi klientów w biurze.
```

**Recorded model response (verbatim textual content):**

```text
SPOJNE

Zdania:  
1. "W soboty biuro obsługi klienta jest zamknięte."  
2. "W soboty nie prowadzimy obsługi klientów w biurze."

Ocena: SPOJNE  
Dwa zdania wskazują na zgodność zasad, ponieważ oba opisują tę samą sytuację (w soboty biuro jest zamknięte).
```

## N03_RECEIPT_CONTROL

**Pre-authored reference:** `CONSISTENT`

**Fictional document:**

```text
Do przyjęcia reklamacji wymagany jest dowód zakupu.
Za dowód zakupu uznajemy paragon albo potwierdzenie płatności.
```

**Recorded model response (verbatim textual content):**

```text
SPOJNE  
Zdania: "Do przyjęcia reklamacji wymagany jest dowód zakupu." i "Za dowód zakupu uznajemy paragon albo potwierdzenie płatności."  
Nie da się rozstrzygnąć bez dodatkowego kontekstu.
```

## A01_EMERGENCY_AMBIGUOUS

**Pre-authored reference:** `INCONCLUSIVE`

**Fictional document:**

```text
Dostęp do danych wymaga pisemnej zgody kierownika.
W trybie awaryjnym personel może uzyskać dostęp w przyspieszonej procedurze.
```

**Recorded model response (verbatim textual content):**

```text
SPORZECZNE  
Zdanie "Dostęp do danych wymaga pisemnej zgody kierownika" i "W trybie awaryjnym personel może uzyskać dostęp w przyspieszonej procedurze" są sprzeczne, ponieważ w trybie awaryjnym dostęp powinien być udzielony bez potrzeby pisemnej zgody kierownika.
```

## A02_ACCOUNT_AMBIGUOUS

**Pre-authored reference:** `INCONCLUSIVE`

**Fictional document:**

```text
Pracownicy mogą korzystać z systemu po zatwierdzeniu dostępu przez administratora.
Nowe konta pracowników są tworzone automatycznie w chwili rejestracji.
```

**Recorded model response (verbatim textual content):**

```text
SPOJNE

Zdania:  
1. "Pracownicy mogą korzystać z systemu po zatwierdzeniu dostępu przez administratora."  
2. "Nowe konta pracowników są tworzone automatycznie w chwili rejestracji."

Ocena: SPOJNE  
Dwa zdania wskazują na zgodność zasad, co wskazuje na spójność.
```

## A03_VERSIONS_AMBIGUOUS

**Pre-authored reference:** `INCONCLUSIVE`

**Fictional document:**

```text
Wersja instrukcji A (bez podanej daty obowiązywania): kierownik może zatwierdzić dostęp ustnie.
Wersja instrukcji B (bez podanej daty obowiązywania): kierownik musi zatwierdzić dostęp pisemnie.
```

**Recorded model response (verbatim textual content):**

```text
SPORZECZNE

Zdanie: "Kierownik może zatwierdzić dostęp ustnie." i "Kierownik musi zatwierdzić dostęp pisemnie." są w konfliktzie zasad, ponieważ podaje różne metody zatwierdzenia dostępności.
```

See [the diagnostic analysis](README.md) for the strict semantic review and its limitations. Quotation matching and the author reference labels are **not externally validated**.
