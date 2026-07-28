---
name: calculus-optimization
description: Scope and standards for math/calculus-optimization — series, integration tricks, Taylor expansion, Lagrange multipliers, convexity, KKT, gradient methods. Use when tutoring or writing a problem in math/calculus-optimization/, or when an ML or quant question reduces to an optimization.
---

# Calculus & optimization

Folder: [math/calculus-optimization/](../../../math/calculus-optimization/)

Two flavors: manipulation speed (limits, series, slick integrals) and optimization structure
(convexity, constraints, what an algorithm converges to). Quant desks test the first, ML
interviews the second.

## Scope

Limits and asymptotics · Taylor/Maclaurin expansions and when to truncate · series convergence
tests · integration by parts, substitution, symmetry tricks, Feynman's trick ·
`∫₀^∞ e^{-x²}dx` and the Gaussian family · multivariable gradients, Hessians, Jacobians ·
unconstrained optimization and second-order conditions · Lagrange multipliers · KKT conditions
for inequality constraints · convexity: definitions, why it matters, how to prove it · Jensen's
inequality · gradient descent, learning rate, convergence intuition · Newton's method ·
duality at an intuitive level.

## Techniques worth having reflexive

1. **Taylor to first or second order** as the universal approximation move — small-`x`
   behavior, error estimates, and delta-method arguments all come from it. Know
   `e^x`, `ln(1+x)`, `(1+x)^α`, `sin x` to two terms.
2. **Symmetry in integrals** — odd function over a symmetric interval is 0; `x ↔ a-x`
   substitution halves many definite integrals.
3. **Lagrange multipliers**, and reading the multiplier as a shadow price. Interviewers like
   asking what `λ` *means*.
4. **Convexity proofs**: second derivative ≥ 0, or Hessian PSD, or composition rules (sum of
   convex, max of convex, convex ∘ affine). Composition rules are faster than Hessians.
5. **Jensen** for inequality questions — `E[f(X)] ≥ f(E[X])` for convex `f`.
6. **AM–GM and Cauchy–Schwarz** for optimization-flavored inequalities without calculus.
7. **Envelope/first-order conditions** to reason about how an optimum moves with a parameter.

## What a good problem here looks like

- A definite integral or limit with a trick that takes 2 minutes once seen and 20 without.
- Or a constrained optimization small enough to solve fully, with a question about the
  multiplier or about what happens when the constraint tightens.
- Or "prove this function is convex" followed by "so what does that let you conclude".
- Follow-ups connect to ML: why regularized least squares has a unique solution, why
  cross-entropy is convex in the logits but not in the network weights.

## Traps to build into problems and to catch when tutoring

- Setting the gradient to zero and declaring a minimum without checking the second-order
  condition or the boundary.
- Ignoring boundary and non-differentiable points (the optimum of a constrained problem often
  sits on the boundary — that's what KKT complementary slackness encodes).
- Assuming a stationary point is global without convexity.
- Interchanging limits, sums, and integrals without justification.
- Truncating a Taylor series where the neglected term dominates.
- Confusing convex in the *parameters* with convex in the *inputs*.

## Verification standard

Check integrals numerically (`scipy.integrate.quad`) and limits by evaluating close to the
point, in the scratchpad. For an optimization, verify the claimed optimum beats a few random
feasible points — an easy catch for sign errors in the multiplier.

## Sources

Standard calculus texts for the mechanics; Boyd & Vandenberghe, *Convex Optimization*, ch. 2–5
for the structural material (skim, don't read cover to cover).
