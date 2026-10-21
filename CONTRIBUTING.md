# Contributing campaigns and prefabs

This is the authoring side of the repository. If you came to *play* a delve,
[README.md](README.md) is the page you want.

Campaign **sources** for [Delvewright](https://github.com/stellarfeline/delvewright)
delves — the staged DSL documents from which every delve is deterministically
rebuilt, byte for byte. This repo is content; the pipeline that compiles it lives
in the main repo (GPL). Licensing is directory-scoped: `campaigns/` and
`references/` are **CC BY-SA 4.0** (see LICENSE); `prefabs/` items carry per-item licenses
(original, or an ADR-0013 allowlist licence; see `prefabs/LICENSE-ASSETS.md`)
recorded in their metadata; `prefabs/generators/` is GPL-3.0 code, the engine's.

## Layout

```
versions.toml          # which engine release tag a release of this content is built with
.claude/settings.json  # recommends the marketplace and enables the authoring plugin
campaigns/<campaign-id>/               # every campaign, demo levels included
  world.json  npcs.json  classes.json  quest-plan.json  quests.json  dialogue.json
  GENERATION.md        # dsl_version and the campaign's own decisions, no dates
references/<level-id>/                 # a reference level: how to build one kind of map
  world.json  ...      # its campaign documents, as a campaign's
  README.md            # its storybook, as a campaign's
  HOW-IT-IS-BUILT.md   # how the level is built, for an author
  prefabs/             # its own pieces (.nbt + metadata); it builds with these
  forms/  measure/  review/   # what its pieces are made from, and how they were judged
prefabs/               # the shared building-block library (.nbt + metadata, git-lfs)
  generators/          # the programs that wrote its tilesets: provenance records
demos/<demo>/          # a generation-time surface demonstrated: a grammar
                       #   program, the piece it exports, its reports and its
                       #   refusal transcripts. Never a campaign — a stage
                       #   document does not belong here
```

**Authoring is done through the `delvewright` plugin**, not from a file in this
repository. `/plugin marketplace add stellarfeline/delvewright` then `/plugin
install delvewright@delvewright` puts `/delvewright:new-delve` in Claude Code;
`.claude/settings.json` here recommends the marketplace and enables the plugin,
and Claude Code prints the install command when it is not yet installed. The
page works in any directory, so this repository is one place to author in and
not the only one — you clone it to use the shipped prefab library, or to publish
a campaign here through a pull request, and for no other reason.

Cloned, it is a complete authoring environment: every existing
prefab is reusable by any campaign, and a **new prefab ships in the same PR as
the campaign that needs it**. The prefab library lives in `prefabs/`.
The programs that wrote its tilesets are kept beside it in
`prefabs/generators/`, as provenance records (GPL-3.0 code, never built or run
here); a new piece is a grammar program. `.nbt` files are tracked with git-lfs (see `.gitattributes`) — clone with
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

A reference level builds with its own prefab directory instead, and only with
it — `--prefabs` names one flat directory, so a reference level's pieces are
all in its `prefabs/`:

```
delvec --prefabs references/<id>/prefabs build references/<id> -o out/
```

**A reference level** is a short level that shows how to build one kind of map
— an organic structure the party enters, a giant statue. It is a whole level
in one directory, kept apart from the campaigns in the layout above, in its
release tag, its image name and its release title, and it is held to every
gate a campaign is. A level that demonstrates something other than how to
build a kind of map (a renderer, a check) is not one.

## Contribution rules (the community contract)

- **Sources only.** Campaign submissions are the DSL documents above — plain,
  reviewable JSON validated by a closed schema. **No images, no worlds, no
  binaries, ever** — canonical images are built only by trusted CI from these
  sources (determinism makes the build reproducible by anyone).
- **A campaign is compiled by its author, with the engine that author uses.** Run
  `delvec validate` and a full `delvec build` (which implies `analyze`) over your
  campaign, in every language it declares, against the engine the authoring
  plugin pins, and open the pull request on a campaign that builds. CI does not compile campaigns for you: a campaign is
  built only by the engine it pins, and nothing here owes compatibility to a
  campaign already authored. The runtime half of the ladder (PackTest and a bot
  playthrough against the shipped image) runs on a release tag; see *Releasing a
  campaign* below.
- Only distributable-class prefabs (this repo's `prefabs/`, per-item original or
  ADR-0013 allowlist licence with recorded provenance) may be referenced. Prefab additions pass a
  mechanical NBT audit in CI (block-palette allowlist; no command/structure
  blocks, no NBT-bearing spawners; and what the world will settle — stair runs
  and fluid). Run it yourself before you open anything, with the same command CI
  runs: `python3 tools/prefab-audit.py --bin <path to delvec>`. It finds
  every `.nbt` in the repository by walking it, so a piece in a directory nobody
  anticipated is audited too, and it prints what it examined. Campaigns using
  user-local assets are for private play and don't belong here.
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

## Releasing a campaign or a reference level

A release is a tag on this repo, in one of three families:

```
release/<campaign>/v<major>.<minor>.<patch>                e.g. release/vesperhold/v1.1.0
prerelease/<campaign>/v<major>.<minor>.<patch>-<suffix>    e.g. prerelease/vesperhold/v1.1.0-beta.1
reference/<level>/v<major>.<minor>.<patch>                 e.g. reference/the-beached-thing/v1.0.0
```

Pushing any of them runs `.github/workflows/release.yml`, which builds the level
with the engine release pinned in `versions.toml` `[engine].ref` — the `delvec`
binary that release published, downloaded and checked against the release's
`SHA256SUMS`, never compiled here; a pin that is not a published
`delvec--v<version>` release refuses the run — runs the
full release-tier ladder (PackTest + a complete bot playthrough against the
shipped image), and — only on green — publishes the GitHub Release (with
`resourcepack.zip`) and the multi-arch delve image on GHCR. A red ladder
publishes nothing.

Before the build, the same downloaded binary runs `delvec grammar audit
--campaign-root` over the released level alone (a temp content root holding
it as `campaigns/<id>`), for every family, and refuses the release on a red audit. A
campaign with `design/programs/` must carry a `zones.json` that maps every
program to a region and seed, and every program must pass its gates; a campaign
with no `design/programs/` passes, and the log states a zero binding. To check
before tagging, run the same command with the pinned release's `delvec` against
a root that holds only your level under `campaigns/` (a reference level too). The release obtains that
binary with the engine release's own acquisition script, run from an engine
checkout at the pinned tag: `python3 <engine>/.claude/skills/delvewright/skills/new-delve/scripts/fetch-delvec.py
--pin versions.toml --engine <engine> --into <dir>` does the same on your
machine.

The family decides how it is published:

| | Reads | Builds with | Image | GitHub Release | Image tags |
| --- | --- | --- | --- | --- | --- |
| `release/` | `campaigns/<id>` | `prefabs/` | `delve-<id>` | a Release titled `<title> v<version>` | `v<version>` and `latest` |
| `prerelease/` | `campaigns/<id>` | `prefabs/` | `delve-<id>` | a pre-release, never marked latest | `v<version>` only |
| `reference/` | `references/<id>` | `references/<id>/prefabs/` | `delve-reference-<id>` | a Release titled `Reference level: <title> v<version>` | `v<version>` and `latest` |

A reference level has no pre-release family: a `reference/` tag with a
`-<suffix>` is refused (`REFERENCE_HAS_PRERELEASE`). A campaign id may not
begin with `reference-` (`RESERVED_CAMPAIGN_ID`), because that image name
belongs to a reference level.

The version must match the family for a campaign: a `release/` tag with a `-<suffix>` is
refused (`RELEASE_HAS_PRERELEASE`), and so is a `prerelease/` tag without one
(`PRERELEASE_WITHOUT_PRERELEASE`), before anything is built. Build metadata
(`+...`) is refused in every family. `tools/lib/campaign_tags.py` is the grammar; check
a tag before pushing it with `python3 tools/lib/campaign_tags.py parse <tag>`.

The Release's generated changelog starts from the previous tag of the same
level in semver order: a release looks back through `release/` tags only, a
pre-release through both campaign families, a reference level through
`reference/` tags only. A level's first release carries the storybook blurb
and no generated changelog.
`python3 tools/lib/campaign_tags.py previous --tag <tag>` (tags on stdin, from
`git tag -l`) prints the start tag.

Publish a pre-release through its tag, never by hand: the workflow is what
creates a campaign's GHCR package, and a package created from a workstation is
not linked to this repository, so the workflow cannot push to it afterwards.

`workflow_dispatch` on the same workflow is a **dry run**: it takes a category
(`campaign` or `reference`), a level id and a version, exercises build + ladder
+ multi-arch image build, and skips every publishing step. For a campaign a
version with a `-<suffix>` simulates a pre-release and one without simulates a
release; a reference level takes a version without one. Use it to check a campaign is releasable
without minting anything.
