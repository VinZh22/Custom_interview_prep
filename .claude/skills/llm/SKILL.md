---
name: llm
description: Scope and standards for data-science/llm — transformers and attention, tokenization, pretraining and fine-tuning, RLHF/DPO, RAG, prompting, evaluation, agents and tool use, inference cost and serving math. Use when tutoring or writing a problem in data-science/llm/, or when a question turns on how an LLM works, is trained, is evaluated, or is served.
---

# LLMs

Folder: [data-science/llm/](../../../data-science/llm/)

Its own track now, distinct from [ml-theory](../ml-theory/SKILL.md): interviews ask you to
derive attention, size a KV cache, design a retrieval system, and say how you'd know any of
it works. Three interview flavors, and they're graded differently:

1. **Architecture / theory** — derive it on the whiteboard.
2. **Systems** — latency, memory, throughput, cost. Arithmetic under pressure.
3. **Applied / product** — build a RAG or agent system and defend the evaluation plan.

Keep it provider-neutral. Reason about context windows, tokenizers, and pricing as
*parameters*, not memorized vendor facts — the numbers change quarterly and a candidate who
reasons from `$/1M tokens × tokens/request` beats one who recites a price list.

## Scope

**Architecture.** Self-attention: Q/K/V, scaled dot product, why the `√d_k` scale ·
multi-head attention · causal masking · positional encoding: sinusoidal, learned, RoPE, ALiBi
· residual stream, LayerNorm vs RMSNorm, pre-norm vs post-norm · feed-forward block and its
`4×` expansion · GELU/SwiGLU · encoder-only vs decoder-only vs encoder-decoder, and what each
is for · KV cache · MQA/GQA · FlashAttention (an IO/tiling optimization, not an approximation)
· sliding-window and sparse attention · mixture of experts, routing, active vs total params ·
speculative decoding.

**Tokenization.** BPE, WordPiece, SentencePiece/unigram · vocabulary size trade-offs · why
token counts differ across tokenizers and why character-level intuitions mislead · digits,
whitespace, and code tokenizing badly · why a model can't reliably count letters or reverse a
string · non-English inflating token counts.

**Training.** Next-token prediction and cross-entropy · teacher forcing · scaling laws and the
compute-optimal parameter/token trade-off · data curation and dedup · context-length extension
· supervised fine-tuning · parameter-efficient methods: LoRA/QLoRA, adapters, prefix tuning ·
alignment: RLHF (reward model + PPO), DPO, and simpler preference methods · what "instruction
tuned" changes · distillation · quantization (int8/int4, PTQ vs QAT, weight vs activation vs
KV-cache) · catastrophic forgetting.

**Inference and decoding.** Prefill vs decode and why they have opposite bottlenecks ·
greedy, temperature, top-k, top-p, beam search, and when each is wrong · repetition penalties
· batching and continuous batching · paged attention and fragmentation · streaming ·
prompt/prefix caching, and why it's a *prefix* match — one byte early in the prompt
invalidates everything after it · latency decomposition: TTFT vs inter-token latency.

**Prompting and context.** Zero/few-shot · chain of thought and when it doesn't help ·
self-consistency · structured output (schema-constrained decoding, function calling) ·
system vs user roles · context-window budgeting, and the "lost in the middle" position effect
· long-context vs retrieval as alternatives.

**RAG.** Chunking strategy · embeddings and vector similarity · ANN indexes (HNSW, IVF) and
their recall/latency knobs · hybrid retrieval (BM25 + dense) · reranking · query rewriting ·
citation and attribution · staleness and reindexing · the failure taxonomy below.

**Agents and tool use.** Tool/function schemas and how the description drives selection · the
agent loop (call → execute → feed result → repeat) · ReAct-style interleaved reasoning ·
multi-step planning and error recovery · sandboxing and least privilege · when a workflow with
fixed control flow beats an agent (usually) · cost and latency multiplying with step count.

**Evaluation.** Why perplexity is not a product metric · benchmark contamination · LLM-as-judge
and its biases (position, verbosity, self-preference) · pairwise comparison and Elo · human
eval and inter-annotator agreement · task-specific metrics · hallucination and groundedness
measurement · regression suites and golden sets · online metrics and guardrails.

**Safety and failure modes.** Hallucination and its causes · prompt injection, direct and
indirect — the one that matters most in agent/RAG systems, since retrieved or tool-returned
content is untrusted input · jailbreaks · data leakage and PII in prompts and logs · training
data extraction · bias · sycophancy · nondeterminism even at temperature 0 (batching and
kernel nondeterminism).

## Formulas and numbers to have instant

- **Attention:** `softmax(QKᵀ/√d_k)V`. The scale keeps the dot products from growing with
  `d_k` and saturating the softmax into a near-one-hot distribution with vanishing gradients.
  Be able to derive that in one sentence.
- **Attention cost:** `O(L² · d)` time and `O(L²)` attention weights for a sequence of length
  `L`; FlashAttention keeps the compute but avoids materializing the `L × L` matrix.
- **KV cache per token** = `2 (K and V) × n_layers × n_kv_heads × d_head × bytes_per_value`.
  Multiply by sequence length and batch. This is the single most-asked systems calculation.
- **GQA saving** = `n_q_heads / n_kv_heads`, applied directly to the KV cache.
- **Weight memory** = `params × bytes_per_param`; fp16 ≈ `2 bytes`, int8 ≈ `1`, int4 ≈ `0.5`.
  A 7B model is ~14 GB in fp16. Training needs roughly 4× more than inference for
  weights + gradients + Adam's two moments, before activations.
- **Decode is memory-bandwidth-bound**, prefill is compute-bound. Each decode step reads
  every weight once, so single-stream tokens/second ≈ `HBM bandwidth / model bytes`. That
  ceiling is why batching raises throughput without hurting per-token latency much.
- **Training compute** ≈ `6 × params × tokens` FLOPs (forward + backward); inference forward
  pass ≈ `2 × params` per token.
- **Cost** = `(input tokens × input price + output tokens × output price)` per request. Output
  tokens are several times more expensive than input, so latency and cost usually improve most
  by cutting *output* length.
- Roughly **1 token ≈ 4 characters** of English prose — a Fermi tool only, and wrong for code,
  digits, and non-English.

## What a good problem here looks like

- **Systems:** concrete numbers and a decision. "Here's the model shape, the GPU, the target
  batch and context — does it fit, and what do you change first?" Clean powers of two so the
  arithmetic is doable out loud.
- **Theory:** a derivation with a stated conclusion. "Why divide by `√d_k`?" "Why can't a
  decoder-only model attend forward?" "What breaks if you remove the residual stream?"
- **Applied:** an underspecified product ask plus the hidden constraints an interviewer reveals
  only if asked — latency budget, corpus size, update frequency, accuracy bar, privacy
  requirement. That hidden list is what makes the file reusable.
- **Evaluation is part of the answer, not a follow-up.** A design answer without a measurement
  plan is incomplete; write problems that force it.
- Follow-ups escalate to: 10× the context, 10× the QPS, a hard latency SLA, a fixed budget, or
  "now the retrieved documents are adversarial".

## Traps to build into problems and to catch when tutoring

- Forgetting the factor of **2** for K *and* V, or the `n_layers` multiplier, in a cache
  calculation. Also: quoting GQA savings while using `n_q_heads` for the cache.
- Treating attention as `O(L)` in memory, or claiming FlashAttention changes the math (it
  changes the IO pattern; outputs are the same).
- Reasoning about prefill and decode as if they had the same bottleneck — the most common
  serving mistake.
- Assuming a bigger context window removes the need for retrieval: cost grows with context,
  and mid-context recall degrades.
- Chunking a corpus without considering the query — chunks that split a fact across a boundary
  can't be retrieved.
- Evaluating a RAG system end-to-end only, so a retrieval failure and a generation failure look
  identical. **Measure retrieval separately** (recall@k on a labeled set) before blaming the
  model.
- LLM-as-judge scored without validating the judge against human labels, or with the two
  candidates always in the same order.
- Reporting benchmark numbers without considering contamination.
- Fine-tuning to add knowledge (retrieval is usually the right tool; fine-tuning is for
  *behavior*, format, and style).
- Assuming temperature 0 gives determinism.
- Treating retrieved documents or tool output as trusted instructions — the indirect
  prompt-injection hole.
- Reciting a specific model's context window or price as a fact; those change. Reason from the
  parameters.
- Character-level reasoning about a tokenizer's behavior.

## Verification standard

- **Arithmetic:** compute it in the scratchpad (Python) before writing the solution. Cache and
  cost problems are exactly where a plausible-looking wrong answer slips in — check the units
  at every step and state whether you mean GB or GiB, since the two differ by ~7%.
- **Claims about behavior:** if it's checkable, check it. Token counts should come from a real
  tokenizer, not an estimate, whenever a problem's answer depends on them.
- **Anything provider-specific** (a model's context window, price, or API parameter) must be
  verified against current documentation at the time of writing, or written parametrically so
  it can't go stale. Prefer parametric.

## Sources

The original *Attention Is All You Need*; the annotated-transformer walkthroughs for the
mechanics; the Chinchilla scaling-laws paper; the FlashAttention and GQA papers for the systems
side; Chip Huyen's *AI Engineering* and *Designing Machine Learning Systems* for the applied
framing. For anything about a specific provider's API, read that provider's current docs rather
than a secondary source.

Adjacent skills: [ml-theory](../ml-theory/SKILL.md) for the classical foundations,
[system-design](../system-design/SKILL.md) for serving architecture,
[experimentation](../experimentation/SKILL.md) for measuring a shipped change,
[linear-algebra](../linear-algebra/SKILL.md) for the matrix mechanics underneath attention.
