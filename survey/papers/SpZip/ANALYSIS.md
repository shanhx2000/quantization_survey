# SpZip — paper notes

**SpZip: Architectural Support for Effective Data Compression In Irregular Applications**
Yifan Yang, Joel S. Emer, Daniel Sanchez
**ISCA 2021**, pp. 1069-1082 ｜ DOI: **10.1109/ISCA52012.2021.00087**
Publication info verified 2026-09-02: venue, year **and DOI** all read out of the archived
PDF's own text (IEEE proceedings banner; the DOI was grepped for, not assumed); page range
from the ACM DL / IEEE Xplore record.
Archived here: the **published IEEE version** (the page-1 IEEE proceedings banner is present in the extracted text), 14 pages.

Status: **brief ready** ｜ Last updated: 2026-09-02
Tags: `lossless-compression` `accelerator`
How far it was read: **abstract, introduction, section map, headline result sentences and
conclusion.** The method and evaluation sections were **not** read line by line, and no numbers
have been transcribed into the table below with their full frame — so this stays `brief ready`.
The **cons** in the brief combine the paper's own stated limits with criticisms other entries in
this corpus make of it; where a criticism is another paper's, it is attributed inline.

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

## Brief

### 1. Motivation

Irregular applications (graph analytics, sparse linear algebra) are memory-bandwidth-bound,
so compression should help — but software compression overhead swamps the gain, and prior
hardware compressors assume regular access patterns these workloads do not have.

### 2. Overview

Architectural support that accelerates **traversal, decompression and compression
together**, decoupled from the core so memory and decompression latency are hidden.
Programmable via a **Dataflow Configuration Language**, implemented cheaply through dataflow
execution and time-multiplexing. Evaluated in a simulated multicore across graph and linear-
algebra algorithms.

### 3. Pros and cons

**Pros**

- Correctly identifies that traversal and decompression are *interleaved* in irregular
workloads, so accelerating one without the other does not help — this framing is the
contribution.
- Cheap for what it does: fetcher and decompressor cost **0.2% of a general-purpose core's
area**.
- Strong and consistently reported results: gmean 3.0× over software-only and 1.5× over
hardware-accelerated prior work, with 1.7×/1.4× traffic reduction; composes with
orthogonal schemes (PHI+SpZip is 6.1× over Push).

**Cons**

- **No quantization content whatsoever** — lossless structural compression for graph
workloads; the source list's own note says "No quantization; CSR format".
- Simulation-only evaluation, with no fabricated or synthesized-to-silicon result.
- Programmability via a new configuration language is a real adoption cost that the paper
does not price.

### 4. Where it applies

Outside the taxonomy. Keep for the **lossless-compression / data-movement** cluster as the
graph-workload counterpart to the DNN-focused entries — useful mainly to delimit what the
survey is *not* about.

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

> **Keywords:** No quantization; Compressed Sparse Row (CSR) format


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
