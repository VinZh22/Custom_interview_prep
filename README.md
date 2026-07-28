# Interview Prep

Personal workspace for tech & quant interview preparation: maths, coding, data science,
and behavioral. One problem per file, solution folded in, so any file can be re-attempted
cold months later.

## Layout

| Path | Contents |
| --- | --- |
| [math/](math/) | Probability, statistics, linear algebra, calculus/optimization, combinatorics, brainteasers |
| [coding/](coding/) | Algorithms, data structures, data manipulation (pandas), system design + a runnable Python workspace |
| [data-science/](data-science/) | ML theory, LLMs, experimentation/A-B testing, case studies, product analytics |
| [quant/](quant/) | Market-making games, derivatives, time series, mental math |
| [behavioral/](behavioral/) | STAR stories, per-company notes |
| [mock-interviews/](mock-interviews/) | Timed session write-ups and post-mortems |
| [progress/](progress/) | Practice log and spaced-repetition queue |
| [resources/](resources/) | Books, problem sets, links |
| [templates/](templates/) | Copy these when adding new material |

## Working with Claude Code in here

[CLAUDE.md](CLAUDE.md) has the full brief. Two roles, invoked as skills:

- **`/tutor`** — you're solving, it helps with escalating hints and never gives the full answer.
- **`/problem-setter`** — it writes a new problem into the repo, solving and verifying it first.
  Say what you want: `/problem-setter probability, hard, Markov chains`.

Every sub-category also has a skill of the same name (`probability`, `algorithms`,
`market-making`, …) describing its scope, techniques, and traps. They live in
[.claude/skills/](.claude/skills/).

**No SQL anywhere in this repo** — data wrangling is done in pandas, on purpose.

## Conventions

- **File naming:** `NNN-short-slug.md`, numbered per folder (`math/probability/001-two-envelopes.md`).
- **One problem per file.** Statement at the top, solution inside a `<details>` block so you
  can re-solve without spoilers.
- **Tags** in the front-matter block: topic, difficulty (`easy|medium|hard`), source, and the
  companies that asked it.
- **Difficulty is about *your* experience of it**, not a public rating. Re-tag as it changes.
- **Code lives in [coding/lib/](coding/lib/)** with tests in [coding/tests/](coding/tests/) so
  solutions are actually executed, not just read.

## Workflow

1. Pick a topic folder; work the next unsolved problem *without* opening the solution.
2. Write your attempt, then reveal and diff against the reference solution.
3. Log the attempt in [progress/log.md](progress/log.md); anything you got wrong goes into
   [progress/review-queue.md](progress/review-queue.md).
4. Every week or two, run a timed session and record it under [mock-interviews/](mock-interviews/).

## Running the code

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest                 # all solutions
pytest -k two_sum      # one
```
