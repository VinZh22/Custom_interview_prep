---
name: combinatorics
description: Scope and standards for math/combinatorics — counting, inclusion–exclusion, pigeonhole, generating functions, recurrences, bijections. Use when tutoring or writing a problem in math/combinatorics/, or when a probability or DP problem turns on a counting argument.
---

# Combinatorics

Folder: [math/combinatorics/](../../../math/combinatorics/)

Counting is where careful people beat clever people. Most wrong answers here come from
double-counting or from counting the wrong objects, not from missing a formula.

## Scope

Permutations and combinations, with and without repetition · multinomial coefficients ·
stars and bars · inclusion–exclusion · pigeonhole · bijective proofs · derangements ·
Catalan numbers and the paths/parens/trees family · recurrences and how to solve them
(characteristic roots, unrolling) · generating functions as a bookkeeping device ·
Burnside/symmetry counting at a light level · binomial identities and combinatorial proofs of
them · asymptotics (Stirling, `2ⁿ` vs `n!`).

## Techniques worth having reflexive

1. **State precisely what you're counting**, including whether order and repetition matter, and
   whether objects are distinguishable. Half of all errors die here.
2. **Count the complement** when "at least one" appears.
3. **Inclusion–exclusion** whenever conditions overlap; write the terms out rather than
   guessing signs.
4. **Bijection** to a structure you already know how to count (lattice paths, binary strings,
   balanced parentheses).
5. **Double counting** — count one set two ways to prove an identity.
6. **Recurrence by cases on the last element**; then check small `n` against brute force.
7. **Stars and bars** for distributing identical items into distinct bins, and know the
   `C(n+k-1, k-1)` form cold.
8. **Symmetry / fixing one element** to kill rotational overcounting (circular arrangements:
   `(n-1)!`).

## What a good problem here looks like

- Small enough that the user can brute-force `n = 3` by hand and check the general formula.
- Turns on one structural insight (a bijection, a symmetry, the right complement), not on
  remembering an exotic identity.
- Has an answer that's a clean closed form or a named sequence.
- Follow-ups: generalize the parameter, add a constraint, or ask for the asymptotics.

## Traps to build into problems and to catch when tutoring

- Distinguishable vs indistinguishable objects — the single biggest source of wrong answers.
- Double counting when the same arrangement is reachable two ways; not dividing by the
  symmetry group.
- Circular arrangements and reflections (necklaces) counted as linear.
- Off-by-one in stars and bars (bins allowed to be empty or not).
- Multiplying probabilities of dependent choices, or adding counts of overlapping cases.
- Assuming a formula generalizes from `n = 2, 3` without proof — coincidences are common at
  small `n`.

## Verification standard

**Brute force the small cases in code.** `itertools.permutations`/`combinations` over `n ≤ 6`,
compared against the formula, catches essentially every counting error. Do this in the
scratchpad before committing a solution — it is the single highest-value verification step in
this repo.

## Sources

*Concrete Mathematics* (Graham, Knuth, Patashnik) for depth; Brualdi for a gentler pass;
OEIS to identify a sequence you've derived. Overlaps heavily with
[probability](../probability/SKILL.md) and DP in [algorithms](../algorithms/SKILL.md).
