# Refusals beside The Long Gallery

Each is `campaigns/the-long-gallery` at campaign revision `53592e9` plus one edit to its grammar program (`design/programs/long-gallery.json`), re-expanded at seed 1 and built by `delvec` from the engine's branch `feat/loop-far-end`. The refusal is raised at the world-edits replay, which prints its loop binding first. Each transcript is the build's binding line and its refusal, verbatim.

## The exit brought nearer

The edit: three bays fewer between the slab and the exit, so the lit doorway stands 56 blocks past the slab instead of 74.

Exit status 3.

```text
loop binding: 1 loop(s); slab cells 9; eyes 24 (fog end 1024..1024 blocks as the kernel reads it); span 3750 cells closed in 77 steps, frontier cells closed by geometry 1794 and by fog 0, open faces 0; visible cells 3100 compared as blocks and as light at 2 skies over 1 configuration(s), 851 of them in the near field (13.8..13.8 blocks); far-field differences 396, largest shift 1.4672° of 1.2852°; volumes in span 0, bodies in the near field 0, bodies in the far field 1; forced route meets 1 of 1 holding, exercise steps 1
DW0947 [error] build: after world-edits batch `batch/the-bell`: loop `loop/the-gallery`: 32 far difference(s) shift more than the far field allows; the worst: the visible cell [1, 65, 129] is lit 6 and the cell it is seen as from the slab, [1, 65, 141], is lit 7, at the campaign's brightest reachable sky (15), in the configuration the world as it is placed, before any runtime write — a light far off reaches it and not its image, and its lit area is what is measured — it lies past the near field (13.8 blocks of every eye, for an offset of 12 blocks), but the jump moves it 1.467° across the screen of the eye at [3.80, 66.62, 78.80], 50.8 blocks away, over the 1.2852° the far field is allowed — the largest shift on the one loop on record walked on a client and read as seamless. A difference far off goes unseen only while it moves less than that: put it farther from the eye, shorten the offset, or make the two sections the same
```

The exit is past the near field (13.8 blocks for a 12-block jump), so it may differ from what the slab sees. But the light the last lamps throw on the floor and walls before it has no copy two bays on, and at this distance the jump moves that lit area 1.467° across the screen, over the 1.2852° the far field allows. 1.2852° is the largest shift in the one loop walked and judged seamless. The hall as built puts the exit 74 past the slab, where the largest shift is 0.7374°.

## The approach cut short

The edit: seven bays fewer behind the slab, so the glass at the porch's back stands 36 blocks behind the landing instead of 78.

Exit status 3.

```text
loop binding: 1 loop(s); slab cells 9; eyes 24 (fog end 1024..1024 blocks as the kernel reads it); span 3150 cells closed in 95 steps, frontier cells closed by geometry 1506 and by fog 0, open faces 0; visible cells 2600 compared as blocks and as light at 2 skies over 1 configuration(s), 851 of them in the near field (13.8..13.8 blocks); far-field differences 396, largest shift 2.3942° of 1.2852°; volumes in span 0, bodies in the near field 0, bodies in the far field 1; forced route meets 1 of 1 holding, exercise steps 1
DW0947 [error] build: after world-edits batch `batch/the-bell`: loop `loop/the-gallery`: 59 far difference(s) shift more than the far field allows; the worst: the visible cell [1, 65, 6] is lit 7 and the cell it is seen as from the slab, [1, 65, 18], is lit 5, at the campaign's brightest reachable sky (15), in the configuration the world as it is placed, before any runtime write — a light far off reaches it and not its image, and its lit area is what is measured — it lies past the near field (13.8 blocks of every eye, for an offset of 12 blocks), but the jump moves it 2.394° across the screen of the eye at [3.80, 66.62, 35.70], 29.3 blocks away, over the 1.2852° the far field is allowed — the largest shift on the one loop on record walked on a client and read as seamless. A difference far off goes unseen only while it moves less than that: put it farther from the eye, shorten the offset, or make the two sections the same
```

The rule judges every direction, because a player running from something looks back. The eye it names stands 0.3 short of the landing's approach face (`z 35.70`), where a walking body is when the slab catches it. Cut the approach further, three bays, and the porch falls inside the near field:

```text
loop binding: 1 loop(s); slab cells 9; eyes 24 (fog end 1024..1024 blocks as the kernel reads it); span 2700 cells closed in 95 steps, frontier cells closed by geometry 1290 and by fog 0, open faces 0; visible cells 2225 compared as blocks and as light at 2 skies over 1 configuration(s), 839 of them in the near field (13.8..13.8 blocks); far-field differences 0, largest shift 0.2414° of 1.2852°; volumes in span 0, bodies in the near field 0, bodies in the far field 1; forced route meets 1 of 1 holding, exercise steps 1
DW0946 [error] build: after world-edits batch `batch/the-bell`: loop `loop/the-gallery`: 12 visible cell(s) of the loop's near field (13.8 blocks of an eye) differ from the cell each is seen as from the slab, in the configuration the world as it is placed, before any runtime write — [1, 65, 4] holds `minecraft:glass` and [1, 65, 16] holds `minecraft:air`; [1, 66, 4] holds `minecraft:glass` and [1, 66, 16] holds `minecraft:air`; [1, 67, 4] holds `minecraft:glass` and [1, 67, 16] holds `minecraft:air`; [2, 65, 4] holds `minecraft:glass` and [2, 65, 16] holds `minecraft:red_carpet`; [2, 65, 5] holds `minecraft:air` and [2, 65, 17] holds `minecraft:red_carpet`; [2, 65, 6] holds `minecraft:air` and [2, 65, 18] holds `minecraft:red_carpet`. The view from the landing would not be the view from the slab. Make the two sections the same; never shorten the view to hide the difference
```
