# Delvewright Campaigns

Campaign **sources** for [Delvewright](https://github.com/stellarfeline/delvewright)
delves — the staged DSL documents from which every delve is deterministically
rebuilt, byte for byte. This repo is content; the pipeline that compiles it lives
in the main repo (GPL). Licensing is directory-scoped: `campaigns/` is
**CC BY-SA 4.0** (see LICENSE); `prefabs/` items carry per-item licenses
(CC0 / CC BY / original) recorded in their metadata.

## Layout

```
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
