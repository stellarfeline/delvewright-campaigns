# The Reckoning — design record

A demo level for spec-0108: an ending reads the whole run, and the world after
the ending is the world the ending said it left. One mechanic in the spotlight,
about ten minutes, two speaking parts.

## The place

The Tallyhouse, a small stone shrine standing in the bed of Wend Mere, which is
drained once a year. Four places, all on one floor (the mere bed, y 64):

| place | what it is | what happens there |
|---|---|---|
| `node/mere-bed` | the dry mud in front of the shrine door | arrival; where the party stands after the burning |
| `node/porch` | a low stone hall under a bell beam | the callbell hangs here (thread 1) |
| `node/cell` | the house's cell, off the porch on the left | Tobin Reave is chained here (thread 2) |
| `node/sanctum` | the back room: altar, ledger stand, cold brazier | the keeper; the ledger (thread 3); the reckoning |

## The beats

1. **The summons** (mandatory). The party comes in off the mud and finds
   Ysolde Marrow in the sanctum. She says what the house is, and asks them to
   walk it before she reckons it: the bell, the man in the cell, the ledger.
   She says each is theirs to do or not.
2. **The bell** (elective, a deed). The callbell in the porch. Ringing it calls
   the valley down to the mere to hear the reckoning. A `use` trigger, once.
   Writes `flag/bell-rung` and `state/tally` +1.
3. **The cell** (mandatory talk, a said choice). Tobin Reave asks to be let
   go. *Free him*: he takes the pin out of his chain and walks out of the
   house (`flag/tobin-freed`, `state/tally` +1). *Leave him*: he stays
   (`flag/tobin-left`). The one declared branch point.
4. **The ledger** (elective, an optional quest, a deed). The ledger of the
   valley's debts lies open on its stand beside a cold brazier. Laying it in
   the brazier burns it: the stand is left empty, the brazier lit.
   Writes `flag/ledger-burned`.
5. **The reckoning** (mandatory finale). The party tells Ysolde they are done.
   She speaks one line per thread, saying what they did with it, then her
   verdict; the camera holds on the sanctum, and when it returns the house is
   what the verdict made it.

## The endings

`state/tally` counts the people the party answered for: the valley called by
the bell, the man let out of the cell (0, 1 or 2). The ledger is the deed that
overrides the tally.

| ending | gate | verdict | aftermath, when the camera returns |
|---|---|---|---|
| `ending/the-house-burns` | `flag/ledger-burned` | the debts are gone, and she will not keep a house with nothing in it to keep | the party (and Ysolde) stand out on the mud before the door; fire fills the sanctum floor |
| `ending/the-house-stands` | no `flag/ledger-burned`, `state/tally` at least 1 | the house did some good this year, so it stands another | the party stands in the sanctum; the altar candles are lit |
| `ending/the-house-floods` | no `flag/ledger-burned`, `state/tally` at most 0 | the house called no one and freed no one; the mere may have it | the party stands in the sanctum with the mere's water over the floor |

Every ending's final scene reads four inputs, all written outside the finale
quest: `state/tally` (the bell: did; the cell: said), `flag/ledger-burned`
(finished), `flag/bell-rung` (did), `flag/tobin-freed` (said). The campaign
declares `endings_read: {at_least: 3, deeds_at_least: 2}`.

The keeper's epilogue lines, one per thread, are the siblings of the endings in
the final scene, each gated on its thread's input:

| thread | if done | if not |
|---|---|---|
| bell | the valley came down to the mere to listen | nobody came down; the valley heard nothing |
| cell | Tobin went home to his farm | Tobin is still in his cell |
| ledger | the ledger is ash in the brazier | the ledger is still on its stand |
