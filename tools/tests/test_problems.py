"""Tests for the problem catalogue.

Most tests build a throwaway repo in a tmpdir so they don't drift when real
problems are added; the last few assert against the actual workspace.
"""

from pathlib import Path

import pytest

from tools.problems import ProblemRepository, Status, unsolved_paths
from tools.problems.cli import main, parse_statuses
from tools.problems.parsing import parse_problem
from tools.problems.progress import parse_log, parse_problem_reference
from tools.problems.sources import FilesystemProblemSource

UNTOUCHED = """\
# Two Sum

- **Topic:** arrays, hash map
- **Difficulty:** easy
- **Source:** classic
- **Asked by:** everyone
- **Attempts:** —

## Statement

Given an array, return indices summing to target.

## My attempt

<Write your attempt here before opening the solution.>

---

<details>
<summary>Solution</summary>

## Idea

Use a hash map. This text lives below the fold and must not count as an attempt.

</details>
"""

TRIED = UNTOUCHED.replace(
    "<Write your attempt here before opening the solution.>",
    "<Write your attempt here before opening the solution.>\n\nI tried sorting first, "
    "then two pointers, but that loses the original indices.",
)

SOLVED_BY_FIELD = UNTOUCHED.replace("- **Attempts:** —", "- **Attempts:** 2026-07-01 ✓")


def write_repo(tmp_path: Path, files: dict, log: str = "") -> Path:
    (tmp_path / "CLAUDE.md").write_text("root marker", encoding="utf-8")
    for relative, content in files.items():
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    if log:
        (tmp_path / "progress").mkdir(exist_ok=True)
        (tmp_path / "progress" / "log.md").write_text(log, encoding="utf-8")
    return tmp_path


@pytest.fixture
def repo(tmp_path):
    root = write_repo(
        tmp_path,
        {
            "coding/algorithms/001-two-sum.md": UNTOUCHED,
            "coding/algorithms/002-sliding-window.md": TRIED,
            "math/probability/001-coupons.md": SOLVED_BY_FIELD,
            "math/probability/002-bayes.md": UNTOUCHED,
            "templates/problem.md": UNTOUCHED,  # excluded folder
            "math/README.md": "# not a problem",  # wrong filename shape
        },
    )
    return ProblemRepository(FilesystemProblemSource(root))


# --- parsing ---------------------------------------------------------------


def test_front_matter_and_identity(tmp_path):
    path = tmp_path / "math" / "probability" / "007-coupon-collector.md"
    path.parent.mkdir(parents=True)
    path.write_text(UNTOUCHED, encoding="utf-8")

    problem = parse_problem(path, tmp_path)

    assert problem.key == "math/probability/007"
    assert problem.number == 7
    assert problem.slug == "coupon-collector"
    assert problem.section == "math"
    assert problem.category == "probability"
    assert problem.area == "math/probability"
    assert problem.title == "Two Sum"
    assert problem.difficulty == "easy"
    assert problem.topic == "arrays, hash map"
    assert problem.attempts_field == ""  # em-dash normalised to empty


def test_placeholder_attempt_is_not_an_attempt(tmp_path):
    path = tmp_path / "a" / "b" / "001-x.md"
    path.parent.mkdir(parents=True)
    path.write_text(UNTOUCHED, encoding="utf-8")
    assert parse_problem(path, tmp_path).status is Status.UNSOLVED


def test_prose_under_my_attempt_means_tried(tmp_path):
    path = tmp_path / "a" / "b" / "001-x.md"
    path.parent.mkdir(parents=True)
    path.write_text(TRIED, encoding="utf-8")
    assert parse_problem(path, tmp_path).status is Status.TRIED


def test_solution_body_never_counts_as_an_attempt(tmp_path):
    """The reference solution sits after `<details>` and must be ignored."""
    path = tmp_path / "a" / "b" / "001-x.md"
    path.parent.mkdir(parents=True)
    path.write_text(UNTOUCHED, encoding="utf-8")
    problem = parse_problem(path, tmp_path)
    assert problem.has_written_attempt is False


def test_check_mark_in_front_matter_means_solved(tmp_path):
    path = tmp_path / "a" / "b" / "001-x.md"
    path.parent.mkdir(parents=True)
    path.write_text(SOLVED_BY_FIELD, encoding="utf-8")
    assert parse_problem(path, tmp_path).status is Status.SOLVED


def test_cross_mark_in_front_matter_means_tried(tmp_path):
    path = tmp_path / "a" / "b" / "001-x.md"
    path.parent.mkdir(parents=True)
    path.write_text(UNTOUCHED.replace("**Attempts:** —", "**Attempts:** 2026-07-01 ✗"),
                    encoding="utf-8")
    assert parse_problem(path, tmp_path).status is Status.TRIED


def test_rejects_non_problem_filename(tmp_path):
    with pytest.raises(ValueError):
        parse_problem(tmp_path / "README.md", tmp_path)


# --- practice log ----------------------------------------------------------

LOG = """\
# Practice log

| Date | Problem | Time | Solved | Note |
| --- | --- | --- | --- | --- |
| 2026-07-28 | [math/probability/001](../math/probability/001-coupons.md) | 10 minutes | Yes | clean |
| 2026-07-27 | [coding/algorithms/001](../coding/algorithms/001-two-sum.md) | 25 min | No | missed the map |
| | | | | |
"""


def test_parse_log_reads_rows_and_skips_blanks():
    records = parse_log(LOG)
    assert len(records) == 2
    solved = {r.problem_key: r.solved for r in records}
    assert solved == {"math/probability/001": True, "coding/algorithms/001": False}
    assert records[0].date == "2026-07-28"
    assert records[1].note == "missed the map"


def test_parse_log_is_robust_to_extra_columns():
    text = LOG.replace("| Note |", "| Note | Mood |").replace("| clean |", "| clean | good |")
    records = parse_log(text)
    assert records[0].problem_key == "math/probability/001"
    assert records[0].solved is True


@pytest.mark.parametrize(
    "cell, expected",
    [
        ("[math/probability/001](../math/probability/001-x.md)", "math/probability/001"),
        ("math/probability/1", "math/probability/001"),
        ("[label](../math/probability/012-y.md)", "math/probability/012"),
        ("", None),
        ("no reference here", None),
    ],
)
def test_problem_reference_parsing(cell, expected):
    assert parse_problem_reference(cell) == expected


def test_log_marks_problem_solved_even_when_file_says_nothing(tmp_path):
    root = write_repo(
        tmp_path,
        {"math/probability/001-coupons.md": UNTOUCHED},
        log=LOG,
    )
    repo = ProblemRepository(FilesystemProblemSource(root))
    problem = repo.get("math/probability/001")
    assert problem.status is Status.SOLVED
    assert problem.last_attempted == "2026-07-28"


def test_failed_log_row_makes_it_tried(tmp_path):
    root = write_repo(
        tmp_path,
        {"coding/algorithms/001-two-sum.md": UNTOUCHED},
        log=LOG,
    )
    repo = ProblemRepository(FilesystemProblemSource(root))
    assert repo.get("coding/algorithms/001").status is Status.TRIED


def test_missing_log_is_not_an_error(tmp_path):
    root = write_repo(tmp_path, {"math/probability/001-x.md": UNTOUCHED})
    assert FilesystemProblemSource(root).load_attempts() == []


# --- repository ------------------------------------------------------------


def test_discovery_skips_templates_and_non_problem_files(repo):
    keys = [p.key for p in repo.all()]
    assert keys == [
        "coding/algorithms/001",
        "coding/algorithms/002",
        "math/probability/001",
        "math/probability/002",
    ]


def test_three_statuses_partition_the_catalogue(repo):
    assert [p.key for p in repo.unsolved()] == [
        "coding/algorithms/001",
        "math/probability/002",
    ]
    assert [p.key for p in repo.tried()] == ["coding/algorithms/002"]
    assert [p.key for p in repo.solved()] == ["math/probability/001"]
    assert len(repo.unsolved()) + len(repo.tried()) + len(repo.solved()) == len(repo.all())


def test_pending_is_unsolved_plus_tried(repo):
    assert [p.key for p in repo.pending()] == [
        "coding/algorithms/001",
        "coding/algorithms/002",
        "math/probability/002",
    ]


def test_paths_are_repo_relative(repo):
    assert repo.paths(repo.unsolved()) == [
        Path("coding/algorithms/001-two-sum.md"),
        Path("math/probability/002-bayes.md"),
    ]


def test_filters_compose(repo):
    assert [p.key for p in repo.pending(section="math")] == ["math/probability/002"]
    assert [p.key for p in repo.pending(area="math/probability")] == ["math/probability/002"]
    assert [p.key for p in repo.pending(difficulty=["easy"])] == [
        "coding/algorithms/001",
        "coding/algorithms/002",
        "math/probability/002",
    ]
    assert repo.pending(difficulty=["hard"]) == []
    assert [p.key for p in repo.pending(topic="hash map")] == [
        "coding/algorithms/001",
        "coding/algorithms/002",
        "math/probability/002",
    ]
    assert repo.pending(topic="markov") == []


def test_limit_and_seeded_shuffle(repo):
    assert len(repo.pending(limit=2)) == 2
    first = [p.key for p in repo.pending(shuffle_seed=7)]
    second = [p.key for p in repo.pending(shuffle_seed=7)]
    assert first == second
    assert sorted(first) == sorted(p.key for p in repo.pending())


def test_stats_counts_by_status_and_area(repo):
    stats = repo.stats()
    assert stats["total"] == 4
    assert stats["by_status"] == {"unsolved": 2, "tried": 1, "solved": 1}
    assert stats["by_area"]["math/probability"] == {"unsolved": 1, "tried": 0, "solved": 1}


def test_areas_and_get(repo):
    assert repo.areas() == ["coding/algorithms", "math/probability"]
    assert repo.get("math/probability/002").slug == "bayes"
    assert repo.get("nope/000") is None


def test_reload_picks_up_a_new_problem(repo, tmp_path):
    before = len(repo.all())
    (tmp_path / "math" / "probability" / "003-new.md").write_text(UNTOUCHED, encoding="utf-8")
    assert len(repo.all()) == before, "results are cached until reload()"
    assert len(repo.reload().all()) == before + 1


def test_malformed_file_does_not_break_the_listing(repo, tmp_path):
    (tmp_path / "math" / "probability" / "004-empty.md").write_text("", encoding="utf-8")
    problems = repo.reload().all()
    assert "math/probability/004" in {p.key for p in problems}
    assert repo.get("math/probability/004").status is Status.UNSOLVED


def test_custom_source_needs_no_filesystem():
    """The Protocol is the seam a website would use."""

    class InMemorySource:
        def load_problems(self):
            return [parse_problem(Path("math/probability/001-x.md"), Path("."), UNTOUCHED)]

        def load_attempts(self):
            return []

    repo = ProblemRepository(InMemorySource())
    assert [p.key for p in repo.unsolved()] == ["math/probability/001"]


# --- CLI -------------------------------------------------------------------


def test_parse_statuses_and_aliases():
    assert parse_statuses("unsolved") == [Status.UNSOLVED]
    assert parse_statuses("unsolved,tried") == [Status.UNSOLVED, Status.TRIED]
    assert parse_statuses("pending") == [Status.UNSOLVED, Status.TRIED]
    assert parse_statuses("todo") == [Status.UNSOLVED, Status.TRIED]
    assert set(parse_statuses("all")) == set(Status)
    assert parse_statuses("tried,tried") == [Status.TRIED]


def test_parse_statuses_rejects_junk():
    import argparse

    with pytest.raises(argparse.ArgumentTypeError):
        parse_statuses("almost")


def test_cli_default_prints_pending_paths(tmp_path, capsys):
    root = write_repo(
        tmp_path,
        {
            "coding/algorithms/001-two-sum.md": UNTOUCHED,
            "math/probability/001-coupons.md": SOLVED_BY_FIELD,
        },
    )
    assert main(["--root", str(root)]) == 0
    out = capsys.readouterr().out.split()
    assert out == ["coding/algorithms/001-two-sum.md"]


def test_cli_json_and_table_formats(tmp_path, capsys):
    import json

    root = write_repo(tmp_path, {"coding/algorithms/001-two-sum.md": TRIED})

    main(["--root", str(root), "--status", "tried", "--format", "json"])
    payload = json.loads(capsys.readouterr().out)
    assert payload[0]["status"] == "tried"
    assert payload[0]["key"] == "coding/algorithms/001"

    main(["--root", str(root), "--status", "all", "--format", "table"])
    assert "Two Sum" in capsys.readouterr().out


def test_cli_stats_and_areas(tmp_path, capsys):
    root = write_repo(tmp_path, {"coding/algorithms/001-two-sum.md": UNTOUCHED})
    main(["stats", "--root", str(root)])
    assert "1 unsolved" in capsys.readouterr().out
    main(["areas", "--root", str(root)])
    assert capsys.readouterr().out.strip() == "coding/algorithms"


def test_cli_absolute_paths(tmp_path, capsys):
    root = write_repo(tmp_path, {"coding/algorithms/001-two-sum.md": UNTOUCHED})
    main(["--root", str(root), "--absolute"])
    assert Path(capsys.readouterr().out.strip()).is_absolute()


# --- the real workspace ----------------------------------------------------


def test_real_repo_is_discovered():
    repo = ProblemRepository.from_path(Path(__file__).parent)
    problems = repo.all()
    assert problems, "should find the problems in this repo"
    assert all(p.section and p.category for p in problems)
    assert all(p.title for p in problems)
    # nothing from excluded trees
    assert not any(
        part in {".venv", "templates", "tools"} for p in problems for part in p.path.parts
    )


def test_real_repo_statuses_partition_and_helper_agrees():
    repo = ProblemRepository.from_path(Path(__file__).parent)
    assert len(repo.unsolved()) + len(repo.tried()) + len(repo.solved()) == len(repo.all())
    here = Path(__file__).parent
    assert set(unsolved_paths(here)) == set(repo.paths(repo.pending()))
    assert set(unsolved_paths(here, include_tried=False)) == set(repo.paths(repo.unsolved()))
