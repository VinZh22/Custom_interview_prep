# Will this fit on one GPU?

- **Topic:** LLM serving — KV cache sizing, memory budget, GQA
- **Difficulty:** medium
- **Source:** classic serving question (example file showing the format)
- **Asked by:** ML infra / inference and LLM platform loops
- **Attempts:** 2026-07-29 ✓

## Statement

You're serving a decoder-only transformer on a single 80 GiB GPU:

| property | value |
| --- | --- |
| layers | 32 |
| attention heads | 32 (multi-head — one KV head per query head) |
| head dimension | 128 |
| parameters | 6.7 B |
| weights and KV cache dtype | fp16 (2 bytes) |

Product wants **batch size 16** at a **context length of 8192** tokens.

1. What is the KV cache size per token, per sequence, and for the full batch?
2. Add the weights. Does the deployment fit in 80 GiB?
3. It doesn't fit comfortably. Name the single highest-leverage change and quantify it.
4. Single-stream decoding on this GPU (≈2 TB/s HBM bandwidth): what's the rough ceiling on
   tokens/second, and what sets it?

Do the arithmetic out loud. Powers of two are deliberate — no calculator.

## My attempt

<Write your attempt here before opening the solution.>

1. per token: $2*32*32*128 = 263,144$ -> 262KiB roughly / per sequence: per_token * sequence_len -> 2GiB roughly / full batch: per_sequence * batch_size -> 32 GiB
2. We add 6.7B parameters, in fp16 it would be 13 GiB, with batch-size 16, it would take 208 GiB, it doesn't fit...
3. changing the float precision, maybe to fp4, it would now fit easily. 208 to 52GiB for the weights, and 32 GiB to 8 GiB for KV cache, so in total 60 GiB, fits comfortably.
4. Considering we are now on fp4, we get 33.3 full batch per second, so 533,3 token/second. 

Sorry still used calculator (simple python script), could maybe be done with paper, but seems impossible in the head. 

Attempt 2 for 1:
Use powers to sum directly. We have: 2^{1+5+5+7+13+4+1} = 2^{36} = 2^6 GB

2. the total would be 64+13 = 77 GB...
3. Changing to fp8 would give 37 GB roughly, easy now.

Attempt 2 for 4:
If batch-size of 1 then we can take fp16, giving us 17GB one forward pass + KV Cache, giving us 117 token/sec

Attempt 3 for 4:
The FLOP count for a forward is 2*N*D, so 2*6.7B*117=1,57TFLOP per second
So with a 312TFLOP/s of A100, the bottleneck is memory wise.

3. I could touch the head counts and do a GQA, by grouping the heads.

---

<details>
<summary>Solution</summary>

## Idea

Two independent memory consumers — weights (fixed) and KV cache (grows with `batch × context`)
— and at these settings **the cache dominates the weights by 5×**. The formula to have
memorized:

```
KV bytes per token = 2 (K and V) × n_layers × n_kv_heads × d_head × bytes_per_value
```

## 1. Cache size

Per layer, per token: `2 × 32 heads × 128 = 8192` values, at 2 bytes = **16 KiB**.

Across 32 layers: `16 KiB × 32 = 512 KiB per token`.

```
per sequence  = 512 KiB × 8192 tokens = 4 GiB
full batch    = 4 GiB × 16            = 64 GiB
```

The clean landmark worth remembering: **512 KiB/token, so 8K context = 4 GiB per sequence.**

## 2. Does it fit?

Weights: `6.7e9 × 2 bytes = 13.4 GB = 12.5 GiB`.

```
12.5 GiB (weights) + 64 GiB (cache) = 76.5 GiB of 80 GiB
```

Technically yes, with **~3.5 GiB left** — which is not enough. That headroom still has to cover
activations for the prefill of a 16×8192 batch, the CUDA context and kernel workspaces, and
allocator fragmentation. This deployment OOMs in practice, and it OOMs on a *long* request
rather than at startup — the worst failure mode, because it looks like an intermittent
production bug rather than a capacity error.

## 3. The highest-leverage change: GQA

The cache scales linearly with `n_kv_heads`, and nothing else in the formula is as cheap to
change. Sharing KV across query heads — 32 query heads over **8 KV heads** — divides the cache
by 4:

```
per token = 128 KiB   →   per sequence = 1 GiB   →   batch = 16 GiB
total = 12.5 + 16 = 28.5 GiB of 80 GiB
```

That is the actual reason production models use GQA: it's a serving-memory decision, not an
accuracy one, and quality loss is small when the model is *trained* that way. Say that out
loud — GQA is not a knob you can flip at inference time on an MHA-trained model.

Ranked alternatives, with what each costs:

| Change | Effect on cache | Cost |
| --- | --- | --- |
| GQA, 8 KV heads | ÷4 → 16 GiB | Must be trained in; not a deploy-time switch |
| Quantize the KV cache to int8 | ÷2 → 32 GiB | Small quality hit; deploy-time, composes with GQA |
| Halve max context to 4096 | ÷2 → 32 GiB | Product capability regression |
| Halve batch to 8 | ÷2 → 32 GiB | Halves throughput; hurts the metric you care about |
| Quantize *weights* to int4 | none | Saves only ~9 GiB — attacks the small term |

That last row is the trap: weight quantization is the reflexive answer and it's the wrong one
here, because weights are 16% of the footprint. **Attack the term that dominates.**

## 4. Decode throughput ceiling

Decoding one token requires reading every weight from HBM once, so the floor per step is set by
bandwidth, not FLOPs:

```
13.4 GB / 2000 GB/s ≈ 6.7 ms per token   →   ~150 tokens/second
```

Decode is **memory-bandwidth-bound**; prefill, which processes all prompt tokens in parallel,
is **compute-bound**. This asymmetry is the key serving insight: since a decode step reads the
same weights regardless of batch size, batching multiplies throughput almost for free — which
is exactly why you wanted batch 16, and why the KV cache is what limits how far you can push it.

## Complexity

Cache memory is `O(batch × L × n_layers × n_kv_heads × d_head)` — linear in context length,
not quadratic. (Attention *compute* is quadratic in `L`; the cache is not. Mixing these up is
the most common error on this question.)

## Follow-ups an interviewer would ask

- Context goes to 128K for a single request — what breaks, and what do you do?
  (Cache is 64 GiB for one sequence at MHA, 16 GiB at GQA-8: batch collapses to 1. Real answers
  are sliding-window or sparse attention, and paged attention to stop fragmentation.)
- Requests have wildly varying lengths. How do you avoid reserving worst-case memory per slot?
  (Paged attention: fixed-size blocks allocated on demand. Continuous batching to admit new
  requests as others finish rather than padding to a fixed batch.)
- A shared 2000-token system prompt precedes every request — what do you exploit?
  (Prefix/prompt caching: reuse the KV entries for the shared prefix. It's a *prefix* match, so
  a per-request timestamp at the front of the prompt destroys the benefit for everything after
  it — keep volatile content last.)
- Where does FlashAttention help here? (Prefill compute and activation memory. It does **not**
  shrink the KV cache — different problem.)
- MoE with 8× total parameters but the same active parameters: what changes?
  (Weight memory scales with *total* params; the bandwidth-bound decode ceiling scales with
  *active* params. Cache is unchanged.)

</details>

---

## Notes to self

Memorize the formula: `2 × layers × kv_heads × d_head × bytes`. Then the reflex is to compute
both terms — weights *and* cache — and attack whichever dominates. At long context and real
batch sizes, that's almost always the cache.

Second reflex: **prefill is compute-bound, decode is memory-bandwidth-bound.** Almost every
serving follow-up resolves to one of those two.

Watch the units: 6.7 B params × 2 bytes is 13.4 **GB** but 12.5 **GiB**, and GPU capacity is
quoted in GiB. The ~7% gap is exactly the size of the "does it fit" margin.
