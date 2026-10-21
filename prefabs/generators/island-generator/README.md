# Island set-piece generator — provenance record

`src/main.rs` is the program that wrote the pieces below.

It is a **provenance record** (engine ADR-0018 §6): the program, kept so a
reader can see how the pieces were made. The pieces are the data; this is not
their source of truth. Nothing in this repository builds or runs it, and it
gates nothing.

It last built at engine revision `5bd35334f2dc9600a12d7fd1132d3a6480edbdb4`
(`stellarfeline/delvewright`), where it lived at `prefabs/island-generator` as a member of
that revision's `prefabs/` cargo workspace (`prefabs/Cargo.toml`,
`prefabs/Cargo.lock`), with the shared `prefab-invariants` crate
(`prefabs/invariants`) and a path dependency on `delvewright-dsl`. It does not
compile here: its manifest names that workspace. Run at that revision into an
empty directory, it wrote the 2 island set pieces, `island-beach-camp` and `island-galley` (`../../island-*.nbt` + `.json`); the `.nbt` it wrote are byte-identical to those committed here (sha256, 2 of 2).

Its source is kept exactly as it was, so every path below is a path in the
engine repository at that revision. Licence: GPL-3.0, the engine's.

`../island-tileset.md` describes the set.

## The generator's own notes, as they stood

Deterministic generator for the island remake's **set pieces** (spec-0013): the
sea-level entry `island-beach-camp` and the showcase `island-galley` (an ancient
Greek galley moored offshore). A **sibling** of `prefabs/cave-generator` — its own
`[workspace]`, outside `crates/`, so it never enters the shipped `delvec` binary
and no other tileset's `.nbt` changes (ADR-0006). It reuses the cave-generator
primitives (splitmix64 + trilinear value noise, the structure-NBT writer with
`mtime` pinned to 0, keep-socket geometry, the gravity-substrate invariant).

```sh
# from repo root — writes island-*.nbt + island-*.json into the content library
cargo run --manifest-path prefabs/island-generator/Cargo.toml -- campaigns/prefabs/
```

Byte-identical on every run (double-run hash-checked). Both pieces are open-air,
sky-lit island scenery, not enclosed rock:

- **`island-beach-camp`** (21×15×44) — sand shore rising from a ragged tide line;
  a campfire ring with log benches (the relight fixture), two wool/fence A-frame
  tents, a barrel supply stack, a lantern class post, and driftwood / rock /
  seagrass greeble. One inland `island:socket` (floor_y=2) to greenfield. The
  piece extends south into authored ocean where **the galley hull is stamped in,
  moored just offshore**, reached by a bounded jetty + a walkable **gangplank**
  (spruce treads on oak-fence piles) that climbs from the sand (y=3) to the deck
  (y=5). Anchors: `entry`, `anchor/camp-fire`, `anchor/class-post`,
  `anchor/crew-a`, `anchor/crew-b`, `anchor/surf-wave`, `anchor/gangplank`,
  `anchor/deck`, `anchor/prow`.
- **`island-galley`** (9×15×29) — a flared plank hull with a dark waterline wale,
  a ram + stempost prow, a curled aphlaston stern, oar rows (spruce trapdoors +
  button ports), a single mast with a white-wool square sail, and the apotropaic
  **eye (ophthalmos)** on both bows. Standalone set-piece, one `anchor/deck`.
  `build_galley` authors this hull once; `island-beach-camp` reuses it via
  `stamp_solids`, so this artifact's output is byte-identical to before the merge.

See `../island-tileset.md` for the shared island convention (waterline y=2, walk
plane y=3, `island:socket` floor_y=2), the flood-safety rationale, and the
merged-vs-separate galley decision that the terrain worker's greenfield/mountain
pieces must adopt.
