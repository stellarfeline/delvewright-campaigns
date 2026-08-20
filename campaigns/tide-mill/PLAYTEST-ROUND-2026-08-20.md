# Playtest round — prepared 2026-08-20

> ## Before handing this over — read this box, then delete nothing
>
> This round was **prepared ahead of time**, not on the day it is handed over.
> Everything below was measured on **2026-08-20** against these exact revisions:
>
> | what | revision |
> |---|---|
> | pipeline | `f369ee5713651285dfc191a5df37b72467a144ec` |
> | content — tide mill | `ad8b5ea1b2fb7cbbc3d932a7b9eaf7083b166260`, merged onto content main `72913b0` |
> | content — mill race | `bb7451b40a399c49c8911de93075cde92bf47a98`, merged onto content main `72913b0` |
> | building pieces used for the tide mill | the `tidal-keep` set as it stood on 2026-08-02 |
>
> **If any of those has moved, this page is a stale measurement and is not a
> description of the build in front of you.** Re-run the round before handing it
> over. A prepared build presented later as though it were fresh is the defect
> this box exists to prevent.
>
> Nothing below was run against a live server, and no server port was taken.

Two items were prepared. **One is ready and takes about fifteen minutes. One is
pulled and should not be opened.**

---

## 1. The Mill Race — a water-mill yard · ~10–15 minutes · **ready**

### What it is

One small mill yard, thirteen blocks across and eleven deep. A cobbled yard
fills the west third. Its east edge is a kerb — eleven stone stairs in a line,
low side toward the water — so you step up onto it and look down into a channel
that runs the full depth of the piece, two blocks wide and three deep, walled in
stone either side. An oak wheel five blocks across straddles the channel, its rim
turning just clear of the water. The east third is the mill house: a mossy stone
base, spruce above, one barred window facing the water, and a gabled roof.

It is a length of a longer watercourse, not a pond — the channel enters at one
end and leaves at the other.

### How to look at it

You walk this one in a **browser page**, not in the game. Build the tool once,
then make the page:

```sh
# once, from the pipeline repository
cargo build --release --bin delvec
export PATH="$PWD/target/release:$PATH"
```

```sh
# from the content repository
delvec viewer demos/mill-race/mill-race.nbt -o mill-race.html
open mill-race.html
```

The page is one self-contained file — it needs no network and keeps working if
you move it. **W A S D** walk, the mouse looks, and there is an Orbit button that
swings you around the outside. Textures are taken from the Minecraft jar already
on this machine, so nothing else needs installing.

It opens looking at the yard from the outside. **Walk yourself in** — there is no
preset "stand at the entrance" viewpoint, which is a gap on our side and is noted
below.

### What to look for

These are the judgements only you can make. Everything mechanical about this
piece has been checked and holds.

- **Does it read as a water mill?** Standing in the yard looking east: is that
  obviously a mill race with a wheel turning in it — or does it read as a trench
  with a circle propped over it? The silhouette is doing the work here; there is
  no fine detail and there was never going to be any.
- **Is there enough in it to be worth walking?** It is a small piece. Walk the
  yard, step up on the kerb, follow the channel to both ends. Is that a place, or
  is it a diagram of a place?
- **The kerb.** Eleven stairs in a line, low side to the water. Does stepping up
  onto it and looking down feel like a kerb along a working race — or like a step
  that is there for a reason you cannot see from the yard?
- **The mill house is deliberately scenery** — solid from footing to roof, one
  barred window, and no door. Standing outside it, does a doorless mill house
  read as a building you are not meant to enter, or as one somebody forgot to
  finish?
- **Does the water read as running?** It is still water in the page, and the
  fiction is a race with a current. Is that a problem from inside the yard, or
  does the wheel carry it?

### What is open, and not to test

Named here so they are not discovered by hitting them.

- **There is no way to join a server for this one.** This yard cannot be walked
  in the game at all — the browser page is the only route that exists. That is a
  gap on our side, not something to work around, and it is why this item is
  fifteen minutes rather than an hour.
- **No preset viewpoint inside the piece.** The page cannot set you down at the
  way in, because the yard does not yet name any place inside itself. You walk in
  yourself. Cheap for us to fix.
- **The two rules this demo exists to teach cannot be seen by looking**, on
  purpose. They are about what the game does to a building *after* it is placed —
  a kerb that quietly straightens itself, and water that leaves through a gap in
  a wall. Both are invisible in every picture, which is the demo's entire point.
  So do not go hunting for them in the page. Judging whether the demo *teaches*
  them is a **reading** task on its own page (`demos/mill-race/README.md`), not a
  looking task, and it is optional.

---

## 2. The Tide Mill — **pulled. Do not open it.**

### What it was going to be

A fifteen-minute level about reading a gate instead of gambling on it. Three
water gates stand along a mill race and open and shut on a fixed count; a miller
gives you the count for each. The first gate is generous, the second tighter, and
the third one kills you if you misread it.

### Why it is pulled

It does not build. Four separate things, any one of which would have cost the
whole hour:

1. **Half the level has no pieces.** The opening yard you start in, the miller
   who gives you the count, and the first two gates are all built from a set of
   building pieces that is not in the shared library and never has been. Nothing
   can assemble that half of the level at all. This is not a recent breakage —
   the level has never been buildable from its own branch.

2. **Supplying those pieces by hand does not rescue it.** With them in place the
   build still stops, because there are **53 places along the shore where you can
   walk into the water and not climb out again**. No bank, no step, nothing to
   wade out onto. Anyone who went in would be swimming for the rest of the delve.
   This happens in both English and Chinese, identically.

3. **A known way to strand yourself is still open.** The level moves you across
   to a second area one way only — you cannot swim back up the race. Dying at the
   lethal third gate after that crossing sends you back to the very beginning,
   with no route forward. This was reported the last time the level was looked at
   and it is not fixed.

4. **Nothing has ever watched the lethal gate kill anybody.** The automatic
   run-through has never once reached the third gate — it stops at the second,
   every time it has been tried. The one beat the whole level is built around has
   never been seen working, by a machine or by a person.

### What has to be true before it comes back

It builds; the shoreline no longer strands anybody; dying at the last gate puts
you back within reach of it; and something has watched that gate fire. Until all
four hold there is nothing here to judge, because the level cannot be started.

---

## In one line

**The mill yard is ready** — fifteen minutes in a browser, and the question is
whether it reads as a mill. **The tide mill is not** and should not be put in
front of anyone until it builds.
