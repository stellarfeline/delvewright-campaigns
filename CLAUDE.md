# Delvewright Campaigns — what an agent must know here

This file is not a constitution. The engine repository's `CLAUDE.md` — checked in
at the root of `stellarfeline/delvewright` — governs work in this repository too,
and its operating-practice half, `CLAUDE.local.md`, gitignored at the root of the
engine checkout on the machine this project is operated from, governs how the
deployment runs. **If you have not been given those files, you are working without
the constitution: say so and ask before improvising** — a memory loader loads a
missing file silently, and this repository ran without any `CLAUDE.md` at all for
long enough to prove that silence reads as normal.

`README.md` here is for players and hosts; `CONTRIBUTING.md` is for community
contributors and holds the layout, the community contract, and the release
procedure. Every document has one target reader (engine constitution, audience
separation) — agent material goes here, never into those two.

What follows is only what is true in THIS repository and not derivable from the
engine's text.

- **`campaigns/` IS the content here.** In the engine repository the same name is
  a gitignored dev symlink with zero tracked files — so a constant copied from an
  engine tool that names a path, a directory or a file kind is **re-derived here,
  never carried**. One carried skip list removed 27 tracked files, every campaign
  stage document among them, from pin discovery and a verb enumeration, and
  nothing was red or could have been: the counts were truthful about a smaller
  world than the tool claimed to cover (`.github/pins.toml` `admit-ref` and
  `tools/check-vendored.py` both record it).

- **This repository holds no engine code; the engine revisions it is judged,
  built and AUTHORED by are pins.** All three live in the registry
  `.github/pins.toml`, held to their policies by `tools/check-pins.py`:
  `admit-ref` (site: `.github/workflows/prefab-audit.yml`) names the engine
  commit the NBT audit is built from; `engine-release` (site: `versions.toml`
  `[engine].ref`) names the tagged engine release a delve image is built and
  validated with; and `engine-authoring` (site: `versions.toml`
  `[engine].authoring_ref`) names the engine a creator builds their own
  toolchain from at `/new-delve` Init step 2. They are deliberately different
  and are never collapsed — a released delve must reproduce through an engine
  that never moves, while an author needs the engine the pipeline was last
  walked against, which is neither the newest release nor the default branch.
  `tools/check-authoring-pin.py` holds the last of the three to the two things
  pin discovery structurally cannot see: that the skill page READS the pin, and
  that the revision string lives in `versions.toml` and nowhere else (markdown
  is prose to pin discovery, and a skill page is not prose — it is a procedure
  somebody executes). When judging a red, ask which
  revision the **job** builds, not only which tree you were handed — a stale pin
  manufactures false reds that look exactly like content defects, and this
  repository has produced one: a zone reported red against a rule that no longer
  existed upstream, where the natural "repair" was to build the thing the stale
  gate asked for.

- **Vendored files are byte-for-byte copies of engine files and are never edited
  here.** The registry's `vendors` keys name them — today `tools/check-pins.py` —
  and `tools/check-vendored.py` holds each to the bytes at the pinned revision,
  plus a refusal when the upstream source has moved since review. A local fix to
  a vendored file is the drift the checker exists to catch: fix it in the engine
  and re-pin.

- **A released or accepted campaign is never edited to satisfy a new engine** —
  when it stops building, the finding is a fence defect in the engine. The
  complement is an obligation: **a campaign that has not been released adopts**
  the current engine, and its red under a new obligation is an adoption item on
  the campaign. So the triage question comes before the diagnostic is read: has
  this campaign been released or accepted? Engine surfaces are tested against the
  engine's own gallery, which lives in the engine repository and is never
  released or staged — a campaign here is never the engine's test surface.
  (Engine constitution, "A released campaign is never the engine's test
  surface".)

- **An in-progress campaign lives on its own `campaign/<id>` branch and
  everything of it lands there** — design of record, prefabs, stage documents,
  localisation sidecars, generation logs. Sort a file by **which artifact it
  belongs to**, never by what kind of file it is: if abandoning the campaign
  would delete it, it is the campaign. The branch reaches `main` once, after
  acceptance; `.github/required-status-checks.toml` (`protect-campaign-branches`)
  is the binding.

- **`.nbt` prefabs are git-lfs objects** (`.gitattributes`). A checkout without
  LFS materialises text pointers, and the audit fails to parse them — a tool
  reading such a tree is reading the wrong instrument.

- **English-first and privacy apply here by name**: no artifact in this
  repository — campaign `GENERATION.md` logs included — records personal
  information or who decided something or when (engine constitution,
  Conventions, which names this repository's generation logs explicitly).

- **`tools/tests` is stdlib `unittest`, no install step, deliberately** — it must
  run on a creator's clone with nothing installed. The command CI runs:
  `python3 -m unittest discover -s tools/tests -t tools/tests`.
