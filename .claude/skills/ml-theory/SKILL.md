---
name: ml-theory
description: Scope and standards for data-science/ml-theory — bias/variance, regularization, linear and logistic regression, trees and boosting, SVM, clustering, PCA, neural nets, metrics, leakage, class imbalance. Use when tutoring or writing a problem in data-science/ml-theory/.
---

# ML theory

Folder: [data-science/ml-theory/](../../../data-science/ml-theory/)

Rapid-fire derivation and "why" questions. The bar is being able to derive the thing, state its
assumptions, and say what breaks when they fail — not naming algorithms.

## Scope

Bias–variance trade-off and the MSE decomposition · overfitting, cross-validation schemes
(k-fold, stratified, time-series, grouped) · regularization: L1 vs L2, why L1 is sparse, ridge
as a Bayesian prior · linear regression assumptions and closed form · logistic regression: the
log-odds link, cross-entropy loss, why not squared error · generative vs discriminative ·
naive Bayes and its independence assumption · decision trees, splitting criteria (Gini,
entropy), pruning · bagging vs boosting; random forests vs gradient boosting · SVM, the margin,
the kernel trick · k-means (and why it's not guaranteed optimal), hierarchical clustering,
DBSCAN · PCA and its relation to SVD · neural nets: backprop, activations, vanishing gradients,
batch norm, dropout · embeddings · metrics:
precision/recall/F1, ROC-AUC vs PR-AUC, log loss, calibration · class imbalance · data leakage ·
feature importance and its pitfalls (SHAP vs impurity).

## The questions that come up most, worth having rehearsed

1. **Bias–variance for a specific model** — "what happens to bias and variance as you increase
   tree depth / k in kNN / λ in ridge?" Know the direction cold for each knob.
2. **Why L1 gives sparsity** — the geometry of the constraint region touching an axis, or the
   subgradient argument. Have both.
3. **Why logistic regression uses cross-entropy** — MLE for a Bernoulli, plus squared error
   being non-convex in the parameters through the sigmoid.
4. **ROC-AUC vs PR-AUC under imbalance** — ROC looks great at 1% positives because TNs
   dominate; PR reflects what a user experiences.
5. **Bagging reduces variance, boosting reduces bias** — and what that implies about
   overfitting behavior and how you tune each.
6. **How PCA relates to SVD** and why you center (and often scale) first.
7. **Regularization as a prior**: ridge ↔ Gaussian, lasso ↔ Laplace.

## What a good problem here looks like

- Asks for a derivation with a small concrete number attached, or a decision with a stated
  business constraint ("false positives cost 10× false negatives — pick and justify a metric").
- Forces a trade-off rather than a recital: "you have 500 labeled rows and 2 M unlabeled — what
  do you do?"
- Includes a *diagnosis* variant: "train AUC 0.95, test 0.62 — list causes in order of
  likelihood, and how you'd check each."
- Follow-ups push to deployment: latency, retraining, monitoring, what you'd log.

## Traps to build into problems and to catch when tutoring

- **Leakage**: target-derived features, scaling/imputing before the split, using future
  information, duplicate rows across folds, group leakage (same user in train and test).
- Accuracy on a 1%-positive problem; reporting a single threshold-dependent metric.
- Tuning on the test set; no held-out set at all.
- Standard k-fold on time series or on grouped data.
- Treating correlated features' coefficients as importance; impurity importance biased toward
  high-cardinality features.
- Oversampling before the split (SMOTE applied to the whole dataset).
- Assuming the trained model's calibration survives a class-rebalanced training set.
- Claiming a model is interpretable because it's linear, with 200 correlated features.

## Verification standard

For a derivation, do it symbolically and check a limiting case (λ → 0, λ → ∞). For an empirical
claim, run it — a 15-line sklearn snippet in the scratchpad settles "does regularization help
here" and catches confidently wrong intuitions. State assumptions explicitly in the solution.

## Sources

ISL for the framing, ESL for the depth, *Ace the Data Science Interview* for question style.
Theory backing lives in [statistics](../statistics/SKILL.md) and
[linear-algebra](../linear-algebra/SKILL.md).

**Transformers, attention, and anything LLM-specific live in [llm](../llm/SKILL.md)** — this
skill stops at classical ML plus general neural nets. If a question is about attention, a KV
cache, tokenization, RAG, fine-tuning, or LLM evaluation, use that skill instead.
