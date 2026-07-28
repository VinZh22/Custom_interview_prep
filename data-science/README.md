# Data Science

Two very different interview modes: *theory* (can you derive it) and *case*
(would you ship the right thing). Prepare both separately.

## Folders

- [ml-theory/](ml-theory/) — bias/variance, regularization, linear & logistic regression,
  trees/boosting, SVM, clustering, PCA, neural nets, metrics, leakage, imbalance.
- [llm/](llm/) — transformers and attention, tokenization, fine-tuning and alignment, RAG,
  agents and tool use, evaluation, and inference/serving cost math.
- [experimentation/](experimentation/) — A/B test design, power and sample size,
  multiple testing, CUPED, switchback and network effects, novelty, guardrail metrics.
- [case-studies/](case-studies/) — open-ended prompts: "metric dropped 8% overnight",
  "design ranking for X", "should we launch".
- [product-analytics/](product-analytics/) — funnel, retention/cohort, sessionization and
  attribution, computed **in pandas** (this repo doesn't use SQL). Mechanics live in
  [../coding/data-manipulation/](../coding/data-manipulation/).

## Metric-drop framework (memorize the skeleton)

1. Is it real? Logging, instrumentation, bots, backfill, timezone.
2. Cut it: date, platform, geo, new vs returning, version.
3. Numerator or denominator? Mix shift vs rate change (Simpson's paradox).
4. Internal cause (release, model, pricing) vs external (seasonality, competitor, outage).
5. Quantify each candidate, then say what you'd do about it.

## Model-design framework

Business goal → label definition → unit of prediction → features and their availability
at serve time → baseline → offline metric → online metric → failure modes → monitoring.

## LLM systems: three interview flavors

Prepare separately, they're graded differently — **theory** (derive attention, explain the
KV cache), **systems** (memory, latency, throughput, cost arithmetic under pressure), and
**applied** (design a RAG or agent system, and defend how you'd evaluate it). Evaluation is
part of the answer, never a follow-up. See the [`llm` skill](../.claude/skills/llm/SKILL.md).

## Index

- [experimentation/001-example-sample-size.md](experimentation/001-example-sample-size.md)
- [llm/001-example-kv-cache-sizing.md](llm/001-example-kv-cache-sizing.md)
