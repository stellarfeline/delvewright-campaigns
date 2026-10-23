# Generators — provenance records

Each directory here is a program that wrote pieces of the library one level up
(`../`), kept beside them as their provenance record (engine ADR-0018 §6): never
built or run by this repository, never a gate. The pieces are the data. Each
directory's `README.md` says what it wrote and the engine revision it last built
at. The tileset descriptions are `keep-tileset.md`, `cave-tileset.md` and
`island-tileset.md`.

A new piece is a grammar program (`delvec grammar`), not a new generator.
