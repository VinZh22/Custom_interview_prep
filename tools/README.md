# tools

Workspace tooling — not interview material, and not part of the problem count.

## `tools/problems` — what's left to solve

Scans the content folders for `NNN-slug.md` files, cross-references
[progress/log.md](../progress/log.md), and reports each problem in one of three states:

| Status | Meaning | Detected from |
| --- | --- | --- |
| `unsolved` | Untouched | Nothing but template placeholders under `## My attempt`, no log row |
| `tried` | Attempted, not solved | Prose under `## My attempt`, a `✗` in `Attempts:`, or a `Solved: No` log row |
| `solved` | Done | A `✓` in `Attempts:`, or a `Solved: Yes` log row |

Text below the `<details>` fold is never read as an attempt, so the reference solution
can't mark a problem as tried.

### CLI

```bash
python -m tools.problems                          # paths still to do (unsolved + tried)
python -m tools.problems --status unsolved         # untouched only
python -m tools.problems --status tried            # attempted, not cracked
python -m tools.problems stats                     # counts per status and per area
python -m tools.problems areas                     # the folders in play

python -m tools.problems --section math --format table
python -m tools.problems --area math/probability --status all --format grouped
python -m tools.problems --difficulty medium --difficulty hard
python -m tools.problems --topic bayes
python -m tools.problems --random -n 1             # pick something to work on now
python -m tools.problems -n 1 --format json        # machine-readable
```

`--status` takes a comma-separated list plus the aliases `pending`/`todo`
(= `unsolved,tried`) and `all`. Formats: `paths` (default), `table`, `grouped`, `json`.

### Python

```python
from tools.problems import ProblemRepository, Status

repo = ProblemRepository.from_path()
repo.pending()                       # unsolved + tried
repo.unsolved(section="math")        # untouched, filtered
repo.tried()
repo.paths(repo.pending())          # just the Paths
repo.stats()                         # dashboard payload
repo.get("math/probability/001")
repo.reload()                        # results are cached until you ask for a refresh
```

Or the one-liner: `from tools.problems import unsolved_paths; unsolved_paths()`.

### Layers

Built so the CLI can be replaced by a web or app front end without rewriting anything
underneath it:

| Module | Role |
| --- | --- |
| [problems/models.py](problems/models.py) | `Problem`, `Status`, `AttemptRecord`. Pure data, no I/O. `to_dict()` is the API shape. |
| [problems/parsing.py](problems/parsing.py) | Problem markdown → `Problem`. All knowledge of [templates/problem.md](../templates/problem.md) is here. |
| [problems/progress.py](problems/progress.py) | Practice log → `AttemptRecord`s. Read-only — the log is the user's. |
| [problems/sources.py](problems/sources.py) | `ProblemSource` protocol + `FilesystemProblemSource`. The seam: swap in a DB or HTTP backend. |
| [problems/repository.py](problems/repository.py) | Load-once index, filters, stats. What a web handler should call. |
| [problems/cli.py](problems/cli.py) | argparse + formatters. Presentation only. |

Problems are keyed `section/category/NNN` (`math/probability/001`) rather than by filename,
so renaming a slug doesn't break log cross-references.

Stdlib only — no dependency on pandas or anything in `requirements.txt`.

Tests: [tests/test_problems.py](tests/test_problems.py) — `pytest -k problems`.
