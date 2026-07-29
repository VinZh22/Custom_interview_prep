"""Query layer: load once, then filter.

This is the API a CLI, a web handler or a notebook should use. It holds no
formatting logic and no filesystem knowledge of its own.
"""

from __future__ import annotations

import random
from dataclasses import replace
from pathlib import Path
from typing import Iterable, List, Optional, Sequence

from .models import PENDING_STATUSES, Problem, Status, group_by_area, sort_key
from .progress import index_by_problem
from .sources import FilesystemProblemSource, ProblemSource, find_repo_root


class ProblemRepository:
    """In-memory index over a `ProblemSource`, with a lazy load and `reload()`."""

    def __init__(self, source: ProblemSource) -> None:
        self.source = source
        self._problems: Optional[List[Problem]] = None

    @classmethod
    def from_path(cls, root: Optional[Path] = None) -> "ProblemRepository":
        return cls(FilesystemProblemSource(find_repo_root(root)))

    def reload(self) -> "ProblemRepository":
        self._problems = None
        return self

    def all(self) -> List[Problem]:
        """Every problem, with its attempt history attached."""
        if self._problems is None:
            attempts = index_by_problem(self.source.load_attempts())
            problems = [
                problem
                if problem.key not in attempts
                else replace(problem, attempts=attempts[problem.key])
                for problem in self.source.load_problems()
            ]
            self._problems = sorted(problems, key=sort_key)
        return list(self._problems)

    def query(
        self,
        statuses: Optional[Iterable[Status]] = None,
        section: Optional[str] = None,
        category: Optional[str] = None,
        area: Optional[str] = None,
        difficulty: Optional[Iterable[str]] = None,
        topic: Optional[str] = None,
        limit: Optional[int] = None,
        shuffle_seed: Optional[int] = None,
    ) -> List[Problem]:
        """Filter the catalogue. All criteria are ANDed; `None` means no filter."""
        status_set = set(statuses) if statuses is not None else None
        difficulty_set = {d.lower() for d in difficulty} if difficulty else None
        needle = topic.lower() if topic else None

        results = []
        for problem in self.all():
            if status_set is not None and problem.status not in status_set:
                continue
            if section and problem.section != section:
                continue
            if category and problem.category != category:
                continue
            if area and problem.area != area.strip("/"):
                continue
            if difficulty_set is not None and problem.difficulty not in difficulty_set:
                continue
            if needle and needle not in f"{problem.topic} {problem.title}".lower():
                continue
            results.append(problem)

        if shuffle_seed is not None:
            random.Random(shuffle_seed).shuffle(results)
        return results[:limit] if limit else results

    # Convenience wrappers — the three states, named as the user names them.

    def unsolved(self, **kwargs) -> List[Problem]:
        """Untouched only."""
        return self.query(statuses=[Status.UNSOLVED], **kwargs)

    def tried(self, **kwargs) -> List[Problem]:
        """Attempted but not solved."""
        return self.query(statuses=[Status.TRIED], **kwargs)

    def solved(self, **kwargs) -> List[Problem]:
        return self.query(statuses=[Status.SOLVED], **kwargs)

    def pending(self, **kwargs) -> List[Problem]:
        """Everything still to do: `unsolved` + `tried`."""
        return self.query(statuses=PENDING_STATUSES, **kwargs)

    def paths(self, problems: Optional[Sequence[Problem]] = None) -> List[Path]:
        """Repo-relative paths — the plain answer to "what can I work on"."""
        return [p.path for p in (problems if problems is not None else self.pending())]

    def get(self, key: str) -> Optional[Problem]:
        for problem in self.all():
            if problem.key == key:
                return problem
        return None

    def areas(self) -> List[str]:
        return sorted(group_by_area(self.all()))

    def stats(self) -> dict:
        """Counts per status, overall and per area — the shape a dashboard wants."""
        problems = self.all()
        overall = {status.value: 0 for status in Status}
        per_area: dict[str, dict] = {}
        for problem in problems:
            overall[problem.status.value] += 1
            bucket = per_area.setdefault(
                problem.area, {status.value: 0 for status in Status}
            )
            bucket[problem.status.value] += 1
        return {"total": len(problems), "by_status": overall, "by_area": per_area}


def unsolved_paths(root: Optional[Path] = None, include_tried: bool = True) -> List[Path]:
    """One-liner for scripts: paths of everything not yet solved."""
    repo = ProblemRepository.from_path(root)
    return repo.paths(repo.pending() if include_tried else repo.unsolved())
