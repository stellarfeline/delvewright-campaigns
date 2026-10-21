# Cave/shore tileset generator — provenance record

`src/main.rs` is the program that wrote the pieces below.

It is a **provenance record** (engine ADR-0018 §6): the program, kept so a
reader can see how the pieces were made. The pieces are the data; this is not
their source of truth. Nothing in this repository builds or runs it, and it
gates nothing.

It last built at engine revision `5bd35334f2dc9600a12d7fd1132d3a6480edbdb4`
(`stellarfeline/delvewright`), where it lived at `prefabs/cave-generator` as a member of
that revision's `prefabs/` cargo workspace (`prefabs/Cargo.toml`,
`prefabs/Cargo.lock`), with the shared `prefab-invariants` crate
(`prefabs/invariants`) and a path dependency on `delvewright-dsl`. It does not
compile here: its manifest names that workspace. Run at that revision into an
empty directory, it wrote the 13 `cave-*` pieces of the library (`../../cave-*.nbt` + `.json`); the `.nbt` it wrote are byte-identical to those committed here (sha256, 13 of 13).

Its source is kept exactly as it was, so every path below is a path in the
engine repository at that revision. Licence: GPL-3.0, the engine's.

`../cave-tileset.md` describes the set.

## The generator's own notes, as they stood

Deterministic generator for the cave/shore prefab tileset (the *prefab-ceiling
probe*: can self-created prefabs reach showcase quality via a render-critique
loop?). A **sibling** of `prefabs/generator` (the stone-keep gen): its own
`[workspace]`, outside `crates/`, so it never enters the shipped `delvec` binary
and the keep `.nbt` output stays byte-identical (ADR-0006).

```sh
# from repo root — writes campaigns/prefabs/cave-*.nbt and cave-*.json
cargo run --manifest-path prefabs/cave-generator/Cargo.toml -- campaigns/prefabs/
```

Byte-identical on every run (double-run hash-checked). Three deterministic design
layers, all seeded from a per-piece PRNG + value noise (no wall clock, no unseeded
RNG, no hash-order iteration):

1. **Palette recipes** — weighted multi-block per surface role (wall, floor,
   ceiling, boulder), sampled through a **spatially-coherent value-noise field**
   so blocks cluster into patches (real rock strata / moss) instead of
   salt-and-pepper "tiled noise". A per-cell **edge-distance / height weathering
   bias** (algorithm A1) concentrates mossy + cracked variants near floors and
   walls — a wear gradient, not uniform speckle.
2. **Module grammar + organic shaping** — irregular 2-thick wall lining, a hearth
   (campfire + stone ring), timber sheep pens (fences/gate/hay), a boulder-sealed
   cave mouth. A **4-5-rule cellular automaton** (A8) perturbs the inner wall face
   into alcoves/bumps, and a **silhouette-roughening** pass (A5) erodes the roofline
   crown, chamfers the corners, and divots the outer faces — breaking the box
   outline while leaving every socket byte-identical (roughening only removes shell
   rock, never crosses the AABB, and skips doorway columns).
3. **Detailing / aging** — hanging dripstone stalactites, floor rubble mounds,
   glow-lichen / vine patches, and (shore) a **graded** sand → wet-gravel →
   sand-bottom shallow → stone-bottom sea that laps in from the open front (depth
   grows from the seabed dropping, so there is no vertical wall of water), with an
   irregular inlet tide line, rock scatter, driftwood and seagrass.

Techniques A1/A5/A8 are re-implemented from published description (ideas-only; no
third-party code ingested) — see `docs/ACKNOWLEDGEMENTS.md`.

Sockets reuse keep-socket geometry under the `cave:socket` vocabulary; the
compiler solver reads socket geometry only, so `pool/cave-shore` is a structural
drop-in for `pool/stone-keep`. Lighting is **derived** — a static flood-fill
block-light estimate over walkable floor cells sets `measured_min_light` and the
profile is classified from it (`lit` ≥7 / `dim` 3–6). Firelight pockets are
declared honestly, not hidden. See `../cave-tileset.md` for the piece list and
the render-critique round notes.
