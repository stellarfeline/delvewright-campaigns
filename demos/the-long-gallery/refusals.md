# Refusals beside The Long Gallery

Each is `campaigns/the-long-gallery` plus one edit, built by `delvec` at engine revision `a9b1e259` against this branch's prefab library. The refusal is the build's own line, verbatim.

## The jog removed

The edit: every bay's two baffles replaced by open courses, so the gallery is one straight hall.

Exit status 3.

```text
DW0948 [error] build: loop `loop/the-gallery`: the interact objective `obj/ring-the-bell` at anchor `anchor/gallery-end` stands at [2, 65, 25], inside the loop's periodic span [0, 64, 0]..[4, 68, 26] — a body has an identity the move cannot repeat, so a body moved a bay back would see the same figure twice, or none. Move the body out of the span; a figure that appears mid-loop is placed by an `on_cross` effect outside the visible cells, or summoned after the release
```

## A lantern missing from the landing bay

The edit: the lantern of bay 1, the bay a crossing lands in, left out.

Exit status 3.

```text
DW0946 [error] build: loop `loop/the-gallery`: 1 visible cell(s) of the periodic span differ from the cell each is seen as from the slab, in the configuration the world as it is placed, before any runtime write — [2, 67, 11] holds `minecraft:air` and [2, 67, 17] holds `minecraft:lantern[hanging=true,waterlogged=false]`. The view from the landing would not be the view from the slab. Make the two sections the same; never shorten the view to hide the difference
```

## A lamp round the corner

The edit: glowstone set into the east wall of bay 0's two open courses, behind the bay's east baffle.

Exit status 3.

```text
DW0946 [error] build: loop `loop/the-gallery`: the visible cell [1, 65, 7] is lit 11 and the cell it is seen as from the slab, [1, 65, 13], is lit 8, at the campaign's darkest reachable sky (15), in the configuration the world as it is placed, before any runtime write — something outside the visible cells lights two sections differently, a lamp round a corner or a hole in the roof over the next bay. Make the sections the same
```

## A slab one cell thick under a fall

The edit: the slab turned on its side, one course thick in y, with the landing one course under it.

Exit status 3.

```text
DW0945 [error] build: loop `loop/the-gallery`: its slab [1, 66, 15]..[3, 66, 17] with offset [0, -1, 0] is not a slab the engine can poll — it is too thin to catch a crossing along y: a one-tick poll sees a body in the slab for a window of t + reach = 1 + 1.8 = 2.8 blocks, and a falling body's limit speed (`metrics::POLL_FALL_BLOCKS_PER_TICK`, the fall law's fixed point) is 3.92 blocks a tick, so a body can pass through between two polls. Thicken the slab to at least 3 cells along y. Reshape the slab or move the landing (`to`).
```
