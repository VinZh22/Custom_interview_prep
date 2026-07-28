---
name: problem-setter
description: Write new interview problems into this repo — pick or honor a topic, solve it yourself first, then commit the problem file with the solution hidden behind a details fold. Use when the user asks for a new problem, a set of problems, "give me something on X", a harder variation of an existing problem, or wants to drill a specific weakness.
---

# Problem setter

You write the material. The user solves it later, cold. Everything here serves that: the
problem must be solvable, unambiguous, and the answer must be right — a wrong reference
solution teaches a wrong reflex and is worse than no problem at all.

## Take the request as given

The user says what they want, at whatever precision they like. Honor it:

- `/problem-setter probability, hard, something with Markov chains`
- `/problem-setter a medium pandas groupby problem, no merge`
- `/problem-setter three mental-math drills, 60 seconds each`
- `/problem-setter like coding/algorithms/001 but where the array is streamed`
- `/problem-setter whatever I'm weakest at` → read
  [progress/review-queue.md](../../../progress/review-queue.md) and
  [progress/log.md](../../../progress/log.md) and pick from the gaps

Fill unspecified dimensions with sensible defaults: **medium** difficulty, a topic that
extends recent work rather than repeating it, one problem unless asked for several. Only ask
a clarifying question when two readings would produce genuinely different problems; otherwise
state your assumption in one line and write it.

Before writing, read the sub-category's skill (`probability`, `algorithms`,
`market-making`, …) for that area's scope, standards, and traps.

## Solve it yourself first — non-negotiable

Do this **before** writing the problem file, and do it properly:

1. **Work the solution end to end.** Full derivation for math, real code for coding. No
   hand-waving in the middle; if you can't close a step, the problem isn't ready.
2. **Verify it independently.** Second method, small cases, limiting behavior, or a quick
   simulation. For counting and probability, a 20-line Monte Carlo in the scratchpad
   (`/private/tmp/.../scratchpad`) is usually the fastest check — run it.
3. **For coding: write the implementation and tests, and run pytest.** A solution that hasn't
   executed doesn't go in.
4. **Check it's actually solvable in interview time** — 5 minutes for a quant one-liner,
   20–40 for a coding or case problem. If your own solution needed a machine, it's a bad
   interview problem; rescope it.
5. **Check for ambiguity.** Re-read your statement adversarially: is there a second reading
   that yields a different answer? Pin it down with an explicit constraint.

If verification contradicts your first answer, fix the solution — don't reword the problem to
make your answer true.

## Where it goes

`<section>/<sub-category>/NNN-slug.md`, with `NNN` = highest existing number in that folder
plus one. `ls` the folder first. Slug is short, descriptive, and not the answer
(`003-expected-max-of-n-uniforms.md`, never `003-answer-is-n-over-n-plus-1.md`).

Code goes in `coding/lib/<module>.py` with tests in `coding/tests/test_<module>.py`, linked
from the problem file.

## Format

Copy [templates/problem.md](../../../templates/problem.md) exactly. Non-negotiable parts:

- **Front matter**: topic, difficulty, source, asked-by (real firms if you know the problem's
  provenance, `-` if you invented it — never fabricate attribution), empty attempts line.
- **Statement**: self-contained, all constraints stated, and it says what an acceptable answer
  looks like (closed form? asymptotics? working code? a number to two decimals?).
- **`## My attempt`** left empty with the placeholder line. This is the user's space.
- **Everything else inside `<details><summary>Solution</summary>`** — idea, derivation,
  answer, complexity, follow-ups. Nothing above the fold may leak the answer, including the
  title and the front matter.
- **Follow-ups**: 2–4, the ones a real interviewer would actually ask next. These carry more
  value than the base problem; make them the natural escalation, not trivia.
- **Notes to self**: the *cue* — the surface feature of the problem that should trigger the
  technique. Write it as a pattern the user can generalize.

## What makes a problem worth adding

- **One core insight**, not three. Layer difficulty through follow-ups instead.
- **Tests a transferable pattern**, so solving it pays off on unseen problems. Reject
  problems whose solution is a memorized trick with no reach.
- **Realistic.** Phrase it the way an interviewer speaks, not the way a textbook writes.
  For quant, adversarial framing ("make me a market, then I'll trade"). For DS, a business
  context with a stakeholder.
- **Numbers that stay tractable.** The user has no calculator; pick values where the
  arithmetic is clean enough to do out loud.
- **Not a near-duplicate.** Skim the folder's existing problems; if it's close to one, either
  make it a follow-up on that file or make the difference load-bearing.

## After writing

- Add it to the parent section README's index list.
- Report to the user: path, topic, difficulty, and how you verified the answer. One or two
  lines — don't recap the solution, they haven't solved it yet.
- **Say nothing about the answer**, not even a hint about its shape ("it's a surprisingly
  small number"). You've just spoiled it if you do.
- Do not write to [progress/log.md](../../../progress/log.md) or the review queue.

## Batches

For "give me 5 problems", vary difficulty and sub-topic deliberately, and say the spread in
one line (`2 easy warm-ups on counting, 2 medium conditional-probability, 1 hard martingale`).
Solve and verify every one — the temptation to get sloppy on problem 5 is exactly where a
wrong reference solution enters the repo.
