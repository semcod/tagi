# tagi


## AI Cost Tracking

![PyPI](https://img.shields.io/badge/pypi-costs-blue) ![Version](https://img.shields.io/badge/version-0.3.1-blue) ![Python](https://img.shields.io/badge/python-3.9+-blue) ![License](https://img.shields.io/badge/license-Apache--2.0-green)
![AI Cost](https://img.shields.io/badge/AI%20Cost-$0.03-orange) ![Human Time](https://img.shields.io/badge/Human%20Time-3.1h-blue) ![Model](https://img.shields.io/badge/Model-openrouter%2Fqwen%2Fqwen3--coder--next-lightgrey)

- 🤖 **LLM usage:** $0.0325 (4 commits)
- 👤 **Human dev:** ~$311 (3.1h @ $100/h, 30min dedup)

Generated on 2026-05-26 using [openrouter/qwen/qwen3-coder-next](https://openrouter.ai/qwen/qwen3-coder-next)

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
tagi scan <path> [--grouped]
tagi list-groups <path>
tagi stats <path>
tagi filter <tags> <path> [--all]
tagi file <file_path> <path>
tagi inspect <tag> <path> [--diff]
tagi summary <path> [--output FILE]
tagi draft <tag> <path> [--template TEMPLATE]
tagi send <tag> <path> [--dry-run] [--push] [--template TEMPLATE]
tagi publish <tag> <path> [--dry-run]
```

- `scan` — analiza zmian w repozytorium (z opcją `--grouped` do grupowania po tagach)
- `list-groups` — lista paczek i tagów
- `stats` — statystyki zmian (liczba plików, linii, rozkład typów i tagów)
- `filter` — filtrowanie plików po tagach (comma-separated, np. `#small,#docs`; `--all` wymaga wszystkich tagów)
- `file` — szczegóły pojedynczego pliku (wszystkie tagi, linie zmienione, score ryzyka)
- `inspect` — podgląd paczki i ryzyka (z opcją `--diff` do pokazania zmian)
- `summary` — generuj kompleksowy raport podsumowujący (opcjonalnie zapisz do pliku)
- `draft` — propozycja opisu commita z wyborem szablonu (default, conventional, detailed)
- `send` — po potwierdzeniu wykonuje `git add` i `git commit`; push jest opcjonalny,
- `publish` — rozszerzenie o PR/MR przez provider.

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

## Przykłady użycia

```bash
# Podstawowe skanowanie
tagi scan /path/to/repo

# Skanowanie z grupowaniem po tagach
tagi scan /path/to/repo --grouped

# Statystyki zmian
tagi stats /path/to/repo

# Filtrowanie po jednym tagu
tagi filter "#small" /path/to/repo

# Filtrowanie po wielu tagach (OR logic - pasuje do dowolnego)
tagi filter "#small,#docs" /path/to/repo

# Filtrowanie po wielu tagach (AND logic - wymaga wszystkich)
tagi filter "#config,#small" /path/to/repo --all

# Szczegóły pojedynczego pliku
tagi file README.md /path/to/repo

# Podgląd tagu ze statystykami
tagi inspect #docs /path/to/repo

# Pokaż bezpieczne zmiany do wysłania najpierw
tagi safe /path/to/repo

# Generuj raport podsumowujący
tagi summary /path/to/repo

# Zapisz raport do pliku
tagi summary /path/to/repo --output report.txt

# Lista grup zmian
tagi list-groups /path/to/repo

# Inspekcja z podglądem diffów
tagi inspect #small /path/to/repo --diff

# Draft z konwencjonalnym formatem
tagi draft #small /path/to/repo --template conventional

# Wysłanie z pushem
tagi send #small /path/to/repo --push --template detailed

# Publikacja PR/MR
tagi publish #small /path/to/repo
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
