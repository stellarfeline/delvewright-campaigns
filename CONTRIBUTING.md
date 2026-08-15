# Contributing campaigns and prefabs

This is the authoring side of the repository. If you came to *play* a delve,
[README.md](README.md) is the page you want.

Campaign **sources** for [Delvewright](https://github.com/stellarfeline/delvewright)
delves — the staged DSL documents from which every delve is deterministically
rebuilt, byte for byte. This repo is content; the pipeline that compiles it lives
in the main repo (GPL). Licensing is directory-scoped: `campaigns/` is
**CC BY-SA 4.0** (see LICENSE); `prefabs/` items carry per-item licenses
(CC0 / CC BY / original) recorded in their metadata.

## Layout

```
versions.toml          # which main-repo commit a release of this content is built with
campaigns/<campaign-id>/
  world.json  npcs.json  classes.json  quest-plan.json  quests.json  dialogue.json
  GENERATION.md        # prompt, date, dsl_version, notable decisions
prefabs/               # the shared building-block library (.nbt + metadata, git-lfs)
demos/<demo>/          # a demo level: one mechanic, its own piece, its review shots
catalog/               # catalog cards
tools/                 # the checks CI runs, runnable on your own machine
```

A `.nbt` is audited wherever it sits — the list above is where pieces happen to
live today, not where the audit looks.

Clone this repo and you have the complete authoring environment: every existing
prefab is reusable by any campaign, and a **new prefab ships in the same PR as
the campaign that needs it**. The prefab library now lives in `prefabs/`
(migrated from the main repo in M3); the deterministic generators that produce
those pieces stay in the main repo (GPL code), and their outputs are committed
here. `.nbt` files are tracked with git-lfs (see `.gitattributes`) — clone with
git-lfs installed.

Build any campaign with the main repo's `delvec`:

```
delvec build campaigns/<id> -o out/
```

## Contribution rules (the community contract)

- **Sources only.** Campaign submissions are the DSL documents above — plain,
  reviewable JSON validated by a closed schema. **No images, no worlds, no
  binaries, ever** — canonical images are built only by trusted CI from these
  sources (determinism makes the build reproducible by anyone).
- Campaigns must pass the full validation ladder (`delvec validate` + `analyze`,
  PackTest, bot playthrough) in CI before merge.
- Only distributable-class prefabs (this repo's `prefabs/`, per-item CC0/CC BY/
  original with recorded provenance) may be referenced. Prefab additions pass a
  mechanical NBT audit in CI (block-palette allowlist; no command/structure
  blocks, no NBT-bearing spawners). Campaigns using user-local assets are for
  private play and don't belong here.
- All content you submit is licensed CC BY-SA 4.0 and must be your own or
  compatible.

## Auditing pieces on your own machine

The palette audit that gates a piece is `tools/prefab-audit.py`, and CI runs
nothing else. Build `delve-admit` from the pipeline repo — the source build is
always available and is the guarantee; a prebuilt binary is only a convenience —
and point the script at it:

```
git clone https://github.com/stellarfeline/delvewright
cargo build --manifest-path delvewright/Cargo.toml \
  -p delvewright-admit --bin delve-admit --release

python3 tools/prefab-audit.py \
  --bin delvewright/target/release/delve-admit
```

Use the commit named by `ADMIT_REF` in `.github/workflows/prefab-audit.yml` to
run exactly the rules CI applies.

### What gets audited

Every `.nbt` in the repository, wherever it is. The script walks the working
tree and the directories it finds are an **output** of that walk, printed on
every run — there is no list of audited directories to keep up to date, and no
flag to narrow the walk. Put a piece in `prefabs/`, in a demo folder, or in a
directory that does not exist yet, and it is audited on the run it appears.

The one thing the walk finds and does not audit is a file **git will not
carry**, because such a file cannot reach a merge: build output under `out/`,
or another repository checked out inside this one. The test is git's index, not
`.gitignore` — a piece you commit and *then* add to `.gitignore` stays tracked,
so it stays audited. Whatever is left out is printed by name with the reason.

### What a unit is

The script audits one **unit** at a time. A prefab that fits under the
48-per-axis structure-template cap is one `.nbt`, and that file is the unit. A
zone past the cap ships several `.nbt` plus one metadata `.json` carrying a
`structure_set`, and there is no single `.nbt` at all: for that zone the
**manifest is the unit**, and the tool reads every tile it names and returns
one verdict over the whole zone. Handing it one tile instead is refused,
because a verdict over a fifth of a building reads as a verdict about the
building.

So every audited `.nbt` is either a unit of its own or a tile named by exactly
one manifest beside it, and the script fails if that accounting does not close
— a tile no manifest claims, a manifest naming a file that is not there, a file
git tracks that is missing from the tree, or a repository it found no piece in.

### The binding count

Every run ends with the roots it discovered, the units examined in each, and
the total number of `.nbt` files the walk found. Those figures come from the
walk and from git separately, so they can disagree — and a disagreement is red.
Read them: a piece you just added and cannot see in that count is a piece the
audit did not judge.

## Releasing a campaign

A release is a tag on this repo:

```
release/<campaign>/v<semver>
```

Pushing it runs `.github/workflows/release.yml`, which builds the campaign with
the main-repo commit pinned in `versions.toml` `[engine].ref`, runs the full
release-tier ladder (PackTest + a complete bot playthrough against the shipped
image), and — only on green — publishes the GitHub Release (with
`resourcepack.zip`) and the multi-arch delve image on GHCR. A red ladder
publishes nothing.

`workflow_dispatch` on the same workflow is a **dry run**: it takes a campaign
id and a version, exercises build + ladder + multi-arch image build, and skips
every publishing step. Use it to check a campaign is releasable without minting
a release.
