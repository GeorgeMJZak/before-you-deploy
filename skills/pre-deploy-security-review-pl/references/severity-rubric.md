# Skala istotności

Przypisz dokładnie jeden poziom każdemu znalezisku. Gdy wahasz się między dwoma,
uzasadnij wybór w jednym zdaniu, zamiast iść na kompromis.

| Poziom | Znaczenie | Termin działania | Przykłady |
|--------|-----------|------------------|-----------|
| **KRYTYCZNY** | Nie wdrażaj, dopóki nie naprawione. Bezpośrednie ujawnienie danych, obejście uwierzytelniania lub przejęcie konta — możliwe do wykorzystania małym wysiłkiem lub bez warunku wstępnego. | Zablokuj wdrożenie. | Klucz serwisowy/admina w bundlu przeglądarki; trasa admina/API zwracająca dane użytkowników bez kontroli uprawnień; RLS wyłączony na tabeli dostępnej dla klucza anon; hasła w postaci jawnej; prompt injection do agenta o nadmiarowych uprawnieniach. |
| **WYSOKI** | Napraw w tym tygodniu. Do wykorzystania, ale wymaga warunku lub pewnego wysiłku. | Przed realnym ruchem / w ciągu dni. | Endpoint logowania bez limitu + słabe współdzielone hasło; dostęp poziomy na mniej oczywistym endpoincie; sekret odzyskiwalny z historii gita w repo, które ma stać się publiczne; XSS odbity za stroną wymagającą logowania. |
| **ŚREDNI** | Napraw w tym miesiącu. Realna słabość o ograniczonym zasięgu szkód. | Śledzone z terminem. | Brak CSP/HSTS; rozwlekłe komunikaty błędów umożliwiające enumerację; brak warstwy middleware (kontrole per trasa obecne); HTML autorstwa admina renderowany bez sanityzacji. |
| **NISKI** | Śledź i wróć później. Hardening i higiena. | Backlog. | `Math.random()` dla tokenów niezwiązanych z bezpieczeństwem; brak logowania zdarzeń bezpieczeństwa; limiter w pamięci resetujący się przy zimnym starcie; zależność z ostrzeżeniem o niskiej istotności. |

## Uwagi kalibracyjne

- **Kontekst zmienia istotność.** Sekret w repo **prywatnym** jest utajony; ten sam
  sekret w repo, które ma być **publiczne**, jest KRYTYCZNY. Podaj kontekst, który
  ustala poziom.
- **Zasięg szkód liczy się bardziej niż wyrafinowanie.** Nudny brak kontroli uprawnień,
  który ujawnia całą tabelę, przebija elegancki atak czasowy ujawniający jeden bajt.
- **Znaleziska `[PODEJRZEWANE]` też dostają istotność** — oceń je tak, jakby były
  potwierdzone, i napisz, co je potwierdzi lub obniży.
- **Nie zawyżaj, by wyglądać dokładnie; nie zaniżaj, by uspokajać.** Każdy z tych błędów
  niszczy użyteczność raportu.
