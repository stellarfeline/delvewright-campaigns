# Assembly-rig generator — provenance record

`src/main.rs` is the program that wrote the pieces below.

It is a **provenance record** (engine ADR-0018 §6): the program, kept so a
reader can see how the pieces were made. The pieces are the data; this is not
their source of truth. Nothing in this repository builds or runs it, and it
gates nothing.

It last built at engine revision `5bd35334f2dc9600a12d7fd1132d3a6480edbdb4`
(`stellarfeline/delvewright`), where it lived at `prefabs/rig-generator` as a member of
that revision's `prefabs/` cargo workspace (`prefabs/Cargo.toml`,
`prefabs/Cargo.lock`), with the shared `prefab-invariants` crate
(`prefabs/invariants`) and a path dependency on `delvewright-dsl`. It does not
compile here: its manifest names that workspace. Run at that revision into an
empty directory, it wrote `rigs/tentacle/rig.json`, the tentacle rig (spec-0082). That rig is not on this repository's `main`: it is committed at `prefabs/rigs/tentacle/rig.json` on the `campaign/stranding` and `demo/the-reaching-arm` branches, and the file it wrote is byte-identical to the one on `campaign/stranding` (sha256).

Its source is kept exactly as it was, so every path below is a path in the
engine repository at that revision. Licence: GPL-3.0, the engine's.
