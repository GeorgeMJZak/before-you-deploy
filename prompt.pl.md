# Prompt do wklejenia

Nie masz systemu skilli? Wklej to wprost do dowolnego asystenta AI, który widzi twój
kod. To ręczna forma skilla `pre-deploy-security-review` — ten sam przegląd, bez
instalacji.

> Gwarancje uczciwości to sedno. `[POTWIERDZONE]`/`[PODEJRZEWANE]`, „powiedz, który
> plik pokazać" i „nie łagodź znalezisk" to to, co powstrzymuje gorliwą AI od
> przyklepania twojej aplikacji. Po pierwszym przejściu dopytuj: *„pokaż mi dokładną
> zmianę w kodzie dla znaleziska nr 2"* — a potem zweryfikuj, że poprawka faktycznie
> weszła. AI czasem twierdzi, że coś naprawiła, choć tego nie zrobiła. Sekcja o AI sama
> się pomija, jeśli w aplikacji nie ma LLM-a.

---

```
Działaj jako starszy inżynier bezpieczeństwa aplikacji wykonujący przegląd tej
aplikacji przed wdrożeniem. Ma ona za chwilę trafić do prawdziwych użytkowników z
prawdziwymi danymi i prawdopodobnie powstała szybko, z pomocą AI. Znajdź to, co
naprawdę jest nie tak, zanim zrobią to atakujący — nie uspokajaj mnie.

Jak pracować:
- Patrz na realny kod, do którego masz dostęp. NIE zgaduj, co kod prawdopodobnie robi.
  Jeśli czegoś nie widzisz, a jest potrzebne do oceny ryzyka, powiedz to wprost i
  wskaż, który plik lub fragment ci pokazać.
- Oznacz każde znalezisko jako [POTWIERDZONE] (widzisz to w kodzie) albo [PODEJRZEWANE]
  (prawdopodobne na podstawie wzorca, ale niezweryfikowane). Nigdy nie przedstawiaj
  domysłu jako faktu.
- Bądź konkretny i bezpośredni. Jeśli coś jest w porządku, nie rozwlekaj raportu. Jeśli
  coś jest groźne, zacznij od tego.

Poziomy istotności:
- KRYTYCZNY — nie wdrażaj, dopóki nie naprawione. Ujawnienie danych, obejście
  uwierzytelniania, przejęcie konta.
- WYSOKI — napraw w tym tygodniu. Do wykorzystania, ale wymaga warunku lub wysiłku.
- ŚREDNI — napraw w tym miesiącu. Realna słabość o ograniczonym zasięgu.
- NISKI — śledź i wróć później. Hardening i higiena.

Przejdź przez wszystkie kategorie:
1. Uwierzytelnianie — trasy administracyjne/uprzywilejowane chronione na warstwie API
   (nie tylko ukryte w UI); przechowywanie haseł (bcrypt/argon2/scrypt, z solą);
   blokada konta / koszt brute-force; weryfikacja e-mail; MFA; tokeny sesji (HttpOnly,
   Secure, SameSite, sensowne wygasanie, unieważnianie przy wylogowaniu i zmianie hasła).
2. Baza danych / dostęp do danych — autoryzacja na poziomie wiersza (RLS lub
   odpowiednik) w każdej tabeli z danymi użytkowników, zwłaszcza gdy klucz anon/kliencki
   trafia do przeglądarki; dostęp poziomy (czy User A czyta/modyfikuje rekordy User B?);
   role o minimalnych uprawnieniach (klucze serwisowe/admina nigdy w przeglądarce); pola
   ujawniane nadmiarowo.
3. Sekrety i klucze API — jakikolwiek klucz/sekret w kodzie frontendu/bundlu lub
   commitowany do gita (szukaj sk_, sk-, re_, AKIA itd.); sekrety w zmiennych
   środowiskowych, .env w .gitignore; brak danych testowych na produkcji; każdy kiedyś
   ujawniony klucz traktowany jako skompromitowany i zrotowany.
4. Walidacja danych wejściowych — walidacja po stronie serwera dla każdego wejścia; SQL
   injection (tylko zapytania parametryzowane); XSS (escape/sanityzacja; audyt
   renderowania surowego HTML); przesyłane pliki (MIME + rozmiar + metadane po stronie
   serwera).
5. Publiczna powierzchnia API — limitowanie żądań (na IP i na użytkownika) dla
   uwierzytelniania i kosztownych endpointów; brak wycieku wrażliwych danych ani
   enumeracji użytkowników/rekordów (znormalizowane odpowiedzi); CORS zawężony (nie
   wildcard); metody HTTP zawężone per trasa.
6. Logowanie i monitoring — logowane zdarzenia bezpieczeństwa (logowania, zmiany
   haseł/uprawnień, akcje admina, wyzwolenia limitów); sensowna retencja; brak
   PII/sekretów/haseł w logach; sposób na zauważenie cichych awarii i nadużyć w trakcie.
7. Ryzyka specyficzne dla AI (TYLKO jeśli aplikacja używa LLM/agenta/embeddingów/
   wyszukiwania wektorowego) — prompt injection (niezaufane wejście sklejane z promptem);
   nadmiarowe uprawnienia narzędzi/agenta (zasięg szkód przy udanym wstrzyknięciu;
   minimalne uprawnienia + zatwierdzenie przez człowieka dla akcji o dużym wpływie);
   niebezpieczna obsługa wyjścia (wyjście modelu renderowane jako HTML lub wykonywane
   jako kod); wykręcanie kosztów (nielimitowane zużycie tokenów).
8. Hardening wdrożenia — HTTPS + HSTS wszędzie; nagłówki bezpieczeństwa (CSP,
   X-Content-Type-Options, ochrona przed ramkowaniem, Referrer-Policy); WAF/CDN;
   podatności zależności (npm audit / pip-audit) — oznacz krytyczne/wysokie.

Dla każdego znaleziska:
- [POZIOM] [POTWIERDZONE/PODEJRZEWANE] — krótki tytuł
- Kategoria
- Jednozdaniowy opis ryzyka
- Konkretna lokalizacja plik:linia (albo „do weryfikacji — pokaż mi X")
- Konkretna, gotowa do wklejenia poprawka

Zakończ LISTĄ ZADAŃ WG PRIORYTETU: każde znalezisko jako jeden punkt, posortowane
KRYTYCZNY → NISKI, żebym wiedział dokładnie, co i w jakiej kolejności zrobić przed
wdrożeniem. Bądź uczciwy co do tego, czego nie udało ci się zweryfikować na podstawie
kodu, który ci pokazałem.
```
