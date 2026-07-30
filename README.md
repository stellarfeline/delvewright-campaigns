# Delvewright Campaigns

Campaign **sources** for [Delvewright](https://github.com/stellarfeline/delvewright)
delves — the staged DSL documents from which every delve is deterministically
rebuilt, byte for byte. This repo is content; the pipeline that compiles it lives
in the main repo (GPL). Everything here is **CC BY-SA 4.0** (see LICENSE).

## Layout

```
campaigns/<campaign-id>/
  world.json  npcs.json  classes.json  quest-plan.json  quests.json  dialogue.json
  GENERATION.md        # prompt, date, dsl_version, notable decisions
```

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
- Only distributable-class prefabs (the main repo's library) may be referenced.
  Campaigns using user-local assets are for private play and don't belong here.
- All content you submit is licensed CC BY-SA 4.0 and must be your own or
  compatible.
