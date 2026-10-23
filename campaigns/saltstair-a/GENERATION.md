# Saltstair, variant A — generation record

## Toolchain

- `/new-delve` plugin 1.14.0; engine release `delvec--v1.14.0` (`e51f8bbef8c3a3b58caea451b5f9898b15b00509`); `delvec 1.14.0, dsl 0.56.0, mc 1.21.11`, the release archive `delvec-v1.14.0-x86_64-unknown-linux-gnu.tar.gz` (sha256 `8dad85c5fc80f1cc8cc0dba4e2cee6523e73a3aee36eecfcd8bd2af996130db3`).
- Prefab library: this clone's `prefabs/`, at the revision that carries this directory; the engine's `[content].sha` is `3d8b343dbcb9f44c267da77fa2a31f1c47e8957e`, an ancestor of it.
- The engine constitution's operating half, `CLAUDE.local.md`, was not available to this run; the run decides nothing about dispatch, review, merge or staging.

## What the brief pinned, and what this campaign invented

Pinned, verbatim from `campaigns/hillside/DESIGN.md` §2–§6: the region, the heightmap and its fill, the horizon and boundary, the nineteen places and their extents, floors, headroom and roofs, the eighteen seams, the materials, the light rule, the six cameras, the walk and the five numbers. Pinned by the run's brief: cut A, the id `saltstair-a`, `demo_level: true`, one program per box, the six cameras drawn at day.

Invented: the seed (`20261022`), the title line, the horizon's music (silence — the design states none), the quest's wording.

## Open items

- `world.time`: the design states "late afternoon"; the DSL's sky vocabulary has no position between the sun `high` and the sun `setting` (its disc on the western horizon). The documents carry `day` as a marked placeholder until the owner rules.

## Refusals, in order

Every `DW` refusal `delvec` printed during authoring, with its repair.

| # | Run | Code | What it said | Repair |
|---|---|---|---|---|
| 1 | step 1, validate | DW0874 | classes.json, quest-plan.json, quests.json absent | stubbed the three |
| 2 | step 1, validate | DW0112 | `quest-plan` names `area/site` and the campaign has no placement authority yet | step 2 writes the site-plan pipeline, whose one area is `area/site` |
| 3 | step 1, validate | DW0150 | the planned quest has no stage-5 expansion | the ordinary state until step 5; `quests.json` expands it |
