# IBMCompressionAccelerator — paper notes

**Data Compression Accelerator on IBM POWER9 and z15 Processors — Industrial Product**
Authors: **Bulent Abali², Bart Blaner¹, John Reilly¹, Matthias Klein¹, Ashutosh Mishra¹,
Craig B. Agricola¹, Bedri Sendir³, Alper Buyuktosunoglu², Christian Jacobi¹,
William J. Starke¹, Haren Myneni¹, Charlie Wang¹** — ¹ IBM Systems, ² IBM Research,
³ IBM Cloud. (12 authors; read off page 1 of the archived PDF, 2026-09-14 — **verified**,
p. 1 byline. The earlier "not transcribed" placeholder is now resolved.)
**ISCA 2020, Industry Track** ｜ DOI: **10.1109/ISCA45697.2020.00012**
Publication info verified 2026-09-02: venue, year **and DOI** all read out of the archived
PDF's own text (IEEE proceedings banner; the DOI was grepped for, not assumed); page range
from the IEEE Xplore link in the source CSV. The footnote "This paper is part of the Industry
Track of ISCA 2020's program" is on p. 1 — **verified**.
Archived here: the **published IEEE version**, 14 pages.

Status: **note ready** ｜ Last updated: 2026-09-14
Tags: `lossless-compression` `accelerator`
How far it was read: **full close read of §I–§X (pp. 1–13), Tables I–III, and all figure
captions.** Figures 12, 13, 14, 15 and 17 are vector charts: Fig. 12, Fig. 15 and Fig. 17 were
**rendered to PNG and read visually** to map data labels onto bars (the `pdftotext` extraction
recovers the label *values* but not their bar assignment). **Figs. 13 and 14 carry no data
labels at all** — every throughput number below comes from the prose or from Table I, never
from reading a curve. The 67-entry bibliography was read by grep, not entry by entry; the
load-bearing fact there (zero AI/ML/quantization references) is recorded under
`Method → the scope test`. Skimmed rather than resolved: **Fig. 8** (LZ length-code
distribution — read as a qualitative claim only, no values extracted) and the internal
**CUST1–CUST5** datasets in Fig. 9 (unpublished, so only the ±10% envelope was taken).

> Publisher record: https://ieeexplore.ieee.org/document/9138913
> **There is no arXiv version** (arXiv API title search, 2026-09-02). The PDF was downloaded by a
> human and filed through [`survey/uploads/`](../../uploads/) — the sanctioned route when the
> arXiv-only rule leaves a paper unreachable; see
> [`Notes-002`](../../../Claude/notes/Notes-002-paper-source-access.md).
> The PDF is **not committed** (1.5 MB) and **cannot be re-downloaded by script** —
> both publishers 403. Re-extract with `python3 extract.py` → `extracted/` (committed).
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, ISCA 2020 row, marked "Less related".

---

## Disposition — settled by the human, 2026-09-14

> *"Too general compression, and focus on circuit, not for LLM. Beyond our interested range."*

**Out of scope.** The close read agrees with the ruling and supplies the evidence for it (see
`Method → the scope test`). The note is deliberately short; this file keeps the numbers so the
paper can still be cited as the general-purpose lossless baseline if the survey wants one.

---

## What the close read changed in the brief

Six changes; the brief's substance survives, but every headline number needed a frame.

1. **Authors filled in** — 12 IBM authors across IBM Systems, IBM Research and IBM Cloud.
2. **"388× / 13×" needed their frames.** 388× is against **one** zlib software thread; 13× is
   against **80 SMT4 threads on one POWER9 chip**; both at a **256 KB source size**, and both
   are **compression only** (Table I).
3. **The brief omitted the decompression result, which is the honest half.** POWER9 NXU
   decompression is **0.75×** — *slower* than 80 threads of zlib on the same chip (Table I),
   and Fig. 15 confirms it (11 GB/s for 80-thread zlib vs 7.6 GB/s for NXU).
4. **"z15 doubles it, to 280 GB/s system-wide" conflates two facts.** z15 doubles the
   *per-chip* rate (P9 >7 GB/s → z15 15 GB/s peak, §VIII-C). The **280 GB/s** is a
   **20-chip maximal system topology** and is **cited to reference [6]** (the z15 ISSCC
   paper), not measured in this paper.
5. **"No exploration of alternatives" is too strong.** §II explicitly compares LZ4, Snappy and
   ZSTD/tANS on the ratio-vs-throughput axis and argues the Deflate choice; §X names a
   "configurable/programmable accelerator or a compression-optimized ISA" as future work. What
   is true is that no *AI-specific* data statistics are considered anywhere.
6. **A compression-ratio discrepancy the brief could not have seen.** The prose says NXU output
   is "4-5% larger than GZIP -6" (§VIII-B); Fig. 12's own per-suite averages give
   **8.7% / 10.1% / 12.2%** (Canterbury / Calgary / Silesia) for NXU 2-pass. Recorded as a
   citation hazard.

---

## Brief

### 1. Motivation

Lossless data compression pays for itself in storage, memory and network cost, but is processor-
intensive enough that people skip it or downgrade the codec. An on-chip accelerator makes it
effectively free — and, unlike the PCIe FPGA cards IBM shipped in z13, costs no I/O slot.

### 2. Overview

An **industrial product paper about shipping silicon**: the NXU, an on-chip Deflate
(LZ77 + Huffman) compression/decompression accelerator in IBM POWER9 (2017) and IBM z15 (2019),
14 nm, **< 0.5% of chip area**. Describes the hybrid CAM/pseudo-CAM LZ77 stage, the dynamic
Huffman stage with a hardware table generator, the speculative parallel variable-length decoder,
and the user-mode system-stack integration (a z15 ISA instruction, a POWER9 user-mode page-fault
handler, zlib-API libraries, a Spark/Parquet JNI shim).

### 3. Pros and cons

**Pros**

- Real silicon at scale with the area accounting spelled out: **< 0.5% of chip area** for
  **388×** one zlib thread and **13×** an entire POWER9 chip of cores (compression, 256 KB).
- **End-to-end, not kernel-level**: 23% on Spark TPC-DS, and the data-generation stage 29%
  faster than the Snappy default (Table III) — product numbers, on a real cluster.
- Honest about the ceiling: reports that NXU **loses** to 80 threads of zlib on decompression
  and **loses ~10%** of compression ratio to gzip -6.
- The best available answer to "what does a fixed-function lossless compressor cost in
  production silicon, and what does it deliver".

**Cons**

- **Not a quantization paper, not an AI paper, and not about numeric formats.** Zero
  occurrences of `neural`, `DNN`, `learning`, `inference`, `training`, `quantiz*`, `precision`,
  `bitwidth`, `mantissa`, `exponent`, `tensor` or `GPU`, bibliography included.
- Fixed to Deflate; no ML-specific data statistics anywhere — the gap
  [`ENEC`](../ENEC/ANALYSIS.md) later fills for model weights.
- Industry-track methodology: no area in mm², no NXU-only power figure, no RTL/synthesis data,
  and the flagship 280 GB/s is cited to another paper.

### 4. Where it applies

**Out of scope for the survey body** (human ruling, above). Retain as a **background citation**:
the general-purpose lossless baseline against which every AI-specific compression scheme in the
corpus is judged, and the industrial counterpart to [`ENEC`](../ENEC/ANALYSIS.md).

---

## Conclusions

A dedicated Deflate engine occupying **< 0.5% of a 14 nm server chip** delivers **>7 GB/s
(POWER9) / 15 GB/s peak (z15)** of compression, **~2 orders of magnitude less energy per GB**
than software zlib, and **23% end-to-end** on Spark TPC-DS — at a **~10% compression-ratio
loss** against gzip -6, and with **no advantage over a full chip of cores on decompression**.
It is a circuit-and-integration paper about general enterprise data. Nothing in it concerns
neural networks, numeric formats or precision.

## Method

### The scope test — run first, and it is the finding

Term sweep over the **full extracted text including the 67-entry bibliography**, with
`ﬁ`/`ﬂ` ligatures normalised first (the naive grep undercounts "Deﬂate" to 1). All
**verified**, `10.1109_ISCA45697.2020.00012.raw.txt`:

| Absent (count = 0) | Present |
|---|---|
| `neural` · `DNN` · `deep learning` · `machine learning` · `inference` · `training` · `quantiz*` · `precision` · `bitwidth` / `bit-width` · `INT8` · `FP32` · `mantissa` · `exponent` · `tensor` · `GPU` · `AI` (word-boundary) · `ML` (word-boundary) | `Huffman` 41 · `zlib` 51 · `compression ratio` 39 · `gzip` 27 · `LZ77` 27 · `deflate` 24 · `LZ4` 14 · `zstd` 14 · `snappy` 11 · `entropy` 5 · `lossless` 4 |

Three near-misses, all checked and all false friends — **verified**:

- **`float` × 1**, §V-A: *"Counts are converted to 10-bit **floating point** values to reduce
  the number of latches."* This is a compact representation of **Huffman symbol counters** in
  the sorter, not a data format for any payload. It is the only numeric-format decision in the
  paper and it concerns metadata.
- **`lossy` × 1** and **`accuracy` × 1**, §IV-A: *"pseudo-CAM are imprecise and **lossy**: a
  limited number of SRAM locations may contain a search item… hash and bank collisions gate
  throughput and **accuracy**."* "Lossy" describes **missed dictionary matches**, i.e. lost
  compression ratio. The compressed data is bit-exact throughout; the format is RFC1951.
- **`model` × 5 / `models` × 1** — all "system model AC922", "LogCA accelerator model", "we
  model the accelerator execution time", "TPC-DS models a data warehouse". No ML model.

**Bibliography**: 67 entries, 44 of them numbered lines in the extracted reference block;
`neural|learning|quantiz|DNN|inference|training|precision|GPU|tensor` over that block returns
**0** — **verified**. The references are Deflate/LZ/Huffman theory, FPGA compression engines,
IBM patents and product papers, OS/page-fault work, and Spark/TPC-DS.

**Verdict: the paper has no AI, ML or quantization content of any kind.** This is not an
absence-by-not-noticing (trap 3): it was tested against the specific alternative hypothesis
that a compression paper might discuss numeric formats, and the only "format" in it is a 10-bit
float for Huffman counters.

### What was actually built

**Hybrid LZ77 dictionary — the paper's headline area argument.** Fig. 5 shows compression ratio
saturating with sliding-window size, so the design **budgets area by dictionary range**: an
area-hungry **true CAM of latches** for the **near history (≤ 512 B)** and an area-efficient
**SRAM pseudo-CAM** for the **far history (513 B – 32 KB)**. The near-history CAM is
`M = 8` input-byte columns × `N = 512` history-byte rows of comparators, with a per-column
1-bit `C` "continue" register and a `COUNT` register so matches span cycles; a priority encoder
emits up to **4 LZ symbols/cycle**. The choice of latch-CAM vs SRAM rests on a measured circuit
fact: **SRAM stores 14–16× as many bits per unit area as latches in 14 nm CMOS** (§IV-A) —
**verified**. Area and timing "didn't permit" a CAM larger than 512 B.

**Far-history pseudo-CAM = an 8-way set-associative cache with FIFO replacement.** 8 overlapping
`K`-byte search tokens (**K = 5** firmware default) hash to 8 entries of a **2048 × 144 b** hash
table (16 SRAM banks), each entry holding **8 address+tag pairs** → 64 candidates; a FILTER
reduces 64 → 2 using **6-bit probabilistic tags** (false-positive rate **1/2⁶**, and false
positives are not a correctness issue because the History-FIFO bytes are compared anyway).
**Total dictionary SRAM: 32 KB History-FIFO + 36 KB hash table = 66 KB**, against **1.92 MB**
and **3.15 MB** of FPGA block RAM in the two prior-art engines it cites — **verified**, §IV-D.

**The token-size trade-off is stated as a measurement, not a guess.** `K = 3` finds short
matches but hot entries age out under FIFO replacement; `K = 8` finds only ≥ 8-byte matches.
`K = 5` is best on average; the internal **CUST2** dataset is the outlier where `K = 8` gives
**+10%** ratio (Fig. 9, five unpublished CUST datasets, ±10% envelope) — **verified**.

**Bank conflicts, and the one microarchitectural difference between the two chips.** With 8
requests/cycle into 16 **1-port** SRAM banks, POWER9 conflicts **87% of the time**, average
access latency **2.1 cycles** (1.0 ideal). z15 uses **2-port** SRAMs → **1.12 cycles**, at the
cost of larger arrays. That single change is most of the 2× throughput gap — **verified**,
§IV-D. *Derivation (mine, not the paper's): 8 B/clk × 2.0 GHz ÷ 2.1 = **7.6 GB/s** for POWER9
and 8 B/clk × 2.5 GHz ÷ 1.12 = **17.9 GB/s** for z15, bracketing the measured >7 and 15 GB/s
— **inferred / not verified**.*

**True dynamic Huffman, and the length-limiting trick.** Most hardware Deflate engines use a
static table (z13 picked the best of 15 pre-baked tables); NXU builds a real DHT. Sorting is
2-D **Shear-Sort** in `O(√n log²n)` cycles over latch-stored counts (n = 286 literals/lengths,
30 distances), then an `O(n)` priority-queue Huffman. Length-limiting to Deflate's 15-bit
maximum is done by **iterating `count ← (count + 1)/2`** — boosting rare symbols' probability,
which shrinks tree depth while nearly preserving the sorted order — until
`⌈−log₂ p_min⌉ ≤ 15`. A second iteration "occurs rarely" — **verified**, §V-B.
**POWER9 has no DHTGEN**: software must produce the table and cache recently used ones.
**z15 added a hardware DHTGEN** that unconditionally builds a new table per job. This is the
second POWER9/z15 difference and it is a *lesson-learned* difference, stated as such.

**1.1-pass mode.** Two-pass Huffman halves throughput. z15 instead samples **the first 32 KB**
(configurable) and reuses the resulting DHT for up to **256 KB** of source →
`256/(256+32) = 89%` of hardware peak instead of 50%. Fails on `ptt5` and `pic`, whose first
32 KB are almost all zeros — **verified**, §V-C and §VIII-B.

**Speculative parallel decoder — the "8 codes per cycle" claim.** Deflate codes are 1–15 bits,
concatenated with no delimiters, so naive decoders manage 1 code/cycle. NXU assumes **a code
starts at every one of the 32 bit positions** of the 32-bit input word and decodes all 32
speculatively, invalidating the wrong ones downstream. The area trick is that only a
**First-Bit decoder** (which stores no symbols) is replicated 32×; it hands start positions to
**8 full decoders** (each needing the large 286+30-symbol SRAM), which feed an LZ77 decoder
running **4 LZ references/cycle**. 32 b/cycle in, 64 b/cycle out — **verified**, §VI. Credited
as a reduced-area derivative of the FPGA decoder in ref. [28].

**System-stack integration — this is why the Level is not `ARCH` alone.** z15 adds an
**architected unprivileged instruction, `DFLTCC` ("Deflate Conversion Call")**, implemented in
millicode, giving user-mode access with **no OS or device driver**. POWER9 instead posts a
128-byte **Coprocessor Request Block** to one of two 256-deep hardware job queues with the
`copy`/`paste` instruction pair, mmap'd into user space, with hardware-managed synchronisation
and a "job-limit" register that suspends long jobs by dumping NXU state to the caller's
parameter block. POWER9 also ships a **user-mode page-fault handler in the compression
library**: on a fault NXU reports via a Command Status Block and the library **shrinks the job
and retries**, so no page pinning and no system call. Plus zlib-API-compatible libraries for
z/OS, zLinux and AIX, and a **JNI shim implementing Java `OutputStream`/`InputStream`** for
Spark and Parquet with gzip headers and CRC validation. §VII is a full section and one of the
paper's five listed novel contributions — **verified**.

## Key numbers, with their frame

**POWER9 and z15 are kept separate throughout. Do not pool them.**

| Setting | Workload / data | Metric | Baseline | Result | Source |
|---|---|---|---|---|---|
| POWER9 + z15, 14 nm | — | **Area** | whole processor chip | **< 0.5% of chip area**; z15 unit "slightly larger" (2-port hash SRAMs, hardware DHTGEN). **No mm² anywhere in the paper** | §III p. 3, abstract — **verified** |
| POWER9, 1 NXU @ 2.0 GHz | ≥ 64 KB source | **Compress throughput** | — | **> 7 GB/s** (Fig. 13; Fig. 15 gives 5.0 GB/s at 1 thread, **7.1** at 80) | §VIII-C p. 9 — **verified** (prose + Fig. 15 labels) |
| z15, 1 NXU @ 2.5 GHz | ≥ 64 KB source | **Compress throughput** | POWER9 NXU | **15 GB/s peak = 2× POWER9** | §VIII-C p. 9 — **verified** |
| POWER9, 1 NXU | 256 KB source | **Compress speedup** | zlib 1.2.11, 1 thread / 8 / 80 (SMT4) | **388× / 49× / 13×** | Table I p. 10 — **verified** |
| z15, 1 NXU | 256 KB source | **Compress speedup** | zlib, 1 thread / 8 threads | **574× / 72×** (no 80-thread entry: 8-core LPAR) | Table I — **verified** |
| POWER9 / z15 | 256 KB source | **Compress speedup** | ZSTD / LZ4 tools | P9 **32× / 19×**; z15 **78× / 38×** | Table I — **verified** |
| POWER9, 1 NXU | 256 KB source | **Decompress speedup** | zlib 1 / 8 / 80 threads | **34× / 4.6× / 0.75×** — **loses to a full chip of cores** | Table I — **verified** |
| z15, 1 NXU | 256 KB source | **Decompress speedup** | zlib 1 / 8 threads | **30× / 3.8×**; vs ZSTD 10×, vs LZ4 3.5× | Table I — **verified** |
| z15, 20 chips | maximal system topology | **System compress rate** | — | **280 GB/s**, "highest in the industry"; = 68 PCIe cards at 4 GB/s | §I p. 2 — **verified as a claim, but cited to ref. [6]**, not measured here |
| z15 NXU | Canterbury / Calgary / Silesia averages | **Compression ratio** | LZ4-1 · ZSTD-3 · GZIP-6 | **NXU 1.1-pass 2.81 / 2.65 / 2.34**; **NXU 2-pass 2.89 / 2.68 / 2.38**; GZIP-6 **3.14 / 2.95 / 2.67**; ZSTD-3 **3.14 / 2.88 / 2.70**; LZ4-1 **1.97 / 1.92 / 1.83** | Fig. 12 p. 10 — **verified by rendering the figure and reading the callout lines** |
| — | same | **NXU ratio penalty** | GZIP-6 | Prose: "**4-5% larger**". Fig. 12 averages give **+8.7% / +10.1% / +12.2%** (2-pass) and **+11.7% / +11.3% / +14.1%** (1.1-pass) | §VIII-B vs Fig. 12 — **discrepancy, see citation hazards** |
| POWER9 / z15 | 1 thread | **Setup latency T₀** | — | Compress **2.2 / 5.2 µs**; decompress **2.9 / 1.9 µs**. At 8 threads (≈ pure hardware latency) **0.55–0.78 µs** | Table II p. 11 — **verified** |
| POWER9 / z15 | 1 thread | **Half-peak data size** | — | Compress **16 / 64 KB**; decompress **24 / 16 KB**. At 8 threads **4–12 KB** | Table II — **verified** |
| POWER9, 1 chip | zpipe.c, active (delta) power | **Power** | zlib on cores | NXU **+27 to +42 W**; zlib 1-thread **+30/31 W**, 80-thread **+177/183 W** | Fig. 15 p. 11 — **verified** (rendered) |
| POWER9, 1 chip | same | **Energy per GB** | zlib | NXU **5.7 / 4.7 / 4.2 / 5.5 J/GB** (cmp-1th, cmp-80th, dec-1th, dec-80th); zlib **986 / 219 / 103 / 17**. Ratio **173× / 47× / 25× / 3.1×** | Fig. 15 — **verified** (ratios derived) |
| POWER9 cluster | TPC-DS SF=3000 (3 TB) generation, Parquet | **Size / ratio / time** | Snappy (default) | Snappy 1019 GB / 2.94 / 4.10 h · **Zlib 761 GB / 3.94 / 3.26 h** · **P9 NXU 804 GB / 3.73 / 2.90 h** → NXU **29% faster than Snappy**, and 11% faster than Zlib at 5% worse ratio | Table III p. 12 — **verified** |
| POWER9 cluster, 4 nodes | TPC-DS 4×99 queries, Spark SQL | **Queries per hour** | snappy(Parquet)+lz4(Spark) = **27.06 QpH** baseline | snappy+zlib 18.26 · snappy+NXU 29.33 · zlib+lz4 30.98 (**+14%**) · NXU+lz4 31.08 · **NXU+NXU 33.38 (+23%)**; shuffle bytes **−32%** | Fig. 17 p. 12 + §IX-B — **verified** (rendered; 33.38/27.06 = 1.234 reproduces the abstract's 23%) |
| POWER9 | dictionary storage | **On-chip SRAM** | prior FPGA engines [4], [14] | **66 KB** (32 KB History-FIFO + 36 KB hash) vs **1.92 MB** and **3.15 MB** of FPGA block RAM | §IV-D p. 5 — **verified** |

**Evidence level, uniform and strong: measured on shipping commercial silicon.** POWER9 AC922
(2 sockets, 20 cores/chip @ 3.8 GHz, SMT4, 80 threads/chip; NXU @ 2.0 GHz) and a z15 8-core
LPAR (NXU @ 2.5 GHz), both on Ubuntu 18.04; microbenchmark `compdecomp_th.c`; Silesia,
Canterbury and Calgary corpora; end-to-end on 4× POWER9 LC922 with Hadoop 3.1 / Spark 2.3.3 /
TPC-DS 1.4. **No simulator, no RTL, no synthesis, no analytical projection anywhere** — the
sole model in the paper is the two-parameter `T = T₀ + size/BW` latency fit used to *derive*
T₀ from measured curves. §VIII-A — **verified**.

### Citation hazards

1. **388× is one software thread.** The comparable whole-chip number is **13×**, and it is
   compression-only. Quoting 388× without "vs a single zlib thread at 256 KB" is the standard
   accelerator-vs-one-core inflation.
2. **13× does not generalise to decompression.** Decompression against the same 80 threads is
   **0.75×** — NXU is *slower*. Any sentence of the form "NXU replaces 13 chips of cores" is
   true only for compression.
3. **280 GB/s is not this paper's measurement.** It is a 20-chip maximal z15 topology, cited to
   ref. [6] (ISSCC 2020). Attribute it to the z15 ISSCC paper or state that it is a
   configuration claim.
4. **The compression-ratio prose and Fig. 12 disagree.** "4-5% larger than GZIP -6" (§VIII-B)
   vs **8.7-12.2%** from Fig. 12's own suite averages. Possible reconciliation: the prose may
   aggregate over total bytes while the figure averages per-file ratios — the paper does not
   say. **Quote the figure's numbers, not the 4-5%.**
5. **"< 0.5% of chip area" has no mm² behind it** anywhere in the paper, and it is *one* NXU
   per chip. Do not convert it to an absolute area without an external die-size source.
6. **z15's 2× is not a redesign.** It is 2-port hash SRAMs (1.12 vs 2.1 cycles/access) plus a
   25% higher clock. Compression ratio and dataflow are unchanged between the two chips.
7. **Peak vs end-to-end.** 15 GB/s is a peak reached only at ≥ 256 KB blocks; the half-peak
   data sizes in Table II (16-64 KB single-threaded) are the operating constraint, and the
   application-level number is **23%**.

## Cost and requirements

- **Area**: < 0.5% of a 14 nm POWER9 / z15 processor chip, one unit per chip. No mm², no
  transistor count, no gate count, no NXU-only power figure — the only power data is
  **system delta power** (+27 to +42 W with NXU active, which the authors say is mostly
  core/cache/memory activity, not the NXU itself).
- **On-chip memory**: 66 KB of SRAM for the dictionary (32 KB window + 36 KB hash table) plus
  the near-history latch CAM (8 × 512 comparators + registers) plus the decoder's 8 full-decoder
  symbol SRAMs. z15's arrays are larger (2-port).
- **Frequency**: NXU runs *below* core clock — 2.0 GHz on POWER9 (cores 3.8 GHz), 2.5 GHz on
  z15. Fixed 8 bytes/clock datapath.
- **Software requirement — substantial, and it is a contribution rather than a footnote.**
  POWER9 needs a customised kernel and firmware, a ground-up zlib-API library, a user-mode
  page-fault handler, and (for POWER9 only) **software-generated Huffman tables with a DHT
  cache**. z15 needs the `DFLTCC` architected instruction and millicode. Java workloads need
  the JNI stream shim. There is no "drop-in" path that is purely hardware.
- **Format lock-in**: RFC1951 Deflate only, hard-coded. §X names this as the main regret and
  asks for a configurable accelerator or a compression-optimised ISA.
- **What it does not require**: no retraining, no calibration, no accuracy budget, no
  application change beyond relinking zlib. Output is bit-exact standard Deflate, so any
  software decoder can read it.

## Limitations and open questions

**Admitted by the authors**

- Hard-coded to Deflate; new algorithms cannot be deployed (§X). Their defence is that two
  orders of magnitude of speedup make the algorithm's own inefficiency irrelevant.
- Compression ratio is below gzip -6, and the mechanism is named: 5-byte tokens cannot find
  4-byte matches, and the 8-deep FIFO hash entries lose long repeated strings (`nci`'s
  `"0 "` runs, `xml`'s repeated tags) — §VIII-B.
- 1.1-pass sampling fails when the first 32 KB is unrepresentative (`ptt5`, `pic`).
- POWER9's 87% hash bank-conflict rate; the firmware option to drop conflicting requests trades
  ratio for throughput and is not quantified.
- z15 single-thread compress latency (5.2 µs) is *worse* than POWER9's (2.2 µs), attributed to
  software overhead in the ported zlib.

**Not admitted, or not measured**

- **No NXU-only power or area number.** Every energy claim is a whole-system delta, so the
  "2 orders of magnitude" energy win includes core, cache and memory activity on both sides.
- **Decompression is the weak side and is never discussed as such.** Table I prints 0.75× and
  the text says only that NXU is "still faster than 1-thread zlib".
- **No comparison against a contemporary PCIe/FPGA accelerator on equal terms** — the FPGA
  prior art is compared on *block-RAM capacity* (66 KB vs 1.92/3.15 MB), which is an
  area-efficiency argument, not a throughput or ratio comparison at iso-anything.
- **The 4-5% vs 8.7-12.2% ratio discrepancy is unexplained.**
- **No multi-tenancy or QoS data** despite the job-limit register and shared-queue design.
- **Nothing about compressing anything other than general enterprise data.** No scientific
  data, no floating-point arrays, and — the relevant absence here — no model weights.

## Relation to other entries

**The pair with [`ENEC`](../ENEC/ANALYSIS.md) is the reason to keep this entry at all.** ENEC's
own analysis already names NXU "the direct ancestor". Read together they bracket the
lossless-compression question from both ends:

| | IBM NXU (ISCA'20) | ENEC (ISCA'26) |
|---|---|---|
| What is compressed | any enterprise byte stream | **BF16/FP16/FP32 model weights**, exponent field only |
| Algorithm | Deflate: LZ77 + **dynamic Huffman** (a real entropy coder) | **fixed-length block coding** — because the NPU *cannot* run an entropy coder |
| Where it runs | **fixed-function hardware**, < 0.5% of a 14 nm CPU chip | **software kernels** on a shipping NPU's vector units |
| Ratio | **2.34-2.89×** on standard corpora (general data) | **1.35×** on BF16 (already-dense float) |
| Throughput | **>7 GB/s** (P9) / **15 GB/s** (z15) per chip | **372 GB/s** compress / **214 GB/s** decompress (Ascend 910B2) |
| Evidence | shipping silicon, measured | shipping silicon, measured |
| Hardware cost | area (< 0.5%) and a bespoke ISA/driver stack | none — but 48 vector cores are occupied |

Two things fall out of the table and they are worth a sentence each in the survey:

1. **The ratio gap is the data, not the algorithm.** A real Huffman/LZ77 engine gets 2.3-2.9×
   on text, binaries and databases; the *same class of coder* gets ~1.5× on BF16 weights
   (ENEC's Table II ceiling) because 8 of 16 bits are incompressible mantissa. **Model weights
   are near-incompressible by general-purpose lossless standards** — that is the number the
   survey wants, and it needs both papers to state it.
2. **The throughput gap is the substrate, not the effort.** NXU's 15 GB/s of *fixed-function
   hardware* is 25× slower than ENEC's 372 GB/s of *software on vector units* — because an
   HBM-class NPU's vector array is enormous compared to one 0.5%-of-die macro. ENEC §VII-B
   nonetheless asks future accelerators for exactly NXU's missing block (variable-length decode
   near the vector registers). **Fixed-function lossless compression exists, is cheap in
   silicon, and is absent from AI accelerators.** That is the joint claim.

**Against [`SpZip`](../SpZip/ANALYSIS.md) and
[`CommutativeDataReordering`](../CommutativeDataReordering/ANALYSIS.md)** — these three are the
corpus's genuinely non-numeric compression papers. SpZip compresses graph traversal structure;
CDR reorders data; NXU compresses bytes. None has a numeric format, and `TAXONOMY.md`'s own
worked example gives SpZip `—` on both Data type and Generation. **The same treatment applies
here, and for a stronger reason**: SpZip at least builds hardware for a *data-representation*
question, while NXU implements a 1951 code to a 1996 RFC.

**Against [`Ecco`](../Ecco/ANALYSIS.md) — the one that looks closest and is not.** Ecco also
builds a Huffman decoder in hardware, also targets bandwidth, also sits in a memory hierarchy.
But Ecco's compressibility comes from a **k-means codebook over groups of 128 values**, i.e. a
non-uniform quantizer, and its stored values are **changed**. NXU changes nothing and knows
nothing about what its bytes mean. Ecco belongs inside the survey; NXU does not. Useful as the
sharpest illustration of where the boundary falls: *a Huffman engine is not a quantizer.*

**Against [`TPUv4i`](../TPUv4i/ANALYSIS.md) — the other shipping-silicon industrial entry, and
the cross-reference that is actually interesting.** Both are product papers with measured
production numbers and both make an area argument. TPUv4i spends **28% of its die on SRAM**
because memory movement dominates arithmetic energy (Table 2: 0.07 pJ for an INT8 multiply vs
7.5 pJ for one 64-bit SRAM read vs 250-450 pJ for HBM2). NXU is the **complementary** answer to
the same pressure: instead of caching more bytes, compress them, for **< 0.5% of the die** and
**4-6 J/GB**. Two industrial teams, the same year-ish, the same diagnosis, opposite levers.
That is the one sentence this paper contributes to a quantization survey, and it is a framing
sentence, not a result.

**On the "compression vs cheaper arithmetic" axis** (proposed in `PAPER-READING`): NXU is
**off the axis entirely** — it is pure compression with no arithmetic anywhere near it, and no
value is ever interpreted as a number. Ecco is the midpoint, ENEC the pole, NXU the outside
reference point that shows what the pole costs when you build it in silicon for arbitrary data.

---

## For the note

### §1 one-line summary

> **No quantization and no AI anywhere** — `neural`, `DNN`, `learning`, `inference`, `training`,
> `quantiz*`, `precision`, `bitwidth`, `mantissa`, `exponent`, `tensor` and `GPU` are **zero
> hits each, bibliography included** — this is IBM's shipping **NXU**, a fixed-function
> **Deflate (LZ77 + dynamic Huffman)** engine occupying **< 0.5% of a 14 nm POWER9 / z15 chip**,
> whose contributions are circuit-level (a **hybrid 512-byte latch CAM for near history plus an
> SRAM pseudo-CAM hash table for the 32 KB far history**, 66 KB of SRAM against 1.9-3.2 MB in
> FPGA prior art; a hardware **length-limited dynamic Huffman generator**; a **speculative
> decoder** trying all 32 start positions to reach 8 codes/cycle) and system-level (the z15
> **`DFLTCC`** user-mode instruction, a POWER9 user-mode page-fault handler, zlib-API and JNI
> libraries), delivering **> 7 GB/s (POWER9) / 15 GB/s (z15)** compression measured on shipping
> silicon — **388× one zlib thread but only 13× a full chip of cores, and 0.75× on
> decompression** — at **~10% worse ratio than gzip -6** (2.34-2.89× vs 2.67-3.14×) and
> **4-6 J/GB against zlib's 17-986**, worth **23% end-to-end on Spark TPC-DS**.

### Proposed values on their four axes

| Axis | Proposed | Evidence (one line) |
|---|---|---|
| **Level** | **`ARCH+SYS`** — *seed says `ARCH`; I dispute it* | §VII "Integration of the Accelerator into the System Stack" is a full section and the 5th of the paper's five listed novel contributions: z15 adds an **architected unprivileged ISA instruction (`DFLTCC`)** in millicode; POWER9 adds mmap'd hardware job queues driven by `copy`/`paste`, a **user-mode page-fault handler in the compression library** with job-shrink-and-retry, zlib-API libraries for z/OS, zLinux and AIX, and a **JNI `InputStream`/`OutputStream` shim** for Spark/Parquet with gzip framing and CRC. An ISA section plus a software-stack section is exactly the `AGENT-GUIDE` §0b tell for `SYS`. |
| **Q-oriented** | **`NON-Q-ORIENTED`** — seed agrees; the widest margin in the corpus | The test does not even apply: there is **no numeric format to swap**. The only `float` in the paper is a **10-bit float used to store Huffman symbol counters** in the Shear-Sort array (§V-A) — metadata, not payload. The only `lossy`/`accuracy` mentions describe **missed dictionary matches** in the pseudo-CAM. Output is bit-exact RFC1951. |
| **Data type** | **`—`** — seed agrees | Zero hits for every format term. Precedent: `SpZip` in `TAXONOMY.md`'s worked-example table, and `Cambricon-SR` (2026-09-14). A data-type tag here would be a fabrication. |
| **Generation** | **`—`** — seed agrees | Generation is a **quantization-paradigm** axis and this paper has no position on it. Same reasoning and same precedents (`SpZip`, `Cambricon-SR`, `ELSA`). Not `G1`: `G1` means *"existing numeric formats applied to networks"*, and there are no networks and no numeric formats. |
| **Optimization** (free text) | `Deflate (RFC1951)` `LZ77` `dynamic Huffman` `hybrid CAM + SRAM pseudo-CAM dictionary` `hash-table sliding window` `hardware DHTGEN` `length-limited Huffman` `1.1-pass sampling` `speculative parallel VLC decoder` `user-mode accelerator interface` `DFLTCC ISA instruction` `user-mode page-fault handler` `POWER9 / z15 shipping silicon, 14 nm` | All four seed keywords (`Deflate`, `LZ77`, `Huffman`, `POWER9 / z15 silicon`) are **confirmed in the text** — grepped, not carried. The additions name the five contributions the paper itself lists plus the system-stack half that justifies `SYS`. |

### Proposed venue-list row

```
| [ ] | [Data Compression Accelerator on IBM POWER9 and z15 Processors](https://ieeexplore.ieee.org/document/9138913) | *close read* | ARCH+SYS | non-Q | — | — | `Deflate` `LZ77` `dynamic Huffman` `hybrid CAM + pseudo-CAM dictionary` `hardware DHTGEN` `speculative VLC decoder` `DFLTCC ISA instruction` `user-mode page-fault handler` `POWER9 / z15 shipping silicon 14 nm` | **No AI or quantization content at all** (`neural` `DNN` `learning` `inference` `quantiz*` `precision` `mantissa` `exponent` `tensor`: 0 hits each, bibliography included). General-purpose lossless Deflate in shipping silicon: **< 0.5% of a 14 nm chip**, **>7 GB/s P9 / 15 GB/s z15**, 388× one zlib thread but **13× a full chip** and **0.75× on decompress**, ratio **~10% worse than gzip -6**, **23% end-to-end on Spark TPC-DS**. Keep as the general-purpose lossless baseline against [ENEC](notes/); out of the survey body |
```

*(Changes from the seed at line 89: `ARCH` → `ARCH+SYS` (disputed, evidence above);
`*agent brief*` → `*close read*`; `non-Q`, `—`, `—` all **confirmed**; Optimization gains the
five named contributions and the system-stack items; the Note column now carries the grep
evidence and the numbers with their frames instead of "Sheet comment: Less related".)*

### §4 fairness verdict

**Measured on shipping silicon throughout** — no simulator, RTL or projection — but **not
iso-anything against software**: 388× is one zlib thread, 13× a full POWER9 chip, and
decompression is **0.75×**. **Not iso-ratio** (NXU 2.34-2.89 vs gzip-6 2.67-3.14). **Not to
quote bare:** 388×; 280 GB/s (20-chip topology, cited to [6], not measured here); "4-5% larger
than gzip" (Fig. 12 gives 8.7-12.2%).

---

## Note from the source list

> **Keywords:** on-chip integrated data compression accelerator; to improve IO
>
> **Comment:** Less related

**Confirmed, and stronger than "less related".** The close read finds **no** AI, ML, neural,
numeric-format or quantization content of any kind, in the body or in the 67-entry
bibliography. The human's ruling (2026-09-14): *"Too general compression, and focus on circuit,
not for LLM. Beyond our interested range."*

## Abstract (verbatim, from the archived PDF)

> Lossless data compression is highly desirable in enterprise and cloud environments for
> storage and memory cost savings and improved utilization I/O and network. While the value
> provided by compression is recognized, its application in practice is often limited
> because it’s a processor intensive operation resulting low throughput and high elapsed
> time for compression intense workloads. The IBM POWER9 and IBM z15 systems overcome the
> shortcomings of existing approaches by including a novel on-chip integrated data
> compression accelerator. The accelerator reduces processor cycles, I/O traffic, memory and
> storage footprint of many applications practically with zero hardware cost. The
> accelerator also eliminates the cost and I/O slots that would have been necessary with
> FPGA/ASIC based compression adapters. On the POWER9 chip, a single accelerator uses less
> than 0.5% of the processor chip area, but provides a 388x speedup factor over the zlib
> compression software running on a general-purpose core and provides a 13x speedup factor
> over the entire chip of cores. On a POWER9 system, the accelerators provide an end-to-end
> 23% speedup to Apache Spark TPC-DS workload compared to the software baseline. The z15
> chip doubles the compression rate of POWER9 resulting in even much higher speedup factors
> over the compression software running on general-purpose cores. On a maximally configured
> z15 system topology, on-chip compression accelerators provide up to 280 GB/s data
> compression rate, the highest in the industry. Overall, the on-chip accelerators
> significantly advance the state of the art in terms of area, throughput, latency,
> compression ratio, reduced processor utilization, power/energy efficiency, and integration
> into the system stack. This paper describes the architecture, and novel elements of the
> POWER9 and z15 compression/decompression accelerators with emphasis on trade-offs that
> made the on-chip implementation possible.

---

## Appendix — Fig. 12 compression ratios as printed (page 10)

Recovered by rendering page 10 to PNG at 900 dpi and following each callout line to its bar;
bar order within a group is the legend order (LZ4-1, ZSTD-3, GZIP-6, NXU, NXU 2-pass). Only the
three `AVG.*` groups carry data labels; the per-file bars do not.

| Suite | LZ4-1 | ZSTD-3 | GZIP-6 | NXU (1.1-pass) | NXU 2-pass |
|---|---|---|---|---|---|
| **AVG.Cantrbry** | 1.97 | 3.14 | 3.14 | **2.81** | **2.89** |
| **AVG.Calgary** | 1.92 | 2.88 | 2.95 | **2.65** | **2.68** |
| **AVG.Silesia** | 1.83 | 2.70 | 2.67 | **2.34** | **2.38** |

`pdftotext` recovers these 15 values but assigns them no bars; the mapping above is from the
rendered image. Derived: NXU 2-pass output is **+8.7% / +10.1% / +12.2%** over GZIP-6, and NXU
1.1-pass **+11.7% / +11.3% / +14.1%** — against the prose's "4-5%".

## Appendix — Fig. 15 power and energy as printed (page 11)

POWER9, one chip, active (delta) power = total system power − idle. Rendered and read.

| | NXU GB/s | zlib GB/s | NXU ΔW | zlib ΔW | NXU J/GB | zlib J/GB | Energy ratio |
|---|---|---|---|---|---|---|---|
| Compress, 1 thread | 5.0 | 0.03 | 28 | 30 | **5.7** | **986** | **173×** |
| Compress, 80 threads | 7.1 | 0.8 | 34 | 177 | **4.7** | **219** | **47×** |
| Decompress, 1 thread | 6.5 | 0.3 | 27 | 31 | **4.2** | **103** | **25×** |
| Decompress, 80 threads | 7.6 | **11** | 42 | 183 | **5.5** | **17** | **3.1×** |

The bottom-right cell is the honest one: at 80 threads, software zlib **decompresses faster**
than NXU (11 vs 7.6 GB/s) and is only 3.1× less energy-efficient.

---

## Reported, not applied

Changes I am **not** making, per the standing rule that `survey/README.md`, `survey/TAGS.md`,
`survey/papers-tags.csv` and everything under `QuantArchSurvey/` are the human's.

1. **`survey/README.md`** — status `brief ready` → `analysis ready` (master table line 184).
   Also: the "Papers the taxonomy has no box for" section can now record this entry as
   **explicitly excluded** rather than open, on the human's 2026-09-14 ruling. Following
   `ENEC`'s reasoning, the seven no-box papers do **not** share one disposition:
   `Ecco` belongs inside (it has a real quantizer); `ENEC` is `Q-ORIENTED` but outside the
   boxes; `IBMCompressionAccelerator`, `SpZip` and `CommutativeDataReordering` are not about
   numeric formats at all; `Gist` and `JPEG-ACT` are training-activation work.
2. **`survey/papers-tags.csv`** line 7 — `brief ready` → `analysis ready`. Tags
   `lossless-compression; accelerator` are **both correct and should stay**: TAGS.md defines
   (8) `accelerator` as "custom hardware: ASIC, NPU, or FPGA", and a hard macro on a commercial
   server CPU is the least ambiguous instance of that in the whole corpus.
3. **`QuantArchSurvey/venues/ISCA/README.md` line 89** — the row above. The seed's `non-Q`,
   `—`, `—` and all four Optimization keywords are **confirmed**; the only dispute is
   `ARCH` → `ARCH+SYS`.
