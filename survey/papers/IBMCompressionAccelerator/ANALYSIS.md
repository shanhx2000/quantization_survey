# IBMCompressionAccelerator — paper notes

**Data Compression Accelerator on IBM POWER9 and z15 Processors**
Authors: **not transcribed** — a large industrial author list; read it off page 1 of the PDF before citing.
**ISCA 2020** ｜ DOI: **10.1109/ISCA45697.2020.00012**
Publication info verified 2026-09-02: venue, year **and DOI** all read out of the archived
PDF's own text (IEEE proceedings banner; the DOI was grepped for, not assumed); page range
from the IEEE Xplore link in the source CSV.
Archived here: the **published IEEE version** (the page-1 IEEE proceedings banner is present in the extracted text), 14 pages.

Status: **brief ready** ｜ Last updated: 2026-09-02
Tags: `lossless-compression` `accelerator`
How far it was read: **abstract, introduction, section map, headline result sentences and
conclusion.** The method and evaluation sections were **not** read line by line, and no numbers
have been transcribed into the table below with their full frame — so this stays `brief ready`.
The **cons** in the brief combine the paper's own stated limits with criticisms other entries in
this corpus make of it; where a criticism is another paper's, it is attributed inline.

> Publisher record: https://ieeexplore.ieee.org/document/9138913
> **There is no arXiv version** (arXiv API title search, 2026-09-02). The PDF was downloaded by a
> human and filed through [`survey/uploads/`](../../uploads/) — the sanctioned route when the
> arXiv-only rule leaves a paper unreachable; see
> [`Notes-002`](../../../Claude/notes/Notes-002-paper-source-access.md).
> The PDF is **not committed** (1.5 MB) and **cannot be re-downloaded by script** —
> both publishers 403. Re-extract with `python3 extract.py` → `extracted/` (committed).
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, ISCA 2020 row.

---

## Brief

### 1. Motivation

Lossless compression pays for itself in storage, memory and network cost, but is processor-
intensive enough that people skip it. An on-chip accelerator can make it effectively free.

### 2. Overview

An **industrial product paper**: the on-chip Deflate (LZ77 + Huffman)
compression/decompression accelerator — the NXU — shipped in IBM POWER9 and z15. Describes
the LZ77 stage, the Huffman stage, the decompressor, and the system-stack integration, with
emphasis on the trade-offs that made an on-chip implementation viable.

### 3. Pros and cons

**Pros**

- Real silicon at scale, with the area accounting spelled out: **<0.5% of chip area**,
delivering 388× the throughput of software zlib on a core and 13× the whole chip of cores;
z15 doubles it, to 280 GB/s system-wide.
- End-to-end rather than kernel-level: 23% speedup on Spark TPC-DS, which is the number that
matters for a product.
- Genuinely useful as the ceiling reference for what fixed-function lossless compression
costs and delivers in production silicon.

**Cons**

- **Not a quantization paper and not about AI** — general-purpose enterprise data
compression. Its presence here is contextual.
- Fixed to the Deflate format; no exploration of alternatives or of ML-specific data
statistics, which is exactly the gap [`ENEC`](../ENEC/ANALYSIS.md) later fills for model
weights.
- Industry-track paper: methodology and comparisons are product-shaped, not controlled
experiments.

### 4. Where it applies

Context and calibration for the **lossless-compression** cluster. The source list marks it
**"Less related"**; keep it as the industrial reference point against which
[`ENEC`](../ENEC/ANALYSIS.md) and [`SpZip`](../SpZip/ANALYSIS.md) can be positioned.

---

## Conclusions

**Not read in full.** The brief above is the current state of knowledge; nothing below it
has been filled in, and no number from this paper may be cited without reading the
evaluation section first.

---

## Method

## Key numbers, with their frame

| Setting | Model | Metric | Baseline | Result | Source |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

## Cost and requirements

## Limitations and open questions

## Relation to other entries

## Note from the source list

> **Keywords:** on-chip integrated data compression accelerator; to improve IO
>
> **Comment:** Less related

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
