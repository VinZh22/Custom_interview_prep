"""Where problems come from.

`ProblemSource` is the seam that keeps this scalable: today the only
implementation walks the repo, but a web app can drop in one backed by a
database, a cache or an HTTP call without touching the repository or CLI.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, List, Protocol, Sequence

from .models import AttemptRecord, Problem
from .parsing import is_problem_file, parse_problem
from .progress import load_log

#: Folders that never hold problems. Skipped whole, so a big `.venv` costs nothing.
DEFAULT_EXCLUDED_DIRS = frozenset(
    {
        ".git",
        ".venv",
        "venv",
        ".pytest_cache",
        "__pycache__",
        ".claude",
        ".idea",
        ".vscode",
        "node_modules",
        "templates",
        "progress",
        "resources",
        "mock-interviews",
        "tools",
        "lib",
        "tests",
    }
)

DEFAULT_LOG_PATH = Path("progress/log.md")


class ProblemSource(Protocol):
    """Anything that can produce problems and the attempt history for them."""

    def load_problems(self) -> Sequence[Problem]:
        ...

    def load_attempts(self) -> Sequence[AttemptRecord]:
        ...


class FilesystemProblemSource:
    """Walks the repo for `NNN-slug.md` files under the content sections."""

    def __init__(
        self,
        root: Path,
        excluded_dirs: Iterable[str] = DEFAULT_EXCLUDED_DIRS,
        log_path: Path = DEFAULT_LOG_PATH,
    ) -> None:
        self.root = Path(root).resolve()
        self.excluded_dirs = frozenset(excluded_dirs)
        self.log_path = log_path

    def iter_problem_paths(self) -> Iterable[Path]:
        stack = [self.root]
        while stack:
            directory = stack.pop()
            try:
                entries = sorted(directory.iterdir())
            except (PermissionError, FileNotFoundError):
                continue
            for entry in entries:
                if entry.is_dir():
                    if entry.name not in self.excluded_dirs and not entry.name.startswith("."):
                        stack.append(entry)
                elif entry.suffix == ".md" and is_problem_file(entry):
                    yield entry

    def load_problems(self) -> List[Problem]:
        problems = []
        for path in self.iter_problem_paths():
            try:
                problems.append(parse_problem(path, self.root))
            except (ValueError, OSError, UnicodeDecodeError):
                continue  # malformed file shouldn't take the whole listing down
        return problems

    def load_attempts(self) -> List[AttemptRecord]:
        return load_log(self.root / self.log_path)


def find_repo_root(start: Path | None = None) -> Path:
    """Nearest ancestor holding a `CLAUDE.md` (falling back to a `.git`)."""
    current = Path(start or Path.cwd()).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "CLAUDE.md").is_file() or (candidate / ".git").exists():
            return candidate
    return current
