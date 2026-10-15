# The Armoury — generation record

## What the brief pinned down

The engine's demo-level queue row for spec-0111 pinned: one room with a rack
of three armour stands (a helmet, a sword, a shield in the off hand), a map in
a glow item frame beside the door, and a chest holding nothing but arrows
under the window; the quest item is the sword, taken from its stand. It is the
first read of whether a player understands, unprompted, that the worn sword is
theirs to take, and of where on a stand players click. Small, one mechanic,
minimum cast. Holders are placed by the piece and owned by the engine;
`loot[]` and `collect` fill them by slot.

## What was invented here

- The fiction: Greyholt, a watch-house on a moor road; Ide Fenwick, its keeper
  for thirty winters, handing the post over to the new watch; the post sword
  that goes with the post.
- A yard in front of the armoury, so the warden has somewhere to stand that is
  not the room the level is about, and the sword has somewhere to be carried
  to.
- Which stand is which: the shield to the north, the sword in the middle, the
  helmet to the south. The frame is east of the door on the door wall; the
  window is in the middle of the north wall with the chest under it.
- One class, the New Watch, carrying a bow and four arrows, so the chest of
  arrows is worth opening and the sword is the one blade in the party's hands.

## Posture note

The level tells the player one thing outright — the sword on the rack is the
post's, and the post is theirs now — and leaves the room to show how a sword
on a stand is taken. Ide never says how to take anything; she says where it
is and whose it is. The end is her walking down the road, not a speech.

## The design gate

Step 4 was not passed: no reference images were drawn and no one approved a
design walkthrough. This is a demo level whose gate is the built level itself;
`design/` and `design.json` do not exist, and no showcase camera is written.
