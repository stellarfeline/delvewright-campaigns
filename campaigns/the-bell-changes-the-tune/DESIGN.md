# The Bell Changes the Tune — design

The demo level for **a scene states its music** (spec-0109): every place and
the ground say what they play, silence included; a story stage moves the music
by repainting a place; a cut is a verb; a cutscene declares what it hears and
the build confirms it. Music is judged by ear, so this level exists to be
listened to.

## The place

A walled churchyard at dusk with a small stone chapel on its north side. Grid:
x east, z south; the walk plane is y 64. Horizon `void`.

| place | box | carries | what it is |
|---|---|---|---|
| `node/yard` (entry) | x 8184–8207, z 8200–8219, open | `atmosphere/yard` | the churchyard: lychgate in the south wall where the party arrives, a flagstone path straight north to the chapel door, leaning headstones either side, the old yew in the north-east corner |
| `node/chapel` (goal) | x 8193–8199, z 8186–8198, roofed | `atmosphere/chapel` | one nave: an arched doorway in the south front, pews either side of the aisle, the passing bell on its floor frame on the altar step at the north end |

The yard's last row (z 8200) and the chapel's first (z 8198) sit in different
biome cells (8200–8203 and 8196–8199), so the two places carry two skies with
nothing shared between them: the doorway is the threshold where the music
changes.

## What each place plays

| biome | declares | a playing track, on entering |
|---|---|---|
| `atmosphere/yard` | `music.overworld.meadow`, 2400–6000 ticks between pieces, no replace | plays out |
| `atmosphere/chapel` | silence (`{}`), `music_volume` 0.0 | fades over about fifteen seconds |
| `atmosphere/dread` | `music_disc.11`, no gap, replaces | is cut, and the disc loops back to back |
| the ground (`horizon`) | silence (`{}`) | plays out (no camera stands in it) |

## The beats, in order

| # | act | kind | where | music it moves |
|---|---|---|---|---|
| 1 | go into the chapel | `reach` | chapel | walking in under the roof: the yard's track fades |
| 2 | ring the passing bell | `interact`, bell prop | chapel | `set-atmosphere` paints the yard with `atmosphere/dread` |
| 3 | go back out among the stones | `reach`, the yew | yard | stepping out: the dread replaces whatever was still playing; sets `flag/dread-heard` |
| 4 | come back inside | `reach`, open from the moment the party reaches the yew, so its title and hint are on screen for the whole walk back | chapel | the approach trigger just inside the door (`anchor/threshold`, range 1), armed by `flag/dread-heard`, carries `stop-sound {category: music}`: the dread stops at the door instead of fading on inside; the beat's own completion carries the same `stop-sound`, so the music is stopped before the ending whichever fires first |
| — | ending | `cutscene`, `hears: atmosphere/dread` | camera over the yard | the camera stands in the dread: the disc comes back |

## Hour and weather

Dusk, clear. No mob is fielded, so the burning hour decides nothing. The
yard is lit by sixteen lanterns on posts and the nave by five hanging lanterns
and the altar candles, placed with the room (`design/build_pieces.py --light`
prints a rough estimate; the build's dark-cell proof is the judge).

## How the map is made

`design/build_pieces.py` writes the two place programs under `programs/`;
`delvec detail campaigns/the-bell-changes-the-tune --all` freezes them as the
pieces `prefabs/the-bell-changes-the-tune-yard` and `-chapel`. Two headstones
were moved off the churchyard wall and the yew's foot, where the leave-proof
found a body could climb onto the wall from them and drop out into the open
ground beyond (`DW0921`).
