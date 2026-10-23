# Stone-keep tileset generator — provenance record

`src/main.rs` is the program that wrote the pieces below.

It is a **provenance record** (engine ADR-0018 §6): the program, kept so a
reader can see how the pieces were made. The pieces are the data; this is not
their source of truth. Nothing in this repository builds or runs it, and it
gates nothing.

It last built at engine revision `5bd35334f2dc9600a12d7fd1132d3a6480edbdb4`
(`stellarfeline/delvewright`), where it lived at `prefabs/generator` as a member of
that revision's `prefabs/` cargo workspace (`prefabs/Cargo.toml`,
`prefabs/Cargo.lock`), with the shared `prefab-invariants` crate
(`prefabs/invariants`) and a path dependency on `delvewright-dsl`. It does not
compile here: its manifest names that workspace. Run at that revision into an
empty directory, it wrote the 13 `keep-*` pieces of the library (`../../keep-*.nbt` + `.json`); the `.nbt` it wrote are byte-identical to those committed here (sha256, 13 of 13).

Its source is kept exactly as it was, so every path below is a path in the
engine repository at that revision. Licence: GPL-3.0, the engine's.

`../keep-tileset.md` describes the set.

## The generator's own notes, as they stood

Deterministic generator for the stone-keep prefab tileset. Emits, for each piece,
a gzip-framed vanilla structure `.nbt` and its metadata `.json` into an output
directory. Byte-identical on every run (ADR-0006): fixed iteration order, gzip
mtime pinned to 0, fixed compression level.

The library itself now lives in the **content repo** (`delvewright-campaigns`),
symlinked at `campaigns/` for local dev (spec-0007 Step 0). The generator stays
here (GPL code) and writes its outputs into the content repo's `prefabs/`:

```sh
# from repo root — writes campaigns/prefabs/keep-*.nbt and campaigns/prefabs/keep-*.json
# (campaigns/ is the symlink to the content repo; commit the outputs there).
cargo run --manifest-path prefabs/generator/Cargo.toml --release -- campaigns/prefabs/
```

This is a member of the `prefabs/` workspace, deliberately outside `crates/` —
and excluded by the root workspace — so it is not a member of the engine's
workspace and never enters the shipped `delvec` binary. Every prefab generator
is a member of it, `hello-room` included (`prefabs/hello-room-generator`), and
they share the rule crate `prefabs/invariants` (`prefab-invariants`).

Piece geometry, the connection ("keep-socket-v1") convention, and the live-probed
lighting minimums are documented in `../keep-tileset.md`. `measured_min_light` in
each emitted JSON comes from a live 1.21.11 probe (sealed-doorway block light);
the table in `src/main.rs` (`measured_min`) records those measured values.
