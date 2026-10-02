#!/usr/bin/env python3
"""
Publish the human's paper notes into the shared team repo.

  python3 Claude/scripts/sync_notes.py [--dry-run]

Source : survey/papers/<Name>/paper-note.md   -- the human's working draft
Target : QuantArchSurvey/venues/ISCA/notes/<short-name>.md

This is the ONLY thing in this project that writes into QuantArchSurvey/, and it
writes nothing of its own: every published byte is the human's, minus two
publish-time removals that they asked for.

  1. Section `## 6. Claude notes` and everything after it is dropped. That section
     is the reading agent's suggestions and says so in its own first line.
  2. Inside `## 5. Comment`, blocks labelled `**Unadmitted.**` or `**Pair with ...**`
     are dropped (instruction of 2026-09-03). Their material belongs in ANALYSIS.md,
     not in the venue note.

Nothing else is touched -- no reformatting, no rewrapping. Re-run it any time; it is
idempotent, and it reports what changed.
"""
import re
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / "survey" / "papers"
DST = ROOT / "QuantArchSurvey" / "venues" / "ISCA" / "notes"

# Out of scope for the survey, removed from the team repo on 2026-09-14.
# Kept filed here -- the reading stands, it just is not a quantization paper.
# Listed so that a later sync cannot silently republish them; the script also
# deletes their notes from the team repo if it finds them there.
EXCLUDED = {
    "Cambricon-SR",              # pruning of an Instant-NGP hash grid; no quantization
    "SpZip",                     # lossless sparse-traversal compression; no quantization
    "IBMCompressionAccelerator", # Deflate engine; no AI content at all
    "CommutativeDataReordering", # DRAM bus switching activity; no value changes
    "ELSA",                      # SNN -- removed again 2026-10-02 (ISCA Pass 13); Phi stays
    # ELSA and Phi (SNN) were excluded 2026-09-14 and restored 2026-10-01 (ISCA Pass 11).
}

# survey/papers directory name -> published note filename
NAMES = {
    "BitFusion":        "bit-fusion",
    "DRQ":              "drq",
    "EVA":              "eva",
    "Ecco":             "ecco",
    "LightNobel":       "lightnobel",
    "NDPLowBitFP":      "ndp-low-bit-fp",
    "P3-LLM":           "p3-llm",
    "Phi":              "phi",
    "RaPiD":            "rapid",
    "SamsungNPU":       "samsung-npu",
    "AQB8":             "aqb8",
    "AQuant":           "aquant",
    "Cambricon-SR":     "cambricon-sr",
    "CommutativeDataReordering": "commutative-data-reordering",
    "ELSA":             "elsa",
    "ENEC":             "enec",
    "FATE":             "fate",
    "Gist":             "gist",
    "IBMCompressionAccelerator": "ibm-compression-accelerator",
    "JPEG-ACT":         "jpeg-act",
    "LoKA":             "loka",
    "MXFFP":            "mxffp",
    "RAELLA":           "raella",
    "RingCNN":          "ringcnn",
    "SingularBit":      "singularbit",
    "SmartExchange":    "smartexchange",
    "SpZip":            "spzip",
    "TPUv4i":           "tpuv4i",
    "UniCore":          "unicore",
    "XtraMAC":          "xtramac",
    "LUTTensorCore":   "lut-tensor-core",
    "MicroScopiQ":     "microscopiq",
    "Mokey":           "mokey",
    "Oaken":           "oaken",
    "OASIS":           "oasis",
    "OLAccel":         "olaccel",
    "OliVe":           "olive",
    "Omni-LUT":        "omni-lut",
    "Tender":          "tender",
    "TransitiveArray": "transitive-array",
}

DROP_LABEL = re.compile(r"^\*\*(Unadmitted\.|Pair with\b)")


def publish(text):
    """Apply the two publish-time removals. Returns (text, dropped_labels)."""
    dropped = []

    # 1. cut the agent's section and everything after it
    m = re.search(r"^## 6\.", text, re.M)
    if m:
        text = text[: m.start()]

    # 2. drop the named blocks, but only inside section 5
    m = re.search(r"^## 5\. Comment\s*$", text, re.M)
    if m:
        head, body = text[: m.end()], text[m.end():]
        kept = []
        for block in body.split("\n\n"):
            if DROP_LABEL.match(block.lstrip()):
                dropped.append(block.lstrip().split("\n")[0][:52])
            else:
                kept.append(block)
        text = head + "\n\n".join(kept)

    return text.rstrip("\n") + "\n", dropped


def status_of(d):
    """The paper's declared status, read from its ANALYSIS.md header."""
    a = d / "ANALYSIS.md"
    if not a.is_file():
        return None
    for line in a.read_text().splitlines():
        if line.startswith("Status:"):
            return line.split("**")[1] if "**" in line else None
    return None


def check_map_is_complete():
    """Every note-ready paper must have a published name. Fail loudly if one does not.

    The slugs are chosen by meaning, not by a rule (LUTTensorCore -> lut-tensor-core, but
    MicroScopiQ -> microscopiq and OliVe -> olive), so the map is hand-written -- which
    means a new note can silently go unpublished. This is the guard for that.
    """
    orphans = sorted(
        d.name for d in SRC.iterdir()
        if (d / "paper-note.md").is_file()
        and status_of(d) == "note ready"
        and d.name not in NAMES
        and d.name not in EXCLUDED
    )
    if orphans:
        sys.exit(
            "these directories have a paper-note.md but no entry in NAMES, so they would "
            "not be published:\n"
            + "".join(f"    {o}\n" for o in orphans)
            + f"add each to NAMES in {pathlib.Path(__file__).name} with the filename it "
              "should get in notes/."
        )


def main():
    dry = "--dry-run" in sys.argv
    if not DST.is_dir():
        sys.exit(f"no target directory: {DST}\n(is QuantArchSurvey/ cloned?)")
    check_map_is_complete()

    # Withdraw anything now out of scope before publishing the rest.
    for name in sorted(EXCLUDED):
        stale = DST / f"{NAMES[name]}.md" if name in NAMES else None
        if stale and stale.is_file():
            print(f"  {name:<18} -- EXCLUDED from the survey; removing {stale.name}")
            if not dry:
                stale.unlink()

    changed = missing = same = held = 0
    for src_name, out_name in sorted(NAMES.items()):
        if src_name in EXCLUDED:
            continue
        src = SRC / src_name / "paper-note.md"
        if not src.is_file():
            print(f"  {src_name:<18} -- no paper-note.md yet, skipped")
            missing += 1
            continue

        # Only `note ready` is publishable. A drafted note that the human has not yet
        # adopted stays here: the status is their statement that it goes out under their
        # name, and the agent never sets it. See AGENT-GUIDE.md section 5.
        st = status_of(SRC / src_name)
        if st != "note ready":
            print(f"  {src_name:<18} -- draft note, status `{st}` (not `note ready`), held back")
            held += 1
            continue

        out, dropped = publish(src.read_text())
        dst = DST / f"{out_name}.md"
        before = dst.read_text() if dst.is_file() else None

        if before == out:
            print(f"  {src_name:<18} -> {out_name+'.md':<22} unchanged")
            same += 1
        else:
            verb = "new" if before is None else "updated"
            print(f"  {src_name:<18} -> {out_name+'.md':<22} {verb}"
                  f"{'' if before is None else f' ({len(before.splitlines())} -> {len(out.splitlines())} lines)'}")
            changed += 1
            if not dry:
                dst.write_text(out)
        for d in dropped:
            print(f"       dropped from §5: {d}")

    print(f"\n{changed} written, {same} unchanged, {held} held back as draft, "
          f"{missing} awaiting a note"
          f"{'  [DRY RUN -- nothing written]' if dry else ''}")
    # a note in the target with no source is a rename or a stale file: worth saying
    published = {f"{n}.md" for n in NAMES.values()}
    for f in sorted(DST.glob("*.md")):
        if f.name not in published:
            print(f"  ! {f.name} in notes/ has no source in survey/papers -- stale?")


if __name__ == "__main__":
    main()
