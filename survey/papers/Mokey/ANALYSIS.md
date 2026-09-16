# Mokey — paper notes

**Mokey: Enabling Narrow Fixed-Point Inference for Out-of-the-Box Floating-Point Transformer Models**
Ali Hadi Zadeh, Mostafa Mahmoud, Ameer Abdelhadi, Andreas Moshovos
**ISCA 2022** ｜ DOI: **not recorded** — the ACM/IEEE record is not reachable by script (403); look it up when citing
Venue evidence (2026-09-02): arXiv `comments` field, verbatim: *"Accepted at the 49th IEEE/ACM International Symposium on Computer Architecture (ISCA '22)"*
Archived here: **arXiv:2203.12758v1** (2022-03-23), 14 pages — **the preprint, not the
published ISCA 2022 version**; the two were **not compared**.

Status: **note ready** ｜ Last updated: 2026-09-09
Tags: `non-analytical-dtype` `new-data-type` `lut-accelerator` `combined-dtype` `accelerator`
How far it was read: **full read of §I introduction, §II quantization (all of A–G, including
the exponential derivation and the outlier scheme), §III memory layout and processing units,
§IV evaluation (Tables I, II, IV and the speedup/energy figures) and §VI conclusion.** §V
related work was read for its comparison claims only. Every number below carries its frame.
Not cross-checked against released code — no artifact is referenced — so this is
`analysis ready`, not `thorough ready`.

> Original: https://arxiv.org/abs/2203.12758
> The PDF is **not committed** (1.4 MB). Re-download: `curl -sSL -o 2203.12758.pdf https://arxiv.org/pdf/2203.12758`
> Extract text: `python3 extract.py` → `extracted/` (committed, greppable)
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, ISCA 2022 row.

---

## Brief

### 1. Motivation

Transformer models are large and getting larger, and for long sequences **activations
dominate the footprint** (past 512 tokens in BERT-Large). Quantization helps, but most
methods need fine-tuning — and the training resources or datasets are often simply
unavailable to whoever is deploying the model.

### 2. Overview

Quantize every value to a **4-bit index into a dictionary of representative 16-bit fixed-
point centroids**, with **no fine-tuning**. The trick that makes it a hardware paper:
centroids are chosen to also fit an exponential curve, so most of the original multiply-
accumulates can be replaced by **narrow 3-bit fixed-point additions**. Can also serve purely
as a memory-compression front-end for another accelerator.

### 3. Pros and cons

**Pros**

- No fine-tuning required — the paper is explicit that this is an accessibility argument,
not just a convenience, and it is within 1% of the FP baseline.
- The exponential-curve constraint on centroids is the elegant part: it turns a lookup-based
scheme into an **arithmetic** simplification rather than just a storage one.
- Order-of-magnitude energy-efficiency improvement over a Tensor Cores baseline with 4–15×
performance depending on model and buffer size; optionally deployable as a compression
assist, which lowers the adoption barrier.

**Cons**

- Dictionary-based (non-analytical) representation means codebook storage, lookup traffic
and a calibration step — costs that scale with how many dictionaries you keep.
- Outliers still need separate handling (~2.5% of values in the worst case), so the clean
"everything is a 4-bit index" story has an exception.
- Evaluated on BERT-class encoder models; generative LLM decoding, where the memory-
boundedness is different, is not covered.

### 4. Where it applies

The earliest **§1.3 lookup-table** entry in the corpus and the direct ancestor of the
2025–26 LUT thread ([`LUTTensorCore`](../LUTTensorCore/ANALYSIS.md),
[`OASIS`](../OASIS/ANALYSIS.md), [`EVA`](../EVA/ANALYSIS.md)). Read it first in that group.

---

## Conclusions

Numbered so later entries can cite them. **verified** = read directly in the paper;
**inferred** = my reading, not the authors' words.

1. **The contribution is a constraint, not a codebook.** Mokey's centroids are non-uniform,
   but they are not free: every one must sit on the curve `a^int + b` with `a = 1.179`,
   `b = −0.977`, `int ∈ [0,7]`. Accuracy is given up at the fit in exchange for the identity
   `a^i · a^j = a^(i+j)`, which is what makes the arithmetic collapse. **verified** (§II-B/D)
2. **The multiply becomes an index addition, and the accumulate becomes a histogram.** With
   both operands on the curve, the dominant term of `A·W` has exponent `int_A + int_W ∈
   [0,14]` — **15 possible values instead of 256 possible products** — so a dot product is
   computed by counting how often each exponent sum occurs and doing one weighted reduction at
   the end. The three remaining terms are a sum over activations, a sum over weights (static),
   and `N·b²`. **verified** (§II-D, Fig. 3–4)
3. **The dictionary is model-independent.** Agglomerative clustering — chosen over k-means
   because it is not sensitive to initialisation — is run **once**, offline, on 50,000 samples
   of a synthetic `N(0,1)` distribution. Every per-tensor dictionary is then `GD × s + m`, a
   non-iterative linear transform from that tensor's own mean and standard deviation.
   **verified** (§II-B/C)
4. **Scale granularity is per tensor and nothing finer.** One `(m, s)` pair per tensor, two
   dictionaries (Gaussian 8×16b, outlier 16×16b), no groups, blocks or channels. This is the
   coarsest granularity of any codebook entry in this corpus and the single most likely reason
   it would not survive to LLM scale. **verified** for the mechanism, **inferred** for the
   consequence.
5. **Outliers are isolated by a pointer list, not by extra bits.** Widening one dictionary to
   reach them would need `int` up to 45, i.e. 7 bits per value. Instead every value stays a
   4-bit index and a separate list marks which indices point into the outlier dictionary.
   **verified** (§II-E)
6. **The outlier path is a real multiplier.** Any product with an outlier operand is expanded
   to 16-bit fixed-point centroids and executed as an ordinary MAC in a shared
   Outlier/Post-Processing unit — one at a time, eight Gaussian PEs sharing one OPP. It is
   affordable only because it is under 4% of BERT's multiplications. **verified** (§II-E, §III-B)
7. **Post-training, and cheaply so.** No fine-tuning; activation statistics come from a single
   profiling batch of 8 samples, and the paper shows repeated profiling runs give near-identical
   accuracy — because the exponential bins widen with the index, so the bins that catch outliers
   are very wide. **verified** (§II, §IV-B, Fig. 8)
8. **The comparison is set up conservatively and the authors say so.** Iso-compute-area and
   iso-buffer-capacity against FP16 Tensor Cores; total chip area for Mokey is *smaller*
   (narrower buffers and interconnect) and they explicitly decline to spend that advantage.
   They also note an FP32 baseline — more common in practice — would have flattered them more.
   **verified** (§IV-C)
9. **65 nm.** Absolute area and energy here are not comparable with the 28 nm and 7 nm entries
   elsewhere in this corpus. Only the ratios travel. **verified** (§IV-B)

---

## Method

**What is quantized.** Weights, embeddings and activations — all of them, to 4-bit indices.
A 4-bit code is **1 sign bit + 3-bit index**; the value is `θ·(a^int + b)·s + m`.

**The three-step process.**

1. *Golden Dictionary, once, offline, model-independent.* Generate a random Gaussian
   (m=0, s=1) with 50,000 samples; run **agglomerative clustering** to 16 centroids; repeat and
   average. Symmetric around zero, so only 8 magnitudes are stored.
2. *Per tensor.* Take that tensor's mean and standard deviation — statically for weights, by
   profiling for activations — and apply `GD × s + m`. Non-iterative. Split the range into the
   **Gaussian subset G** (>98% of weights, >95% of activations) and the **outliers OT**.
3. *Pre-encode weights offline.* The model is then ready for inference.

**The exponential fit.** Half the (symmetric) Golden Dictionary is fitted to `a^int + b` by
MATLAB curve fitting, weighted so densely populated bins near zero count more — weights run
`2^7` at the inner bin down to `2^0` at the outer. Result: `a = 1.179`, `b = −0.977`,
`int ∈ [0,7]`.

**Why that makes MACs disappear.** For a weight/activation pair both on the curve,

    Σ A·W  =  s_A·s_W·Σ a^(int_A + int_W)  +  b-weighted sums of each operand  +  N·b²

The first term needs only the **sum of two 3-bit indices**, which lands in `[0,14]`. So the
hardware keeps 15 counters, increments one per pair, and performs a single weighted reduction
against the 15 centroid products at the end. The activation sum is computed while the previous
layer's output is being quantized; the weight sum is a compile-time constant.

**Outliers.** Separate 16-entry outlier dictionary; all values remain 4-bit indices; a list of
pointers records which are outliers. Products involving one are expanded to 16-bit fixed-point
centroids and run as a conventional MAC in the shared OPP unit.

**Hardware.** Tiles of 8 cascaded Gaussian PEs sharing one Outlier/Post-Processing unit. A
serial cascaded leading-one detector picks the first GPE holding an outlier and routes it to the
OPP; the OPP is also the post-processing engine for the final summations. Output activations
are produced as 16-bit fixed-point and requantized on the fly: compare against all 32 centroids
(G and OT are sorted), leading-one detector plus two muxes select the two neighbouring
centroids, subtract and compare to pick the nearer, encode as an index.

**Deployment modes.** Full Mokey accelerator, or **compression plug-in** — keep an existing
FP16 accelerator and use Mokey only to compress values into and out of memory.

## Key numbers, with their frame

| Setting | Model | Metric | Baseline | Result | Source |
|---|---|---|---|---|---|
| W4 only, PTQ | BERT-Base | MNLI Acc-m | FP 84.44 | 84.80 (**−0.36**, i.e. better) | Table I |
| **W4A4**, PTQ | BERT-Base | MNLI Acc-m | FP 84.44 | 84.22 (**0.22**) | Table I |
| W4A4, PTQ | BERT-Large | MNLI Acc-m | FP 86.65 | 85.69 (**0.96**) | Table I |
| W4A4, PTQ | RoBERTa-Large | SQuAD F1 | FP 93.56 | 92.58 (**0.98** — worst case) | Table I |
| W4A4, PTQ | DeBERTa-XL (750M) | MNLI Acc-m | FP 91.75 | 91.18 (**0.57**) | Table I |
| Outlier fraction | 4 models | % of values | — | **W 1.2–1.6%, A 1.7–4.5%** | Table I |
| Iso-area, iso-buffer, 512KB | BERT-Base | cycles | FP16 TC 167M | **29M** (GOBO 52M) | Table II |
| Iso-area, iso-buffer, 512KB | BERT-Base | energy | FP16 TC 0.36 J | **0.09 J** (GOBO 0.17 J) | Table II |
| Iso-area, iso-buffer, 512KB | BERT-Base | compute units / area | TC 2048 / 16.1 mm² | **3072 / 14.8 mm²** | Table II |
| PE only, equal MAC/cycle | — | area | tensor-core unit | **39% smaller** | §IV-C |
| Compute units | — | energy / area | FP16 Tensor Cores | **2.7× less energy, 1.6× smaller** | §I, §IV |
| Accelerator | NLP suite | speedup | FP16 TC, same buffer | **11× at small buffers → 4.1× at 4 MB** | Fig. 10 |
| Accelerator | NLP suite | energy efficiency | FP16 TC | **78× at 256 KB → 13× at large buffers** | Fig. 11 |
| Accelerator | NLP suite | energy efficiency | **GOBO** | **9× at small buffers → 2× at 4 MB** | §IV-C |
| **Compression plug-in only** | NLP suite | speedup | FP16 TC | **3.9× at 256 KB → 4.3× at 4 MB** | Fig. 14 |
| Compression plug-in only | NLP suite | energy efficiency | FP16 TC | **11× at 256 KB → 7.8× at 4 MB**; DRAM energy 4× | Fig. 15 |
| Iso-task, PTQ vs QAT | BERT-Base MNLI | error / compression | Q8BERT 0.69 / 4.0×; I-BERT 0.32 / 4.0×; Q-BERT 0.55 / 6.9×; GOBO 0.68 / 4.1×; TernaryBERT 1.14 / 10.8× | **Mokey 0.22 / 7.9×**, and the only row that is both fixed-point **and** post-training | Table IV |

**Evidence level: post-layout** (Verilog, Synopsys DC N-2017.09, Innovus place-and-route,
**TSMC 65 nm**, 1 GHz; CACTI for on-chip memories) **plus a custom cycle-accurate simulator**
for cycle counts. No silicon, no released artifact.

## Cost and requirements

- **Metadata per tensor**: G dictionary 8×16b, OT dictionary 16×16b, a few constants, and the
  outlier pointer list. Negligible against the tensors themselves, but the pointer list scales
  with the outlier count, which is where activations (up to 4.5%) cost more than weights.
- **A profiling pass** over one batch of 8 inputs before deployment.
- **The accuracy claim needs the Mokey hardware** for the compute results; the compression-only
  numbers do run on a stock Tensor Core accelerator.
- Requires the value distribution to actually be Gaussian-ish. The paper leans on layer
  normalization and softmax to keep ranges bounded.

## Limitations and open questions

**Admitted.** Outliers need a separate dictionary and a real multiplier path. The baseline is
FP16 rather than the more common FP32, which understates the gain. Dictionary size trades
accuracy against overhead.

**Not admitted.**

- **Per-tensor scaling is the ceiling.** Every 2023+ paper in this corpus moved to per-channel,
  per-token or per-group scales precisely because per-tensor breaks once activation outliers
  grow. Mokey predates that pressure and never tests a model where it bites. **inferred**
- **The exponential constraint is never ablated.** How much accuracy does forcing centroids
  onto `a^int + b` cost versus free agglomerative-clustering centroids? The paper reports the
  end-to-end accuracy but not that decomposition, and it is the paper's central trade.
  **inferred**
- **Encoder-only, ≤750M parameters, ≤512-token tasks.** No decoder model, no generation, no KV
  cache — the workload the entire 2024–26 LUT thread targets.
- **65 nm** makes every absolute number incomparable to the rest of this corpus.
- The headline **78×** energy figure is the 256 KB operating point, where the baseline is most
  starved. The honest range is 13–78×.

## Relation to other entries

**This is the root of the corpus's lookup thread, and the structure it invents is the one the
2025–26 papers rediscover.** "Count how often each index combination occurs, then do one
weighted reduction against a small table" is Mokey (2022) and it is also
[`OASIS`](../OASIS/ANALYSIS.md) (2026), which quantizes both operands so its table becomes the
Cartesian product of two codebooks — 256 static entries, reduction independent of `K`. Mokey
gets to 15 bins instead of 256 by *constraining the centroids to an exponential curve*; OASIS
gets to 256 by *learning both codebooks and paying for the bigger table*. Same problem, two
different prices, four years apart, and **OASIS does not cite Mokey**.

- [`TransitiveArray`](../TransitiveArray/ANALYSIS.md) — the other "the table is built by the
  GEMM itself" design. Mokey's histogram is a table of *counts*; TransArray's is a table of
  *partial sums*. Both avoid materialising products.
- [`LUTTensorCore`](../LUTTensorCore/ANALYSIS.md) — eager, per-tile, weight-only. Mokey is the
  only member of this group that quantizes **activations to the same width as weights**.
- [`OLAccel`](../OLAccel/ANALYSIS.md) (ISCA'18) — the outlier-thread root, four years earlier.
  Mokey's outlier handling is recognisably the same shape: dense low-precision majority, a
  sparse high-precision path, and an explicit list saying which is which.
- [`Ecco`](../Ecco/ANALYSIS.md) — the closest modern relative on the *non-uniform codebook plus
  entropy structure* axis, but at the GPU cache rather than in the datapath.
- **GOBO (MICRO'20)** is Mokey's direct predecessor and its main baseline; it is **not in this
  corpus** (MICRO), which is a gap the survey's §5.5 will feel.

## Note from the source list

> **Keywords:** quantizing all values to 4-bit indexes into dictionaries of representative 16-bit fixed-point centroids; Golden Dictionary generation


## Abstract (verbatim, arXiv:2203.12758v1)

> Increasingly larger and better Transformer models keep advancing state-of-the-art accuracy
> and capability for Natural Language Processing applications. These models demand more
> computational power, storage, and energy. Mokey reduces the footprint of state-of-the-art
> 32-bit or 16-bit floating-point transformer models by quantizing all values to 4-bit
> indexes into dictionaries of representative 16-bit fixed-point centroids. Mokey does not
> need fine-tuning, an essential feature as often the training resources or datasets are not
> available to many. Exploiting the range of values that naturally occur in transformer
> models, Mokey selects centroid values to also fit an exponential curve. This unique
> feature enables Mokey to replace the bulk of the original multiply-accumulate operations
> with narrow 3b fixed-point additions resulting in an area- and energy-efficient hardware
> accelerator design. Over a set of state-of-the-art transformer models, the Mokey
> accelerator delivers an order of magnitude improvements in energy efficiency over a Tensor
> Cores-based accelerator while improving performance by at least $4\times$ and as much as
> $15\times$ depending on the model and on-chip buffering capacity. Optionally, Mokey can be
> used as a memory compression assist for any other accelerator, transparently stashing wide
> floating-point or fixed-point activations or weights into narrow 4-bit indexes. Mokey
> proves superior to prior state-of-the-art quantization methods for Transformers.
