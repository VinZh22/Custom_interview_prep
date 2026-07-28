---
name: system-design
description: Scope and standards for coding/system-design — requirements, capacity estimates, data model, API, scaling, trade-offs, and ML system design. Use when tutoring or writing a problem in coding/system-design/.
---

# System design

Folder: [coding/system-design/](../../../coding/system-design/)

Unlike the rest of the repo there's no correct answer — you're graded on whether you drive the
conversation, quantify, and name trade-offs instead of listing technologies.

## Scope

Requirements gathering and scoping · back-of-envelope capacity estimation · API design ·
data modeling and storage choice (relational, document, key-value, wide-column, object,
time-series) · indexing and access patterns · caching (where, eviction, invalidation,
stampedes) · replication and partitioning/sharding · consistency models, CAP in practice,
idempotency · queues and async processing, at-least-once vs exactly-once · rate limiting ·
load balancing · observability · failure modes and blast radius. For ML systems: training vs
serving path, feature stores, online/offline skew, latency budget, retraining cadence,
monitoring for drift.

## The structure to follow, with time budget for a 45-minute question

1. **Requirements (5 min).** Functional, then non-functional. Pin down: read/write ratio,
   latency target, consistency need, retention. Ask what's *out* of scope.
2. **Estimates (5 min).** DAU → QPS (peak ≈ 2–3× average) → storage/year → bandwidth. Round
   aggressively; the number's order of magnitude is what matters, and it's what justifies every
   later decision.
3. **API (3 min).** A handful of endpoints with their key parameters.
4. **Data model (5 min).** Entities, then the access patterns, then the storage choice —
   in that order, because the access pattern is what picks the store.
5. **High-level design (10 min).** Boxes and arrows, request path narrated end to end.
6. **Scale and harden (10 min).** Find the bottleneck *from your own estimates*, then fix it:
   cache, shard, replicate, queue. Say what each fix costs.
7. **Trade-offs and failure modes (5 min).** What breaks, what you'd monitor, what you'd do
   differently at 10× scale.

## Numbers to have memorized

Memory reference ~100 ns · SSD read ~100 µs · network round trip within a datacenter ~0.5 ms ·
cross-continent ~150 ms · disk seek ~10 ms. 1 M writes/day ≈ 12/s. 1 KB × 1 M/day ≈ 1 GB/day
≈ 365 GB/year. A single well-indexed relational instance handles thousands of QPS — say so
before reaching for a distributed store.

## What a good problem here looks like

- A recognizable product ("design a URL shortener / notification service / news feed / trade
  execution log / feature store"), stated in one line with the ambiguity left in on purpose.
- Written as a prompt plus the requirements the interviewer would reveal only if asked — that
  hidden list is what makes the file reusable.
- The reference write-up commits to specific choices and states what it's giving up, rather than
  surveying options.
- Follow-ups: 10× the traffic, add a hard consistency requirement, add multi-region, make it
  cost-constrained.

## Traps to build into problems and to catch when tutoring

- Jumping to a diagram before requirements and estimates.
- Naming technologies as answers ("use Kafka") without saying what property is needed.
- Distributing before proving a single node is insufficient.
- Ignoring the hot-key / celebrity problem when sharding.
- Cache invalidation hand-waved; no TTL, no stampede protection.
- Claiming exactly-once delivery; not designing idempotent consumers.
- No mention of failure, backpressure, or what the user sees during a partial outage.
- For ML: training/serving skew, label leakage, and no plan for retraining or drift detection.

## Tutoring note

Don't design it for them. Ask the interviewer's questions: "what's your peak QPS?", "where does
that write go?", "what happens if that node dies?", "why that store and not the boring one?".
Make them produce the estimate before they choose the architecture.

## Sources

*Designing Data-Intensive Applications* (Kleppmann) — the one book that matters here;
*Designing Machine Learning Systems* (Huyen) for the ML variant.
