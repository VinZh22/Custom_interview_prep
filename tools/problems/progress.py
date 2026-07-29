"""Read `progress/log.md` — the user's own record of attempts.

Read-only on purpose: CLAUDE.md forbids writing to the practice log.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable, Optional

from .models import AttemptRecord
from .parsing import FILENAME_RE, problem_key

#: `[math/probability/001](../math/probability/001-example-....md)`
LINK_RE = re.compile(r"\[(?P<label>[^\]]*)\]\((?P<target>[^)]+)\)")

#: `math/probability/001` or `math/probability/001-some-slug`
KEY_RE = re.compile(r"(?P<area>[a-z0-9][a-z0-9-]*(?:/[a-z0-9][a-z0-9-]*)?)/(?P<number>\d{1,4})\b")

SEPARATOR_RE = re.compile(r"^\s*\|?[\s:|-]+\|?\s*$")

TRUTHY = {"yes", "y", "true", "✓", "solved", "1"}


def _cells(line: str) -> list[str]:
    stripped = line.strip()
    if not stripped.startswith("|"):
        return []
    return [cell.strip() for cell in stripped.strip("|").split("|")]


def _key_from_target(target: str) -> Optional[str]:
    """Resolve a link target such as `../math/probability/001-x.md` to a key."""
    path = Path(target.split("#", 1)[0])
    parts = [p for p in path.parts if p not in ("..", ".", "")]
    if len(parts) < 2:
        return None
    match = FILENAME_RE.match(parts[-1])
    if match is None:
        return None
    number = int(match.group("number"))
    section = parts[-3] if len(parts) >= 3 else parts[-2]
    category = parts[-2] if len(parts) >= 3 else ""
    return problem_key(section, category, number)


def _key_from_text(text: str) -> Optional[str]:
    match = KEY_RE.search(text)
    if match is None:
        return None
    area = match.group("area").split("/")
    section = area[0]
    category = area[1] if len(area) > 1 else ""
    return problem_key(section, category, int(match.group("number")))


def parse_problem_reference(cell: str) -> Optional[str]:
    """Best-effort key for the `Problem` cell of a log row."""
    for link in LINK_RE.finditer(cell):
        key = _key_from_target(link.group("target")) or _key_from_text(link.group("label"))
        if key:
            return key
    return _key_from_text(cell)


def parse_log(text: str) -> list[AttemptRecord]:
    """Extract attempt rows from the practice log's markdown table(s).

    Header order is read from the table header rather than assumed, so adding a
    column to the log doesn't break this.
    """
    records: list[AttemptRecord] = []
    columns: list[str] = []

    for line in text.splitlines():
        cells = _cells(line)
        if not cells:
            columns = []
            continue
        if SEPARATOR_RE.match(line) and len(set("".join(cells))) <= 2:
            continue

        lowered = [c.lower() for c in cells]
        if "problem" in lowered and ("solved" in lowered or "date" in lowered):
            columns = lowered
            continue
        if not columns:
            continue

        row = dict(zip(columns, cells))
        key = parse_problem_reference(row.get("problem", ""))
        if not key:
            continue  # blank template row, or a summary line
        records.append(
            AttemptRecord(
                date=row.get("date", ""),
                problem_key=key,
                time=row.get("time", ""),
                solved=row.get("solved", "").strip().lower() in TRUTHY,
                note=row.get("note", ""),
            )
        )
    return records


def load_log(path: Path) -> list[AttemptRecord]:
    if not path.is_file():
        return []
    return parse_log(path.read_text(encoding="utf-8"))


def index_by_problem(records: Iterable[AttemptRecord]) -> dict[str, tuple[AttemptRecord, ...]]:
    grouped: dict[str, list[AttemptRecord]] = {}
    for record in records:
        grouped.setdefault(record.problem_key, []).append(record)
    return {key: tuple(value) for key, value in grouped.items()}
