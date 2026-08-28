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
.claude/skills/new-delve/SKILL.md   # the authoring procedure, run from this directory
campaigns/<campaign-id>/
  world.json  npcs.json  classes.json  quest-plan.json  quests.json  dialogue.json
  GENERATION.md        # prompt, date, dsl_version, notable decisions
prefabs/               # the shared building-block library (.nbt + metadata, git-lfs)
```

Clone this repo and you have the complete authoring environment: every existing
prefab is reusable by any campaign, and a **new prefab ships in the same PR as
the campaign that needs it**. The prefab library now lives in `prefabs/`
(migrated from the main repo in M3); the deterministic generators that produce
those pieces stay in the main repo (GPL code), and their outputs are committed
here. `.nbt` files are tracked with git-lfs (see `.gitattributes`) — clone with
git-lfs installed.

Build any campaign with the main repo's `delvec`. **`--prefabs prefabs` is not
optional here.** The flag defaults to `campaigns/prefabs`, which is where the
library sits when the compiler is run from a main-repo checkout; standing in
this repository that path resolves to nothing and the run exits 10 with
`internal error: cannot read prefabs dir campaigns/prefabs` — which reads as a
broken compiler and is not one. It is a global option, so it goes before the
subcommand:

```
delvec --prefabs prefabs build campaigns/<id> -o out/
```

## Contribution rules (the community contract)

- **Sources only.** Campaign submissions are the DSL documents above — plain,
  reviewable JSON validated by a closed schema. **No images, no worlds, no
  binaries, ever** — canonical images are built only by trusted CI from these
  sources (determinism makes the build reproducible by anyone).
- Campaigns must compile in CI before merge. Every push and pull request runs
  `delvec validate` and a full `delvec build` (which implies `analyze`) for every
  campaign in this repo, in every language it declares, against the engine pinned
  in `versions.toml` — so a campaign that no longer compiles is red here, not
  discovered at release time. Run exactly what CI runs, before you push:
  `python3 tools/campaign-build.py --delvec <path to delvec>`, or
  `--discover-only` to see which campaigns it finds without building them. The
  runtime half of the ladder (PackTest and a bot playthrough against the shipped
  image) runs on a release tag; see *Releasing a campaign* below.
- Only distributable-class prefabs (this repo's `prefabs/`, per-item CC0/CC BY/
  original with recorded provenance) may be referenced. Prefab additions pass a
  mechanical NBT audit in CI (block-palette allowlist; no command/structure
  blocks, no NBT-bearing spawners; and what the world will settle — stair runs
  and fluid). Run it yourself before you open anything, with the same command CI
  runs: `python3 tools/prefab-audit.py --bin <path to delve-admit>`. It finds
  every `.nbt` in the repository by walking it, so a piece in a directory nobody
  anticipated is audited too, and it prints what it examined. Campaigns using
  user-local assets are for private play and don't belong here.
- **The engine you author with is named, not assumed.** `versions.toml`
  `[engine].authoring_ref` is the engine revision `/new-delve` Init builds your
  toolchain from; the page reads it from there and never restates it, so
  `versions.toml` is where that revision is written. Anywhere else it stands has
  to be a file `.github/pins.toml` declares as some pin's site — a revision
  pasted into a page or a script drifts the first time the pin moves, and
  nothing would report it. Editing the pin means editing its entry in
  `.github/pins.toml` too. Run the check yourself with the same command CI runs:
  `python3 tools/check-authoring-pin.py`. It needs no network and nothing
  installed.
- All content you submit is licensed CC BY-SA 4.0 and must be your own or
  compatible.
- **Touching a workflow means saying what it gates.**
  `.github/required-status-checks.toml` records which CI jobs block a merge and
  on which refs, and `tools/check-required-contexts.py` holds that file, the
  workflows, and the live rulesets in lockstep — so a renamed job reds on the
  pull request that renamed it instead of blocking every future one, and a job
  that gates nothing reds instead of looking green. Run it yourself with the
  same command CI runs: `python3 tools/check-required-contexts.py`. Add
  `--offline` with no network; it prints which comparison it skipped.

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
