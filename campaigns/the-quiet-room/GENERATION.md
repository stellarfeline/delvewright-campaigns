# The Quiet Room — generation record

## Toolchain

- Built from the engine branch that carries quiet guidance (`feat/quiet-guidance`, the unreleased `dsl_version` every stage document states), against this repository's own prefab library.
- Placement: `areas[]`, one area drawn from `pool/stone-keep` at seven to nine pieces; no campaign-built piece, no site plan.

## What this level is for

It is the demo level for quiet guidance: a delve in which the on-screen guidance the engine can give is switched off, every act sits on a real object, and the machine proofs still bind. One small keep shows, in order:

- **a real lever beside a closed gate** — the first objective is an `interact` with a lever `prop` at the warden's empty stand, under `guidance.markers: hidden`: no lantern, no title, no line; the player sees a lever by a shut gate and pulls it, vanilla reports the flip (`default_block_use`), and the gate lifts. The lever is self-evident, so nothing names it;
- **a bell the journal names** — the second objective is an `interact` with a bell `prop` in the side room, the one announced beat of the level (`announcement: shown`, a title and a hint: *Past the gate, a bell stands in the side room*). The bell does not explain itself, so the journal restates what the room shows. Ringing it is vanilla's own act, and its completion spawns the watch around the bell;
- **an untitled kill found by the party** — the `kill` that waits on the bell has no title and no hint; its wave forms up on the bell's own anchor, within the wave's reach of the hand that rang it, which is the second way the engine accepts a fight (`DW0863`);
- **a checkpoint set by approach** — passing through the gatehouse, the one way in, sets the respawn point there; the no-stranding proof roots it where the party can first reach the trigger. It stands on the route every life takes, so a death in the side room comes back to the gatehouse and walks the opened gate again;
- **two talk beats in a row** — the Keeper's two options sit in one node; the second is drawn only once the first is heard, because the button obeys the objective's `after`.

Text comes from the Keeper and from the one journal line. Nothing in the level exists to be read in order to open something.

## Decisions

- The lever stands before the gate, at the gate room's empty stand (`anchor/keeper-stand`), and the bell behind it in the side room (`anchor/wave`), which is also where the watch forms up; so the proven route pulls, then rings, then fights.
- The Keeper has withdrawn to the great hall (`anchor/boss`), the one piece-unique stand behind the gate; the gatehouse's inner cell (`anchor/exit`) is the checkpoint.
- The wave is three zombies named *The Watch*; no `follow_range` is declared, so the engine's default reach is the one it is held to.
- English only. A quiet delve has one line to translate, and the demo is about what is not on screen.
