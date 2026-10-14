# The Thing Across the Water — design record

The demo level for **a shot frames its subject** (spec-0110): every cutscene
shot names what it shows, and the build proves the subject is in the frame, in
sight, present, sent and drawn. One mechanic in the spotlight, one character,
about ten minutes.

## The place

A grey bay at dusk on an ocean horizon.

| place | what it is | where |
|---|---|---|
| `node/jetty` | a stone jetty, 5 wide and 24 long, railed along both sides, a bell on a post at its north end | the entry; runs north from the hall's door |
| `node/hall` | the harbour hall: one long room under a pitched roof, its wide door (3 × 3) open onto the jetty, the keeper's desk against the back wall facing the door | south of the jetty, its door the seam |
| `node/stack` | a sea-stack: a rock pillar out of the bay, its flat top twelve courses above the deck. Scenery (`reached: false`): seen, never entered | ninety blocks north of the bell |

## The figure

The thing across the water is an assembly of block displays (`assembly/the-thing`,
the library's `rig/tentacle`): a limb of thirty-four segments that rises out of
the stack's top and stands twenty-five blocks over it, leaning toward the
jetty. It is spawned by the bell's beat, rising from inside the rock, and
stays standing for the rest of the delve.

## The beats

1. **At the door** (`obj/at-the-door`, a `reach-anchor` three steps out from the
   hall's door). Cutscene **the keeper**: the camera stands on the jetty outside
   the open door and looks in at the keeper behind his desk. Subject
   `{"npc": "npc/keeper"}`.
2. **Hear the keeper** (`obj/hear-the-keeper`, `talk-to`). He tells the party
   to walk to the end of the jetty and look at the stack, and that the bell is
   there to be rung.
3. **The end of the jetty** (`obj/jetty-end`, a `reach-anchor` under the bell).
   Cutscene **the bay**, two shots: an establishing shot gliding out over the
   water, declared `"landscape"`; then a slow pass near the stack, subject
   `{"place": "node/stack"}`, aimed at its top.
4. **Ring the bell** (`obj/ring-the-bell`, an `interact` whose prop is the
   bell). In one effect list: `spawn-assembly` (the figure, playing `rise`),
   then cutscene **it rises**: the camera on the jetty behind the bell, looking
   across ninety blocks of water at the stack while the figure rises. Subject
   `{"assembly": "assembly/the-thing"}`; its `view_range` is the one the build
   derives.
5. **Tell the keeper** (`obj/tell-the-keeper`, `talk-to`). The delve ends.

## Refusals kept beside it

Each is the primary plus one declared edit, and each transcript is printed by
the same binary that builds the level:

| edit | code |
|---|---|
| the bay's stack shot aimed twenty blocks up (sea and sky) | `DW1033` |
| the keeper framed from beside the door, through the hall's wall | `DW1033` |
| the figure's `spawn-assembly` moved after its cutscene | `DW1034` |
| the bell's camera backed to two hundred blocks off, under `view_distance: 20` | `DW1034` |
| the keeper shot with its `subject` deleted | `DW0199` |

## Branches and endings

None. One ending, in the hall.
