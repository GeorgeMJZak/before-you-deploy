# Kategoria 7 — Ryzyka specyficzne dla AI

**Oceniaj tę kategorię tylko, jeśli aplikacja faktycznie używa LLM, agenta,
embeddingów lub wyszukiwania wektorowego.** Dla zwykłej aplikacji CRUD pomiń ją w
raporcie całkowicie — nie zaśmiecaj aplikacji bez AI znaleziskami o AI.

Żadne z tych ryzyk nie jest egzotyczne. Wszystkie są dziś do wykorzystania.

| Ryzyko | Istotność | Co zweryfikować |
|--------|-----------|-----------------|
| **Prompt injection** | KRYTYCZNY | Czy niezaufany tekst użytkownika jest wstrzykiwany wprost do promptu systemowego? Atakujący pisze „zignoruj poprzednie instrukcje i…", a agent słucha. Traktuj całe wejście użytkownika jako niezaufane; nigdy nie sklejaj go surowo z promptem. Używaj jasnych separatorów; waliduj wyjście przed działaniem. |
| **Nadmiarowe uprawnienia narzędzi/agenta** | KRYTYCZNY | Jeśli agent może wykonywać kod, wysyłać e-maile, przelewać pieniądze lub modyfikować dane — jaki jest zasięg szkód, gdy prompt injection się powiedzie? Ogranicz uprawnienia narzędzi do minimum. Wymagaj potwierdzenia przez człowieka dla akcji o dużym wpływie. |
| **Eksfiltracja danych przez wyjście** | WYSOKI | AI z dostępem do bazy można podstępem zmusić do ujawnienia danych, których proszący użytkownik nie powinien widzieć. Jeśli model może czytać więcej niż użytkownik, ta luka zostanie wykorzystana. Zawęź dostęp AI dokładnie do tego, do czego proszący użytkownik ma prawo. |
| **Wykręcanie kosztów** | WYSOKI | Jeden nieuwierzytelniony, nielimitowany użytkownik potrafi w popołudnie wykręcić rachunek za tokeny na tysiące. Limituj endpointy AI. Ogranicz miesięczny budżet tokenów per użytkownik. Monitoruj nietypowe zużycie. |
| **Niebezpieczna obsługa wyjścia** | WYSOKI | Jeśli renderujesz wyjście modelu jako HTML, atakujący może wstrzyknąć przez prompt HTML uruchamiany w przeglądarkach twoich użytkowników. Jeśli wykonujesz kod wygenerowany przez AI, może wstrzyknąć złośliwy kod. Traktuj wyjście AI jak niezaufane wejście do następnego systemu. |
| **Wyciek danych treningowych** | ŚREDNI | Jeśli dostrajasz na danych użytkowników, mogą one wypłynąć w odpowiedziach dla innych użytkowników. Sanityzuj i uzyskaj wyraźną zgodę; większość aplikacji powinna woleć RAG od fine-tuningu. |
| **Podmiana modelu przez dostawcę** | ŚREDNI | Ciche podniesienie wersji modelu przez dostawcę może zmienić zachowanie, na którym polegałeś. Przypinaj wersje modeli, gdzie wolno; testuj przed odpięciem. |
| **Ujawnienie logów rozmów** | ŚREDNI | Logi rozmów z AI mogą zawierać PII, sekrety lub treści zastrzeżone, które użytkownik podał. Chroń je przynajmniej tak dobrze jak dane użytkowników. |

## Model myślowy

> Agent LLM w twojej aplikacji jest mniej więcej tak godny zaufania jak wykonawca,
> którego poznałeś na budowie pięć minut temu. Bystry, zdolny, chętny do pomocy — i na
> pewno nie powinien dostać kluczy głównych, loginu do banku ani nienadzorowanego
> dostępu do części budynku, których nie pokazałbyś obcemu. **Zasada minimalnych
> uprawnień** liczy się *bardziej* dla komponentów AI niż dla jakiejkolwiek innej części
> stacku, bo komponentami AI łatwiej manipulować.

## Punkty styku z regulacjami (jeśli wdrażasz w UE lub do UE)

Akt o AI (EU AI Act) obowiązuje niezależnie od miejsca rejestracji firmy; większość
obowiązków ogólnego przeznaczenia wchodzi falami w ciągu 2026 r. Kilka z nich mapuje
się wprost na tę listę — oznaczaj je, gdy istotne, ale odróżniaj „znalezisko
bezpieczeństwa" od „uwagi compliance":

- **Artykuł 15** (dokładność, odporność, cyberbezpieczeństwo) mapuje się na całą tę
  listę — postura bezpieczeństwa staje się artefaktem regulacyjnym.
- **Artykuł 14** (nadzór człowieka) — nadmiarowe uprawnienia narzędzi/agenta to też
  kwestia compliance w domenach wysokiego ryzyka.
- **Artykuł 12** (prowadzenie rejestrów) — twoje logi audytowe AI mogą być ustawowe, a
  nie opcjonalne.
- **Artykuł 10** (zarządzanie danymi) — jeśli dostrajasz, potrzebujesz historii
  pochodzenia danych i mitygacji uprzedzeń (bias).
- **Nakładka RODO/GDPR** — dane osobowe przechodzące przez komponent AI to wciąż dane
  osobowe; prawo do bycia zapomnianym, minimalizacja danych i ograniczenie celu nadal
  obowiązują.
