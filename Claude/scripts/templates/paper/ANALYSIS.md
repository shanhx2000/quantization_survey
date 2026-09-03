# __NAME__ — paper notes

**__TITLE__**
__AUTHORS__ (__AFFILIATIONS__)
**__VENUE__ __YEAR__**, pp. __PAGES__ ｜ DOI: __DOI__
Publication info verified __DATE__ via __SOURCE__.
<!-- If there is no formal publication: write `preprint`, the arXiv id and version,
     and "no publication record as of <date>, checked on Crossref". Never leave blank,
     never guess. If what we archive is the arXiv version rather than the published
     one, say so here and say whether the two were compared. -->
Archived here: __WHICH_VERSION__ ｜ __N__ pages

Status: **__STATUS__** ｜ Last updated: __DATE__
How far it was read: <!-- required at `analysis ready` and above: name the sections
read closely and the ones only skimmed, so nobody redoes the work or cites a section
nobody read. -->

> Original: __URL__
> The PDF is **not committed** (__SIZE__). Re-download: `__DOWNLOAD__`
> Extract text: `python3 extract.py` → `extracted/` (committed, greppable)
>
> **Why this paper is in the survey**: <!-- one or two sentences: which section of the
> survey it serves, and what it is the evidence for. -->

---

## Conclusions

<!-- Conclusions first, details after (AGENT-GUIDE §4). One numbered point per claim.
     Mark every one **verified** (with the section/table it came from) or
     **inferred / not verified**. At `brief ready` this section is a first pass off
     the abstract and must say so on every line. -->

1.
2.

---

## Method

<!-- What it actually does, in enough detail that the survey can classify it:
     what is quantized (weights / activations / KV cache / gradients), when
     (PTQ / QAT / during training), granularity (per-tensor / per-channel / per-group,
     group size), the numeric format (INT/FP/NF, symmetric or not), and what extra
     machinery it needs (calibration data, a search, a solver, a custom kernel). -->

## Key numbers, with their frame

<!-- AGENT-GUIDE §2.4: a number without its frame does not go into the survey.
     Every row must name the model, the task/dataset, the baseline, the bit-width,
     and the granularity. Quote the original sentence for anything load-bearing. -->

| Setting | Model | Metric | Baseline | Result | Source |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

## Cost and requirements

<!-- Quantization time, calibration set size, whether it needs a GPU to quantize,
     whether the speedup requires a custom kernel, and which hardware the kernel
     targets. This is what separates methods that ship from methods that don't. -->

## Limitations and open questions

<!-- What the paper itself concedes; what it does not evaluate; where our reading is
     uncertain. Anything to check on a closer read goes here as a question. -->

## Relation to other entries

<!-- Link with relative paths, e.g. `[GPTQ](../GPTQ/ANALYSIS.md)`. Note baselines it
     compares against, papers that later contradict it, and any conflicting numbers
     between entries -- conflicts are recorded, not silently resolved. -->

## Abstract (verbatim)

> <!-- paste unedited -->
