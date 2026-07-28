# CLAUDE.md

Interview-prep workspace for tech and quant interviews. This file tells you how to move
around it and how to behave in it.

## Two modes, and you must be in exactly one

Everything you do here is either **tutoring** (the user is solving) or **setting**
(you are producing new material). They have opposite rules about revealing answers, so
never blur them.

| Mode | Skill | Use when |
| --- | --- | --- |
| Tutor | `tutor` — [.claude/skills/tutor/SKILL.md](.claude/skills/tutor/SKILL.md) | The user is working a problem and wants help. **Never give the full answer.** |
| Problem setter | `problem-setter` — [.claude/skills/problem-setter/SKILL.md](.claude/skills/problem-setter/SKILL.md) | The user wants a new problem written into the repo. Solve it yourself first. |

Invoke the skill; don't reimplement it from memory. If the user's intent is ambiguous —
they paste a problem with no instruction — assume **tutor**, and ask before revealing
anything.

### The one rule that overrides convenience

When tutoring, a full solution is a failure even if the user asks for one. Escalate hints
instead. The only exception: the user has produced a complete attempt and explicitly asks
to compare against the reference — then walk the existing `<details>` block with them.

## Repo map

| Path | Contents |
| --- | --- |
| [math/](math/) | probability · statistics · linear-algebra · calculus-optimization · combinatorics · brainteasers |
| [coding/](coding/) | algorithms · data-structures · data-manipulation · system-design |
| [data-science/](data-science/) | ml-theory · experimentation · case-studies · product-analytics |
| [quant/](quant/) | market-making · derivatives · time-series · mental-math |
| [behavioral/](behavioral/) | stories · company-notes |
| [coding/lib/](coding/lib/), [coding/tests/](coding/tests/) | Runnable implementations + pytest suite |
| [templates/](templates/) | `problem.md`, `behavioral-star.md`, `mock-interview.md` |
| [progress/](progress/) | `log.md` (attempts), `review-queue.md` (spaced repetition) |
| [mock-interviews/](mock-interviews/) | Timed session write-ups |
| [resources/](resources/) | Books and links, with a position marker |

Each sub-category has a skill of the same name describing its scope, core techniques, and
what a good problem in it looks like. Read that skill before writing or tutoring a problem
in that area — e.g. `probability`, `algorithms`, `market-making`, `experimentation`.
They live in [.claude/skills/](.claude/skills/).

## Conventions

- **One problem per file**, named `NNN-slug.md`, numbered per folder. Next number = highest
  existing + 1 in that folder; check with `ls` before writing.
- **Structure comes from [templates/problem.md](templates/problem.md)**: front-matter block,
  statement, empty "My attempt" section, solution inside `<details>`, follow-ups,
  notes-to-self. Never put the answer above the `<details>` fold — not in the statement, not
  in the title, not in an aside.
- **Difficulty** (`easy|medium|hard`) is the user's experienced difficulty, not a public
  rating.
- **Code is executed, not just written.** Implementations go in `coding/lib/<module>.py`,
  tests in `coding/tests/test_<module>.py`, and the problem file links to both. Run
  `pytest -k <module>` before claiming it works.
- **Cross-link** related problems with relative paths, and link back to the technique in the
  parent section README.

## No SQL — use pandas

The user does not want SQL. Anything that would naturally be a query is written as pandas:

- [coding/data-manipulation/](coding/data-manipulation/) — the mechanics: `groupby`/`agg`,
  `merge`, reshaping, `MultiIndex`, window and rolling ops, vectorization.
- [data-science/product-analytics/](data-science/product-analytics/) — the analyses those
  mechanics serve: funnels, retention/cohorts, attribution.

Never write a `SELECT` statement in this repo, and don't suggest "the SQL equivalent" as a
teaching aid.

## Running things

```bash
source .venv/bin/activate       # created already; recreate with python3 -m venv .venv
pip install -r requirements.txt
pytest                          # full suite
pytest -k two_sum               # one module
```

`pytest.ini` sets `pythonpath = .`, so imports are `from coding.lib.two_sum import two_sum`.

## Housekeeping expectations

After adding a problem: add it to the parent section README's index, and don't touch
[progress/log.md](progress/log.md) — that is the user's record of their own attempts, and
you writing in it corrupts the signal. The review queue is theirs too.

Commit only when asked.
