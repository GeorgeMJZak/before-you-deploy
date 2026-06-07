# Lista kontrolna — 8 kategorii

Weryfikuj każdy punkt względem **realnego kodu**. Oznaczaj znaleziska
`[POTWIERDZONE]` lub `[PODEJRZEWANE]`. To rozszerzenie do `SKILL.md`.

---

## 1. Uwierzytelnianie
*Większość incydentów zaczyna się przy drzwiach frontowych. Jeśli drzwi frontowe są źle zrobione, reszta budynku nie ma znaczenia.*

- [ ] **Trasy administracyjne/uprzywilejowane chronione od końca do końca** — na
  warstwie API, nie tylko ukryte w UI. Bramka w UI to wygoda dla uczciwych
  użytkowników; bramka API to realna ochrona. Jeśli jakiś URL zwraca wrażliwe dane
  bez sprawdzenia uprawnień, zostanie odkryty.
- [ ] **Hasła przechowywane poprawnie** — hashowane bcrypt/argon2/scrypt, z solą per
  użytkownik. Nigdy jawnie, nigdy szyfrowaniem odwracalnym. Hasła w postaci jawnej to
  błąd kończący karierę.
- [ ] **Koszt brute-force / blokada konta** — powtarzane nieudane próby muszą kosztować
  atakującego więcej, niż kosztują ciebie. Endpoint logowania bez limitu to nieograniczony
  cel ataku siłowego.
- [ ] **Weryfikacja adresu e-mail przed dostępem do wrażliwych funkcji.**
- [ ] **MFA dostępne dla wrażliwych akcji** — TOTP w aplikacji authenticator to tani
  domyślny wybór. SMS jest lepszy niż nic, ale podatny na SIM swap.
- [ ] **Tokeny sesji obsłużone poprawnie** — HttpOnly, Secure, SameSite=Lax (lub Strict
  dla przepływów o wysokim bezpieczeństwie). Sensowne wygasanie. **Unieważniane przy
  wylogowaniu i przy zmianie hasła.** Powiązane z user agentem, jeśli się da.

> Kod uwierzytelniania generowany przez AI *wygląda* poprawnie, bo trzyma się znanych
> wzorców, ale często pomija szczegóły, które czynią te wzorce bezpiecznymi — rotację
> tokenów, unieważnianie sesji przy zmianie hasła, ochronę przed powtórzeniem. Zapytaj
> wprost: *„przeprowadź mnie przez to, co się dzieje, gdy (a) użytkownik zmienia hasło,
> (b) wycieka token sesji, (c) użytkownik się wylogowuje, (d) ktoś próbuje tego samego
> hasła 50 razy. Pokaż mi każdą ścieżkę w kodzie."*

## 2. Baza danych / dostęp do danych
*Jeśli użytkownicy mogą czytać nawzajem swoje dane, nie masz aplikacji. Masz wyciek danych z interfejsem na wierzchu.*

- [ ] **Autoryzacja na poziomie wiersza (RLS lub odpowiednik) w każdej tabeli z danymi
  użytkowników** — zwłaszcza w Supabase/Firebase/dowolnym backendzie, gdzie klucz
  anon/kliencki trafia do przeglądarki. RLS to mur między „co zamierza twój kod" a „co
  przeglądarka faktycznie może zrobić". Bez niego muru nie ma.
- [ ] **Użytkownicy nie mają dostępu do cudzych danych.** Przetestuj wprost: jako User
  A spróbuj odczytać rekord, o którym wiesz, że należy do User B. Jeśli API go zwróci,
  to pozioma eskalacja uprawnień — jeden z najczęstszych błędów generowanych przez AI,
  bo endpoint odczytu dodano bez zawężenia do uwierzytelnionego użytkownika.
- [ ] **Role o minimalnych uprawnieniach.** Rola anon dostaje minimum. Klucz
  serwisowy/admina **nigdy** nie może trafić do przeglądarki. Tabele tylko dla admina
  mają anon całkowicie odebrany.
- [ ] **Wrażliwe pola nie są nadmiarowo ujawniane.** E-mail, telefon, adres, ID
  wewnętrzne, flagi admina — jeśli klient ich nie potrzebuje, API nie powinno ich
  zwracać. Zdefiniuj jawny schemat publiczny i trzymaj się go.
- [ ] **Kopie zapasowe istnieją, a odtwarzanie zostało przetestowane.** „Mamy backupy"
  ≠ „przetestowaliśmy, że umiemy odtworzyć z backupów".

> **Pułapka Supabase/Firebase/nocode:** hostowane backendy wysyłają klucz anon/kliencki
> w twoim frontendzie — co jest OK *tylko jeśli* RLS lub równoważne reguły są
> skonfigurowane. Wiele aplikacji „vibe-coded" wdraża się z wyłączonym RLS na każdej
> tabeli, czyli klucz anon, który każdy odwiedzający wyciągnie z twojego JavaScriptu, ma
> pełny odczyt/zapis do całej bazy. Sprawdź to przed startem. To darmowa poprawka i
> kompletna zmiana postury.

## 3. Sekrety i klucze API
*Każdy sekret, który trafi do repo lub bundla frontendu, jest sekretem w otwartym internecie.*

- [ ] **Żadnych kluczy API w kodzie frontendu.** Wszystko w `src/` lub `public/` staje
  się częścią bundla JS. Przeszukaj prefiksy każdego dostawcy, którego używasz — Stripe
  (`sk_`), Resend (`re_`), OpenAI/Anthropic (`sk-`), AWS (`AKIA`) itd. Jeśli pojawia się
  poza odwołaniem do zmiennej środowiskowej, rotuj natychmiast.
- [ ] **Sekrety w zmiennych środowiskowych**, nie w kodzie ani w commitowanej
  konfiguracji. Sprawdź, czy `.gitignore` zawiera `.env*`, a plik z sekretami jest po
  stronie ignorowanej.
- [ ] **Dane testowe nie trafiają na produkcję.** Szablony generowane przez AI często
  zostawiają klucze/audytoria testowe.
- [ ] **Klucze konta serwisowego o minimalnych uprawnieniach** — konkretne buckety,
  projekty, role. Nie klucz, który czyta wszystko.
- [ ] **Każdy kiedykolwiek ujawniony klucz został zrotowany.** Bez wyjątków. Jeśli
  trafił do publicznego repo choćby na dziesięć sekund, jest skompromitowany — GitHub
  indeksuje commity w minuty, a boty skanują nowe repozytoria w godziny.

## 4. Walidacja danych wejściowych
*Każdy formularz, endpoint i parametr URL to okazja, by wysłać coś, czego się nie spodziewasz. Zakładaj złośliwe wejście domyślnie.*

- [ ] **Walidacja po stronie serwera dla każdego wejścia.** Walidacja po stronie
  klienta to UX, nie bezpieczeństwo. `curl` omija każdą kontrolę w JavaScripcie.
- [ ] **SQL injection niemożliwe** — zapytania parametryzowane / prepared statements.
  Nigdy nie sklejaj wejścia użytkownika w SQL. ORM-y/buildery zapytań zwykle to
  obsługują — sprawdź wszelkie surowe zapytania, które napisałeś.
- [ ] **XSS zablokowany** — tekst od użytkownika jest escapowany lub sanityzowany.
  React/Vue/Svelte robią to domyślnie, *dopóki* nie użyjesz `dangerouslySetInnerHTML` /
  `v-html` / surowego HTML. Zaudytuj każde takie użycie.
- [ ] **Przesyłane pliki zwalidowane** — sprawdzenie MIME po stronie serwera (nie tylko
  nagłówek od klienta), limit rozmiaru, usunięte metadane, nazwa pliku nigdy nie
  zaufana. Przekoduj obrazy biblioteką, która porzuca wszystko poza danymi pikseli.
- [ ] **Honeypoty na publicznych formularzach** — ukryte pole (`website`/`hp`), którego
  prawdziwy użytkownik nie wypełni, a bot tak. Jeśli wypełnione, po cichu odrzuć.

## 5. Publiczna powierzchnia API
*Każdy endpoint jest publicznym celem ataku, dopóki go jawnie nie zabezpieczysz.*

- [ ] **Limitowanie żądań na miejscu** — na IP, na użytkownika, na endpoint. Większość
  platform (Cloudflare, Vercel, AWS API Gateway) oferuje to w kilka kliknięć. Endpoint
  logowania bez limitu to nieograniczony cel brute-force. *(Uwaga: limitery
  w pamięci resetują się przy zimnym starcie serverless i są per instancja — użyj
  współdzielonego magazynu jak Redis dla realnej trwałości.)*
- [ ] **Wrażliwe dane nieujawniane** — endpoint „pobierz profil" nie powinien zwracać
  hashy haseł, ID wewnętrznych ani flag admina. Jawny schemat publiczny.
- [ ] **Brak enumeracji użytkowników/rekordów** — rejestracja zwracająca „e-mail już
  istnieje" pozwala enumerować użytkowników. Logowanie odróżniające „złe hasło" od „brak
  użytkownika" — tak samo. Znormalizuj odpowiedzi.
- [ ] **CORS zawężony** — konkretne zaufane originy, nigdy `*`, gdy w grę wchodzą
  poświadczenia.
- [ ] **Metody HTTP zawężone per trasa** — endpointy tylko do odczytu odrzucają POST;
  endpointy modyfikujące odrzucają GET.

## 6. Logowanie i monitoring
*Nie obronisz tego, czego nie widzisz. Pierwsze, co zabiera atakujący, to twoja zdolność wiedzieć, że tam jest.*

- [ ] **Zdarzenia istotne dla bezpieczeństwa logowane** — udane i nieudane logowania,
  zmiany haseł, zmiany uprawnień, akcje admina, błędy API, wyzwolenia limitów. Trzymaj na
  osobnej powierzchni niż logi aplikacji, jeśli możesz.
- [ ] **Logi przechowywane wystarczająco długo** — minimum 90 dni dla większości
  aplikacji; dłużej dla danych regulowanych. Logi kasowane po 24 h nie łapią niczego.
- [ ] **Możesz wykryć nadużycie w trakcie** — skok nieudanych logowań, nietypowa
  geografia, nowe IP wykonujące wywołania API admina. Alertuj na to, co oczywiste; to
  proste.
- [ ] **Zauważasz ciche awarie** — podepnij śledzenie błędów (Sentry/Rollbar/itp.).
  Usługa e-mail zwracająca ignorowany kod błędu zawodzi niewidocznie, aż klienci się
  poskarżą.
- [ ] **Brak PII/sekretów/haseł w logach.** Logi też wyciekają. Jeśli musisz zalogować
  identyfikator, zhashuj go.

## 7. Ryzyka specyficzne dla AI
**Dotyczy tylko, jeśli aplikacja używa LLM / agenta / embeddingów / wyszukiwania
wektorowego. Jeśli nie — pomiń całą tę kategorię.** Pełne szczegóły w
[ai-specific-risks.md](ai-specific-risks.md).

## 8. Hardening wdrożenia
*Ostatni etap. Tu można zrobić wszystko inne dobrze i wciąż mieć publiczny incydent.*

- [ ] **HTTPS wymuszony wszędzie** — żadnego HTTP, żadnej mieszanej zawartości. Nagłówek
  HSTS z sensownym `max-age`. Zwykłe HTTP przekierowuje, a nie jest po prostu dostępne.
- [ ] **Nagłówki bezpieczeństwa skonfigurowane** — Content-Security-Policy (nawet
  liberalny start bije brak), `X-Content-Type-Options: nosniff`, `X-Frame-Options` /
  `frame-ancestors`, `Referrer-Policy`. Pięć linii konfiguracji blokujących połowę
  typowych ataków.
- [ ] **WAF / CDN z przodu** — darmowy plan Cloudflare ogarnia większość potrzeb małej
  aplikacji. Bez niego jesteś bezpośrednio wystawiony.
- [ ] **Mitygacja DDoS** — włącz odpowiednie funkcje platformy.
- [ ] **Podatności zależności sprawdzone** — `npm audit` / `pip-audit` przy każdym
  wdrożeniu; napraw krytyczne/wysokie przed startem. Włącz Dependabot/Renovate.
- [ ] **Hardening domeny** — DNSSEC, blokada u rejestratora, prywatność WHOIS, silne
  hasło + MFA na koncie dostawcy DNS. Twoja domena to twoja tożsamość w sieci.
