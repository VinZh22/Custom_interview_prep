"""Command line front end. Presentation only — all logic lives in the repository.

    python -m tools.problems                      # paths still to do
    python -m tools.problems --status unsolved    # untouched only
    python -m tools.problems --format table --section math
    python -m tools.problems stats
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import replace
from pathlib import Path
from typing import List, Optional, Sequence

from .models import DIFFICULTIES, PENDING_STATUSES, Problem, Status, group_by_area
from .repository import ProblemRepository

STATUS_ALIASES = {
    "unsolved": [Status.UNSOLVED],
    "tried": [Status.TRIED],
    "solved": [Status.SOLVED],
    "pending": list(PENDING_STATUSES),
    "todo": list(PENDING_STATUSES),
    "all": list(Status),
}

STATUS_MARKS = {Status.UNSOLVED: "·", Status.TRIED: "~", Status.SOLVED: "✓"}


def parse_statuses(value: str) -> List[Status]:
    """`--status unsolved,tried` -> the two statuses. Aliases: pending, todo, all."""
    statuses: List[Status] = []
    for token in value.split(","):
        token = token.strip().lower()
        if not token:
            continue
        if token not in STATUS_ALIASES:
            raise argparse.ArgumentTypeError(
                f"unknown status {token!r}; choose from "
                f"{', '.join(sorted(STATUS_ALIASES))}"
            )
        for status in STATUS_ALIASES[token]:
            if status not in statuses:
                statuses.append(status)
    if not statuses:
        raise argparse.ArgumentTypeError("--status needs at least one value")
    return statuses


def format_paths(problems: Sequence[Problem]) -> str:
    return "\n".join(str(p.path) for p in problems)


def format_json(problems: Sequence[Problem]) -> str:
    return json.dumps([p.to_dict() for p in problems], indent=2, ensure_ascii=False)


def format_table(problems: Sequence[Problem]) -> str:
    if not problems:
        return "No problems match."
    rows = [
        (
            STATUS_MARKS[p.status],
            str(p.path),
            p.difficulty or "-",
            p.title or p.slug,
        )
        for p in problems
    ]
    widths = [max(len(row[i]) for row in rows) for i in range(3)]
    return "\n".join(
        f"{r[0]:<{widths[0]}}  {r[1]:<{widths[1]}}  {r[2]:<{widths[2]}}  {r[3]}"
        for r in rows
    )


def format_grouped(problems: Sequence[Problem]) -> str:
    if not problems:
        return "No problems match."
    blocks = []
    for area, group in group_by_area(problems).items():
        lines = [f"{area}  ({len(group)})"]
        lines += [
            f"  {STATUS_MARKS[p.status]} {p.number:03d}  {p.title or p.slug}"
            f"{'  [' + p.difficulty + ']' if p.difficulty else ''}"
            for p in group
        ]
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks)


FORMATTERS = {
    "paths": format_paths,
    "table": format_table,
    "grouped": format_grouped,
    "json": format_json,
}


def format_stats(stats: dict) -> str:
    by_status = stats["by_status"]
    header = (
        f"{stats['total']} problems — "
        f"{by_status['unsolved']} unsolved · {by_status['tried']} tried · "
        f"{by_status['solved']} solved"
    )
    lines = [header, ""]
    width = max((len(a) for a in stats["by_area"]), default=0)
    for area, counts in sorted(stats["by_area"].items()):
        lines.append(
            f"{area:<{width}}  {counts['unsolved']:>3} unsolved  "
            f"{counts['tried']:>3} tried  {counts['solved']:>3} solved"
        )
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m tools.problems",
        description="List interview problems in this repo by status.",
    )
    parser.add_argument(
        "command",
        nargs="?",
        default="list",
        choices=["list", "stats", "areas"],
        help="list (default), stats, or areas",
    )
    parser.add_argument(
        "--status",
        type=parse_statuses,
        default=list(PENDING_STATUSES),
        help="comma-separated: unsolved, tried, solved, pending (default), all",
    )
    parser.add_argument("--section", help="e.g. math, coding, quant")
    parser.add_argument("--category", help="e.g. probability, algorithms")
    parser.add_argument("--area", help="section/category, e.g. math/probability")
    parser.add_argument(
        "--difficulty",
        action="append",
        choices=list(DIFFICULTIES),
        help="repeatable",
    )
    parser.add_argument("--topic", help="substring match on topic and title")
    parser.add_argument("-n", "--limit", type=int, help="cap the number of results")
    parser.add_argument(
        "--random",
        dest="seed",
        nargs="?",
        type=int,
        const=0,
        help="shuffle results; optional integer seed for reproducibility",
    )
    parser.add_argument(
        "-f",
        "--format",
        choices=list(FORMATTERS),
        default="paths",
        help="paths (default), table, grouped, json",
    )
    parser.add_argument(
        "--root",
        type=Path,
        help="repo root (default: nearest ancestor with CLAUDE.md)",
    )
    parser.add_argument(
        "--absolute",
        action="store_true",
        help="print absolute paths",
    )
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    repo = ProblemRepository.from_path(args.root)

    if args.command == "stats":
        print(format_stats(repo.stats()))
        return 0
    if args.command == "areas":
        print("\n".join(repo.areas()))
        return 0

    problems = repo.query(
        statuses=args.status,
        section=args.section,
        category=args.category,
        area=args.area,
        difficulty=args.difficulty,
        topic=args.topic,
        limit=args.limit,
        shuffle_seed=args.seed,
    )

    if args.absolute:
        root = repo.source.root
        problems = [
            p if p.path.is_absolute() else replace(p, path=root / p.path)
            for p in problems
        ]

    output = FORMATTERS[args.format](problems)
    if output:
        print(output)
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
