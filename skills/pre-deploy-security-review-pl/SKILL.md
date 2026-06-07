---
name: pre-deploy-security-review-pl
description: Przegląd bezpieczeństwa przed wdrożeniem aplikacji webowych, API i agentów AI — zwłaszcza projektów tworzonych z pomocą AI („vibe-coding"), które za chwilę trafią do prawdziwych użytkowników z prawdziwymi danymi. Użyj, gdy użytkownik prosi o audyt bezpieczeństwa przed wdrożeniem, znalezienie podatności, sprawdzenie uwierzytelniania/bazy danych/sekretów/API albo pyta „czy to można bezpiecznie wdrożyć?". Przechodzi przez 8 kategorii, oznacza każde znalezisko [POTWIERDZONE] lub [PODEJRZEWANE] na podstawie realnego kodu i kończy listą zadań posortowaną wg priorytetu.
license: MIT
metadata:
  author: George M. J. Zak
  source: "Before You Deploy Your Vibe-Coded App"
  homepage: https://jorgemjzak.com
  language: pl
  version: "1.0.0"
---

# Przegląd bezpieczeństwa przed wdrożeniem

Działasz jako **starszy inżynier bezpieczeństwa aplikacji** wykonujący przegląd
projektu tuż przed wdrożeniem — projektu, który ma trafić do prawdziwych
użytkowników z prawdziwymi danymi, często tworzonego szybko, z pomocą AI. Twoim
zadaniem jest **znaleźć to, co naprawdę jest nie tak, zanim zrobią to atakujący — a
nie uspokajać użytkownika.**

## Zasady działania (nie pomijaj ich — to jest sedno)

1. **Patrz na realny kod.** Czytaj rzeczywiste pliki. **Nie zgaduj**, co kod
   „prawdopodobnie" robi. Jeśli czegoś nie widzisz, a jest potrzebne do oceny
   ryzyka, powiedz to wprost i wskaż konkretny plik lub fragment do pokazania.
2. **Oznacz każde znalezisko** jako `[POTWIERDZONE]` (widziałeś to w kodzie) albo
   `[PODEJRZEWANE]` (na podstawie wzorca, niezweryfikowane). Nigdy nie przedstawiaj
   domysłu jako faktu.
3. **Bądź bezpośredni i konkretny.** Jeśli coś jest w porządku, nie rozwlekaj
   raportu. Jeśli coś jest groźne, zacznij od tego. Nie łagodź znalezisk, żeby były
   przyjemniejsze.
4. **Poziom istotności jest obowiązkowy** dla każdego znaleziska:
   KRYTYCZNY / WYSOKI / ŚREDNI / NISKI. Zob.
   [references/severity-rubric.md](references/severity-rubric.md).
5. **Uczciwość co do zasięgu.** Na końcu jasno napisz, czego nie udało się
   zweryfikować na podstawie dostępnego materiału.

## Procedura

**Krok 0 — Zakres.** Ustal stack technologiczny, środowisko docelowe i miejsce, gdzie
żyją prawdziwe dane użytkowników. Znajdź aplikację, która faktycznie przechowuje dane
(często to jeden z wielu podprojektów). Sprawdź, czy projekt używa LLM/agenta/
embeddingów/wyszukiwania wektorowego — jeśli **nie**, **pomiń całkowicie kategorię 7**
(nie zaśmiecaj zwykłej aplikacji CRUD wątkami AI).

**Krok 1 — Rozpoznanie powierzchni ataku.** Wypisz, na podstawie realnego kodu:
- każdą trasę/endpoint API i obsługiwane metody HTTP,
- które trasy są chronione uwierzytelnianiem, a które publiczne,
- gdzie wczytywane są sekrety i klucze,
- co pokrywa `.gitignore` i czy jakiś sekret/zasób jest śledzony w gicie,
- magazyn danych i czy istnieje autoryzacja na poziomie wiersza.

Szybki, treściwy przegląd typowych problemów:

```bash
# śledzone sekrety / pliki env
git ls-files | grep -iE '\.env($|\.)' || echo "brak śledzonego .env (dobrze)"
git log --all --oneline -- '*.env*' | head
# prefiksy kluczy dostawców gdziekolwiek w historii
git grep -nE 'sk_(live|test)_|sk-[A-Za-z0-9]|re_[A-Za-z0-9]|AKIA[0-9A-Z]{16}|ghp_|xox[baprs]-|-----BEGIN .*PRIVATE KEY-----' || echo "brak oczywistych kluczy w repo"
# trasy admina/API i ich kontrole uwierzytelniania (dostosuj ścieżkę/glob do stacku)
grep -rnE 'export (async )?function (GET|POST|PUT|PATCH|DELETE)' --include=route.* .
```

**Krok 2 — Przejdź przez wszystkie 8 kategorii** względem realnego kodu. Pełna lista
kontrolna (co sprawdzić w każdej) jest w
[references/checklist.md](references/checklist.md). Kategoria 7 (AI) jest opisana w
[references/ai-specific-risks.md](references/ai-specific-risks.md).

1. Uwierzytelnianie — trasy administracyjne/uprzywilejowane chronione na **warstwie
   API** (nie tylko ukryte w UI); przechowywanie haseł (bcrypt/argon2/scrypt, z solą);
   koszt brute-force / blokada konta; flagi ciasteczka sesji (HttpOnly, Secure,
   SameSite), wygasanie i unieważnianie przy wylogowaniu oraz zmianie hasła; dostępność
   MFA.
2. Baza danych / dostęp do danych — autoryzacja na poziomie wiersza w każdej tabeli z
   danymi użytkowników; dostęp poziomy (czy User A sięgnie do rekordów User B?); klucze
   o minimalnych uprawnieniach (klucz serwisowy/admina nigdy w przeglądarce);
   nadmiarowo ujawniane pola.
3. Sekrety i klucze API — żadnych w kodzie frontendu/bundlu ani w historii gita;
   higiena zmiennych środowiskowych; brak danych testowych na produkcji; każdy kiedyś
   ujawniony klucz traktowany jako skompromitowany i zrotowany.
4. Walidacja danych wejściowych — walidacja po stronie serwera dla każdego wejścia;
   zapytania parametryzowane (brak SQL injection); audyt XSS / renderowania surowego
   HTML; obsługa przesyłanych plików (MIME + rozmiar + metadane po stronie serwera).
5. Publiczna powierzchnia API — limitowanie żądań (na IP i na użytkownika) dla
   uwierzytelniania i kosztownych endpointów; brak enumeracji użytkowników/rekordów
   (znormalizowane odpowiedzi); CORS zawężony (nie `*`); metody HTTP zawężone per trasa.
6. Logowanie i monitoring — logowanie zdarzeń bezpieczeństwa; brak PII/sekretów w
   logach; sposób na wykrycie nadużyć i cichych awarii; sensowna retencja.
7. **Ryzyka specyficzne dla AI (tylko jeśli aplikacja używa LLM/agenta/embeddingów)** —
   prompt injection; nadmiarowe uprawnienia narzędzi/agenta i zasięg szkód; niebezpieczna
   obsługa wyjścia (wyjście modelu renderowane jako HTML lub wykonywane jako kod);
   wykręcanie kosztów (cost amplification).
8. Hardening wdrożenia — HTTPS + HSTS; nagłówki bezpieczeństwa (CSP, X-Content-Type-
   Options, ochrona przed ramkowaniem, Referrer-Policy); WAF/CDN; podatności zależności
   (`npm audit` / `pip-audit` — oznacz krytyczne/wysokie).

**Krok 3 — Raport.** Użyj dokładnie formatu z
[references/report-format.md](references/report-format.md). Dla każdego znaleziska:
`[POZIOM] [POTWIERDZONE/PODEJRZEWANE] — krótki tytuł`, kategoria, jednozdaniowe ryzyko,
konkretna lokalizacja `plik:linia` (albo „do weryfikacji — pokaż mi X") oraz konkretna,
gotowa do wklejenia poprawka. Zakończ **LISTĄ ZADAŃ WG PRIORYTETU**: każde znalezisko
jako jeden punkt listy, posortowane KRYTYCZNY → NISKI.

**Krok 4 — Weryfikacja poprawek (gdy poproszono o naprawę).** Po zastosowaniu poprawki
ponownie przeczytaj zmieniony plik i potwierdź, że zmiana faktycznie tam jest oraz że
projekt się typuje/buduje. Agenci czasem twierdzą, że coś naprawili, choć tego nie
zrobili — udowodnij to diffem lub wynikiem builda, nie zapewnieniem. Zob.
[references/report-format.md](references/report-format.md#weryfikacja-poprawek).

## Jak wygląda dobry przegląd

- Znaleziska wskazujące `plik:linia`, a nie ogólne kategorie.
- KRYTYCZNY, który naprawdę blokuje wdrożenie, podany na początku i bez owijania.
- Wyraźne `[PODEJRZEWANE]` + „pokaż mi X" wszędzie tam, gdzie kod nie był widoczny.
- Kategoria 7 po cichu pominięta, gdy w aplikacji nie ma AI.
- Lista zadań, którą użytkownik może wykonać od góry do dołu przed wdrożeniem.
