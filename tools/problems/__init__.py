"""Catalogue of the problems in this repo, and what state each one is in.

Three states, resolved in `Problem.status`: `unsolved` (nothing written),
`tried` (an attempt exists but isn't solved), `solved`.

    from tools.problems import ProblemRepository

    repo = ProblemRepository.from_path()
    for problem in repo.pending():           # unsolved + tried
        print(problem.path, problem.status.value)

Layers, so a website can reuse everything below the CLI:

- `models`     — `Problem`, `Status`, `AttemptRecord` (no I/O)
- `parsing`    — problem markdown -> `Problem`
- `progress`   — `progress/log.md` -> `AttemptRecord`s (read-only)
- `sources`    — `ProblemSource` protocol + the filesystem implementation
- `repository` — load-once index with filters and stats
- `cli`        — argparse front end, presentation only
"""

from .models import (
    PENDING_STATUSES,
    AttemptRecord,
    Problem,
    Status,
    group_by_area,
)
from .repository import ProblemRepository, unsolved_paths
from .sources import FilesystemProblemSource, ProblemSource, find_repo_root

__all__ = [
    "AttemptRecord",
    "FilesystemProblemSource",
    "PENDING_STATUSES",
    "Problem",
    "ProblemRepository",
    "ProblemSource",
    "Status",
    "find_repo_root",
    "group_by_area",
    "unsolved_paths",
]
