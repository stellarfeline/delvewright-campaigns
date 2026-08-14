# Z2 门楼 — review set

Judged against `../../concept/z2-gatehouse.jpg`.

**The concept is an interior.** An exterior orbit render cannot judge it, so the
set below leads with eye-level views from inside the passage. `ext-se.png` and
`top.png` are here for massing and plan only; neither settles whether the
gatehouse reads.

| image | where the body stands | what it is for |
|---|---|---|
| `eye-look-gate-out.png` | the passage's deep end, looking back at the gateway | the concept's own composition: portcullis, vault, channel, the opening beyond |
| `eye-look-gate-in.png`  | just inside the approach, looking down the passage | what a player sees walking in |
| `eye-look-nave.png`     | mid-passage, looking toward the approach | depth, and the watch bay's mouth |
| `eye-look-drain.png`    | beside the channel, facing the outer wall | the drain mouth, the spur, and the mitred kerbs at the turn |
| `eye-look-ports.png`    | mid-passage, facing the ported wall | the row of openings, and the vault springing over them |
| `eye-watch.png`         | inside the watch bay | what the bay commands |
| `eye-gate.png`          | the gate span | the portcullis at walking height |
| `eye-threshold.png`     | the ambush door beyond the passage | the piece Z2 leaves by |

## Reproducing the set

```sh
delve-grammar expand --file design/programs/z2-gate-ward.json \
    --region 20x10x84 --seed 0 --id z2-gate-ward -o out/
delve-render --size 900 piece out/z2-gate-ward.json -o shots/
```

The region is the zone's own: 20 x 10 x 84, seed 0.

Five of the standpoints are **review standpoints, not campaign anchors**. They
are not declared by the program — the anchor set a campaign binds to is
unchanged — so they are added to the expansion's metadata before rendering:

| name | pos | facing |
|---|---|---|
| `anchor/look-gate-out` | 14, 5, 68 | south |
| `anchor/look-gate-in`  | 15, 5, 80 | north |
| `anchor/look-nave`     | 13, 5, 74 | south |
| `anchor/look-drain`    | 14, 5, 77 | east |
| `anchor/look-ports`    | 16, 5, 76 | west |

An eye camera is level and fixed at Minecraft's own first-person field of view;
it is aimed only by an anchor's `facing`, which is why a standpoint is a piece of
data rather than a command-line flag.

## What the renders cannot show

The passage's approach face is open, and beyond it the renderer has nothing to
draw, so it reads as flat grey. In the assembled world Z1 崖道 stands there, and
that opening is where the concept's daylight and sea come from. Judge the
gateway's shape and proportion here; judge the view through it once the zones
are placed together.
