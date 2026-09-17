# Vesperhold — design record

The authoritative design of this campaign. Every later round is judged against it.

## The hidden story (never shown whole)

The great bell of Vesperhold, the Vesper, rang at every dusk. Its ringing kept the Undertide — a grey tide of forgetting that rises from under the castle's rock — asleep. The bell took its price from whoever rang it: each dusk the bell-warden forgot one more day of their own life.

Warden Ilse Hesk rang it for thirty years. By the end she could not remember her own daughter, Tamsin, who was her apprentice. On the day now called the Last Vesper, Tamsin struck the bell with a smith's hammer to spare her mother the next ringing. The Vesper cracked; its tongue fell through the tower floor into the undercroft. That dusk the Undertide rose.

The court forgot itself instead of one woman. The guards still walk their rounds without remembering what they guard. King Oswin forgot his own name and kept only his last order — hold the watch, keep the gates shut — and he has kept it for ten years, because he is right: the Undertide stays inside Vesperhold only while the castle stays shut.

Tamsin, grown, keeps a fire at the foot of the causeway and hires strangers to go in. She tells them the castle is cursed. She does not tell them who cracked the bell.

What the party can learn, and where (each fact is placed at least twice):

| fact | where it is told |
|---|---|
| the bell took the ringer's memory | the Warden's Ledger (scriptorium); Warden Hesk's own words in the memory |
| Tamsin cracked the bell | young Tamsin's hammer in the remembered stair; the Ringer Unmade drops a smith's hammer; Tamsin's last dialogue if asked |
| the king's watch is what holds the Undertide in | the King's dying words; the Ledger's last page; Ser Halvard's oath |
| the Undertide eats names | blank nameplates in the barracks; the Unremembered Guard's items; Brother Pellam forgetting his own lie |

## Brief constraints honoured

- Dark-souls-like combat, exploration and a cryptic main plot, in one huge Gothic castle with regions and a spectacular exterior.
- More than twenty designed places (26), about half of Stormveil Castle in structure (5 regions plus a memory wing, 3 rest points, 1 gatekeeper, 1 mid-boss, 1 final boss, 1 optional elite, 3 shortcuts, a front gate and a side route).
- Up to four players, co-op, 60+ minutes (`target_minutes` 80).
- A second timeline, ten years earlier, as a **memory wing** (see below).

## Regions and places

Floors (datums): valley 64, causeway 76, castle 80, keep dais 84, rampart 92, belfry 108, undercroft 68.

| region | place | size | floor | what the player does there |
|---|---|---|---|---|
| Approach | Wayside Shrine | room 12×12, open | 64 | spawn; **Causeway Fire** (rest point 1); Tamsin hires the company |
| Approach | Pilgrim Road | road 8×44, open | 64 | the walk in; the castle's silhouette over the valley; the road climbs at its north end |
| Approach | Hanging Causeway | road 8×40, open | 76 | a bridge over the valley floor; vista of the keep and the bell tower |
| Approach | Barbican | hall 24×16, roofed | 80 | **gatekeeper: the Porter**; the portcullis to the ward is shut; the postern to the west is locked |
| West cliffs | Postern Ledge | corridor 32×4, open | 80 | the side route out along the cliff face |
| West cliffs | Cliff Stair Path | corridor 4×36, open | 80 | the ledge turns north; archers above |
| West cliffs | Stables | room 24×12, roofed | 80 | ambush: the grooms who forgot the horses died |
| Ward | Outer Ward | arena 40×40, open | 80 | the plaza; five ways out; the portcullis winch (**shortcut 1** back to the barbican) |
| Ward | Barracks | hall 20×16, roofed | 80 | a fight; the blank nameplates |
| Ward | Armory | room 12×12, roofed | 80 | optional loot; a false chest (mimic) |
| Ward | Keep Steps | room 12×8, roofed | 80 | the sealed Keep Doors — "they open to the bell" |
| Cathedral | Cloister Garth | hall 32×32, open | 80 | **Cloister Fire** (rest point 2); Ser Halvard keeps his first watch here |
| Cathedral | Chapel of Hours | hall 24×20, tall | 80 | the tall mirror that remembers; the way into the memory wing |
| Cathedral | Scriptorium | room 16×16, roofed | 80 | the Warden's Ledger; the Psalter Wall (illusory — strike it) |
| Undercroft | Psalter Niche | alcove 8×8 | 80 | behind the illusory wall; the stair down |
| Undercroft | Crypt of Wardens | hall 24×24 | 68 | the wardens' tombs; **optional elite: the Last Warden-Knight**, kneeling until struck |
| Undercroft | Undertide Pool | arena 32×32 | 68 | the source; a lethal well of grey water; **the Drowned Choir** guards the fallen bell-tongue |
| Undercroft | Well-House | alcove 8×8 | 80 | stair up from the pool; **shortcut 2** opens into the cloister |
| Memory | Mirror Passage | corridor 4×24 | 80 | through the mirror; the sky turns to a clear noon ten years ago |
| Memory | Remembered Hall | hall 24×20 | 80 | the court intact, the morning of the Last Vesper; Warden Hesk, who does not know her daughter |
| Memory | Remembered Stair | room 12×12 | 80 | young Tamsin with the hammer; the Warden's Key, taken out of the memory |
| Heights | East Rampart | road 8×96, open | 92 | the long wall walk north; archers and a volley trap |
| Heights | Watch Tower | room 12×12 | 92 | Brother Pellam's stall; Ser Halvard's second watch |
| Heights | Buttress Walk | corridor 48×4, open | 92 | high over the keep roofs; the Warden's Door at its west end opens only to the key from the memory |
| Heights | Bell Tower Stair | room 16×16, tall | 92 | the climb |
| Heights | Belfry | hall 16×16, open | 108 | **mid-boss: the Ringer Unmade**; hang the tongue, ring the cracked Vesper once |
| Keep | Great Hall | hall 28×24, tall | 80 | the Unremembered Guard; the Almoner's Door (**shortcut 3** to the cloister) |
| Keep | Antechamber | room 16×12 | 84 | **Throne Fire** (rest point 3); Ser Halvard's fate |
| Keep | Throne Hall | arena 32×32, tall | 84 | **final boss: King Oswin, who kept the watch**; the last choice |

## The route

Shrine → road → causeway → barbican (Porter) → postern ledge → cliff path → stables → outer ward → cloister (fire) → scriptorium (ledger, illusory wall) → niche → crypt → Undertide Pool (tongue) → well-house (shortcut) → cloister → chapel → mirror → remembered hall → remembered stair (key) → back → ward → east rampart → watch tower → buttress walk → Warden's Door → bell tower → belfry (Ringer, ring the bell; the Keep Doors open) → ward → keep steps → great hall → antechamber (fire) → throne hall (King) → the choice.

Loops: the portcullis (ward ↔ barbican) folds the whole approach back to the Causeway Fire; the well-house door folds the undercroft back to the Cloister Fire; the Almoner's Door folds the keep back to the Cloister Fire.

## The memory wing — how the second timeline works

The engine has no timeline primitive, and the design does not pretend otherwise. The memory wing is a real, walkable wing behind the Chapel of Hours' mirror, built as the court was ten years ago. Crossing into it cuts the sky from `dusk` + `rain` to `noon` + `clear`; crossing back cuts it back. Sky is world-wide, so while anyone is in the memory the whole castle is under the remembered noon — the fiction owns that ("while one of you remembers, the castle remembers with you"). One thing is carried out of the memory: the Warden's Key, and with it the flag that opens the Warden's Door in the present.

No fight happens in the memory.

## Skies

| sky | when |
|---|---|
| `dusk` + `rain` | the present, the whole campaign by default |
| `noon` + `clear` | the memory wing |
| `dawn` + `clear` | ending: the Vesper rings |
| `night` + `thunder` | ending: the long quiet |

## Acts and quests

1. **The Causeway Fire** — Tamsin at the shrine hires the company; the fire is lit.
2. **The Porter** — the gatekeeper in the barbican; it carries the postern key; the postern opens.
3. **The Cliff Path** — along the cliff; the stables ambush; into the ward.
4. **The Cloister Fire** — the second fire; Ser Halvard keeps his watch; he asks for news of his king.
5. **The Warden's Ledger** — the scriptorium; the ledger; the Psalter Wall gives way to a blow.
6. **Beneath the Psalter** — down through the crypt to the Undertide Pool; the Drowned Choir; the bell-tongue.
7. **The Mirror of Hours** — Tamsin opens the mirror when she sees the tongue; the memory; Warden Hesk; the Warden's Key.
8. **The Bell Road** — the east rampart, the watch tower, Brother Pellam, the Warden's Door.
9. **The Ringer Unmade** — the belfry fight; the tongue is hung; the Vesper rings once, cracked; the Keep Doors open.
10. **The Keep** — the Unremembered Guard in the Great Hall; the Throne Fire; Ser Halvard's fate.
11. **The King Who Kept the Watch** — King Oswin.
12. **The Last Vesper** — Tamsin at the throne; the choice.

## Branches and endings

| point | opens at | branches | leads to |
|---|---|---|---|
| Halvard's oath | quest 8, at the watch tower | *tell him the king is gone* — Halvard lays down his oath and leaves the castle alive; *let him keep it* — he goes ahead of the party into the keep and is found dead at the Throne Fire, his sword across the doorway | both converge at quest 10 |
| The last vesper | quest 12, at the throne | **Ring**: Tamsin takes the warden's rope; the Vesper rings at dawn; the court wakes remembering; Tamsin will forget the company by nightfall | `ending/the-vesper-rings` |
| | | **Silence**: the tongue goes into the Undertide; the castle lets its watch end; the company walks out under thunder while Vesperhold forgets it was ever a place | `ending/the-long-quiet` |

Neither ending is labelled good.

## Souls elements

- Three rest points with the full rest-and-refill contract; enemies return on rest.
- A death leaves your **Tallow** where you fell; die again first and it is gone.
- Tallow is a currency; Brother Pellam sells for it and lies about what he sells.
- A gatekeeper before the castle proper, a front gate that is a shortcut and a side route that is the real way in.
- An illusory wall on the main path, hinted twice (the ledger, the cracked psalter shelves).
- A false chest, a volley trap on the rampart, a lethal well in the Undertide Pool.
- A dormant optional elite that stands up only when struck.
- A recurring ally whose fate turns on one choice.
- A trickster merchant.
- Lore told in items, rooms and fragments, never whole.

## Capability gaps (said, not faked)

- **No timeline primitive** — answered by the memory wing above.
- **No party-size scaling** — the engine never scales a fight by party size. Fights are tuned for a party of two to four at `normal`; a solo player will find the bosses long.
- **No fighting ally** — every NPC is inert, so Ser Halvard never fights beside the party.
- **No fleeing treasure mob** — left out.
