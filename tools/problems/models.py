"""Domain objects: what a problem is, and what "solved" means.

Deliberately free of I/O so a future web app can build `Problem` values from a
database or an API response instead of from the filesystem.
"""

from __future__ import annotations

import enum
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Optional


class Status(str, enum.Enum):
    """Where a problem stands. Ordered from least to most progress.

    - `unsolved` — nothing written under "My attempt", no log entry.
    - `tried` — an attempt exists (or a failed log row) but it isn't solved.
    - `solved` — a ✓ in the front matter, or a `Solved: yes` row in the log.
    """

    UNSOLVED = "unsolved"
    TRIED = "tried"
    SOLVED = "solved"

    @property
    def is_solved(self) -> bool:
        return self is Status.SOLVED


#: Still to do — the default view. Named separately from `Status.UNSOLVED` so
#: "untouched" and "not yet solved" never get confused. The CLI, the repository
#: and any future HTTP layer all read it from here.
PENDING_STATUSES = (Status.UNSOLVED, Status.TRIED)

DIFFICULTIES = ("easy", "medium", "hard")


@dataclass(frozen=True)
class AttemptRecord:
    """One row of `progress/log.md`."""

    date: str
    problem_key: str
    time: str = ""
    solved: bool = False
    note: str = ""


@dataclass(frozen=True)
class Problem:
    """A single problem file, parsed.

    `key` is the stable identity — `math/probability/001` — so the practice log
    can point at a problem without depending on the slug, which may be renamed.
    """

    key: str
    path: Path
    section: str
    category: str
    number: int
    slug: str
    title: str = ""
    topic: str = ""
    difficulty: str = ""
    source: str = ""
    asked_by: str = ""
    attempts_field: str = ""
    has_written_attempt: bool = False
    attempts: tuple[AttemptRecord, ...] = field(default_factory=tuple)

    @property
    def status(self) -> Status:
        """Solved beats attempted beats untouched.

        A ✓ in the front-matter `Attempts:` line or a `Solved: yes` row in the
        practice log both count as solved; prose under "My attempt" only counts
        as attempted.
        """
        if any(a.solved for a in self.attempts) or "✓" in self.attempts_field:
            return Status.SOLVED
        if self.has_written_attempt or self.attempts or "✗" in self.attempts_field:
            return Status.TRIED
        return Status.UNSOLVED

    @property
    def is_solved(self) -> bool:
        return self.status.is_solved

    @property
    def area(self) -> str:
        """`math/probability` — the folder that owns the problem."""
        return f"{self.section}/{self.category}" if self.category else self.section

    @property
    def last_attempted(self) -> Optional[str]:
        dates = sorted(a.date for a in self.attempts if a.date)
        return dates[-1] if dates else None

    def to_dict(self) -> dict:
        """JSON-serialisable view — the shape a web API would return."""
        return {
            "key": self.key,
            "path": str(self.path),
            "section": self.section,
            "category": self.category,
            "area": self.area,
            "number": self.number,
            "slug": self.slug,
            "title": self.title,
            "topic": self.topic,
            "difficulty": self.difficulty,
            "source": self.source,
            "asked_by": self.asked_by,
            "status": self.status.value,
            "has_written_attempt": self.has_written_attempt,
            "attempt_count": len(self.attempts),
            "last_attempted": self.last_attempted,
        }


def sort_key(problem: Problem) -> tuple:
    """Stable display order: section, then category, then number."""
    return (problem.section, problem.category, problem.number, problem.slug)


def group_by_area(problems: Iterable[Problem]) -> dict[str, list[Problem]]:
    grouped: dict[str, list[Problem]] = {}
    for problem in sorted(problems, key=sort_key):
        grouped.setdefault(problem.area, []).append(problem)
    return grouped
