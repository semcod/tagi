# tagi


## AI Cost Tracking

![PyPI](https://img.shields.io/badge/pypi-costs-blue) ![Version](https://img.shields.io/badge/version-0.49.9-blue) ![Python](https://img.shields.io/badge/python-3.9+-blue) ![License](https://img.shields.io/badge/license-Apache--2.0-green)
![AI Cost](https://img.shields.io/badge/AI%20Cost-$1.99-orange) ![Human Time](https://img.shields.io/badge/Human%20Time-14.7h-blue) ![Model](https://img.shields.io/badge/Model-openrouter%2Fqwen%2Fqwen3--coder--next-lightgrey)

- 🤖 **LLM usage:** $1.9865 (24 commits)
- 👤 **Human dev:** ~$1475 (14.7h @ $100/h, 30min dedup)

Generated on 2026-07-03 using [openrouter/qwen/qwen3-coder-next](https://openrouter.ai/qwen/qwen3-coder-next)

---

`tagi` to paczka Python i CLI do **orkiestracji wysyłania zmian Git**, a nie zamiennik komendy `git`.

## Pozycjonowanie

- **Git** odpowiada za wykonanie (`status`, `add`, `commit`, `push`).
- **tagi** odpowiada za analizę, grupowanie, planowanie i bezpieczne uruchomienie workflow.
- **gh/glab** odpowiadają za integrację i auth z providerami.

## Cel

`tagi` pomaga zdecydować, **co** wysłać i **jak** to opisać, a następnie uruchamia istniejące narzędzia (`git`, opcjonalnie `gh`/`glab`) po jawnym potwierdzeniu użytkownika.

## Zasady projektu

- jawność przed magią,
- preview → confirm → execute,
- brak ukrywania realnych komend,
- deterministyczne tagowanie jako domyślne.
- LLM opcjonalnie do redakcji opisów, nie do sterowania logiką wysyłki.

## Zakres odpowiedzialności

### Co `tagi` powinien robić

- analizować `git status --porcelain` i diffy,
- budować grupy zmian na podstawie heurystyk,
- proponować paczki wysyłkowe i plan wykonania,
- generować draft tytułu i treści opisu commita,
- uruchamiać `git` i opcjonalnie `gh`/`glab` dopiero po decyzji użytkownika.

### Czego `tagi` nie powinien robić

- zastępować `git add/commit/push`,
- implementować własnego modelu stanu repo poza `.git`,
- ukrywać jakie komendy wykona,
- zmieniać semantyki commit/push,
- zastępować workflow branch/rebase/merge.

## Komendy

```bash
tagi scan <path> [--grouped] [--by-branch]
tagi list-groups <path>
tagi stats <path>
tagi filter <tags> <path> [--all] [--min-risk FLOAT] [--max-risk FLOAT] [--min-complexity FLOAT] [--max-complexity FLOAT] [--min-impact FLOAT] [--max-impact FLOAT]
tagi file <file_path> <path>
tagi inspect <tag> <path> [--diff]
tagi summary <path> [--output FILE]
tagi safe <path>
tagi init <path>
tagi auth <path> [--provider PROVIDER]
tagi hooks <path> [--install] [--uninstall] [--list]
tagi deps <path> [--cycles] [--critical]
tagi metrics <path> [--output FILE] [--report]
tagi draft <tag> <path> [--template TEMPLATE]
tagi send <path> [tags...] [--dry-run] [--push] [--template TEMPLATE] [--interactive] [--auto-order]
tagi auto <path> [--dry-run] [--template TEMPLATE]
tagi deploy <path> [--dry-run] [--koru-host HOST] [--koru-port PORT]
tagi publish <tag> <path> [--dry-run] [--template TEMPLATE]
```

- `scan` — analiza zmian w repozytorium (z opcją `--grouped` do grupowania po tagach)
- `list-groups` — lista paczek i tagów
- `stats` — statystyki zmian (liczba plików, linii, rozkład typów i tagów)
- `filter` — filtrowanie plików po tagach (comma-separated, np. `small,docs`; `--all` wymaga wszystkich tagów)
- `file` — szczegóły pojedynczego pliku (wszystkie tagi, linie zmienione, score ryzyka)
- `inspect` — podgląd paczki i ryzyka (z opcją `--diff` do pokazania zmian)
- `summary` — generuj kompleksowy raport podsumowujący (opcjonalnie zapisz do pliku)
- `safe` — pokaż bezpieczne zmiany do wysłania najpierw (niskie ryzyko, małe, nie risky/deps/config)
- `init` — wygeneruj plik konfiguracyjny `tagi.toml.example`
- `auth` — sprawdź status autoryzacji GitHub/GitLab (opcjonalnie dla konkretnego providera)
- `hooks` — zarządzaj integracją git hooks (instalacja, odinstalowanie, lista, status)
- `deps` — analizuj graf zależności zmian Python (cykle, ścieżka krytyczna, kolejność)
- `metrics` — zbieraj i wyświetlaj metryki o zmianach (eksport JSON, raport)
- `draft` — propozycja opisu commita z wyborem szablonu
- `send` — po potwierdzeniu wykonuje `git add` i `git commit`; push jest opcjonalny (z trybem interaktywnym); akceptuje wiele tagów w kolejności priorytetu, np. `tagi send . small docs`; bez tagów lub z flagą --auto-order sortuje automatycznie od najprostszych do najtrudniejszych
- `auto` — automatycznie skanuje, sortuje i wysyła wszystkie zmiany z pushem (odpowiednik `tagi scan . && tagi send . --auto-order --push`)
- `deploy` — wdraża zmiany na serwer z analizą priorytetów przez API Koru (inteligentna kolejność wdrażania)
- `publish` — rozszerzenie o PR/MR przez provider z auto-detection (GitHub/GitLab)

## Architektura (kierunek)

```text
src/tagi/
  scanner/
  cli.py
  config.py
  models/
    change.py
    group.py
    plan.py
  scanner/
    status.py
    diff.py
    files.py
  heuristics/
    tags.py
    scoring.py
    rules.py
  planner/
    grouper.py
    selector.py
    preview.py
  composer/
    commit_message.py
    summary.py
  executor/
    git.py
    publish.py
  providers/
    base.py
    github.py
    gitlab.py
  llm/
    llx_adapter.py

## System priorytetyzacji

`tagi` automatycznie priorytetyzuje zmiany na podstawie heurystyk ryzyka i złożoności:

### Hierarchia tagów (od najwyższego priorytetu)
```
#risky > #large > #deps > #config > #new > #tests > #docs > #feature > #refactor > #small
```

### Algorytm priorytetyzacji
- **Risk score** (0-1) - wyższy = większe ryzyko
- **Lines changed** - więcej linii = większa złożoność  
- **Change type** - MODIFIED < ADDED < DELETED
- **Tag priority** - według hierarchii powyżej

### Przykład automatycznej priorytetyzacji
```bash
# Zmiany zostaną automatycznie posortowane:
# 1. config.yaml (risk: 0.1, lines: 2) → #config
# 2. test.py (risk: 0.2, lines: 5) → #small  
# 3. test_file.py (risk: 0.3, lines: 20) → #tests
# 4. big.py (risk: 0.8, lines: 100) → #risky (najwyższy priorytet!)
```

## Przykłady użycia

### Podstawowe operacje
```bash
# Podstawowe skanowanie
tagi scan /path/to/repo

# Skanowanie z grupowaniem po tagach
tagi scan /path/to/repo --grouped

# Statystyki zmian
tagi stats /path/to/repo
```

### Filtrowanie i analiza
```bash
# Filtrowanie po jednym tagu
tagi filter "small" /path/to/repo

# Filtrowanie po wielu tagach (OR logic - pasuje do dowolnego)
tagi filter "small,docs" /path/to/repo

# Filtrowanie po wielu tagach (AND logic - wymaga wszystkich)
tagi filter "config,small" /path/to/repo --all

# Filtrowanie po zakresie ryzyka
tagi filter "all" /path/to/repo --min-risk 0.5 --max-risk 0.8

# Szczegóły pojedynczego pliku
tagi file README.md /path/to/repo

# Podgląd tagu ze statystykami
tagi inspect docs /path/to/repo

# Pokaż bezpieczne zmiany do wysłania najpierw
tagi safe /path/to/repo
```

### Raporty i podsumowania
```bash
# Generuj raport podsumowujący
tagi summary /path/to/repo

# Zapisz raport do pliku
tagi summary /path/to/repo --output report.txt

# Lista grup zmian
tagi list-groups /path/to/repo

# Inspekcja z podglądem diffów
tagi inspect #small /path/to/repo --diff
```

### Tworzenie commitów
```bash
# Draft z konwencjonalnym formatem
tagi draft small /path/to/repo --template conventional

# Draft z prostym formatem
tagi draft small /path/to/repo --template simple

# Draft z formatem jednej linii
tagi draft small /path/to/repo --template oneline

# Draft z formatem skupionym na plikach
tagi draft small /path/to/repo --template files
```

### Wysyłanie z priorytetyzacją
```bash
# Wysłanie pojedynczej grupy z pushem
tagi send small /path/to/repo --push --template detailed

# Wysłanie wielu grup w określonej kolejności
tagi send /path/to/repo small docs tests --push

# Automatyczna priorytetyzacja (od najbezpieczniejszych)
tagi send /path/to/repo --auto-order --push

# Wysyłanie tylko bezpiecznych zmian
tagi send /path/to/repo $(tagi safe /path/to/repo --tags-only) --push
```

### Publikacja PR/MR
```bash
# Opublikuj PR/MR (szablon conventional)
tagi publish small /path/to/repo --template conventional

# Publikacja z automatycznym wykrywaniem providera
tagi publish risky /path/to/repo --dry-run
```

### Integracja z Koru (wdrożenia na serwer)
```bash
# Analiza priorytetów wdrożenia z API Koru
tagi deploy /path/to/repo

# Podgląd planu wdrożenia
tagi deploy /path/to/repo --dry-run

# Wdrożenie z niestandardowym hostem Koru
tagi deploy /path/to/repo --koru-host 192.168.1.100 --koru-port 8790
```

**Korzyści z integracji z Koru:**
- 🎯 **Inteligentna kolejność** - analiza priorytetów przez API Koru
- 📊 **Analiza ryzyka** - ocena wpływu zmian na system
- 🏗️ **Kontekst projektu** - uwzględnienie topologii i zależności
- 🚦 **Quality gates** - automatyczne sprawdzanie jakości
- 📋 **Planfile tickets** - integracja z systemem ticketów

### Automatyzacja
```bash
# Pełna automatyzacja - skanuj, sortuj, commituj i pushuj
tagi auto /path/to/repo

# Automatyzacja z podglądem
tagi auto /path/to/repo --dry-run

# Automatyzacja z konwencjonalnym formatem
tagi auto /path/to/repo --template conventional
```

### Przepływy pracy (workflows)
```bash
# Workflow 1: Szybka automatyzacja
tagi auto /path/to/repo

# Workflow 2: Bezpieczne zmiany najpierw
tagi safe /path/to/repo
tagi send /path/to/repo $(tagi safe /path/to/repo --tags-only) --push

# Workflow 3: Priorytetyzacja od ryzykownych
tagi scan /path/to/repo --grouped
tagi send /path/to/repo risky large --push

# Workflow 4: Pełny cykl development
tagi scan /path/to/repo
tagi summary /path/to/repo --output dev-report.txt
tagi auto /path/to/repo  # zamiast send + push
tagi publish /path/to/repo feature --template detailed

# Workflow 5: Inteligentne wdrożenie z Koru
tagi deploy /path/to/repo --dry-run  # analiza priorytetów
tagi deploy /path/to/repo  # wdrożenie z uwzględnieniem kolejności

# Workflow 6: Pełny cykl z wdrożeniem
tagi scan /path/to/repo
tagi auto /path/to/repo  # commit lokalny
tagi deploy /path/to/repo  # wdrożenie na serwer z analizą
```

## Konfiguracja

Utwórz plik `tagi.toml` w katalogu repozytorium:

```toml
[rules]
"frontend/" = "#frontend"
"backend/" = "#backend"
"migration/" = "#risky"

[colors]
# Własne kolory dla tagów (nazwy kolorów Rich)
"#frontend" = "blue"
"#backend" = "green"
"#risky" = "red"

[heuristics]
# Własne heurystyki - mapuj wzorce do wielu tagów
"api/" = ["#api", "#backend"]
"cli/" = ["#cli", "#tool"]
"migration/" = ["#risky", "#database"]

[tag_definitions]
# Opisy tagów
"#small" = "Małe zmiany (< 10 linii)"
"#large" = "Duże zmiany (> 100 linii)"
"#risky" = "Zmiany wysokiego ryzyka"

[templates]
# Własne szablony komunikatów commitów
default = "{tag}: {count} plików ({files})"
detailed = "Commit {tag}\n\nZmienione pliki ({count}):\n{files}\n\nWygenerowane przez tagi"

[ignore]
# Wzorce do ignorowania podczas skanowania
["node_modules/", ".git/", "__pycache__/", "*.pyc", ".idea/", ".vscode/"]
```

## Definicja produktu

> `tagi` to orchestrator wysyłania zmian Git: analizuje nie wysłane pliki, grupuje je hashtagami, proponuje sensowne paczki commitów i uruchamia istniejące narzędzia Git/GitHub/GitLab do publikacji.


## License

Licensed under Apache-2.0.
