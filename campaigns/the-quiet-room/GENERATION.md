# The Quiet Room — generation record

## Toolchain

- Built from the engine branch that carries quiet guidance (`feat/quiet-guidance`, the unreleased `dsl_version` every stage document states), against this repository's own prefab library.
- Placement: `areas[]`, one area drawn from `pool/stone-keep` at seven to nine pieces; no campaign-built piece, no site plan.

## What this level is for

It is the demo level for quiet guidance: a delve in which every form of on-screen guidance the engine can give is switched off, and the machine proofs still bind. One small keep shows, in order:

- **an unmarked interact** — the slate on the far wall of the entry hall is an `interact` with no `prop` under the campaign's `guidance.markers: hidden`; no lantern glows over it, and reading it is what opens the gate;
- **no chrome** — `guidance.announcements: hidden` and no objective carries a `title`, so nothing is printed when a beat begins or ends; the story moves in the narrated lines the acts themselves produce;
- **a fight started by a use, with an untitled kill** — the lever in the side room is a `use` trigger standing on the wave's own anchor, so the watch comes up within the wave's reach of the hand that pulled it; the `kill` objective that waits on it has no title and no hint and is still found by the party, which is the second way the engine accepts;
- **a checkpoint set by approach** — walking up to the warden's empty stand sets the respawn point there; the no-stranding proof roots it where the party can first reach the stand, not at the entry;
- **two talk beats in a row** — the Keeper's two options sit in one node; the second is drawn only once the first is heard, because the button obeys the objective's `after`.

## Decisions

- The slate stands before the gate and the lever behind it, and the lever is gated on having read the slate, so the proven route pulls the lever after the gate is open rather than at the earliest possible step.
- The Keeper has withdrawn to the great hall (`anchor/boss`), the one piece-unique stand behind the gate; the gate room's stand is empty and is the checkpoint.
- The wave is three zombies named *The Watch*, seated around the lever's anchor; no `follow_range` is declared, so the engine's default reach is the one it is held to.
- English only. A quiet delve has little to translate, and the demo is about what is not on screen.
