# Z7 钟塔 — review set

Judged against `../../concept/z7-bell-tower.jpg`.

## What this set no longer depicts

**Every image here was rendered from a 41x48x125 expansion, and the program
refuses that region.** `shots.json` records `size: [41, 48, 125]`; `zones.json`
declares `[41, 50, 125]`, and expanding the current program at 48 courses fails
outright — `no alternative of rule "zone_plan" applies`, because the tower needs
`base_height + storeys + belfry_run = 48` courses of shaft with the ground split
under them. So the reproduce command at the foot of this page reproduces
nothing, and no image here can be re-taken as it stands.

The zone rose two courses so its foot stands on the rock rather than in the sea.
Every eye camera in the set moved with it, and the set was taken before it:

| image | camera when taken | the same anchor now |
|---|---|---|
| `eye-belfry_bay` | `11,33,94` | `11,35,94` |
| `eye-bell_mouth` | `20,32,94` | `20,34,94` |
| `eye-bell_walk` | `14,32,94` | `14,34,94` |
| `eye-boss` | `22,25,94` | `22,27,94` |
| `eye-broken_flight` | `14,7,97` | `13,9,97` |
| `eye-louvre_1` | `22,19,86` | `22,21,86` |
| `eye-ramp_foot` | `20,1,0` | `20,3,0` |
| `eye-ramp_head` | `20,7,65` | `20,9,65` |
| `eye-ringing_floor` | `22,13,94` | `22,15,94` |
| `eye-ruin_cell_4` | `35,2,14` | `35,4,14` |
| `eye-shortcut_foot` | `20,7,84` | `20,9,84` |
| `eye-stair_landing_1` | `14,8,101` | `13,10,101` |
| `eye-tower_foot` | `22,7,94` | `22,9,94` |

Thirteen of thirteen. `ext-nw`, `ext-se`, `ext-sw`, `top` and
`anchor-bell_mouth` frame the whole zone, so all five are two courses out too.

## What the belfry-deck repair adds on top of that

The deck stopped roofing the cell the last step-up is taken from, which is what
joined the belfry to the tower (`../../GENERATION.md`, Z7). It removes five floor
cells — `x 12..16, y 33, z 95` — so the stair opening is one cell longer at the
head of the climb. **It moves no camera**: all thirteen anchors above are
identical before and after it. The one anchor it does move,
`anchor/belfry-stairhead`, is the one this set deliberately carries no shot for.

Shot by shot, and the last column separates what is measured from what is read
off the geometry:

| image | the repair in frame | why |
|---|---|---|
| `eye-bell_walk` | **yes, and it is the change this shot is about** | stands `14,34,94` facing south with 30 cells clear; the five removed cells are the floor at `z 95`, one cell ahead and one below the feet. The lane now begins at the lip of the stair opening |
| `eye-belfry_bay` | **yes** | stands `11,35,94` facing east across the room; the opening lies one cell south of the sight line and two below the eye, in the lower right of a 70 degree frame |
| `anchor-bell_mouth` | **yes** | a downward oblique whose subject is the belfry in section, so the deck and its opening are the floor of the picture |
| `top` | **yes, if the cutaway band takes the deck** | a plan of the tower draws the opening as a hole; it is now one cell longer |
| `eye-bell_mouth` | no | stands `20,34,94` facing **north**; the opening is at `z >= 95`, behind the camera |
| `ext-nw`, `ext-se`, `ext-sw` | a sliver at most | the belfry is arcaded, so a slant view sees some deck through the openings; the silhouette does not move |
| the nine climb shots | no | every one stands below `y 33`, and none of them looks at the deck from underneath |

**The stone re-tiles, and that is not a geometry change.** Five fewer cells
shift the mix draw, so 7 298 cells keep their solidity and take a different
member of the same mix, plus 91 cells of rubble scatter at `y 9..11` re-draw in
the rear ward — **none of it inside the tower footprint**. All of it lies at
`z >= 84`, so `eye-ruin_cell_4`, `eye-ramp_foot` and `eye-ramp_head` stand in
untouched ground, and the nine interior shots see the same stone in a different
order. Mix membership, proportions and every wall line are unchanged.

**So this set is owed a re-render for the two-course rise regardless, and the
repair does not add a shot to that list — it changes what four of them show.**

**A camera in this set is a declared anchor.** The shot plan is the instrument's:
four exterior three-quarters, a plan cutaway, one surroundings view per anchor,
and one eye-level view per anchor, looking the way that anchor faces. Nothing
aims a camera by hand, so **the way to get an eye on a thing is to declare an
anchor at it** — and the anchors below were placed for the campaign first and
chosen as cameras second, which is why a few of them photograph a wall and say so.
Three anchors declared after this set was taken have no camera in it yet; the last
section names them.

There is **no square-on elevation of any face** anywhere in the set. Every
exterior camera sits on a corner bearing and the only level camera stands inside
the piece, so the west front is judged from `ext-nw`/`ext-sw` at a slant and from
`eye-ramp_foot` in perspective. That is the whole of what this engine can
photograph.

## Read these first

| image | camera | what it is for |
|---|---|---|
| `eye-ramp_foot.png` | at the foot of the ramp, 20,1,0, facing south, 18 cells clear | **the zone's own composition** — the cobbled way climbing between collapsed low buildings with the tower at the head of it, the bell hanging in the open belfry. The anchor stands 120 blocks back because a level 70° eye reaches about 0.7 × its distance above itself: from the ramp *head* the same camera photographs the doorway and not the tower |
| `eye-belfry_bay.png` | in the belfry's west arcade bay, 11,33,94, facing east, 29 cells clear | **the bell.** Ten courses of oxidised copper flaring 3 → 5 → 7 across, hung from the timber head-frame, seen across the walk-around from the far side of the room. This is the shot that decides whether Mercy is a structure or a fitting |
| `eye-bell_mouth.png` | standing under the bell, 20,32,94, facing north | the underside of the casting overhead, four courses of clear headroom, and the arcade beyond. A body stands *inside* the tower's namesake |
| `eye-bell_walk.png` | in the west walk lane, 14,32,94, facing south, 30 cells clear | the lane between the bell and the arcade — whether the belfry is a room walked around the bell or a shelf it sits on |

## The climb, in the order a body meets it

| image | camera | what it is for |
|---|---|---|
| `eye-ruin_cell_4.png` | inside a ruined building beside the way, 35,2,14, facing north | the collapsed low buildings are entered, not looked at: each terrace of the ramp carries one, and each has a doorway onto the way |
| `eye-ramp_head.png` | at the ramp head, 20,7,65, facing south, 37 cells clear | the last approach, where the tower stops being a silhouette and becomes a wall |
| `eye-shortcut_foot.png` | in the tower's arched door, 20,7,84, facing north, 84 cells clear | the shortcut at the tower's foot, photographed the way it is used — looking back down the whole street it saves |
| `eye-tower_foot.png` | in the entry hall, 22,7,94, facing north | the foot storey, with the fallen courses heaped along its side walls |
| `eye-broken_flight.png` | at the break, 14,7,97, facing north, 4 cells clear | **the broken first flight**, from the wrong end: the treads at its foot are gone and what is left climbs four courses and stops |
| `eye-stair_landing_1.png` | on the first foot landing, 14,8,101, facing north | the well the stair switchbacks up, and the arrival level of a flight |
| `eye-ringing_floor.png` | on the ringing floor, 22,13,94, facing north | the storey the rope comes down to. The chain hangs in the anchor's own column, so it is above this camera rather than in front of it |
| `eye-louvre_1.png` | on the louvre stage, 22,19,86, facing east, 5 cells clear | a timber sound-board standing floor to ceiling between the racks |
| `eye-boss.png` | on the stairhead floor, 22,25,94, facing north, 8 cells clear | the last storey below the belfry, left clear because a fight happens on it |

## Massing

| image | camera | what it is for |
|---|---|---|
| `ext-nw.png`, `ext-se.png`, `ext-sw.png` | planned exterior three-quarters, yaw 315/135/225, pitch 30 | the silhouette, and the proportion of belfry to shaft |
| `top.png` | planned plan cutaway, pitch 90 | plan only: the tower square in the ward, the way running out of it |
| `anchor-bell_mouth.png` | surroundings view on the bell, yaw 45, pitch 55 | the belfry in section — the head-frame beams over the bell and the arcade around it |

`shots.json` is the authority on every camera: kind, yaw, pitch, field of view,
and for each eye shot the cell the body stands in, how that cell was chosen, and
how many open cells lie ahead of it.

## Two anchors have no useful eye shot, and both are structural

- **`anchor/belfry-stairhead`** is the opening the stair arrives through, so it is
  a hole in the belfry deck. No body stands in it; the renderer steps the camera
  back off the deck into open air and reports zero clearance. The belfry is
  judged from `eye-belfry_bay`, `eye-bell_walk` and `eye-bell_mouth` instead.
- **`anchor/stair-head-1`** is the top of the broken flight, which stops one
  block short of the tower's front wall. Its derived facing is the way the climb
  runs, so it looks into that wall at zero clearance. `eye-broken_flight` is the
  view of the same break from below, which is the one the beat is about.

## Three anchors this set does not photograph

`anchor/tread-stand`, `anchor/tread-lower` and `anchor/tread-upper` are where the
broken flight is repaired (`../../GENERATION.md`, Z7). They are declared for the
campaign, and `shots.json` was taken before them, so the set is three cameras
short. Two of the three could never carry a useful one: `tread-lower` at
`13,11,87` and `tread-upper` at `13,12,86` are cells the way lays, so no body
stands in either — the same reason `anchor/belfry-stairhead` photographs nothing.
`tread-stand` at `13,11,88` is a body's cell with two clear cells ahead of it, the
two courses that are missing and the front wall behind them; that is the shot the
next render pass owes, and it is the view the party has while doing the work,
where `eye-broken_flight` is the view they have while finding it.

## Reproducing the set

```sh
delve-grammar expand --file design/programs/z7-bell-tower.json \
    --region 41x48x125 --seed 1 --traversable --id z7-bell-tower -o out/
delve-render piece out/z7-bell-tower.json -o shots/ --size 900
```

The zone is past the 48-per-axis structure-template cap, so `expand` writes a
**tile set** — three `.nbt` tiles and one manifest — and `delve-render piece`
takes the **manifest**, reassembling the tiles into one scene before any camera
is placed. Every image here frames the whole zone; none of them is a slice.
