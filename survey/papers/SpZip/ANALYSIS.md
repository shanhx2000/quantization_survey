# SpZip — paper notes

**SpZip: Architectural Support for Effective Data Compression In Irregular Applications**
Yifan Yang, Joel S. Emer, Daniel Sanchez (MIT · NVIDIA)
**ISCA 2021**, pp. 1069-1082 ｜ DOI: **10.1109/ISCA52012.2021.00087**
Publication info verified 2026-09-02: venue, year **and DOI** all read out of the archived
PDF's own text (IEEE proceedings banner; the DOI was grepped for, not assumed); page range
from the ACM DL / IEEE Xplore record.
Archived here: the **published IEEE version** (the page-1 IEEE proceedings banner is present in the extracted text), 14 pages.

Status: **note ready** ｜ Last updated: 2026-09-14
Tags: `lossless-compression` `accelerator`
How far it was read: **full close read of §I-§VII (pp. 1069-1081) plus the reference list
(pp. 1081-1082) by grep.** Read line by line: §I; §II-A (DCL operators, queues), §II-B (CSR,
Fig. 1-3 and **footnote 1**, the load-bearing sentence), §II-C (PageRank/BFS pipelines,
Fig. 5-6), §II-D (Update Batching, PHI, preprocessing, the BFS/uk-2005 case study of
Fig. 7-8); §III-A to §III-E (fetcher microarchitecture, AU/DU/scheduler/queues, the
compressor, MQU, order-insensitive resorting, system integration, Table I area); §IV
(methodology, Tables II-III, **"Schemes"** — the other load-bearing paragraph); §V-A to §V-D
(all four evaluation subsections); §VI-§VII.
**Skimmed, and itemised honestly:** (a) the **reference list** was read by grep, not entry by
entry — the load-bearing fact is that a de-hyphenated sweep for
`quantiz|precision|bit-width|INT8|FP16|FP32|low-bit|codebook|numeric|fixed-point` over
pp. 1081-1082 returns **zero**; (b) **Figs. 7, 8, 15, 16, 17, 18, 19, 20, 21, 22 are raster
bar charts.** Their axis labels and a handful of clipped bar annotations extract as text but
the bars themselves do not, so **every number below is one the prose states**; no bar value
has been read off a plot. Where the prose gives only a geomean I have not invented per-input
values. (c) Fig. 11's fetcher-configuration table extracts as scrambled column fragments and
was read for field *names* (`idxSz (B)`, `elemSz (B)`, `lastVal`, `width`) rather than for its
numbers. **Not resolved:** the paper never states the width of the floating-point vertex data
it compresses (see `## Method`, "The datapath question"), and the word `lossless` never
appears — losslessness is an inference from the two algorithms cited, not a quotation.

> Publisher record: https://ieeexplore.ieee.org/document/9499902
> **There is no arXiv version** (arXiv API title search, 2026-09-02). The PDF was downloaded by a
> human and filed through [`survey/uploads/`](../../uploads/) — the sanctioned route when the
> arXiv-only rule leaves a paper unreachable; see
> [`Notes-002`](../../../Claude/notes/Notes-002-paper-source-access.md).
> The PDF is **not committed** (1.2 MB) and **cannot be re-downloaded by script** —
> both publishers 403. Re-extract with `python3 extract.py` → `extracted/` (committed).
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, ISCA 2021 row.

---

## ⚠ The taxonomy's own worked example: verdict upheld, justification wrong

`QuantArchSurvey/TAXONOMY.md` uses this paper as its counterexample —
*"SpZip (ISCA'21) | `ARCH` | `NON-Q-ORIENTED` | — | —"*, glossed as **"SpZip has no
quantization at all, only sparse-format compression."** That is load-bearing for the survey's
own definitions, so it was tested rather than inherited. Two findings, and they point
different ways.

**1. "No quantization at all" is CORRECT, and now rests on evidence.** A negative claim needs
the same evidence as a positive one (the `XtraMAC` precedent).

**2. "only sparse-format compression" is WRONG, and the paper says so itself in a footnote.**
SpZip's compression is *not* the sparse format. It is **lossless value/entropy compression —
delta byte-coding and Bit-Plane Compression — applied to the payload values as well as to the
index streams**, floating-point vertex data included. The `NON-Q-ORIENTED` tag survives; the
one-line reason printed next to it does not.

### The sweep

Counted over `extracted/10.1109_ISCA52012.2021.00087.raw.txt` **after de-hyphenating across
line breaks** (`-\n` joined) so that `quan-\ntization` could not hide; cross-checked against
the `-layout` text. Whole document, bibliography included.

| Term | Hits | Term | Hits | Term | Hits |
|---|---|---|---|---|---|
| `quantiz*` / `quantis*` | **0** | `precision` | **0** | `bitwidth` / `bit-width` / `bit width` | **0** |
| `INT8` / `int8` / `INT4` / `INT16` | **0** | `FP32` / `FP16` / `BF16` | **0** | `fixed-point` / `fixed point` | **0** |
| `mantissa` / `exponent` | **0** | `low-bit` | **0** | `numeric` / `word length` | **0** |
| `codebook` | **0** | `lookup` / `look-up` / `LUT`† | **0** | `bit-pack` / `bitpack` | **0** |
| `value compression` | **0** | `residual` | **0** | `accuracy` | **0** |
| `approximat*` / `error` / `rounding` / `truncat*` | **0** | `lossless` / `lossy` | **0** | `Huffman` / `varint` | **0** |
| `dictionary` | **1**‡ | `floating-point` | **1** | `float` (as a word) | **1** (same sentence) |
| `data type` | **3**§ | `delta` | **16** | `BPC` / `bit-plane` / `bitplane` | **9** / **2** / **1** |
| `entropy` | **2** | `run-length` | **1** | `compress*` | **295** |

† All `lut` substring hits are inside `polluting` and the surname `Lutz` (ref. [4]). Zero as a word.
‡ Reference [55], *"Dictionary sharing: An efficient cache compression scheme"* — a cache-compression paper, not a quantization one.
§ All three are Figs. 7/15's *"breakdown of main memory traffic by data type"*, where "data type" means **adjacency matrix / source vertex / destination vertex / updates** — a data-*structure* class, not a numeric type. A trap for a grep-only reader.

**The bibliography is clean.** 82 references, pp. 1081-1082. Zero quantization papers; zero
low-precision papers. The nearest neighbours are all cache/memory compression
(BDI [57], LCP [56], VSC [7], HyComp [8], SC² [9], dictionary sharing [55], BPC [35], IBM
MXT [69], IBM NXU [1]) and graph systems. Exactly two DNN-literature citations exist and
neither is about numeric formats: [58] SIGMA (a sparse GEMM accelerator, cited as an
irregular-application accelerator) and [67] Sze/Chen/Yang/Emer's *Efficient Processing of
Deep Neural Networks*, cited **for run-length encoding** as an example compression format the
DCL could host. **verified** (references, pp. 1081-1082). The authors do not situate
themselves in the quantization literature at all.

### The hypothesis that mattered: structural or payload?

The interesting question is not whether the word "quantization" appears but **what SpZip
compresses** — positions and offsets only (purely structural), or the sparse tensor's values
too. Delta encoding plus variable-length packing of integers is value compression, and shades
toward a numeric-format question. **It is the payload too, explicitly, and the paper is
unambiguous about it.**

1. **The paper refuses the "sparse-format compression" reading in its own footnote.**
   Footnote 1, p. 1070: *"The term compressed here means that zeros are not explicitly
   stored. To avoid confusion, in this paper we use the term compression only to refer to
   **data (entropy) compression**, and refer to CSR simply as a sparse data structure."*
   **verified** (§II-B footnote 1, p. 1070). CSR's structural sparsity is the *workload*;
   entropy compression on top of it is the *contribution*. Fig. 3's caption reads *"DCL
   pipeline for matrix where each sparse row is **entropy-compressed**."*
2. **Vertex data — the values — are compressed, and the paper says which experiments do it.**
   §IV, "Schemes", p. 1077, verbatim: *"For Push, we compress the adjacency matrix, but not
   vertex data; **for UB and PHI, we compress all structures (adjacency matrix, update bins,
   and vertex data)**; destination vertex data is compressed after applying each bin in the
   accumulation phase. We compress the adjacency matrix using delta encoding, and each
   application uses the best of BPC [35] and delta encoding for the other structures."*
   **verified**.
3. **Update bins carry values, not just indices.** A bin entry is a
   `{dst, contribs[src]}` tuple (Listing 3, p. 1073; Listing 5 line 13, p. 1076) — a
   destination id *and* a numeric update. Compressing bins is the single largest traffic win
   without preprocessing (§V-C, p. 1080). **verified**.
4. **The payload is floating-point in two of the seven benchmarks, and the paper reports the
   consequence.** §V-A, p. 1078: *"Its benefits are more muted on PR and PRD because they have
   **floating-point values with little value locality, making them harder to compress**."*
   And §V-C, p. 1080: *"in DC, where **degree counts are small and highly compressible
   integers**."* **verified.** These two sentences are the whole case: SpZip's codes are being
   run over application *values*, and their effectiveness is being reported as a function of
   the values' numeric character.
5. **The codes themselves are integer value codes.** §III-B, p. 1074: delta encoding *"simply
   subtracts the previous and current inputs, and emits an N-byte output if their delta (plus
   a small length prefix) fits within N bytes (some prior work calls this a byte code [62])"*
   — i.e. variable-length **byte**-packing (not bit-packing) of first-order differences. BPC
   [35] is Kim et al.'s Bit-Plane Compression: a delta transform followed by a bit-plane
   transpose and per-bit-plane symbol coding. **verified**.
6. **A further value-level trick: resorting.** §III-C, p. 1076: chunks of order-insensitive
   data (bins, the frontier) are optionally **sorted before compression** — 32 elements in the
   implementation — *"This places similar values nearby, which improves compression ratios in
   both delta encoding and BPC."* Sorting binned updates lifts their compression ratio from
   **1.26× to 1.55×** (CC on UB, all inputs; §V-C, p. 1080). **verified.** That is a
   value-distribution optimization, not a structural one.

### But it is still not quantization, for three reasons

- **Nothing is lost.** Both codes are exactly invertible, results are exact, and no accuracy,
  error, approximation or quality metric appears anywhere in the paper (`accuracy`,
  `error`, `approximat*`, `rounding`, `truncat*`: **0** hits each). *(The word `lossless`
  itself never appears — this is **inferred / not verified** from the algorithms cited and
  from the absence of any error metric, not from a sentence.)*
- **No format is designed or narrowed.** SpZip never proposes a numeric type, never reduces an
  element's width, and never inspects an element's fields. Contrast [`ENEC`](../ENEC/ANALYSIS.md),
  which was ruled `Q-ORIENTED` on 2026-09-14 precisely because it targets the **exponent field**
  of BF16. BPC and delta are **format-blind**: they see bytes and bit-planes. The clearest
  proof is negative — when floats do turn up, the paper's only comment is that they compress
  *badly*, and it makes no attempt to exploit their structure (§V-A, p. 1078).
- **Swap the format for plain INT8 and everything survives** — the DCL, the fetcher, the
  time-multiplexed operator contexts, the scheduler, the MQU, the decoupling, the markers, the
  resorting. Nothing in the design reads the width or the meaning of a value; element size is
  a per-operator configuration field (`elemSz (B)`), not a design variable.

**Verdict: `NON-Q-ORIENTED`, data type `—`, generation `—` — tags unchanged.** But
`TAXONOMY.md`'s gloss should read something like *"SpZip has no quantization at all: its
compression is **lossless entropy coding of the values and indices** an irregular application
streams, not a change of numeric format"*. As written, the gloss teaches the wrong test —
that a paper is out of scope because it compresses *structure*. SpZip compresses values and
is still out of scope, and that is the more instructive case. **Reported, not applied** —
`QuantArchSurvey/` is read-only.

---

## What the close read changed in the brief

**The headline finding survived; three things needed fixing and two numbers needed frames.**
(1) The brief's con *"No quantization content whatsoever — lossless structural compression for
graph workloads; the source list's own note says 'No quantization; CSR format'"* is **half
wrong**: the no-quantization half is confirmed on a ~35-term de-hyphenated sweep plus the
bibliography, but *"structural"* and *"CSR format"* are refuted by the paper's own footnote 1
and by §IV's Schemes paragraph — **vertex data and update values are compressed too**.
(2) The brief's *"gmean 3.0× over software-only and 1.5× over hardware-accelerated prior
work"* is correct but **frameless and quotable in a misleading way**: 3.0× is
**UB+SpZip over UB**, and SpZip on a plain Push multicore is only **1.6×**. (3) *"PHI+SpZip is
6.1× over Push"* was in the brief; the close read pins it as a **gmean without preprocessing**
(5.9× with), with per-application maxima of 15.4×/16.9× and a per-input maximum of 17×/24×
that must not be quoted bare. (4) New material the brief did not have: the entire
value-vs-structure finding above; the fact that **compression, not decoupling, is what pays**
(decoupling alone is +9%/+14%); and that **the paper reports no energy or power number at
all**, which for a data-movement paper is the most surprising omission.

---

## Brief

### 1. Motivation

Irregular applications (graph analytics, sparse linear algebra) are memory-bandwidth-bound,
so compression should help — but software compression overhead swamps the gain (Ligra+ [62]
gets 14%), and prior hardware compressors either assume long sequential streams (IBM
MXT/NXU [1, 69]) or compress fixed-size lines transparently and are blind to application
semantics (VSC [7], BDI [57], LCP [56]). **verified** (§I, §VI, pp. 1069, 1081). SpZip aims at
the gap in the middle: **short but compressible chunks**, reached by data-dependent
indirections.

### 2. Overview

Architectural support that accelerates **traversal, decompression and compression
together**, decoupled from the core so memory and decompression latency are hidden.
Programmable via a **Dataflow Configuration Language** (DCL) — an acyclic graph of
memory-access operators (indirection, range fetch) and (de)compression operators wired by
queues — implemented cheaply through dataflow execution and time-multiplexing of two
functional units over up to 16 operator contexts and 16 queues in a 2 KB scratchpad.
Evaluated in a simulated 16-core system across graph and linear-algebra algorithms, on top of
three execution strategies (Push, Update Batching, PHI) and five preprocessing orders.

### 3. Pros and cons

**Pros**

- Correctly identifies that traversal and decompression are *interleaved* in irregular
  workloads, so accelerating one without the other does not help — this framing is the
  contribution. **verified** (§I, p. 1069).
- **Per-data-structure compression is the real idea.** Rather than one code for the address
  space, each data structure gets the code its access pattern can afford: delta on short
  neighbour sets, BPC on long bin chunks, nothing on scattered single-element updates.
  **verified** (§III-B, p. 1074).
- Cheap for what it does: fetcher **47.3k µm²** and compressor **45.5k µm²** at 45 nm, together
  **0.2% of a general-purpose core's area**. **verified** (Table I, §III-E, p. 1077).
- Strong and consistently reported: gmean **3.0×** over UB and **1.5×** over PHI, with
  **1.7×/1.4×** traffic reduction; composes with orthogonal schemes (PHI+SpZip **6.1×** over
  Push). **verified** (abstract, §I, §V-A).
- **The paper argues against itself where it should.** §V-A concedes compression *"barely
  helps"* on plain Push; §V-C shows decoupling alone is worth only 9-14%; §V-B shows the
  headline depends on which preprocessing order you use. Unusually well-conditioned claims.

**Cons**

- **No quantization** — but for the *right* reason: the compression is lossless entropy coding
  of values and indices, format-blind, with no numeric type designed. See the ⚠ section.
- **Simulation-only.** zsim cycle-level simulation; hardware exists only as RTL synthesized
  with yosys/FreePDK45 for an area figure. No silicon, no PnR. **verified** (§III-E, §IV).
- **No energy or power number anywhere in the paper** (`power` 1 hit, in a reference title;
  `energy` 2 hits, both in reference titles; `watt` 0). A data-movement-reduction paper that
  never prices the energy it claims to save. **verified** by sweep.
- **Iteration sampling**: every 5th iteration simulated, the rest fast-forwarded. Disclosed
  and defended (*"characteristics of graph algorithms change slowly over iterations"*), but it
  is an approximation in the headline. **verified** (§IV, p. 1077).
- Programmability via a new configuration language is a real adoption cost the paper does not
  price: DCL programs are *"manually extracted via analyzing the data structures and their
  traversal pattern"*, and automatic generation from TACO/GraphIt is speculation, not built.
  **verified** (§III-D, p. 1076).
- Compression is worthless on the access pattern that dominates unoptimized graph code:
  scatter updates to single elements, >80% of Push's traffic. SpZip's gains need UB, PHI or
  preprocessing to first *make* the traffic compressible. **verified** (§II-D, p. 1072).

### 4. Where it applies

Outside the taxonomy. Keep for the **lossless-compression / data-movement** cluster as the
graph-workload counterpart to the DNN-focused entries — and, now, as the corpus's clean
example of **lossless value compression that is nonetheless not a quantization paper**, which
is a sharper boundary marker than "it only compresses structure" was.

---

## Conclusions

Read in full. The tags stand; the taxonomy's one-line justification for them does not. The
paper's transferable idea for a quantization survey is **per-data-structure code selection
under a decoupled programmable fetcher** — the observation that the right compression format
is a property of the *access pattern*, not of the data, and that it must be chosen per
structure rather than per address space.

## Method

**The DCL — the hardware/software interface, and the paper's named contribution.** An acyclic
dataflow graph of operators communicating through queues. Two memory-access operators:
*indirection* (`i → A[i]`) and *range fetch* (`i:j → A[i..j-1]`). Plus
*decompression/compression* operators, one per supported format. Queues are circular buffers
in a scratchpad with min/head/tail/max pointers, and carry **markers** — each 32-bit word has
a marker bit; a set bit means "chunk boundary" rather than data, which is how variable-length
chunks survive a fixed-width queue. Markers pass through every operator, so the core can
recover chunk structure from a flat stream. On x86 the marker bit is delivered in the
**overflow flag** of the `dequeue` instruction. **verified** (§II-A, §III-B, pp. 1070, 1074).

**Fetcher microarchitecture — time-multiplexing as the cheap route to programmability.** The
rejected alternative is a reconfigurable fabric of operators wired by an interconnect. The
observation that kills it: a unit sized at 32 B/cycle only needs to fire ~33% of cycles to
run ahead of the core, so operators have low activity factors and can share physical units.
Result: one **Access Unit** (address generator + response handler, up to 8 outstanding cache
lines), one **Decompression Unit** holding logic for every supported format, a **2 KB
scratchpad** holding all queues, and a **scheduler** picking one ready operator per cycle
round-robin. 16 contexts, 16 queues. **verified** (§III-B, p. 1074).

**Compressor — the dual, plus the memory-backed queue.** Same skeleton, but it issues **LLC**
accesses rather than L2 (to avoid polluting private caches with write-once data) and its
functional units are a Compression Unit, a Stream Writer Unit and a **Memory-backed Queue
Unit**. The MQU exists for Update Batching: 1024 bins would need 2048 scratchpad queues, so
instead the queue storage *and its pointers* live in ordinary cached memory, and the MQU
enqueues `(queueId, value)` tuples with plain loads and stores. When an in-memory queue fills
it streams out as a chunk to be compressed; when a compressed bin runs out of space the MQU
interrupts the core to allocate more (initial allocation e.g. 2 MB/bin). **verified**
(§III-C, pp. 1075-1076).

**The two codes, and why two.** *"we observe that no algorithm dominates"* — **delta encoding**
[57] is a byte code: subtract previous from current, emit an N-byte field plus a short length
prefix if it fits. Cheap, works on short streams like a single neighbour set. **BPC** [35]
needs ~32 elements to pay off but compresses better, so it goes on long chunks like UB bins.
The implementation supports **32- or 64-bit elements** and uses *"a simple byte-level symbol
encoding for each bitplane"*. Assignment in the evaluation: adjacency matrix always delta;
everything else *"the best of BPC and delta encoding"*, per application. **verified**
(§III-B, §III-E, §IV, pp. 1074, 1077).

**Order-insensitive resorting.** Bins and the frontier are *sets*, so element order is
semantically free. SpZip optionally sorts each 32-element chunk before compressing it, which
clusters similar values and helps both codes. **verified** (§III-C, p. 1076).

**System integration — this is what makes the Level call interesting.** New `enqueue`/`dequeue`
**instructions**; memory-mapped I/O for queue and context configuration; operation on
**virtual addresses** through the core's L2 TLB with page faults raised as interrupts to the
core; coherent accesses, with shared read-modify-write vertex data left to the core's atomics
and merely *prefetched* by the fetcher; **architecturally visible state** that the OS must
quiesce and save on a process context switch. Application code is unchanged — a modified
Ligra-style framework holds the DCL programs. **verified** (§III-D, p. 1076).

**The datapath question — what widths exist, since a width is a fact worth recording even in a
`NON-Q-ORIENTED` paper.** SpZip's data path is format-agnostic byte plumbing, but it is not
width-agnostic:

| Where | Width | Source |
|---|---|---|
| Range-fetch index | **8 / 16 / 32 / 64-bit**, per-operator config | §III-B, p. 1074, **verified** |
| Element size | per-operator field `elemSz (B)`; Fig. 11 shows **8 B** and **4 B** operators | Fig. 11, p. 1075, **verified** |
| Queue word + marker | **32-bit word + 1 marker bit** | §III-B, p. 1074, **verified** |
| BPC operand | **32- or 64-bit elements**, byte-level symbol per bit-plane | §III-E, p. 1077, **verified** |
| Delta operand | arbitrary; output is an **N-byte** field + length prefix | §III-B, p. 1074, **verified** |
| Vertex data in PR/PRD | **floating-point**, width never stated | §V-A, p. 1078 — **not resolved** |
| Vertex data in DC | *"small and highly compressible integers"*, width never stated | §V-C, p. 1080 — **not resolved** |
| Cache line / flit | 64 B lines, 128-bit flits | Table II, p. 1077, **verified** |

So: **8/16/32/64-bit elements, and the only format ever named is "floating-point", once, as a
reason compression works badly.** That is the whole numeric-format content of the paper.

## Key numbers, with their frame

All performance and traffic numbers are **zsim cycle-level simulation** of a 16-core
Haswell-like system (Table II: 3.5 GHz OOO, 32 KB L1, 256 KB private L2, 32 MB shared L3,
4×4 mesh, MESI, 4× DDR3-1600 = 51.2 GB/s), with **iteration sampling (every 5th iteration)**.
Area is **yosys + FreePDK45 45 nm synthesis** plus CACTI for SRAM. **There is no energy or
power number in the paper.** Do not pool these three evidence levels.

| Setting | Model / workload | Metric | Baseline | Result | Source |
|---|---|---|---|---|---|
| Headline, abstract | 7 apps × 5-6 inputs | speedup, gmean | **UB** (best software-only) | **3.0×** | Abstract; §I; §V-A **verified** |
| Headline, abstract | same | speedup, gmean | **PHI** (hw-accelerated SOTA) | **1.5×** | Abstract; §V-A **verified** |
| Headline, abstract | same | DRAM traffic | UB / PHI | **1.7× / 1.4×** less | Abstract; §I **verified** |
| No preprocessing | same | speedup, gmean | **Push** | **1.6×** — *the number a reader assumes "3.0× over a multicore" means* | §V-A, p. 1078 **verified** |
| No preprocessing | same | speedup, gmean, max | UB (software-only) | 3.0×, **up to 5.2×** | §I, p. 1070 **verified** |
| No preprocessing | same | speedup, gmean | Push | **PHI+SpZip 6.1×** (up to **15.4×** on DC); 4.8× over UB | §V-A, p. 1078 **verified** |
| With DFS preprocessing | same | speedup, gmean | Push / UB / PHI | **1.5× / 4.2× / 1.8×**; PHI+SpZip **5.9×** over Push (up to **16.9×** on DC) | §V-A, p. 1078 **verified** |
| Per-input maxima | DC on `arb` | speedup | Push | **17× / 24×** (without / with preprocessing) | §V-A, p. 1078 **verified** — *max over a grid* |
| Per-input maxima | DC on `twi` | traffic | Push | **9.5× / 6.2×** | §V-A, p. 1078 **verified** — *max over a grid* |
| No preprocessing | same | traffic | Push | UB+SpZip **1.9×**, PHI **2.2×**, PHI+SpZip **3.3×** (up to 7.2× on DC) | §V-A, p. 1078 **verified** |
| With preprocessing | same | traffic | own baseline | Push+SpZip **1.4×**, UB+SpZip **2.1×**, PHI+SpZip **1.7×** | §V-A, p. 1078 **verified** |
| Case study | BFS on `uk-2005`, 16 cores | speedup | Push | Push+SpZip 1.7×; UB 2.5×; UB+SpZip 6.0×; **PHI+SpZip 7.4×** (6.3× with preprocessing) | §II-D, pp. 1072-1073 **verified** — *one app, one graph* |
| Ablation | all apps/inputs | speedup | PHI | **decoupling alone +9% / +14%**; with compression **1.5× / 1.8×** | §V-C, p. 1080 **verified** — *compression, not decoupling, is what pays* |
| Ablation | all apps/inputs | compression ratio | — | binned updates **1.26× → 1.55×** from sorting 32-element chunks (CC on UB) | §V-C, p. 1080 **verified** |
| Preprocessing choice | `uk-2005`, 6 apps | adjacency-matrix compression ratio | uncompressed | DegreeSort **1.4×**, BFS **2.3×**, DFS **2.4×**, GOrder **2.4×** | §V-B, p. 1079 **verified** |
| vs compressed memory hierarchy | all apps/inputs | speedup | Push (no CMH) | **CMH: Push +0%, UB +11%** (no preprocessing); **+3%, +28%** (with) vs SpZip's **1.5×, 4.2×** | §V-D, p. 1080 **verified** — CMH = VSC + BDI + LCP, re-implemented |
| Sensitivity | CC on `uk-2005` | speedup | 1 KB scratchpad | 2 KB **+2.6% / +10%**; 4 KB negligible further | §V-C, p. 1080 **verified** |
| Area | — | µm², 45 nm | Haswell core scaled to 45 nm | Fetcher **47.3k** (AccU 10.1k, DecompU 22.5k, scratchpad 6.8k, sched 7.9k); Compressor **45.5k** (MQU+SWU 5.8k, CompU 25.0k, scratchpad 6.8k, sched 7.9k) = **0.2% of a core** | Table I, §III-E, p. 1077 **verified** |
| Energy / power | — | — | — | **none reported** | sweep **verified** |

**Inputs** (Table III, p. 1077): `arb` arabic-2005 (22 M vertices / 640 M edges), `ukl`
uk-2005 (39/936), `twi` Twitter followers (41/1468), `it` it-2004 (41/1150), `web`
webbase-2001 (118/1020); `nlp` nlpkkt240 (27/760) for SpMV. Non-preprocessed variants are made
by **randomizing vertex ids**. **Applications** (§IV, p. 1077): all-active PR, DC, SP;
non-all-active PRD, BFS, CC, RE. >100 billion instructions simulated for the largest graph.

### Citation hazards

1. **"3.0×" is not "over a multicore".** It is **UB+SpZip over UB**, i.e. SpZip added to the
   best software-only *optimized* strategy. Adding SpZip to a plain Push multicore gives
   **1.6×** (1.5× with preprocessing). The abstract's phrasing — *"outperforms prior
   state-of-the-art software-only (hardware-accelerated) systems by gmean 3.0× (1.5×)"* — is
   accurate; the paraphrase in the intro, *"Over a multicore without hardware support,"* is
   what invites the misreading.
2. **6.1× and 7.4× are stacked numbers.** 6.1× is **PHI+SpZip** over Push — most of it is
   PHI's own ~4.1×. 7.4× (and 6.3×) are **BFS on uk-2005 only**, from the motivation section,
   not a geomean.
3. **15.4× / 16.9× / 17× / 24× are maxima over a grid** (DC, and DC on `arb`), with no average
   attached in the same sentence. `SmartExchange` / `Ecco` / `NDPLowBitFP` failure mode.
4. **Compression, not decoupling, is the mechanism** — but the paper is a *fetcher* paper by
   title. The 9%/14% decoupling-only ablation should accompany any citation that presents
   SpZip as a prefetcher/fetcher result.
5. **Do not pool the area figure with the speedups.** 0.2% is 45 nm RTL synthesis; the
   speedups are simulation of a Haswell-like core that was never synthesized. And there is no
   energy number to pool at all.

## Cost and requirements

- **Area:** 92.8k µm² per core (fetcher + compressor) at 45 nm FreePDK45 = **0.2% of a core**.
  Includes a 2 KB SRAM scratchpad in each engine (CACTI). **verified** (Table I).
- **ISA:** two new instructions, `enqueue` / `dequeue`, the latter returning a value plus the
  marker bit (in the x86 overflow flag). **verified** (§III-B).
- **OS:** architecturally visible fetcher/compressor state must be quiesced and saved on a
  process context switch; page faults from the engines interrupt the core. **verified**
  (§III-D).
- **Cache hierarchy:** fetcher issues to the private L2, compressor to the shared LLC.
  Compressed data stays compressed in L2 and LLC, raising effective capacity. **verified**
  (§III-B, §III-C). Unlike PHI, SpZip does **not** modify the cache hierarchy itself.
- **Software:** DCL programs, currently hand-derived from the data structures and embedded in
  a modified Ligra-style framework; application code unchanged. Automatic generation from
  TACO/GraphIt is proposed, not built. **verified** (§III-D).
- **Memory:** software must pre-allocate per-bin space (e.g. 2 MB) and handle grow-on-demand
  interrupts from the MQU. **verified** (§III-C).
- **Accuracy cost:** none — the codes are exactly invertible. **inferred / not verified**
  (never stated; `lossless` 0 hits, no error metric anywhere).

## Limitations and open questions

- **Compression only pays where the access pattern is already contiguous.** *"compression
  opportunities exist whenever the application accesses contiguous sequences of elements,
  i.e., after range fetch operators"* (§II-B, p. 1072). Scattered single-element updates —
  >80% of Push's traffic — are incompressible by construction, so SpZip's value depends on UB,
  PHI or preprocessing having already restructured the traffic. The paper is candid about
  this; a citation that is not would be misleading.
- **Preprocessing does much of the work and is not costed.** DFS reordering raises the
  adjacency matrix's compression ratio from ~1.4× to 2.4×, and the paper notes preprocessing
  cost *"is often much higher than the algorithm itself"* without amortizing it into any
  headline. **verified** (§II-D, §V-B).
- **Compression favours a different preprocessing choice than the field's default.** DegreeSort
  is the widely used one; with compression, topological orders (BFS/DFS/GOrder) win because
  they cluster *values*, not just degrees. A genuine finding, buried in §V-B.
- **Two codes, chosen by hand.** The DU holds logic for every supported format, so adding a
  third code costs area in every core; and *"each application uses the best of BPC and delta
  encoding"* is an oracle choice made offline, not a runtime decision.
- **No energy model.** The entire argument is data movement, and the paper never converts
  traffic into joules.
- **Simulation only, and no comparison against a graph ASIC.** §VI argues SpZip would *benefit*
  Graphicionado-class accelerators; it does not evaluate that.
- **Open, and relevant to this survey:** the paper never asks what happens if the payload is
  *already* quantized. Its own evidence says floating-point values compress badly; INT8 vertex
  data with clustered values is exactly the case delta/BPC should love, and nobody has run it.
  This is the same composition question [`ENEC`](../ENEC/ANALYSIS.md) leaves open, on the
  other side of the datapath.

## Relation to other entries

**Where it belongs: with the compression / data-movement cluster, and it should stay the
cluster's reference case.**

- **It supplies the boundary the survey actually needs, and not the one the taxonomy thinks.**
  Put next to [`ENEC`](../ENEC/ANALYSIS.md), SpZip makes the `Q-ORIENTED` line crisp. Both are
  **lossless compression, no value changed, hardware/kernels outside the arithmetic**. ENEC was
  ruled `Q-ORIENTED` because it reads the **exponent field** of BF16 — the design is
  conditioned on the numeric format. SpZip is `NON-Q-ORIENTED` because BPC and delta are
  **format-blind byte and bit-plane codes**: the paper's only remark about floats is that they
  compress badly, and it does nothing about it. **The discriminator is not lossy-vs-lossless
  and not value-vs-structure — it is whether the code knows the format.** That sentence is
  worth more to the survey than either paper's numbers.
- **A correction to** [`ENEC/ANALYSIS.md`](../ENEC/ANALYSIS.md) **(line 412).** It says *"SpZip
  compresses **graph traversal structure** (CSR indices, bitvectors) with **no floating-point
  values in play**"*. Both halves are wrong: §IV's Schemes paragraph compresses **vertex data
  and update bins**, and §V-A explicitly attributes PR/PRD's weaker results to
  **floating-point values**. (`bitmap`/`bitvector`: **0** hits in SpZip.) The *conclusion* —
  that ENEC and SpZip should not share a box — survives, but on the format-awareness ground
  above rather than on "SpZip has no values in play". **Reported, not applied** (parallel
  agents own that file).
- **A correction to** [`Cambricon-SR/ANALYSIS.md`](../Cambricon-SR/ANALYSIS.md) **(line 455)
  and** [`TransitiveArray/ANALYSIS.md`](../TransitiveArray/ANALYSIS.md) **(line 351)**, both of
  which repeat the taxonomy's *"sparse-format compression"* gloss verbatim. The pairing with
  Cambricon-SR is still right — both leave the value representation untouched — but
  Cambricon-SR really *is* structural (a bitmap over table entries), whereas SpZip is not, so
  they are two different kinds of non-quantization paper. **Reported, not applied.**
- [`CommutativeDataReordering`](../CommutativeDataReordering/ANALYSIS.md) — the closest sibling:
  same year-adjacent venue, same "reduce data-movement energy on sparse workloads" framing.
  Worth reading as a pair.
- [`Ecco`](../Ecco/ANALYSIS.md) — the **compression-vs-cheaper-arithmetic axis** that Ecco's
  read proposed now has three points and a clean ordering by *how much the compressor knows
  about the number*: **SpZip** (nothing — bytes and bit-planes, decompressed before the core
  sees them) → **ENEC** (the exponent field, decompressed on a different core type) →
  **Ecco** (a k-means codebook that *is* a quantizer, decompressed between L1 and L2) →
  **EVA/TransArray** (compute through the code). Ecco's own note guessed that `Gist`, `SpZip`,
  `JPEG-ACT` and `IBMCompressionAccelerator` sit *"on the same side of that line"* — SpZip sits
  at the far end of it, which makes it the axis's anchor rather than just a member.
- [`IBMCompressionAccelerator`](../IBMCompressionAccelerator/ANALYSIS.md) — SpZip cites it
  ([1] NXU, [69] MXT) as the thing it is not: fixed-function engines for *long sequential
  streams*. The two together define the compression-granularity axis: page/stream (NXU) →
  cache line (BDI/LCP/VSC) → **application-defined chunk (SpZip)** → tensor group (Ecco).
  SpZip's §V-D actually *measures* the cache-line point and finds it worth +0-28%.
- **Not related to** [`Mokey`](../Mokey/ANALYSIS.md), [`EVA`](../EVA/ANALYSIS.md),
  [`OASIS`](../OASIS/ANALYSIS.md) **on the codebook axis** — tested. `codebook`, `lookup`,
  `LUT`, `dictionary` (as SpZip's own mechanism): **0** hits. Delta and BPC are stateless
  transforms with no table.

**Keep or cut? — recommendation: KEEP, as a single background citation, and keep it as the
taxonomy's worked example, with the gloss rewritten.** Three reasons. (i) It is the *reference*
negative case for the whole survey: a paper that compresses application values losslessly and
is still not a quantization paper. That is a harder and more useful boundary than
Cambricon-SR's (which never touches a value at all), and the survey needs both ends. (ii) One
transferable idea earns a sentence in the survey's data-movement paragraph, and it is not a
graph idea: **the right compression format is a property of the access pattern, so it must be
chosen per data structure, not per address space** — which is exactly the argument for
per-tensor-class format selection in a quantized accelerator (weights delta-coded, KV cache
group-quantized, activations left alone). (iii) The ISCA venue list is a complete enumeration
of the source CSV; dropping a row breaks that property. What it must **not** get is a body
paragraph, a data-type tag, or a generation.

---

## For the note

### §1 one-line summary

> **No quantization** — no value is ever changed, no numeric type is designed, and
> `quantiz*`, `precision`, `bitwidth`, `INT8`, `FP16`/`FP32`, `mantissa`/`exponent`, `codebook`
> and `accuracy` return **zero hits each**, bibliography included; what SpZip adds is a
> **fetcher and a compressor beside each core** (47.3k + 45.5k µm² at 45 nm = **0.2% of a
> core**) that run little dataflow programs written in a new **Dataflow Configuration
> Language** — range fetches, indirections and (de)compression operators wired by
> marker-carrying queues, time-multiplexed over two functional units — so that **lossless
> delta byte-coding and Bit-Plane Compression can be applied per data structure**, to the
> **payload values as well as the index streams** (adjacency lists, update bins, and vertex
> data, floating-point vertex data included), decoupled from the core so decompression
> latency hides behind the traversal: **gmean 3.0× over Update Batching and 1.5× over PHI**,
> with **1.7× / 1.4×** less DRAM traffic, in cycle-level simulation of a 16-core system.

### Proposed values on their four axes

| Axis | Proposed | Evidence (one line) |
|---|---|---|
| **Level** | **`ARCH+SYS`** — *seed says `ARCH`; I dispute it, with the counter-evidence stated* | The **DCL is claimed as a contribution in the abstract** (*"a novel Dataflow Configuration Language"*), and §III-D is a genuine system-integration section: two new ISA instructions (`enqueue`/`dequeue`, marker in the x86 overflow flag), memory-mapped configuration, virtual addressing through the core's L2 TLB with page faults as interrupts, coherence, and architecturally visible state the OS must save on a context switch — plus a modified Ligra-style runtime that leaves application code unchanged. That is the RaPiD ruling's *"the thing that drives the hardware, treated as a contribution"*. **Counter-evidence, stated honestly:** no compiler is built — *"The DCL program is manually extracted via analyzing the data structures"* (§III-D) — and TACO/GraphIt generation is speculation. If the human requires a *shipped* stack, `ARCH` alone is defensible. |
| **Q-oriented** | **`NON-Q-ORIENTED`** — seed agrees, but for a different reason | Swap the format for plain INT8 and the DCL, the fetcher, the time-multiplexed contexts, the scheduler, the MQU, the markers and the resorting all survive untouched; element size is a per-operator config field (`elemSz (B)`), never a design variable. **The taxonomy's stated reason — "only sparse-format compression" — is wrong** (footnote 1, p. 1070 explicitly excludes CSR from what it calls compression; §IV compresses vertex data and update values). The right reason is **format-blindness**: BPC and delta see bytes and bit-planes, and the paper's only remark about floats is that they compress badly. |
| **Data type** | **`—`** — seed agrees | No format is ever named. The nearest facts are element *widths*: range-fetch indexes at **8/16/32/64-bit**, BPC operands at **32 or 64-bit**, a 32-bit queue word plus marker bit, and one unqualified mention of *"floating-point values"* (§V-A) whose width the paper never gives. Widths of an opaque byte stream are not a data type; they are recorded in `ANALYSIS.md` and belong nowhere near a tag. |
| **Generation** | **`—`** — seed agrees | Generation is a quantization-paradigm axis and a paper with no quantization has no position on it. Matches the corpus convention for non-Q rows (`ELSA`, `Cambricon-SR`, and this row). |
| **Optimization** (free text) | `lossless value compression` `delta byte-code` `bit-plane compression (BPC)` `per-data-structure format selection` `decoupled traversal` `dataflow configuration language` `time-multiplexed operators` `memory-backed queues` `order-insensitive resorting` `graph analytics` `SpMV` | The seed's `lossless compression`, `decoupled traversal` and `graph workloads` all hold. **`CSR` should go** — the paper's footnote 1 explicitly refuses to call CSR compression, and leaving the keyword there is what produced the taxonomy's wrong gloss. The added keywords name the mechanisms and, crucially, record that the compression is of **values**. |

### Proposed venue-list row

```
| [ ] | [SpZip: Architectural Support for Effective Data Compression In Irregular Applications](https://doi.org/10.1109/ISCA52012.2021.00087) | *close read* | ARCH+SYS | non-Q | — | — | `lossless value compression` `delta byte-code` `bit-plane compression` `per-data-structure format selection` `decoupled traversal` `dataflow configuration language` `time-multiplexed operators` `memory-backed queues` `graph analytics` | ⚠ **No quantization — confirmed on a full read** (zero hits for quantiz*/precision/bitwidth/INT8/FP16/FP32/mantissa/exponent/codebook/accuracy, **bibliography included**). But **"only sparse-format compression" is wrong**: footnote 1 (p. 1070) explicitly excludes CSR from what the paper calls compression, and §IV compresses **update bins and vertex data**, floating-point included. It is **lossless entropy coding of values** by two format-blind codes (delta byte-code, BPC). `NON-Q-ORIENTED` because the codes do not know the format — the boundary case worth citing against `ENEC` |
```

*(Changes from the seed at line 80: `ARCH` → **`ARCH+SYS`** (disputed, evidence above);
`non-Q`, `—`, `—` unchanged and now sourced; Verified `*agent brief*` → `*close read*`;
Optimization loses `CSR` and gains the mechanisms; the Note is rewritten because the seed's
one-line reason is factually wrong.)*

*(A second, more important correction — to `QuantArchSurvey/TAXONOMY.md` itself, the
"Worked examples" section. The sentence "SpZip has no quantization at all, only sparse-format
compression" should become something like "**SpZip has no quantization at all: it applies
lossless, format-blind entropy coding — delta byte-codes and bit-plane compression — to
whatever an irregular application streams, values included. Compressing values is not
quantizing them.**" As written, the taxonomy teaches the wrong test. Reported, never applied.)*

### §4 fairness verdict

> Fair. Iso-simulator, iso-input, iso-system; UB and PHI baselines re-run from the authors'
> own code, and the compressed-memory-hierarchy comparison re-implemented, not quoted;
> 0.2%/core area disclosed. Not silicon (zsim + 45 nm synthesis); **no energy or power number
> anywhere**; iteration-sampled 1-in-5. Don't quote 3.0× as "over a multicore" — it is
> UB+SpZip over UB, and Push+SpZip is 1.6× — nor 15.4×/24× (maxima over a grid).

### §5 comment — dictated by the human, not left empty

**Exception to the usual "leave §5 empty" rule.** The human issued a scope ruling on
2026-09-14 while this read was in progress: *"General compression for sparse data, not for
LLM. Might also be marked as beyond our interested range."* §5 of `paper-note.md` carries
that verbatim, with the hedge kept:

> General compression for sparse data. Not for LLM. **Likely beyond our interested range.**

The note was cut short to match — §2 and §3 are a few lines each. The one thing kept at full
rigour is the grep evidence against `TAXONOMY.md`'s claim, because that bears on the team's
own reference document rather than on this row. The `Keep or cut?` recommendation above is
consistent with the ruling: **keep the row as a background citation, no body paragraph, no
data-type tag, no generation** — the disagreement, if any, is only about whether it also stays
as the taxonomy's *worked example*, and that is the human's call.

---

## Note from the source list

> **Keywords:** No quantization; Compressed Sparse Row (CSR) format

*(The CSR half of this note is what propagated into `TAXONOMY.md` and then into three of our
own `ANALYSIS.md` files. The paper's footnote 1 refutes it. See the ⚠ section.)*

## Abstract (verbatim, from the archived PDF)

> Irregular applications, such as graph analytics and sparse linear algebra, exhibit
> frequent indirect, data-dependent accesses to single or short sequences of elements that
> cause high main memory traffic and limit performance. Data compression is a promising way
> to accelerate irregular applications by reducing memory traffic. However, software
> compression adds substantial overheads, and prior hardware compression techniques work
> poorly on the complex access patterns of irregular applications. We present SpZip, an
> architectural approach that makes data compression practical for irregular algorithms.
> SpZip accelerates the traversal, decompression, and compression of the data structures
> used by irregular applications. In addition, these activities run in a decoupled fashion,
> hiding both memory access and decompression latencies. To support the wide range of access
> patterns in these applications, SpZip is programmable, and uses a novel Dataflow
> Configuration Language to specify programs that traverse and generate compressed data. Our
> SpZip implementation leverages dataflow execution and time-multiplexing to implement
> programmability cheaply. We evaluate SpZip on a simulated multicore system running a broad
> set of graph and linear algebra algorithms. SpZip outperforms prior state-of-the art
> software-only (hardware-accelerated) systems by gmean 3.0× (1.5×) and reduces memory
> traffic by 1.7× (1.4×). These benefits stem from both reducing data movement due to
> compression, and offloading expensive traversal and (de)compression operations.
