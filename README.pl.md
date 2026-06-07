<div align="center">

[🇬🇧 English](README.md) · **🇵🇱 Polski**

# 🛡️ Before You Deploy

### Przegląd bezpieczeństwa przed wdrożeniem, który dowolny agent AI uruchomi na twoim realnym kodzie

Zamień **Claude**, **Codexa** lub **Gemini** w starszego inżyniera bezpieczeństwa
aplikacji, który audytuje twoją aplikację *zanim* trafi na produkcję — 8 kategorii,
uczciwe znaleziska, lista zadań do wykonania. Bez SaaS, bez rejestracji. Zainstaluj raz,
używaj zawsze.

[![CI](https://github.com/GeorgeMJZak/before-you-deploy/actions/workflows/ci.yml/badge.svg)](https://github.com/GeorgeMJZak/before-you-deploy/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Release](https://img.shields.io/github/v/release/GeorgeMJZak/before-you-deploy?color=success)](https://github.com/GeorgeMJZak/before-you-deploy/releases)
[![SKILL.md](https://img.shields.io/badge/SKILL.md-otwarty%20standard-7c3aed)](https://agentskills.io/specification)

**Działa z** &nbsp;`Claude Code`&nbsp; · &nbsp;`claude.ai`&nbsp; · &nbsp;`OpenAI Codex`&nbsp; · &nbsp;`Gemini CLI`&nbsp; · &nbsp;`Cursor`&nbsp; · &nbsp;dowolnym narzędziem `AGENTS.md`

[Szybki start](#-szybki-start) · [Co robi](#-co-robi) · [Kompatybilność](#-kompatybilność) · [Użycie](#-użycie) · [Struktura](#-struktura-repozytorium)

</div>

---

## ⚡ Szybki start

```bash
git clone https://github.com/GeorgeMJZak/before-you-deploy.git
cd before-you-deploy
./install.sh claude     # lub: codex · gemini · all
```

Potem, w dowolnym projekcie:

> **„Zrób przegląd bezpieczeństwa tego repozytorium przed wdrożeniem."**

Nie masz systemu skilli? Wklej [`prompt.pl.md`](prompt.pl.md) do dowolnego asystenta.
Ten sam przegląd, zero instalacji.

---

## 🎯 Co robi

Działające uzupełnienie eseju **„Before You Deploy Your Vibe-Coded App"** autorstwa
George'a M. J. Zaka. PDF mówi, *co* sprawdzić — to sprawia, że twoja AI faktycznie *to
robi*, na twoim realnym kodzie:

- 🔍 **Mapuje realną powierzchnię ataku** — trasy, bramki uwierzytelniania, gdzie
  wczytywane są sekrety, co jest śledzone w gicie — zamiast zgadywać.
- 🧭 **Przechodzi przez 8 kategorii** — Uwierzytelnianie · Baza danych/dostęp do danych ·
  Sekrety i klucze API · Walidacja danych wejściowych · Publiczna powierzchnia API ·
  Logowanie i monitoring · Ryzyka specyficzne dla AI · Hardening wdrożenia.
- ✅ **Oznacza każde znalezisko** `[POTWIERDZONE]` (widziane w kodzie) lub
  `[PODEJRZEWANE]` (na podstawie wzorca) — nigdy domysł podany jako fakt.
- 🚦 **Przypisuje istotność** KRYTYCZNY / WYSOKI / ŚREDNI / NISKI i kończy **listą zadań
  wg priorytetu**, którą wykonasz od góry do dołu.
- 🤖 **Sam pomija sekcję o AI** w zwykłych aplikacjach CRUD — bez wypełniacza.

> **Dlaczego skill, a nie tylko prompt?** Ładuje się na żądanie, niesie pełną listę
> kontrolną i skalę istotności jako pliki referencyjne (progresywne odsłanianie) i ma
> testy, więc metodyka nie zardzewieje po cichu. Gwarancje uczciwości to sedno —
> powstrzymują gorliwą AI od przyklepania twojej aplikacji.

---

## 🔌 Kompatybilność

| Agent | Instalacja | Wywołanie |
|-------|------------|-----------|
| **Claude Code** | `./install.sh claude` → `~/.claude/skills/` | „zrób przegląd bezpieczeństwa przed wdrożeniem" |
| **claude.ai** | spakuj `skills/pre-deploy-security-review-pl/`, wgraj w **Ustawienia → Capabilities → Skills** | wspomnij o przeglądzie bezpieczeństwa |
| **OpenAI Codex** | `./install.sh codex` → `~/.agents/skills/` | `/skills` lub `$pre-deploy-security-review` |
| **Gemini CLI** | `./install.sh gemini` | `/security-review` |
| **Cursor / inne** | wrzuć [`adapters/AGENTS.md`](adapters/AGENTS.md) do repo | zawsze aktywne |
| **Cokolwiek innego** | wklej [`prompt.pl.md`](prompt.pl.md) | — |

Wersja polska skilla mieszka w `skills/pre-deploy-security-review-pl/`, angielska w
`skills/pre-deploy-security-review/`. Dla instalacji **per projekt** skopiuj wybrany
katalog skilla do `.claude/skills/`, `.agents/skills/` lub `.gemini/skills/` w repo.

---

## 💬 Użycie

Znaleziska wracają konkretne i bezpośrednie — `plik:linia` i gotowa poprawka:

```text
[KRYTYCZNY] [POTWIERDZONE] — Klucz serwisowy trafia do bundla przeglądarki
Kategoria: Sekrety i klucze API
Ryzyko:    Każdy odwiedzający może wyciągnąć klucz z bundla JS i czytać/zapisywać
           całą bazę, omijając autoryzację na poziomie wiersza.
Lokalizacja: src/lib/supabase.ts:6
Poprawka:  Przenieś klienta z kluczem serwisowym do kodu serwerowego; w przeglądarce
           używaj klucza anon z RLS. Zrotuj wyciekły klucz teraz — zakładaj, że jest
           skompromitowany.

LISTA ZADAŃ WG PRIORYTETU
[ ] KRYTYCZNY — Wynieś klucz serwisowy z bundla przeglądarki + zrotuj go
[ ] WYSOKI    — Limituj POST /api/auth/login + wymień słabe współdzielone hasło
[ ] ŚREDNI    — Dodaj nagłówki CSP + HSTS
[ ] NISKI     — Zamień Math.random() na crypto.randomUUID() przy generowaniu kodów
```

**Jak używać dobrze:** czytaj, co wypłynie — *ty* decydujesz, co warto naprawić.
Dopytuj (*„pokaż mi dokładną zmianę dla znaleziska nr 2"*), a potem **zweryfikuj, że
poprawka faktycznie weszła** — AI czasem twierdzi, że coś naprawiła, choć tego nie
zrobiła. Powtarzaj przed każdym wdrożeniem.

---

## 📁 Struktura repozytorium

```
before-you-deploy/
├── skills/
│   ├── pre-deploy-security-review/      # skill (EN)
│   └── pre-deploy-security-review-pl/   # skill (PL)
│       ├── SKILL.md
│       └── references/
│           ├── checklist.md             # pełna lista kontrolna 8 kategorii
│           ├── severity-rubric.md       # definicje KRYTYCZNY/WYSOKI/ŚREDNI/NISKI
│           ├── ai-specific-risks.md     # kategoria 7 + punkty EU AI Act
│           └── report-format.md         # format raportu + reguły weryfikacji poprawek
├── adapters/                            # AGENTS.md, GEMINI.md, komenda /security-review
├── prompt.md / prompt.pl.md             # prompt do wklejenia (bez instalacji)
├── install.sh                           # instalacja jedną komendą per agent
├── scripts/validate_skill.py            # walidator standardu SKILL.md (sama stdlib)
├── tests/test_skill.py                  # testy pytest (zgodność + niezmienniki treści)
└── .github/workflows/ci.yml             # walidacja + testy przy każdym push/PR
```

---

## 🧪 Rozwój i walidacja

```bash
python3 scripts/validate_skill.py --all   # sprawdź SKILL.md względem standardu
python3 -m pytest -q                        # uruchom zestaw testów
```

CI uruchamia oba przy każdym push i pull requeście. Zob. [CONTRIBUTING.md](CONTRIBUTING.md).

---

## 📜 Autorstwo i licencja

Metodyka i tekst zaadaptowane z **„Before You Deploy Your Vibe-Coded App"** autorstwa
**George'a M. J. Zaka** — strategia AI, cyberbezpieczeństwo i ludzka strona technologii
([jorgemjzak.com](https://jorgemjzak.com)).

Wydane na [licencji MIT](LICENSE). Wolno używać, forkować i dzielić się.
