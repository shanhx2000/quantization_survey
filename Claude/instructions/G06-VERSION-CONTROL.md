# G06 — VERSION CONTROL (general)

**General file.** Identical in every repo under `~/moe_ws/`. Fix it in
`~/moe_ws/Claude-template/`, then re-sync — not in a repo copy.

Simple on purpose. The rules below exist because each one was broken at least once in
this workspace, usually by an agent working alongside another agent in the same repo.

---

## 1. What is versioned

| Repo | Versioned? | Note |
|---|---|---|
| `moe_placement/` | yes, remote `origin` on GitHub | |
| `quantization_survey/` | yes, remote `origin` on GitHub | contains `QuantArchSurvey/`, which is **read-only** — never its files, config, branches, commits or remotes |
| `MobiQuant/` | **no** | ~43 GB of checkpoints and archives. Do not `git init` it without a plan for those |
| `giantlut/` | **no** | small; could reasonably become a repo — ask the human first |

In a non-git repo there is no undo. **Before overwriting or deleting anything there,
copy it aside first**, and say in your report that there is no history to fall back on.

## 2. Staging — the rule that matters most

**Never `git add -A`, `git add -u`, or `git add .`. Name the paths you changed.**

More than one agent works in these repos at once, and repos routinely carry a large pile
of uncommitted work that is not yours — `moe_placement` was at 92 uncommitted paths while
this file was written. A wildcard add sweeps a colleague's half-finished work into your
commit under your message. That happened here: `git add -A Claude/` pulled another agent's
in-flight notes and report into a commit about GPU leases.

```bash
git status --short          # always first. Expect other people's work to be here.
git add path/one path/two   # only yours
git diff --cached           # read what you are about to commit
```

**If a file you must touch already has someone else's uncommitted changes**, do not
bundle them. Either leave the file unstaged and say so in your summary, or commit it on
its own with a message that says whose work it is. Both are fine; silently absorbing it
is not.

## 3. When to commit

- **Commit when the human asks**, and at checkpoints you can describe in one line.
- **Do not commit broken code silently.** If you commit work in progress, say so in the
  message.
- **Commit promptly once you change shared state** — an instruction file, a task board, a
  status table. Another agent is reading the old version until you do.

## 4. Branches

- Anything substantial gets a branch: `git checkout -b <topic-in-kebab-case>`.
- **Do not commit directly to `main`** unless it is a small, self-contained fix.
- Check which branch you are on before starting. Repos here are often left on an
  unrelated topic branch from previous work.
- **Do not rewrite shared history.** No `push --force`, no `rebase` of anything already
  pushed, no `reset --hard` on a branch someone else may hold.

## 5. Commit messages

English (`G02`). Subject in the imperative, roughly ≤72 characters, prefixed with the
area it touches. Then a blank line and a body that says:

- **what** changed,
- **why** — the reason, not a restatement of the diff,
- **how far it was verified** — tests run, what was only smoke-tested, what was not run,
- **what was deliberately left out.**

End with the attribution line the harness specifies for this session.

```
q15: add the three-way branch router and a CPU smoke test

Freezes the 4-bit base and learns one reconstruction head per half. The per-branch
reconstruction term is the only genuinely new part -- without it the two halves are a
residual code and the LSB branch cannot work.

Verified: 37 unit tests pass, CPU end-to-end smoke test green for both heads.
Not done: never run on real weights; base is RTN only; fake-quant, so no speed claim.
```

## 6. What never goes in git

PDFs, model weights, checkpoints, datasets, logs, experiment outputs, upstream clones,
and the shared GPU lease directory. **Read `.gitignore` before adding anything new**, and
if you add a new kind of artefact, add its rule in the same commit.

`git status --short` showing an unexpected large file is a stop sign, not a nuisance.

## 7. Working next to other agents

- `git status` before you stage. Every time.
- **Numbering collides.** `Notes-NNN` / `Reports-NNN` are allocated by whoever writes
  first, and two agents picked `Notes-012` on the same day here. Before allocating, check
  `ls` **and** `git log` for numbers committed since you last looked. If you collide and
  the other file is already committed, yours is the one that moves.
- Do not check out, reset, or delete a branch you did not create.
- If you need someone else's work in order to finish yours, say so in your summary rather
  than committing it for them.
