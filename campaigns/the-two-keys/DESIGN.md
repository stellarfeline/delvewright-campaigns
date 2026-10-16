# Two Keys — design record

The demo level for party-shared progression (spec-0018), from its row in the
engine's `docs/demo-levels.md`: a two-player vault where progression is
provably split — `carrier: one` items and AND-join objectives — and which one
player can still finish alone (`min_players` is left at its floor of 1).

## The place

The Staple Hall at Marrowby, a guild hall of stone with plank floors, in one
row west to east:

- **The archive** (west wing) — the Clerk's room: shelves of rolls, a lectern,
  and the Clerk's key in its box on the west wall.
- **The hall** (entry) — the great room. The strongroom door stands barred in
  the middle of the north wall, with a lock plate either side of it: the
  Warden's lock to the east, the Clerk's lock to the west. The steward, Hesketh
  Marr, keeps his post by his table in front of the door. A plain doorway in
  each side wall leads to a wing.
- **The counting room** (east wing) — the Warden's room: a counting table, a
  strongbox, and the Warden's key on its hook on the east wall.
- **The strongroom** — behind the hall's north wall: a low stone room with the
  charter chest against its north wall.

## The beats

One quest, `quest/the-charter`:

1. **Meet the steward** (talk-to, the hall). Hesketh explains the rule: two
   keys, two rooms, and the keeper of the door may hold neither.
2. **Two arms, each its own room, both open once the steward has spoken:**
   - *The Warden's arm* — take the Warden's key from its hook in the counting
     room (`give-item`, `carrier: one`: the key goes to the one player who took
     it), then turn it in the Warden's lock (an `interact` that needs the
     Warden's key **held** in the main hand).
   - *The Clerk's arm* — the same in the archive, with the Clerk's key and the
     Clerk's lock.
   The two keys are different items (a trial key and an ominous trial key), so
   each lock answers only to its own key.
3. **Open the strongroom** (talk-to, the hall) — the AND-join:
   `after: [obj/turn-the-warden-lock, obj/turn-the-clerk-lock]`. Hesketh draws
   the bolts only once both locks are turned, by anyone; the strongroom door
   opens (`open-gate`) and the flag `flag/strongroom-open` is set.
4. **Take the charter** from the chest in the strongroom (collect).
5. **Bring the charter** to Hesketh (talk-to). The campaign completes.

With two players the natural division is one wing each; one player alone
walks both wings in turn. Nothing forks: there is no branch and one ending.

## The party mechanic, as built

- Every progression score is the party's (`#party`), so one player's lock
  advances both players' journal.
- A key is one copy, in the inventory of whoever took it; the other player
  receives nothing. A key can be handed over by dropping it.
- The join is proven on a server by the generated two-dummy
  `party_join_obj-open-the-strongroom` PackTest: shut with no lock turned,
  still shut after one, open after both, and the successor completed by the
  player who did not turn the first lock.
