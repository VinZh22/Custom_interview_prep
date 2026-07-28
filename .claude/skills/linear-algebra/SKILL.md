---
name: linear-algebra
description: Scope and standards for math/linear-algebra — rank, eigenvalues, SVD, projections, positive definiteness, least squares, matrix calculus. Use when tutoring or writing a problem in math/linear-algebra/, or when an ML/quant question reduces to a matrix argument.
---

# Linear algebra

Folder: [math/linear-algebra/](../../../math/linear-algebra/)

Interview linear algebra is conceptual and geometric. Almost nothing requires row-reducing a
4×4 by hand; almost everything requires knowing what a matrix *does*.

## Scope

Vector spaces, span, basis, rank and nullity · rank-nullity theorem · determinant and trace as
invariants (product and sum of eigenvalues) · eigenvalues/eigenvectors, diagonalization ·
symmetric matrices and the spectral theorem · positive (semi)definiteness and its three
equivalent characterizations · quadratic forms · orthogonality and projection matrices ·
Gram–Schmidt and QR · SVD and low-rank approximation · least squares and the normal equations
· covariance matrices and PCA · matrix calculus (`∂/∂x` of `xᵀAx`, `‖Ax-b‖²`) · condition
number and numerical stability at an intuitive level.

## Techniques worth having reflexive

1. **Translate to geometry first.** "What does this matrix do to the unit ball?" Singular
   values are the axis lengths.
2. **Invariants before computation.** Trace = Σλ, det = Πλ; a rank-1 matrix `uvᵀ` has one
   nonzero eigenvalue `vᵀu`. Many problems collapse instantly with this.
3. **Projection formula** `P = A(AᵀA)⁻¹Aᵀ`, `P² = P`, `Pᵀ = P` — and least squares as
   projection onto the column space. This is the bridge to regression.
4. **Symmetric ⇒ orthogonal eigenbasis, real eigenvalues.** Reach for it whenever a covariance
   or Hessian appears.
5. **PSD checks**: all eigenvalues ≥ 0 ⟺ `xᵀAx ≥ 0` ∀x ⟺ `A = BᵀB`. Pick whichever is
   cheapest for the problem in front of you.
6. **Matrix calculus identities**: `∇(xᵀAx) = (A + Aᵀ)x`, `∇‖Ax-b‖² = 2Aᵀ(Ax-b)`.
7. **SVD as the universal tool** — pseudo-inverse, low rank, PCA, and conditioning all fall
   out of it.

## What a good problem here looks like

- Answerable in a few lines by naming the right structural fact, with a small concrete matrix
  to make it tangible.
- Connects to something applied: why `XᵀX` singular breaks OLS, why PCA uses eigenvectors of
  the covariance, why a Hessian being PSD means convexity.
- Small numbers, 2×2 or 3×3, so eigenvalues come out clean.
- Follow-ups escalate to "what if it's not full rank / not symmetric / ill-conditioned".

## Traps to build into problems and to catch when tutoring

- Assuming diagonalizable; forgetting defective matrices exist (`[[1,1],[0,1]]`).
- Treating `AB` and `BA` as interchangeable — though they *do* share eigenvalues, and trace.
- Concluding invertibility from nonzero diagonal, or PSD from positive entries.
- Confusing eigenvalues of `A` with singular values of `A` (equal only for symmetric PSD).
- Inverting `XᵀX` when features are collinear, rather than recognizing rank deficiency.
- Sign and orientation ambiguity of eigenvectors / PCA components.

## Verification standard

Check with a 2×2 example by hand, then confirm numerically with numpy (`np.linalg.eig`,
`svd`) in the scratchpad. Verify claimed identities on a random matrix before committing them
to a solution.

## Sources

Strang, *Linear Algebra and Its Applications*; the *Matrix Cookbook* for identities; ISL ch. 6
and 12 for the applied connections.
