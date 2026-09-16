# SpZip: Architectural Support for Effective Data Compression In Irregular Applications

**Venue / Year:** ISCA 2021, pp. 1069-1082 · **Link:** https://doi.org/10.1109/ISCA52012.2021.00087 · **Reader:** Haoxuan · **Date:** 2026-09-14

## Tags

| | |
|---|---|
| **Level** | `ARCH+SYS` |
| **Q-oriented** | `NON-Q-ORIENTED` |
| **Data type** | `—` |
| **Generation** | `—` |
| **Optimization** | lossless value compression · delta byte-code · bit-plane compression (BPC) · per-data-structure format selection · decoupled traversal · dataflow configuration language · time-multiplexed operators · memory-backed queues · graph analytics |

## 1. One-line summary

**No quantization** — nothing is lost, no numeric type is designed, and `quantiz*`, `precision`,
`bitwidth`, `INT8`, `FP16`/`FP32`, `mantissa`/`exponent`, `codebook` and `accuracy` return
**zero hits each**, bibliography included; what SpZip adds is a **fetcher and a compressor beside
each core** (0.2% of a core at 45 nm), running dataflow programs written in a new **Dataflow
Configuration Language**, so that **lossless delta byte-coding and Bit-Plane Compression apply
per data structure — to the payload values as well as the index streams** — decoupled so
decompression hides behind the traversal: **gmean 3.0× over Update Batching, 1.5× over PHI**,
**1.7×/1.4×** less DRAM traffic.

## 2. Data type

**None named.** Zero hits for every quantization term, bibliography included. No value is ever changed; no arithmetic touches compressed data. Outliers, escape hatch, granularity, accumulator, PTQ-vs-QAT: all inapplicable.

**Widths only, of an opaque byte stream.** Range-fetch indexes 8/16/32/64-bit; BPC operands 32 or 64-bit; 32-bit queue word + 1 marker bit; delta emits an N-byte field + length prefix. The one format ever mentioned is *"floating-point values with little value locality, making them harder to compress"* (PR/PRD), width never given.

**It compresses values, not just structure.** Footnote 1 refuses to call CSR compression; §IV compresses adjacency matrix, **update bins and vertex data**. Compressing values is not quantizing them.

## 3. Optimization

**DCL + fetcher/compressor.** Acyclic graph of range-fetch / indirection / (de)compression operators wired by marker-carrying queues, time-multiplexed over two functional units (16 contexts, 16 queues, 2 KB scratchpad) — programmability without a reconfigurable fabric, justified by a 33% operator activity factor. New `enqueue`/`dequeue` instructions, TLB-based virtual addressing, OS-visible state. The compressor is the dual, issuing to LLC, with a **memory-backed queue unit** so 1024 UB bins need no scratchpad queues.

**Two format-blind codes, chosen per data structure.** Delta byte-code on short streams (neighbour sets), BPC on long chunks (bins) — *"no algorithm dominates"*. Order-insensitive chunks are sorted 32-at-a-time before coding: binned-update ratio **1.26× → 1.55×**. Compression, not decoupling, is what pays — decoupling alone is **+9% / +14%**.

## 4. Results

| | |
|---|---|
| Baseline | **Push**, **Update Batching** (Propagation Blocking authors' code), **PHI** (MICRO'19, authors' code), and a compressed memory hierarchy (VSC + BDI + LCP) — all re-implemented in the same simulator |
| Models / datasets | 7 graph/sparse kernels (PR, PRD, CC, RE, DC, BFS, SpMV) × 5 web/social graphs (22-118 M vertices) + nlpkkt240; with and without DFS preprocessing |
| Accuracy delta | **None — lossless.** No accuracy, error or quality metric exists in the paper |
| Speedup | gmean **3.0× over UB**, **1.5× over PHI** (1.8× with preprocessing); **1.6×** over plain Push. PHI+SpZip **6.1×** over Push, up to 15.4× (DC), 17×/24× per-input |
| Traffic | **1.7× / 1.4×** vs UB / PHI; PHI+SpZip 3.3× vs Push. CMH baseline manages only +0-28% |
| Energy / area | **Area 92.8k µm² per core = 0.2%** (fetcher 47.3k, compressor 45.5k). **No energy or power number anywhere in the paper** |
| Technology node | 45 nm FreePDK45 (yosys + CACTI), for area only; simulated system is a 16-core 3.5 GHz Haswell-like with DDR3-1600 |
| Evidence level | **zsim cycle-level simulation** (all speedup/traffic) + **45 nm RTL synthesis** (area only). No silicon, no PnR, no energy model |
| **Is the comparison fair?** | Fair. Iso-simulator, iso-input, iso-system; UB, PHI and the compressed-hierarchy baseline re-run from source, not quoted; 0.2%/core disclosed. Not silicon (zsim + 45 nm synthesis); **no energy or power number anywhere**; iteration-sampled 1-in-5. Don't quote 3.0× as "over a multicore" (it is UB+SpZip over UB; Push+SpZip is 1.6×) or 15.4×/24× (maxima over a grid) |

## 5. Comment

General compression for sparse data. Not for LLM. **Likely beyond our interested range.**

## 6. Claude notes

*Suggestions from the reading agent. **Strip this section before copying into
`QuantArchSurvey/venues/ISCA/notes/`.***

- **Disposition.** Agreed, out of scope. Keep the row as a background citation so the audit trail survives; no body paragraph, no data-type tag, no generation. Note kept short deliberately.
- **`TAXONOMY.md`'s worked example: verdict upheld, justification wrong — and the justification is the part that matters, because it teaches a test.** *"No quantization at all"* is **correct** and now evidenced: de-hyphenated whole-document sweep, bibliography included — `quantiz*`/`quantis*` **0**, `precision` **0**, `bitwidth`/`bit-width`/`bit width` **0**, `INT8`/`INT4`/`INT16` **0**, `FP32`/`FP16`/`BF16` **0**, `fixed-point` **0**, `mantissa`/`exponent` **0**, `low-bit` **0**, `codebook` **0**, `lookup`/`LUT` **0** (2 substring hits are `polluting` and the surname `Lutz`), `bit-pack`/`bitpack` **0**, `value compression` **0**, `numeric`/`word length` **0**, `accuracy`/`error`/`approximat*`/`rounding`/`truncat*` **0**, `lossless`/`lossy` **0**, `dictionary` **1** (ref. [55], a *cache*-compression paper), `floating-point` **1**, `data type` **3** (all Fig. 7/15's *"traffic by data type"*, meaning adjacency matrix / vertex / updates — a grep trap). **Bibliography: 82 refs, zero quantization or low-precision papers**; the only two DNN citations are SIGMA (as an irregular-app accelerator) and Sze et al., cited **for run-length encoding**.
- **But *"only sparse-format compression"* is wrong, and the paper says so itself.** Footnote 1, p. 1070: *"we use the term compression only to refer to **data (entropy) compression**, and refer to CSR simply as a sparse data structure."* §IV Schemes: *"for UB and PHI, we compress all structures (adjacency matrix, **update bins, and vertex data**)"*. §V-A: *"more muted on PR and PRD because they have **floating-point values** with little value locality, making them harder to compress."* **So it compresses payload values, floats included — hypothesis (b), loudly.** `bitmap`/`bitvector`: 0 hits, so it is not even bitmap work.
- **The right reason for `NON-Q-ORIENTED` is format-blindness, not structure.** Delta and BPC see bytes and bit-planes. Put beside **`ENEC`** — ruled `Q-ORIENTED` for targeting BF16's **exponent field** — the pair gives the survey a crisp discriminator: *not* lossy-vs-lossless, *not* value-vs-structure, but **whether the code knows the numeric format**. SpZip's only remark about floats is that they compress badly, and it does nothing about it. That contrast is the one thing I would keep from this paper.
- **Suggested taxonomy gloss, reported never applied:** "SpZip has no quantization at all: it applies lossless, **format-blind** entropy coding — delta byte-codes and bit-plane compression — to whatever an irregular application streams, **values included**. Compressing values is not quantizing them."
- **Two of our own files repeat the wrong gloss and should be corrected when touched** (parallel agents own them, so nothing applied): `ENEC/ANALYSIS.md` line 412 says SpZip has *"no floating-point values in play"* — refuted by §V-A; `Cambricon-SR/ANALYSIS.md` line 455 and `TransitiveArray/ANALYSIS.md` line 351 quote *"sparse-format compression"* verbatim. The Cambricon-SR pairing still holds, but Cambricon-SR really is structural (a bitmap) and SpZip is not — two different kinds of non-quantization paper.
- **Seed-tag dispute, one:** `ARCH` → **`ARCH+SYS`**. DCL is claimed as a contribution in the abstract; §III-D adds two ISA instructions, MMIO configuration, TLB-based virtual addressing with page-fault interrupts, coherence, and OS-visible state saved on context switch, plus a modified Ligra runtime. **Counter-evidence, stated:** no compiler is built (*"the DCL program is manually extracted"*), so plain `ARCH` is defensible if you require a shipped stack. Also drop `CSR` from the Optimization keywords — it is what produced the wrong gloss.
- **Read depth.** Full close read of §I-§VII; reference list by grep. Figs. 7/8/15-22 are raster bar charts — every number above is one the prose states, none read off a plot. Unresolved: the width of the floating-point vertex data (never given), and `lossless` is inferred from the two cited codes, since the word never appears.
