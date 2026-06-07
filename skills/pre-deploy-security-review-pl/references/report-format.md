# Format raportu

Twórz raport dokładnie w tym kształcie. Spójność sprawia, że da się go szybko czytać,
a listę zadań — wykonać.

## Na każde znalezisko

> **[POZIOM] [POTWIERDZONE|PODEJRZEWANE] — krótki tytuł**
> **Kategoria:** jedna z 8
> **Ryzyko:** jedno zdanie o tym, co zyskuje atakujący.
> **Lokalizacja:** `ścieżka/do/pliku.ext:linia` — albo, jeśli nie było widać,
> `do weryfikacji — pokaż mi <konkretny plik/fragment>`.
> **Poprawka:** konkretna, gotowa do wklejenia zmiana (blok kodu, polecenie lub
> konfiguracja), nie „rozważ usprawnienie X".

Przykład:

> **[KRYTYCZNY] [POTWIERDZONE] — Klucz serwisowy trafia do bundla przeglądarki**
> **Kategoria:** Sekrety i klucze API
> **Ryzyko:** Każdy odwiedzający może wyciągnąć klucz z bundla JS i czytać/zapisywać
> całą bazę, omijając autoryzację na poziomie wiersza.
> **Lokalizacja:** `src/lib/supabase.ts:6` — `createClient(url, SERVICE_ROLE_KEY)` w
> pliku importowanym przez komponent kliencki.
> **Poprawka:** Przenieś klienta z kluczem serwisowym do kodu wyłącznie serwerowego. W
> przeglądarce używaj klucza anon z włączonym RLS. Zrotuj wyciekły klucz teraz w panelu
> dostawcy — zakładaj, że jest skompromitowany.

## Kolejność

1. Na górze **podsumowanie** w 2–4 wierszach: stack, gdzie żyją prawdziwe dane i jedna
   najgorsza rzecz, którą znalazłeś.
2. Znaleziska pogrupowane wg istotności, **KRYTYCZNY na początku**.
3. Lista zadań wg priorytetu.
4. Krótka sekcja **„Czego nie udało się zweryfikować"** wymieniająca to, czego nie
   było widać, i dokładnie to, co pokazać, by zamknąć każdą lukę.

## Lista zadań wg priorytetu

Zakończ listą, w której każde znalezisko to jeden punkt, posortowaną KRYTYCZNY →
NISKI, tak by użytkownik wiedział dokładnie, co i w jakiej kolejności zrobić przed
wdrożeniem:

```
LISTA ZADAŃ WG PRIORYTETU
[ ] KRYTYCZNY — Wynieś klucz serwisowy z bundla przeglądarki + zrotuj go
[ ] KRYTYCZNY — Dodaj kontrolę uprawnień do GET /api/admin/export
[ ] WYSOKI    — Limituj POST /api/auth/login + wymień słabe współdzielone hasło
[ ] ŚREDNI    — Dodaj nagłówki CSP + HSTS
[ ] NISKI     — Zamień Math.random() na crypto.randomUUID() przy generowaniu kodów
```

## Weryfikacja poprawek

Gdy użytkownik prosi o zastosowanie poprawek (nie tylko o raport), po każdej zmianie:

1. **Przeczytaj ponownie zmieniony plik** i potwierdź, że zmiana faktycznie tam jest.
2. **Uruchom build / typecheck / testy** i wklej istotny fragment wyniku.
3. Dopiero wtedy powiedz, że naprawione — z diffem lub wynikiem builda jako dowodem,
   nigdy samym „gotowe". Agenci czasem twierdzą, że coś naprawili, choć tego nie
   zrobili; udowodnij to.
4. Jeśli poprawka ma kompromis produkcyjny (np. usunięcie śledzonego zasobu, który
   runtime czyta przy wdrożeniu), **zatrzymaj się i nazwij ten kompromis**, zamiast po
   cichu wprowadzać zmianę, która psuje produkcję lub daje fałszywe poczucie
   bezpieczeństwa.

## Ton

Bezpośredni, konkretny, oparty na dowodach. Bez uspokajającego wypełniacza. Jeśli
aplikacja jest w danej kategorii naprawdę w dobrym stanie, napisz to w jednym wierszu i
idź dalej — nie wymyślaj znalezisk, żeby wyglądać dokładnie.
