# Phi: Leveraging Pattern-based Hierarchical Sparsity for High-Efficiency Spiking Neural Networks

**Venue / Year:** ISCA 2025 (Tokyo) · **Link:** https://arxiv.org/abs/2505.10909 (DOI 10.1145/3695053.3731035) · **Reader:** Haoxuan · **Date:** 2026-09-10

## Tags

| | |
|---|---|
| **Level** | `ARCH` |
| **Q-oriented** | `NON-Q-ORIENTED` |
| **Data type** | `BINARY` `VQ` |
| **Generation** | — (see §6 — I'd leave it unassigned) |
| **Optimization** | SNN · pattern-based sparsity · k-means patterns · precomputed products · exact two-level decomposition · Hamming-distance clustering · PWP prefetch · optional PAFT |

## 1. One-line summary

Decomposes a binary spike activation matrix **exactly** into a Level-1 matrix of k-means-clustered
**binary patterns**, whose products with the weights are **precomputed offline** and fetched by
index, plus a Level-2 **{1,−1} element-wise correction** carrying the residual — clustering under
**Hamming distance, so that minimising clustering error and maximising Level-2 sparsity are the
same objective** — reaching **96.80% element sparsity against ~83% native bit sparsity** for
**3.45× speedup and 4.93× energy efficiency** over the best SNN accelerator, at the cost of
pattern-weight-product traffic of which only **27.73%** is used.

## 2. Data type

**Nothing is quantized.** Activations are 1-bit spikes going in and 1-bit going out. `L1 + L2` reconstructs the activation matrix **exactly** — a lossless decomposition, not an approximation.
**Level 1.** A pre-defined **binary pattern** per row (or all-zeros), stored as an index. The index retrieves an offline-**precomputed pattern-weight product (PWP)**. Structured, vector-wise.
**Level 2.** **{1, −1}** element-wise correction carrying the residual. Irregular, and very sparse: **96.80%** vs ~83% native bit sparsity.
**Codebook.** k-means over binary vectors under **Hamming distance** — chosen because Hamming distance to a pattern *is* that row's Level-2 non-zero count. Centres rounded to {0,1} each iteration.
**Filtered first.** All-zero rows (nothing to compute) and one-hot rows (their PWP is just a weight row, and their L2 sparsity can't beat the original).
**Granularity.** Tiled along K; **128 patterns per K tile**; independent pattern sets **per model, per dataset, per layer, per partition**.
**Outliers.** None — the Level-2 residual is exact, so there is no tail to protect.
**Escape hatch.** None needed; nothing is approximated. The real cost sits in memory, not precision.
**Retraining.** **Calibration only — PAFT is optional.** A small static training subset suffices (activation-row distributions are consistent train-to-test). PAFT buys 1.26×/1.1× and costs accuracy as `lr`/`λ` rise; the paper offers both operating points.

## 3. Optimization

**The decomposition is exact, and that is what makes it work.** There is no accuracy/efficiency
trade at the format level at all — Level 1 handles whatever a pattern captures, Level 2 carries the
rest, and their sum is the original. All the efficiency comes from Level 2 being far sparser than
the tensor it corrects: **96.80% against ~83%**. Zero-skipping SNN accelerators exploit the 83%;
Phi manufactures the extra 14 points by subtracting a pattern first.

**The clustering objective and the hardware objective are the same function.** Patterns are k-means
centroids over binary vectors under **Hamming distance**, and the Hamming distance between a row and
its assigned pattern is exactly the number of Level-2 corrections that row will need. So the
calibration doesn't approximate the hardware goal — it *is* the hardware goal. Centres are rounded
back to binary each iteration to stay representable.

**Level 1 removes work rather than skipping it.** Because patterns are fixed offline, their products
with the weights are computed once, offline, and at runtime a pattern index is a **memory read, not
an arithmetic operation**. This is the structural win, and it is different in kind from
zero-skipping: the computation never enters the inference loop.

**The cost is that it converts compute into traffic, and the paper says so.** 128 PWP sets per K
tile strain the on-chip buffer; **only 27.73% of precomputed PWPs are used per Level-1 tile**. Phi
answers with a **PWP prefetcher** that reads pattern indices ahead — possible because the K-first
processing order generates the next layer's patterns during the current layer — but still concedes
**"our DRAM energy is not significantly reduced"**.

## 4. Results

| | |
|---|---|
| Baseline | **Stellar** (best, and the headline), SpinalFlow, SATO, PTB, Spiking Eyeriss. **Four are re-simulated in Phi's framework; Stellar is quoted from its own paper** |
| Models / datasets | Spiking CNNs (VGG, ResNet) and spiking transformers (Spikformer, SDT, SpikeBERT, SpikingBERT) on CIFAR10, CIFAR100, CIFAR10-DVS, SST-2, SST-5, MNLI |
| Accuracy delta | **None from the decomposition — it is exact.** PAFT trades accuracy for pattern strength as `lr`/`λ` rise, but **no accuracy table is given for those operating points** |
| Speedup | **3.45× vs Stellar**; 6.29× / 6.57× / 12.18× vs SpinalFlow / SATO / PTB |
| Energy / area | **4.93× vs Stellar**; 2.23× / 2.77× / 13.48× / 31.59× vs SpinalFlow / SATO / PTB / Spiking Eyeriss. **DRAM energy conceded not to improve.** Level-2 element sparsity **96.80%** vs ~83% bit sparsity; PWP utilisation **27.73%** |
| Technology node | **28 nm** (SystemVerilog + Synopsys DC), CACTI 7.0 for buffers, DRAMsim3 for off-chip |
| Evidence level | **RTL + synthesis** + a simulation framework hosting four of five baselines. No silicon |
| **Is the comparison fair?** | Four of five baselines re-simulated at the same node with CACTI and DRAMsim3 — but **the headline baseline, Stellar, is quoted from its own paper**, the one comparison not run in Phi's framework. **Whether 3.45×/4.93× include the optional PAFT is never stated**; without it, ≈2.7×/4.5×. Speedup headline is the most conservative of four; energy headline is not. DRAM energy conceded flat |

## 5. Comment

May not count as a quantization paper, unless one views SNN as a special case of 1-bit
quantization.

## 6. Claude notes

> **Suggestions from the reading agent. Strip this section before copying into
> `QuantArchSurvey/venues/ISCA/notes/`.**

- **Generation: I'd leave it unassigned, and the revision log already invites that call.** The log
  set Phi to `G3` "per the data-type change" and flagged "off-workload (SNN), so flag if you would
  rather this stay unassigned." Having read it: the `G3` is defensible **by mechanism analogy
  only** — codebook-plus-precomputed-products is exactly Mokey's and EVA's move. But Generation
  classifies *quantization paradigms*, and **Phi quantizes nothing**. A `G3` here reads as a claim
  about precision the paper never makes. If you keep it, I'd add "(mechanism only)".
- **`non-Q` is right, but the log's reason isn't the strongest one.** The log says "strip the
  codebook and the sparsity hierarchy survives." The sharper argument: **there is no quantization
  to strip.** Activations are 1-bit in and 1-bit out, and `L1 + L2` is exact. This is the corpus's
  best case for judging `Q-oriented` by *what is traded*, not *what machinery is used* — Phi has
  the full non-analytic apparatus (k-means, codebook, indices, precomputed products) and reduces
  nobody's precision by a single bit.
- **§5 material, if you want it.** Three papers in this corpus now use the same k-means codebook
  machinery for three different objectives: **Ecco** builds one to *store* through (never computes
  on indices), **EVA** builds one to *compute* through (never reconstructs weights), and **Phi**
  builds one to *skip* through (the index fetches a precomputed product; nothing is compressed).
  "Codebook-based" as a single survey category conflates all three.
- **The brief's headline con was wrong and I've corrected it.** It said Phi "needs pattern-aware
  fine-tuning, so it is not a drop-in." §3.3 says PAFT is **optional** and §5.4 prices it at
  1.26×/1.1×. Phi *is* a drop-in for a trained SNN, calibration-only, at a 1.26× discount — a
  materially better story.
- **On the §5.6 table-construction axis**, Phi joins OASIS at **offline-static** — and the pair is
  interesting because they're there for opposite reasons: OASIS to avoid arithmetic, Phi to avoid
  redundant work.
- **Two things to watch if we cite the numbers.** The headline is against **Stellar, the one
  baseline not re-simulated**. And whether it includes PAFT is unstated — that's a 1.26× swing on
  the speedup.
- **Shared authorship with EVA and Ecco** (Duke — Cong Guo, Bowen Duan, Chiyue Wei, Hai Li, Yiran
  Chen appear across all three). Worth knowing when reading their cross-citations, and relevant to
  how the survey handles the EVA self-citation question.
