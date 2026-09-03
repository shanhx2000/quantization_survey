# ENVIRONMENT — host facts for `quantization_survey`

Last verified: **2026-09-02**. Everything below was measured on this host, not copied
from documentation. All the commands are read-only; re-run them any time
(`bash Claude/scripts/check_host.sh`).

This is a **text-only project**: read papers, write a survey. It needs a PDF text
extractor, a network connection, and git. It does not need GPUs, CUDA, or a
conda environment — the GPU section below is here only so nobody assumes otherwise.

---

## Host

| Item | Value | Source |
|---|---|---|
| hostname | `hl279-cmp-04` | `hostname` |
| OS | Ubuntu 22.04.5 LTS, kernel `5.15.0-153-generic` | `/etc/os-release`, `uname -r` |
| CPU | 2 × Intel Xeon Gold 6254 @ 3.10 GHz, 18C/36T each → **72 logical cores** | `lscpu` (inherited from `moe_placement/`, not re-measured) |
| Memory | **1510 GB** total | `free -g` (inherited, not re-measured) |
| Disk | `/home` = 56T, **72% used, ~16T free** (measured 2026-09-02) | `df -h /home` |

⚠️ Disk has been the tightest constraint on this host before (784G free on
2026-08-27). It can fill up again at any time. This project stores only text and a
handful of PDFs, so it is not the problem — but **check `df -h /home` before writing
anything large, and do not trust the snapshot value above**.

## Toolchain that this project actually uses

| Component | Version / path | Verified |
|---|---|---|
| `pdftotext` | **22.02.0**, `/usr/bin/pdftotext` (poppler-utils) | 2026-09-02, `pdftotext -v` |
| `pdfinfo` | `/usr/bin/pdfinfo` (same package) | 2026-09-02 |
| `curl` | `/usr/bin/curl` | 2026-09-02 |
| `git` | 2.34.1, `user.name=shanhx2000`, `user.email=hs359@duke.edu` | inherited from `moe_placement/` |
| `python3` | 3.10.12, `/usr/bin/python3` | 2026-09-02 |

**The extraction scripts deliberately depend on nothing but the standard library
plus poppler-utils** (`extract.py` shells out to `pdftotext`/`pdfinfo`; `fetch.py`
uses `urllib` + `html.parser`). So `/usr/bin/python3` is enough and **this project
needs no conda environment**. Do not add one, and do not install packages into the
other projects' envs.

## Network

Direct outbound HTTPS works for arXiv and for open publisher pages
(`extract.py` documents a `curl` command per paper; `fetch.py` snapshots web pages).
**ACM DL, IEEE Xplore, and other subscription publishers return 403 to scripts.**
Those go through the human-download flow — see AGENT-GUIDE §3 and
[`../../survey/uploads/README.md`](../../survey/uploads/README.md). Duke access is via
campus network / VPN and belongs to the human, not the agent.

## GPUs — not used by this project

4 × NVIDIA TITAN RTX (24 GB each), driver `550.163.01`, no NVLink; system `nvcc` is
CUDA 11.5 while the driver supports up to a 12.4 runtime. Full detail, including the
PCIe topology, is in `~/moe_ws/moe_placement/Claude/instructions/ENVIRONMENT.md`.

They are shared with other users. **This project has no reason to touch them.** If a
task ever does need a GPU (e.g. reproducing a quantization result), that is a scope
change: ask the human, and pin one card with `CUDA_VISIBLE_DEVICES=<i>`.

## Permissions

- `hs359` has **no sudo**.
- `hs359` is in the `docker` group, which is technically root-equivalent. **That is
  not permission to change system state** — see AGENT-GUIDE §6.

## Relationship to the sibling project

`~/moe_ws/moe_placement/` is a separate repo (MoE expert placement, simulation-led).
Its `survey/` already holds four quantization-adjacent papers — `MoEQuant`,
`MixtureCompressor`, `D2MoE-DeltaDecompression`, `D2MoE-OnDevice` — read there from a
*placement* angle ("how much space does one expert take"). **When one of those enters
this survey, re-read it here for this survey's purpose and write a fresh
`ANALYSIS.md`; do not copy the file across**, and note in the header that a
placement-angle reading also exists over there.
