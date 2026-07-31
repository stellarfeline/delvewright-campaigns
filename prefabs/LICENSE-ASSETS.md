# Prefab & content asset licensing

This file states the licensing boundary for creative assets, per **ADR-0007**
(monorepo; GPL code, separately-licensed content) and the CLAUDE.md forbidden
zones.

## In-repo prefab assets

Prefab assets committed to this repository (`prefabs/**`) must carry an
**ADR-0013 allowlist** license: **original, CC0, CC BY, MIT, Apache-2.0, or a
GPL-3.0-compatible license (incl. LGPL-3.0)**. **CC BY-NC / ND / ShareAlike or
unknown-license material is never ingested** — the `delve-admit` catalog-card
license check enforces this. The source and license of every asset are recorded
in that asset's prefab metadata (`prefabs/<id>.json` `license` block) and its
catalog card (`catalog/<id>.json`), so provenance is auditable at all times.

### Third-party attribution

External prefabs ingested through the `delve-admit` pipeline (spec-0007), with
the license verified via the source's API **and** project page:

| Prefab(s) | Source | Author | License |
| --- | --- | --- | --- |
| `hero-galleon-oak` | [Ships](https://modrinth.com/datapack/ships) (Modrinth) | EMD123 | Apache-2.0 |
| `hero-temple-ruin-hall`, `hero-temple-ruin-arch` | [Moss Ruins](https://modrinth.com/datapack/moss-ruins) (Modrinth) | LordGacie | MIT |
| `hero-standing-monolith` | [Little Structures](https://modrinth.com/datapack/little-structures) (Modrinth) | MatBayern | LGPL-3.0-only |

Full provenance (download URL, retrieval date, sha256 of the original download,
source path within the datapack) lives in each prefab's metadata and catalog
card.

## Generated delve content

Generated campaigns and worlds are **not** stored in this repository. They ship
separately — via GitHub Releases / the OCI registry — and are distributed under
**CC BY-SA 4.0** (ADR-0007). The pipeline code in this repo is licensed under
GPL-3.0-or-later (see root `LICENSE`); the license boundary is a directory
boundary.
