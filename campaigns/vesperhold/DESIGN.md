# Vesperhold — design record

The authoritative design of this campaign. Every later round is judged against it.

## The one standing requirement

The castle's exterior is designed, block by block, and reads at least as well as the Doune Castle site in this repository: dressed and weathered stone, crenellated walls, pitched slate roofs, towers that read against the sky, and the ground it stands on. No part of the castle is left as massing.

## The hidden story (never shown whole)

The great bell of Vesperhold, the Vesper, rang at every dusk. Its ringing kept the Undertide — a grey tide of forgetting that rises from under the castle's rock — asleep. The bell took its price from whoever rang it: each dusk the bell-warden forgot one more day of their own life.

Warden Ilse Hesk rang it for thirty years. By the end she could not remember her own daughter, Tamsin, who was her apprentice. On the day now called the Last Vesper, Tamsin struck the bell with a smith's hammer to spare her mother the next ringing. The Vesper cracked; its tongue fell through the tower into the undercroft. That dusk the Undertide rose.

The court forgot itself instead of one woman. The guards still walk their rounds without remembering what they guard. King Oswin forgot his own name and kept only his last order — hold the watch, keep the gates shut — and he has kept it for ten years, because he is right: the Undertide stays inside Vesperhold only while the castle stays shut.

Tamsin, grown, keeps a fire at the foot of the causeway and hires strangers to go in. She tells them the castle is cursed. She does not tell them who cracked the bell.

**The past is heard, not visited.** The cracked Vesper still hums. Where its shards lie, the castle remembers: for the length of an echo the sky over Vesperhold is the clear noon of the Last Vesper's morning, and the people of that morning stand in the room again, in the same place, saying what they said. Then the rain comes back and they are gone. No one leaves the present; the present remembers around them.

What the party can learn, and where (each fact is placed at least twice):

| fact | where it is told |
|---|---|
| the bell took the ringer's memory | the Warden's Ledger (scriptorium); Warden Hesk's own words in the chapel echo |
| Tamsin cracked the bell | the tower-stair echo (the girl and the hammer); the Ringer Unmade drops a smith's hammer; Tamsin's last dialogue if asked |
| the king's watch holds the Undertide in | the King's dying words; the Ledger's last page; Ser Halvard's oath |
| the Undertide eats names | blank nameplates in the barracks; the Unremembered Guard's items; Brother Pellam forgetting his own lie |

## Placement

One area, `area/castle`, bound to one campaign-built piece, `prefab/vesperhold`: the whole site — valley floor, approach, crag, castle and undercroft — as one grammar program generated from `design/programs/`. A `valley` surround rings it. Piece axes: x east, y up, z south; the approach is the south end.

## The site

The layout of record is `design/programs/castle/layout.py`; the generator and the layout chart both read it.

The side route runs from the postern in the barbican's south face, west of where the causeway meets it, west along a shelf under the south curtain, round the crag's south-west corner, north along a shelf under the west curtain, and in at the stables' west door. A gap of open air keeps the shelf from the causeway.

Heights (feet): valley floor 8, crag top and castle floor 24, keep dais 28, wall walks and tower rooms 36, bell deck 52, undercroft 12. The crag stands sixteen blocks over the valley floor with sheer faces on the south and west.

| region | place | what the player does there |
|---|---|---|
| Approach | Wayside Shrine | spawn; **Causeway Fire** (rest 1); Tamsin hires the company |
| Approach | Pilgrim Road | the walk in across the valley floor; the whole castle over the crag |
| Approach | Causeway Stair | an open flight on an arcaded ramp, sixteen blocks up to the bridge deck |
| Approach | Hanging Causeway | a bridge on piers over the valley floor to the gatehouse |
| Approach | Barbican | **gatekeeper: the Porter**; the portcullis to the ward is shut; a postern in its south face opens onto the shelf |
| West cliffs | Postern Ledge | a shelf outside the south curtain, the drop to the valley on one side |
| West cliffs | Cliff Path | the shelf turns north along the crag's west face, under archers on the wall |
| West cliffs | Stables | the long stable block on the crag's west edge; spear-armed grooms among the undead horses |
| Ward | Outer Ward | the hub; the portcullis windlass against the gatehouse wall beside the gate (**shortcut 1**) |
| Ward | Barracks | a fight among bunks with scraped-blank nameplates |
| Ward | Armory | two real chests, each holding one better piece (the Garrison Blade, the Garrison Hauberk); a false chest among them — a trapped chest, the same shape as the real ones — that becomes a shulker and an ambush |
| Ward | Cloister Lane | the walled lane from the ward's north-west corner to the cloister |
| Ward | Keep Steps | the sealed Keep Doors — "they open to the bell" |
| Cathedral | Cloister Garth | **Cloister Fire** (rest 2); Ser Halvard's first watch; the well-house; an old dark oak over the lawn |
| Cathedral | Chapel of Hours | the first shard at the altar; **the chapel echo** |
| Cathedral | Scriptorium | the Warden's Ledger; the Psalter Wall (illusory — strike it) |
| Undercroft | Psalter Stair | the stair cut down into the rock behind the wall |
| Undercroft | Crypt of Wardens | **optional elite: the Last Warden-Knight**, kneeling until struck |
| Undercroft | Undertide Pool | a lethal well of grey water with steps up out of it on its north and south, a lamp either side of each; **the Drowned Choir**; the fallen bell-tongue |
| Undercroft | Well-House | the stair up into the cloister; **shortcut 2** |
| Heights | Rampart Stair | the tower up to the wall walk |
| Heights | East Rampart | the long wall walk north; archers, and a pressure plate in the flagstones that looses a volley |
| Heights | Watch Tower | **Watch Fire** (rest 3); Brother Pellam's stall and the anvil at its end; Ser Halvard's second watch and his choice |
| Heights | Buttress Walk | a high walk along the north edge over the keep's buttresses to the Warden's Door |
| Heights | Bell Tower Stair | **Tower Fire** (rest 4), lit when the shard wakes; the climb; the second shard; **the tower echo** |
| Heights | Belfry | **mid-boss: the Ringer Unmade**; hang the tongue, ring the cracked Vesper once; **the belfry echo** |
| Keep | Great Hall | the Unremembered Guard; the Almoner's Door to the cloister lane, barred for good |
| Keep | Antechamber | **Throne Fire** (rest 5); Ser Halvard standing dead in the doorway, if he kept his oath |
| Keep | Throne Hall | **final boss: King Oswin, who kept the watch**; the last choice |
| East side | Chandlery Yard | behind the garden gate: **optional elite: the Chandler**, rendering the dead into tallow; his three hands in the lean-to |
| East side | Spur Passage | a vaulted way under the rampart spur, the yard to the garden |
| East side | Hedge Garden | the parterre and the dry fountain — **the Gilded Bowman** on its plinth, hedge-lurkers in the alcoves behind the walk; the orchard and its gardeners |
| East side | Summerhouse | **optional elite: the Hedge Knight** |

Thirty-three places: twenty-nine on or beside the road, four off it on the east side.

## The route

Shrine → road → causeway stair → causeway → barbican (Porter) → postern ledge → cliff path → stables → outer ward → cloister lane → cloister (fire) → scriptorium (ledger, illusory wall) → psalter stair → crypt → Undertide Pool (tongue) → well-house (shortcut) → cloister → chapel (echo; the Warden's Key) → ward → rampart stair → east rampart → watch tower (fire) → buttress walk → Warden's Door → bell tower (echo; fire) → belfry (Ringer; ring; echo; the Keep Doors open) → ward → keep steps → great hall → antechamber (fire) → throne hall (King) → the choice.

## Off the road

The east side is the castle's off-path pocket, entered by the garden gate in the ward's east wall. Nothing on the road needs it; everything in it is optional, and each optional elite in it drops the piece it fought in.

- **The Chandler** (Chandlery Yard) — a zombie villager with a diamond axe (Sharpness III, Unbreaking II), which he drops. He rises at his vat when the company comes within five blocks of it; the way to the Spur Passage passes the vat at twice that.
- **The Gilded Bowman** (Hedge Garden) — the set piece. A skeleton in gold stands on the dry fountain's plinth, four blocks up, where the terrain holds him: the plinth has no stair, only a ladder on its far face that a body can climb. He is in sight from the walk and draws the company up it; when they reach the fountain, three hedge-lurkers come out of the alcoves they walked past. No telegraph.
- **The gardeners** (the orchard) — three, working the dead rows, back after every rest.
- **The Hedge Knight** (Summerhouse) — a knight in a diamond breastplate (Protection III, Unbreaking II) who keeps a watch nobody set him; he rises in the summerhouse when the company comes within four blocks of it, and drops the breastplate.

With the Last Warden-Knight kneeling beside the road in the crypt, the castle holds three optional elites, each dropping one high-tier piece; the rank and file on the east side return on every rest.

## The echoes

An echo is a `sequence` fired by an interaction at a shard: the sky cuts to `noon` + `clear`, the people of that morning appear where they stood (deferred NPCs and staged actors wearing their faces), they play their moment, and after it the sky cuts back to `dusk` + `rain` and they are removed. Nothing moves the party.

The party keeps control through the chapel and tower echoes and may walk among the figures and speak with Warden Hesk; the belfry echo is a camera cutscene, the only one in the campaign.

1. **Chapel echo** — the court at morning prayers; Warden Hesk reads from her ledger what she has lost and says she is afraid of the day she will not know the girl beside her. She hangs the Warden's Key on the altar hook; when the rain returns, the key is still there — the party takes it.
2. **Tower echo** — the apprentice alone on the stair with the smith's hammer.
3. **Belfry echo** — after the Vesper is rung: the moment of the blow, the crack, the tongue falling; a camera over the castle as the grey rises.

## Skies

| sky | when |
|---|---|
| `dusk` + `rain` | the present, the whole campaign by default |
| `noon` + `clear` | during an echo |
| `dawn` + `clear` | ending: the Vesper rings |
| `night` + `thunder` | ending: the long quiet |

## Acts and quests

1. **The Causeway Fire** — Tamsin hires the company; the fire is lit.
2. **The Porter** — the gatekeeper; its key opens the postern.
3. **The Cliff Path** — the cliff shelf; the stables ambush; into the ward.
4. **The Cloister Fire** — the second fire; Ser Halvard asks for news of his king.
5. **The Warden's Ledger** — the ledger; the Psalter Wall gives way to a blow.
6. **Beneath the Psalter** — the crypt; the Undertide Pool; the Drowned Choir; the bell-tongue.
7. **The Chapel Echo** — Tamsin, seeing the tongue, tells the company to wake the shard at the altar; the echo; the Warden's Key.
8. **The Bell Road** — the rampart, the Watch Fire, Brother Pellam, Halvard's choice, the hired knives, the Warden's Door, the tower echo and the Tower Fire.
9. **The Ringer Unmade** — the belfry fight; the tongue is hung; the Vesper rings once; the belfry echo; the Keep Doors open.
10. **The Keep** — the Unremembered Guard; the Throne Fire; Halvard's fate.
11. **The King Who Kept the Watch** — King Oswin.
12. **The Last Vesper** — Tamsin at the throne; the choice.

## Branches and endings

| point | opens at | branches | leads to |
|---|---|---|---|
| Halvard's oath | quest 8, at the watch tower | *tell him the king is gone* — he lays down his oath and leaves the castle alive; *let him keep it* — he goes ahead into the keep and is found standing dead in the antechamber doorway, sword in hand; his sword is the party's to take | both converge at quest 10 |
| The last vesper | quest 12, at the throne | **Ring**: Tamsin takes the warden's rope; the Vesper rings at dawn; the court wakes remembering; Tamsin will forget the company by nightfall | `ending/the-vesper-rings` |
| | | **Silence**: the tongue goes into the Undertide; the watch ends; the company walks out under thunder while Vesperhold forgets it was ever a place | `ending/the-long-quiet` |

Neither ending is labelled good.

## Souls elements

- Five rest points with the full rest-and-refill contract; enemies return on rest. The Watch Fire stands at the east end of the hired knives' walk and the Tower Fire one flight under the Ringer, so a lost fight is retried from a short, safe walk away.
- A death leaves your **Tallow** where you fell; die again first and it is gone. Tallow is a currency; Brother Pellam sells for it — arrows, a golden apple, an iron spear, a crossbow, a diamond sword, three enchanted books (Smite III, Protection II, Power II) and an iron sword with Smite II — and lies about what he sells. An anvil stands at the end of his counter, so a book goes into a weapon or a piece of armour on the spot.
- Every boss and elite shows a health bar, drawn for a player from the moment they cross into its arena until it falls: the Porter, the Drowned Choir, the Last Warden-Knight, the Chandler, the Hedge Knight, the Ringer Unmade, the Unremembered Guard and King Oswin. The Gilded Bowman is bait and shows none.
- A gatekeeper before the castle proper; a front gate that is a shortcut; a side route that is the real way in.
- An illusory wall on the main path, hinted twice.
- Real chests and a false one in the armory, a volley trap on the rampart, a lethal well in the Undertide Pool with a way out of the water.
- A bait enemy held up by the terrain, covering an ambush from behind (the Hedge Garden).
- Three optional elites off the road (the Last Warden-Knight, the Chandler, the Hedge Knight), each dropping the high-tier piece it fought with.
- A recurring ally whose fate turns on one choice; a trickster merchant.
- Lore told in items, rooms, echoes and fragments, never whole.

## Capability limits (said, not faked)

- **No second space.** The engine's one-area site takes no separate area, and a teleport-only room fails the completability proof; the past is therefore an echo in the present room.
- **Sky is world-wide.** While an echo plays, the whole castle is under its noon; the fiction owns it ("the castle remembers, all of it at once").
- **No party-size scaling.** Fights are tuned for two to four at `normal`.
- **NPCs never fight**, cannot lie down or kneel, and cannot drop a prop on the floor: Halvard's death is shown standing.
- **No riders.** The stables' undead horses are staged, riderless.
- **No custom head blocks** in the campaign documents.
- **No tallow for an ordinary kill.** Tallow comes from story beats; a wave that returns on rest pays nothing when it falls again, because the engine has no per-kill yield. The rank and file off the road are there for the fight, not the purse.
- **The anvil wears out.** Vanilla damages an anvil on use and the engine does not repair it; once broken it stays broken. The stall expects a handful of uses per run.
