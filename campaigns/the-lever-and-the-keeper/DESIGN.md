# The Lever and the Keeper — design record

A demo level: one hall, one keeper, one lever, one sign, one two-shot cutscene.
It exists so the review frames drawn by Lumenwright can be confirmed on a level
whose every frame has a known answer.

## Layout

- **The porch** (`node/porch`, the entry): a flagged porch open to the sky in
  front of the Gap House door. The party arrives here.
- **The hall** (`node/hall`): one long stone hall, nine blocks across and
  fifteen deep from the door wall to the far wall, under a timber roof, lit by
  two hanging lanterns. The keeper stands at the far end, facing the door. On
  the west wall, halfway down, is the place the bell lever is set; a lettered
  sign hangs over it.
- **The door** (`edge/hall-door`): a heavy plank door in the hall's south wall,
  barred from inside. It opens when the party comes up to it and is barred
  again behind them once they have greeted the keeper; it stays shut to the
  end.

## Beats

1. **Come to the door** (porch). The bar lifts inside and the door opens.
2. **Greet the keeper** (hall, far end). Bet Ashby explains the gap bell and
   bars the door behind the party.
3. **The lever appears.** The second quest activates, and its `interact`
   objective places the lever on the west wall, under the sign. Before this
   beat the wall is bare.
4. **Ring the gap bell** (hall, west wall). Pulling the lever cuts the time to
   dusk, then plays a two-shot cutscene: a push-in on the keeper, then a still
   wide shot of the hall from above the porch, at dusk.
5. The campaign completes: the house is shut for the night.

## What is looked at

- The POV frame on the lever's leg shows the lever, the sign's letters and the
  keeper, drawn, facing the door, lit by the lanterns' block light.
- The POV frame on the leg before it shows the west wall bare.
- The first cutscene frame stands where the push-in starts and says what it
  shows.
- The second cutscene frame is lit at dusk and names the step that set it.

There are no branches and no endings table: one route, one ending.
