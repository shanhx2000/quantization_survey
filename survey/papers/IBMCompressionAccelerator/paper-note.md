# Data Compression Accelerator on IBM POWER9 and z15 Processors (Industrial Product)

**Venue / Year:** ISCA 2020, pp. 1-14 · **Link:** https://doi.org/10.1109/ISCA45697.2020.00012 · **Reader:** Haoxuan · **Date:** 2026-09-14

## Tags

| | |
|---|---|
| **Level** | `ARCH+SYS` |
| **Q-oriented** | `NON-Q-ORIENTED` |
| **Data type** | `—` |
| **Generation** | `—` |
| **Optimization** | Deflate (RFC1951) · LZ77 · dynamic Huffman · hybrid latch-CAM + SRAM pseudo-CAM dictionary · hardware DHTGEN · speculative parallel VLC decoder · `DFLTCC` ISA instruction · user-mode page-fault handler · POWER9 / z15 shipping silicon, 14 nm |

## 1. One-line summary

**No AI and no quantization anywhere** — `neural`, `DNN`, `learning`, `inference`, `training`,
`quantiz*`, `precision`, `bitwidth`, `mantissa`, `exponent`, `tensor`, `GPU`: **zero hits each,
bibliography included** — this is IBM's shipping **NXU**, a fixed-function **Deflate
(LZ77 + dynamic Huffman)** engine in **< 0.5% of a 14 nm POWER9 / z15 chip**, contributing
circuits (**512 B latch CAM for near history + SRAM pseudo-CAM hash table for the 32 KB far
history**, 66 KB SRAM vs 1.9-3.2 MB in FPGA prior art; a decoder speculating a code at all 32
bit positions for 8 codes/cycle) and a system stack (`DFLTCC`, user-mode page-fault handling),
measured at **> 7 GB/s (POWER9) / 15 GB/s (z15)** — **388× one zlib thread but 13× a full chip
of cores, and 0.75× on decompression** — at **~10% worse ratio than gzip -6**, **4-6 J/GB vs
zlib's 17-986**, and **+23% end-to-end on Spark TPC-DS**.

## 2. Data type

**There is none.** No format, bitwidth, granularity, outlier mechanism, accumulator or PTQ/QAT — opaque bytes in, bit-exact RFC1951 out.

**The only numeric-format decision is metadata:** Huffman symbol counters kept as **10-bit floating point** "to reduce the number of latches" in the sorter.

**"Lossy" is a false friend** — the one occurrence describes the pseudo-CAM **missing dictionary matches** (lost ratio), not lost data.

## 3. Optimization

**Area budgeted by dictionary range.** Ratio saturates with window size, so an area-hungry **latch CAM** covers the **near history ≤ 512 B** and an **SRAM pseudo-CAM** the **513 B - 32 KB far history** — an 8-way set-associative cache with FIFO replacement, 8 five-byte tokens hashing into a 2048×144 b table, 64 candidates filtered to 2 by 6-bit tags. **66 KB SRAM** vs **1.92 / 3.15 MB** of block RAM in the FPGA engines cited; SRAM holds **14-16× more bits per unit area than latches** at 14 nm. Dynamic Huffman is real, not a static table: Shear-Sort the counts, then enforce Deflate's 15-bit ceiling by iterating `count ← (count+1)/2` until `⌈−log₂ p_min⌉ ≤ 15`. **1.1-pass** samples the first 32 KB and reuses the table for 256 KB — 89% of peak instead of 50%.

**POWER9 vs z15 is one array and one clock.** P9's 1-port hash banks conflict **87%** of the time (2.1 cycles/access); z15's 2-port banks give **1.12**, and z15 clocks 2.5 vs 2.0 GHz — that is the entire 2×. z15 also adds a **hardware Huffman-table generator**; POWER9 makes software build and cache the table.

**`ARCH+SYS`, not `ARCH`.** §VII is one of five listed contributions: z15's architected unprivileged **`DFLTCC`** instruction in millicode (no OS, no driver); POWER9's mmap'd job queues via `copy`/`paste` plus a **user-mode page-fault handler** that shrinks and retries the job instead of pinning pages; zlib-API libraries and a Spark/Parquet JNI shim.

## 4. Results

| | |
|---|---|
| Baseline | zlib 1.2.11 at 1 / 8 / 80 SMT4 threads on the same chip; gzip, ZSTD, LZ4 tools; Spark baseline = snappy (Parquet) + lz4 (shuffle) |
| Workloads | Silesia / Canterbury / Calgary corpora; Spark 2.3.3 + TPC-DS SF=3000 on 4× POWER9 LC922 |
| Accuracy delta | **N/A — lossless**, bit-exact RFC1951 |
| Compression ratio | Suite averages (Cantrbry / Calgary / Silesia): **NXU 2.89 / 2.68 / 2.38** vs **GZIP-6 3.14 / 2.95 / 2.67**, ZSTD-3 3.14 / 2.88 / 2.70, LZ4-1 1.97 / 1.92 / 1.83 |
| Throughput | **P9 > 7 GB/s, z15 15 GB/s peak** per chip. Compress **388× / 49× / 13×** (P9) and 574× / 72× (z15) vs zlib 1 / 8 / 80 threads; **decompress 34× / 4.6× / 0.75×** (P9), 30× / 3.8× (z15). Hardware setup latency 0.55-0.78 µs |
| End-to-end | TPC-DS **33.38 vs 27.06 QpH = +23%**, shuffle bytes **−32%**; 3 TB generation **29% faster than Snappy** |
| Energy / area | **< 0.5% of chip area** (no mm² given); **4.2-5.7 J/GB** vs zlib **17-986** (up to 173×); +27 to +42 W system delta |
| Technology node | **14 nm**; NXU @ 2.0 GHz (P9) / 2.5 GHz (z15), 8 B/clock |
| Evidence level | **Silicon measurement throughout** — POWER9 AC922 and a z15 LPAR, real cluster end-to-end. No simulator, RTL, synthesis or projection |
| **Is the comparison fair?** | Measured on shipping silicon throughout — no simulator, RTL or projection. **Not iso-thread** (388× is one zlib thread; 13× a full chip; decompress **0.75×**); **not iso-ratio** (2.34-2.89 vs gzip-6's 2.67-3.14). Not to quote bare: **388×**; **280 GB/s** (20-chip topology, cited to the z15 ISSCC paper, not measured here); "4-5% larger than gzip" (Fig. 12 gives **8.7-12.2%**) |

## 5. Comment

Too general compression, and focuses on circuit design. Not for LLM. **Beyond our interested range.**

## 6. Claude notes

*Suggestions from the reading agent. **Strip this section before copying into
`QuantArchSurvey/venues/ISCA/notes/`.***

- **Out of scope per your ruling — kept short deliberately.** Recommend **keep the row as a background citation, do not delete it**: it is the corpus's only measured-silicon general-purpose lossless baseline, and the row is the audit trail.
- **Read depth.** Full close read §I-§X + Tables I-III. Figs. 12, 15, 17 **rendered to PNG and read visually** (pdftotext recovers their labels without bar assignments); **Figs. 13-14 have no labels**, so every throughput number is prose or Table I. Skimmed: Fig. 8, and Fig. 9's unpublished CUST1-5 datasets.
- **One seed dispute: `ARCH` → `ARCH+SYS`** (ISA instruction + user-mode fault handler, a listed contribution). `non-Q`, `—`, `—` and all four seed keywords **confirmed by grep**, not carried. Generation `—` follows the `SpZip` / `Cambricon-SR` precedent: no numeric format, so no position on the paradigm axis.
- **Exclude 388× (one zlib thread; chip-level is 13×, decompress is 0.75×) and 280 GB/s (20-chip topology, cited to ref. [6]).** Also: §VIII-B says NXU is "4-5% larger than gzip -6" while its own Fig. 12 averages give **8.7-12.2%** — unexplained; use the figure.
- **If it is cited at all, cite it with [`ENEC`](../ENEC/ANALYSIS.md).** A real LZ77+Huffman engine gets **2.3-2.9×** on general data; the same class of coder gets **~1.35-1.5×** on BF16 weights. **Model weights are near-incompressible by general-purpose lossless standards** — that sentence needs both papers, and ENEC's wish list for future NPUs is precisely NXU's Huffman block.
- **`survey/README.md` / `papers-tags.csv`, reported not applied:** `brief ready` → `analysis ready`; the "no box" entry moves from open to **explicitly excluded**. Tags `lossless-compression` `accelerator` both stay.
