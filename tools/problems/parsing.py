"""Turn a problem markdown file into a `Problem`.

Everything that knows about the layout of `templates/problem.md` lives here, so
a template change is a one-file change.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

from .models import Problem

#: `001-example-two-sum.md` -> number 1, slug `example-two-sum`.
FILENAME_RE = re.compile(r"^(?P<number>\d+)-(?P<slug>[^/]+)\.md$")

#: `- **Topic:** probability — Bayes`
FRONT_MATTER_RE = re.compile(r"^\s*[-*]\s*\*\*(?P<label>[^:*]+):?\*\*:?\s*(?P<value>.*)$")

TITLE_RE = re.compile(r"^#\s+(?P<title>.+?)\s*$")
HEADING_RE = re.compile(r"^(?P<hashes>#{1,6})\s+(?P<text>.+?)\s*$")

ATTEMPT_HEADING = "my attempt"

#: Lines the template leaves behind that must not be mistaken for real work:
#: `<Write your attempt here...>` placeholders, HTML comments, and rules.
PLACEHOLDER_RE = re.compile(r"^\s*(<[^>]*>|<!--.*?-->|-{3,}|\*{3,})\s*$")

FIELD_ALIASES = {
    "topic": "topic",
    "difficulty": "difficulty",
    "source": "source",
    "asked by": "asked_by",
    "attempts": "attempts_field",
}

EMPTY_MARKERS = {"", "-", "—", "–", "n/a", "none", "tbd", "?"}


def is_problem_file(path: Path) -> bool:
    return FILENAME_RE.match(path.name) is not None


def problem_key(section: str, category: str, number: int) -> str:
    """`math/probability/001` — identity that survives a slug rename."""
    area = f"{section}/{category}" if category else section
    return f"{area}/{number:03d}"


def _normalise_value(value: str) -> str:
    value = value.strip()
    return "" if value.lower() in EMPTY_MARKERS else value


def _split_sections(lines: list[str]) -> dict[str, list[str]]:
    """Map lowercased `##`-level heading -> its body lines.

    Fenced code blocks are skipped so a `# comment` inside python can't be read
    as a heading.
    """
    sections: dict[str, list[str]] = {}
    current: Optional[str] = None
    in_fence = False

    for line in lines:
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            if current is not None:
                sections[current].append(line)
            continue
        if in_fence:
            if current is not None:
                sections[current].append(line)
            continue

        heading = HEADING_RE.match(line)
        if heading and len(heading.group("hashes")) >= 2:
            current = heading.group("text").strip().lower()
            sections.setdefault(current, [])
            continue
        if current is not None:
            sections[current].append(line)

    return sections


def _body_before_solution(lines: list[str]) -> list[str]:
    """Drop everything from `<details>` on — the reference solution is not an attempt."""
    out = []
    for line in lines:
        if "<details" in line.lower():
            break
        out.append(line)
    return out


def has_content(lines: list[str]) -> bool:
    """True when a section holds anything the user actually wrote."""
    return any(
        line.strip() and not PLACEHOLDER_RE.match(line)
        for line in lines
    )


def parse_problem(path: Path, root: Path, text: Optional[str] = None) -> Problem:
    """Parse `path` into a `Problem`. `text` lets callers supply content directly."""
    match = FILENAME_RE.match(path.name)
    if match is None:
        raise ValueError(f"not a problem filename: {path.name}")

    if text is None:
        text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    relative = path.relative_to(root) if path.is_absolute() else path
    parts = relative.parts
    section = parts[0] if len(parts) > 1 else ""
    category = parts[1] if len(parts) > 2 else ""

    title = ""
    fields: dict[str, str] = {}
    for line in lines:
        if not title:
            title_match = TITLE_RE.match(line)
            if title_match:
                title = title_match.group("title").strip()
                continue
        front = FRONT_MATTER_RE.match(line)
        if front:
            key = FIELD_ALIASES.get(front.group("label").strip().lower())
            if key and key not in fields:
                fields[key] = _normalise_value(front.group("value"))
        elif line.startswith("## "):
            break  # front matter is over

    sections = _split_sections(lines)
    attempt_body = _body_before_solution(sections.get(ATTEMPT_HEADING, []))

    number = int(match.group("number"))
    return Problem(
        key=problem_key(section, category, number),
        path=relative,
        section=section,
        category=category,
        number=number,
        slug=match.group("slug"),
        title=title,
        topic=fields.get("topic", ""),
        difficulty=fields.get("difficulty", "").lower(),
        source=fields.get("source", ""),
        asked_by=fields.get("asked_by", ""),
        attempts_field=fields.get("attempts_field", ""),
        has_written_attempt=has_content(attempt_body),
    )
