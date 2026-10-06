# Refusals beside The Long Gallery

Each is `campaigns/the-long-gallery` at campaign revision `ec9954f` plus one edit, built by `delvec` from the engine's integration branch `integration/stranding-capabilities` at `edab67d9`, against this branch's prefab library, with the piece re-expanded where the edit is to the piece. The refusal is the build's own line, verbatim. Coordinates are the world's; the piece stands at the origin with its floor at y 64, so x and z are the piece's own.

## The fog removed

The edit: `atmosphere/close-air` deleted, and `area/gallery` carries no atmosphere.

Exit status 3.

```text
DW0948 [error] build: after world-edits batch `batch/the-bell`: loop `loop/the-gallery`: the interact objective `obj/ring-the-bell` at anchor `anchor/gallery-end` stands at [18, 65, 33], inside the loop's periodic span [16, 64, 8]..[20, 68, 34] — a body has an identity the move cannot repeat, so a body moved a bay back would see the same figure twice, or none. Move the body out of the span; a figure that appears mid-loop is placed by an `on_cross` effect outside the visible cells, or summoned after the release
```

With no fog, every eye on the landing sees the whole hall, so the span grows to the walls at both ends and takes in the bell. The hall is walled at both ends, so geometry closes the view and `DW0947` has nothing to refuse. The engine stops at the first thing the move cannot repeat.

## The fog thinned

The edit: `visual/fog_end_distance` 8.3 instead of 8.

Exit status 3.

```text
DW0946 [error] build: after world-edits batch `batch/the-bell`: loop `loop/the-gallery`: 1 visible cell(s) of the periodic span differ from the cell each is seen as from the slab, in the configuration the world as it is placed, before any runtime write — [18, 65, 27] holds `minecraft:air` and [18, 65, 33] holds `minecraft:bell`. The view from the landing would not be the view from the slab. Make the two sections the same; never shorten the view to hide the difference
```

## The paint cut to the gallery

The edit: the piece expanded without its void margin, at 5 × 5 × 27. The area's paint is then only the gallery's own cells, and each eye's fog blends with the unpainted default.

Exit status 3.

```text
DW0948 [error] build: after world-edits batch `batch/the-bell`: loop `loop/the-gallery`: the interact objective `obj/ring-the-bell` at anchor `anchor/gallery-end` stands at [2, 65, 25], inside the loop's periodic span [0, 64, 0]..[4, 68, 26] — a body has an identity the move cannot repeat, so a body moved a bay back would see the same figure twice, or none. Move the body out of the span; a figure that appears mid-loop is placed by an `on_cross` effect outside the visible cells, or summoned after the release
```

## A lantern missing from the landing bay

The edit: the lantern of the second bay, the bay a crossing lands in, left out.

Exit status 3.

```text
DW0946 [error] build: after world-edits batch `batch/the-bell`: loop `loop/the-gallery`: 2 visible cell(s) of the periodic span differ from the cell each is seen as from the slab, in the configuration the world as it is placed, before any runtime write — [18, 67, 13] holds `minecraft:lantern[hanging=true,waterlogged=false]` and [18, 67, 19] holds `minecraft:air`; [18, 67, 19] holds `minecraft:air` and [18, 67, 25] holds `minecraft:lantern[hanging=true,waterlogged=false]`. The view from the landing would not be the view from the slab. Make the two sections the same; never shorten the view to hide the difference
```

## A lamp in the fog

The edit: glowstone set at head height into the middle of the porch's end wall, a cell the fog hides from every eye on the landing.

Exit status 3.

```text
DW0946 [error] build: after world-edits batch `batch/the-bell`: loop `loop/the-gallery`: the visible cell [17, 65, 10] is lit 11 and the cell it is seen as from the slab, [17, 65, 16], is lit 9, at the campaign's darkest reachable sky (15), in the configuration the world as it is placed, before any runtime write — something outside the visible cells lights two sections differently, a lamp round a corner or a hole in the roof over the next bay. Make the sections the same
```

## A slab one cell thick under a fall

The edit: the slab turned on its side, one course thick in y, with the landing one course under it.

Exit status 3.

```text
DW0945 [error] build: after world-edits batch `batch/the-bell`: loop `loop/the-gallery`: its slab [17, 66, 23]..[19, 66, 25] with offset [0, -1, 0] is not a slab the engine can poll — it is too thin to catch a crossing along y: a one-tick poll sees a body in the slab for a window of t + reach = 1 + 1.8 = 2.8 blocks, and a falling body's limit speed (`metrics::POLL_FALL_BLOCKS_PER_TICK`, the fall law's fixed point) is 3.92 blocks a tick, so a body can pass through between two polls. Thicken the slab to at least 3 cells along y. Reshape the slab or move the landing (`to`).
```
