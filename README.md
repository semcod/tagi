# tagi

`tagi` to paczka Python i CLI do **orkiestracji wysyłek zmian Git**, a nie zamiennik komendy `git`.

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
- deterministyczne tagowanie jako domyślne,
- LLM opcjonalnie do redakcji opisów, nie do sterowania logiką wysyłki.

## Zakres odpowiedzialności

### Co `tagi` powinien robić

- analizować `git status --porcelain` i diffy,
- budować grupy zmian na podstawie heurystyk,
- proponować paczki wysyłkowe i plan wykonania,
- generować draft opisu commita,
- uruchamiać `git` i opcjonalnie `gh`/`glab` dopiero po decyzji użytkownika.

### Czego `tagi` nie powinien robić

- zastępować `git add/commit/push`,
- implementować własnego modelu stanu repo poza `.git`,
- ukrywać jakie komendy wykona,
- zmieniać semantyki commit/push,
- zastępować workflow branch/rebase/merge.

## Proponowane komendy

```bash
tagi scan
tagi list
tagi inspect #small
tagi draft #small
tagi send #small
tagi publish #small
```

- `scan` — analiza zmian,
- `list` — lista paczek/tagów,
- `inspect` — podgląd paczki i ryzyka,
- `draft` — propozycja opisu i planu,
- `send` — stage/commit/(opcjonalnie) push po potwierdzeniu,
- `publish` — rozszerzenie o PR/MR przez provider.

## Architektura (kierunek)

```text
src/tagi/
  scanner/
  heuristics/
  planner/
  composer/
  executor/
  providers/
  llm/
```

- `scanner`: odczyt stanu repo,
- `heuristics`: tagi, scoring, ryzyko,
- `planner`: budowa paczek i preview,
- `composer`: opisy commitów,
- `executor`: cienka warstwa uruchamiająca `git`/`gh`/`glab`,
- `providers`: integracje GitHub/GitLab,
- `llm`: opcjonalna redakcja komunikatów.

## Minimalne MVP

- analiza `git status --porcelain`,
- podstawowe tagi: `#small`, `#new`, `#deps`, `#docs`, `#tests`, `#risky`,
- lista paczek zmian,
- podgląd planu wysyłki,
- draft commit message,
- `--dry-run` dla bezpieczeństwa.

Przykład:

```bash
tagi scan
tagi list
tagi inspect #small
tagi draft #small
tagi send #small --dry-run
```

## Definicja produktu

> `tagi` to orchestrator wysyłek zmian Git: analizuje nie wysłane pliki, grupuje je hashtagami, proponuje sensowne paczki commitów i uruchamia istniejące narzędzia Git/GitHub/GitLab do publikacji.
