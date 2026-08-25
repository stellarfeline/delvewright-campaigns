# The Bowl

A demo level for the horizon's surround — the ground a map stands in.

Six small places, one short walk from a sky-open mouth to a sky-open lip, and
**three different amounts of world around them.** The level is the SET of three
builds, not any one of them:

| build | horizon | what a body sees |
|---|---|---|
| void | `"void"` | six boxes hanging in nothing; step off the last floor and fall forever |
| rim 24 | `{base: "valley", rim_height: 24}` | the same six boxes on a floor that runs out to the foot of a low rim |
| rim 96 | `{base: "valley", rim_height: 96}` | the same walk, inside a bowl the sky is a lid on |

**Nothing about the map changes between the three.** Same boxes, same seams,
same route in blocks. What it is for is that a reader can feel how much of a
place is the space around it.

## The map

Plan at grade; east is `+x`, south is `+z`. Region `[0, 48, 0]` extent
`[48, 48, 40]`, and no box may grow past it.

```
        x:  4      11  21          36 38    45
  z:  4     [mouth ]     [ledge ] 24..31, floor 69
             open                  under a 3-cell ceiling
  z: 13     [  court  ]  [   gallery   ]  [lip]
             4..19 open   21..36 floor 64  38..45
             floor 64     ceiling 8        open
  z: 30     [cistern] 8..15, floor 60, ceiling 7
             a sunken room off the court
```

Six places, five ways between them: two arches at grade, one east arch out to
the lip, a stair up out of the gallery to the ledge, and a stair down out of the
court into the cistern. The cistern carries no beat on purpose — a place off the
mandatory spine is what makes the critical path say something.

The walk: the mouth, the court where the Warden stands, the gallery, up to the
ledge, back down, and out east onto the lip. 97 blocks of route over five legs,
measured over the built blockout.

## The exhibit

Two scripts, both run from the root of this repository. Neither leaves the
campaign edited — every perturbation is made and put back.

```
python3 campaigns/the-bowl/exhibit/three-builds.py \
    --delvec <path to delvec> --repo . --out <somewhere>

python3 campaigns/the-bowl/exhibit/refusals.py \
    --delvec <path to delvec> --repo .
```

### Three builds from one document

`three-builds.py` rewrites exactly one field — `content.horizon` — three times,
and measures *nothing about the map changes* three ways whose failure modes are
unrelated:

* **the derivation's own hash.** All three builds print one `blockout sha256`.
* **every emitted file, hashed by content.** 82 shared paths, 76 byte-identical,
  6 differing, and each of the six is read line by line rather than excluded.
  The assertion is not *these paths may differ* — that is a claim about what the
  answer will be — but that the void build's emission SURVIVES INTACT and
  everything a valley build adds to it is ground: template placements, one
  sentinel each, one forceload, four biome bands between two modification-cap
  lines, and a placement count that moves from 0 to exactly the number the
  surround's own binding line states.
* **`critical-path.json`**, which is what the runtime bot walks: one file in all
  three.

Moving `node/mouth` one block east between builds reds the first two, down to
`teleport @s 7 64 7` becoming `teleport @s 8 64 7`. The third stays green under
that perturbation, which is worth knowing about the third.

### The surround binding line

Part of the exhibit, because it names the rectangle **and which authority stated
it** — the whole difference between a landform a later pass can move and one it
cannot.

```
void      no surround line at all
rim 24    85 templates and 4 biome bands around [0, 0]..[47, 39] stated by the
          site-plan region, with 2742 standable gap-floor cells the climb proof
          floods from
rim 96    95 templates and 4 biome bands around [0, 0]..[47, 39] stated by the
          site-plan region, with 2742 standable gap-floor cells the climb proof
          floods from
```

Ten more templates for four times the rim, the same rectangle, the same
authority, and the same number of gap-floor cells to flood from.

### The two refusals

`refusals.py` trips them rather than describing them.

**`DW0855` — a horizon that builds terrain, on a campaign with no map to build
it around.** The same document with its site plan deleted and its `areas[]`
restored. It reads as an odd thing to refuse until you see what the accepted
version would have been: the exhibit builds that same areas-only document under
`horizon: void` and reports where the compiler actually put the two rooms —
`area/near` at x 0 and `area/far` at **x 256**, because areas sit on the
compiler's fixed stride. The union of what they place is 265 x 11 = 2915
columns, of which 202 carry a room. **6.9%.** That rectangle is the extent a
surround would have had to ring, and the rest of it is nothing.

**`DW0854` — a bowl with a way out of it.** The same valley with a staircase
carved up its inner slope by a stage-7 edit: 27 treads, three cells wide, two
cells of air over each, climbing from the gap floor past the crest. The build
comes back:

```
DW0854 [error] build: the surround's inner slope has grown a standable
staircase: a walk starting on the gap floor stands at [-27, 91, 6], outward of
the crest line, so the landform no longer bounds the map.
```

A valley surround requires a site plan, and a campaign carrying a site plan
declares an empty `areas[]` — so its one place is the synthetic `area/site`, and
a stage-7 batch names it the way a batch names any other area. That is what lets
this case be tripped at all: the staircase is carved by an edit script on a
site-plan campaign, and the refusal that answers it is the surround's own.

`refusals.py` exits 0 when both cases reach their own code, and 1 naming the case
that did not — a refusal nobody tripped is not a demonstration.

### What the transcripts beside the scripts are

`three-builds.txt`, `refusals.txt` and `campaign-build-gate.txt` are the output
of those runs at engine revision `4ee0c0e10741cd018e2ba83c93d3ba5af563bc00`.
They are measurements, not specifications: re-running them against another engine
is how you find out whether they still hold, and a difference is a finding about
that engine rather than about this campaign.

## What this campaign needs from the engine it is built with

The horizon's surround is a `dsl_version` 0.16 surface, and this campaign's
`world.json` declares it. The engine every campaign here is built with is
`versions.toml` `[engine].ref`, whose pin policy is `release`: the value must be
a commit a `v<semver>` tag points at, and `tools/check-pins.py` enforces that
rather than assuming it. So **this campaign builds green only once an engine
release carries the surround** — the gate is not something a pin bump can
satisfy early.

Run against an engine that does carry it, the repository's own gate is green
over everything, this campaign included:

```
campaign build gate: 3 of 3 campaign(s) examined, 5 language build(s),
0 directory/ies excluded and named, 0 finding(s)
```

## Walking it

`delvec build` emits a complete joinable delve: the datapack, the server
configuration, and a world generated on first boot with nothing baked into
region bytes. The compiler's own walk proofs are green over the built bytes —
six places proven reached, five critical-path legs measured, and
`validation/critical-path-waypoints.json` showing the climb to the ledge taken
one block at a time.

Joining it, or running the critical-path bot over it, needs a Minecraft server,
and a Minecraft server needs the Mojang EULA accepted. That acceptance belongs
to whoever is running the delve and is read from the environment, never
hardcoded — so it is the one step this campaign's own tooling does not take for
you.
