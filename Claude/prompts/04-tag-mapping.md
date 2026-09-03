# Prompt — map our tags onto theirs, and draft the 40 ISCA rows

> Run this **once**. It produces the handover artifact for the whole ISCA venue.
> It needs no paper reading — it works from what is already recorded.

---

You are building the bridge between two tag vocabularies for a survey on quantization
architecture, and drafting the venue-list rows the human will paste.

**Read first:**
- `Claude/instructions/AGENT-GUIDE.md` §0b — the read-only rule and what the deliverable is
- `survey/TAGS.md` — **our** 14 tags, with the corpus already tagged
- `QuantArchSurvey/TAXONOMY.md` — **their** four axes. Read all of it, including the worked
  examples and the "judging the generation" section
- `QuantArchSurvey/venues/ISCA/README.md` — their 40 rows with **seed** tags
- `survey/papers-tags.csv` — our 39 papers with links and tags in one table

**Two facts to start from:**

- Our 39 papers match 39 of their 40 rows exactly. The one paper in their list that we do
  **not** have is **TransArray (ISCA'25)** — no link in their list, and their note calls it
  the "G3 codebook anchor on the timeline". Leave its row as a gap and flag it; filling it
  is [`05-fill-gaps.md`](05-fill-gaps.md)'s job.
- Their seed tags are **seeds**. Their workflow says to replace them with what was actually
  found. Where our record disagrees, that is output — but see the trap below.

**Produce `survey/tag-mapping.md`:**

1. **The mapping table**, our 14 tags → their four axes. Be honest about what does not map:
   - `analytical-dtype` / `non-analytical-dtype` / `combined-dtype` split their single
     multi-valued **Data type** axis along a different seam than their tag list does.
   - `multi-bitwidth-hw` is about the datapath; their nearest equivalents live in free-text
     **Optimization** (`bit-serial`, `bit-slice`, `bit-flexible MAC`).
   - We have **no equivalent of their `Q-oriented` axis at all**, and it is the axis they say
     matters most. It must be assigned per paper by their test — *swap the format for plain
     INT8; what is left?* — not derived from our tags.
   - We have **no equivalent of their `Generation` axis** either. Also assign per paper.
   Where a mapping is lossy, say which direction the loss runs.
2. **The 40 proposed rows** for `venues/ISCA/README.md`, in their exact column order, as a
   fenced block the human can review line by line. Mark each row's `Q?` and `Gen` as
   **proposed** with a one-line justification underneath, since neither is derivable from
   our tags.
3. **A disagreement list**: every row where our record contradicts their seed, with the
   evidence and a recommendation. Include the ones I already suspect are genuinely
   arguable — `Ecco` and `AQuant` tagged `NON-Q-ORIENTED`, and `Bringing Near Data
   Processing into the Low-Bit Floating-Point Era` tagged `FP8`/`G1` when the paper is about
   group-wise low-bit FP with per-group scales.
4. **A schema question for the repo owner**: their venue list uses `Q` / `non-Q` while
   `TAXONOMY.md` defines `Q-ORIENTED` / `NON-Q-ORIENTED`. Ask which is canonical rather
   than picking one.

**The trap — do not fall in it:** their taxonomy **deliberately** tags several pre-2023
papers `G3` (OLAccel ISCA'18, GOBO MICRO'20, Mokey ISCA'22) as early instances of the
outlier and codebook threads, and says so explicitly. These are **not** errors. Generation
is judged by paradigm, never by year.

**Also state plainly, near the top:** our tags were assigned from a **brief-level** read
(abstract, intro, section map, headline results, conclusion) — not a full read — and four
papers (`TPUv4i`, `AQB8`, `Cambricon-SR`, `FATE`) have no full text at all and were tagged
from title and abstract only. Every proposed row inherits that uncertainty. Do not present
the mapping as settled.

**Non-negotiable:**

- **Never write anything into `QuantArchSurvey/`.** Not one row. Verify with
  `cd QuantArchSurvey && git status --short` — must be empty. The 40 rows go in
  `survey/tag-mapping.md` for the human to paste.
- Do not edit `survey/README.md` or `survey/TAGS.md`.
- Do not invent a tag on either side. If a paper needs a value neither vocabulary has, say
  so and propose it as a question.
