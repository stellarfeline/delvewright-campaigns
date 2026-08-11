#!/usr/bin/env python3
"""Author one sweep manifest per bell zone, from MASSING.md's decisions.

Every candidate is a VARIATION — region, parameters, or both — never a seed
alone: a box-split grammar picks alternatives by guards on the box's own
dimensions and only consults the RNG where two alternatives apply at once, so a
seed sweep produces one building drawn N times.

Each zone's candidates span the one decision MASSING.md names for it, and each
carries the region change that makes the parameter legal — the zones guard their
own shapes, so a lone parameter move mostly hits a refusal.

**The refusal reading is the solver.** Every guard in these zones is a linear
inequality over the box's own dimensions and the program's parameters, and the
refusal prints both sides, what fed each operand, and how far short it fell. So
the next candidate is deduced, not swept: read the inequality, solve it, carry
the region change it demands. Every comment below that names a number names the
clause it came from.
"""

import json
import os
import sys

OUT = os.path.dirname(os.path.abspath(__file__))
SCHEMA = "delvewright.grammar-sweep/1"


def m(program, seed, candidates, region=None):
    d = {"schema": SCHEMA, "program": program, "seed": seed, "candidates": candidates}
    if region:
        d["region"] = region
    return d


def c(cid, region=None, **params):
    d = {"id": cid}
    if region:
        d["region"] = list(region)
    if params:
        d["params"] = {k.replace("__", "/"): v for k, v in params.items()}
    return d


MANIFESTS = {
    # Z0 — no parameters at all; the region IS the only axis.
    # Decision: does the grave field read as ground the party crosses, or a
    # cluster they walk past?
    #
    # Two facts about this zone's box that the first pass had wrong, and both
    # are facts about every zone in the library:
    #
    # 1. **The box is normalised before it is expanded.** Every zone's frame is
    #    `Reorient::KEEP.y(WorldY).z(Largest)`, so the LOCAL Z is whichever
    #    horizontal axis is longer. A region and its transpose are therefore the
    #    same building placed at ninety degrees — `[19,6,24]` and `[24,6,19]`
    #    both expand as local 19 x 6 x 24. `distinct_massings` reads the
    #    world-space bitmap and counted them as two, and their `filled_cells`
    #    are both 1422. The candidate that varies only the transpose is a
    #    duplicate wearing a distinct digest; `squarer` is now 22x6x23, which
    #    really is a different box.
    # 2. **`elite_ground` floors this zone's width at 19**, exactly as it does
    #    Z3's and Z6's mainline: `X >= radius*2 + 1 + (flank_margin*2 + 2)` =
    #    19 at the design's radius 4 and flank margin 4. The design box's 19 IS
    #    that floor, so the two 15-wide candidates were refused. The narrow
    #    direction is closed on this zone: the grave field can be widened and
    #    cannot be narrowed.
    "bell:barrow-shore": m("bell:barrow-shore", 11, [
        c("as-designed"),                        # local 19 x 6 x 24
        c("tight-landing", region=[19, 6, 20]),  # local 19 x 6 x 20; Z floor is 17
        c("longer-strand", region=[19, 6, 34]),
        c("squarer", region=[22, 6, 23]),
        c("wide-open", region=[26, 6, 28]),
        c("taller-sky", region=[19, 8, 24]),
    ]),

    # Z1 — the owner's set piece, now a switchback. Decision: how far the drop
    # reads and how much margin the ledge leaves. Both knobs are guarded
    # (fall >= 8, sea >= 3), so every candidate carries its region.
    "bell:cliff-road": m("bell:cliff-road", 11, [
        c("as-designed"),
        c("deep-drop", region=[11, 17, 40], fall=12),
        c("wide-gulf", region=[15, 13, 40], sea=6),
        c("sheer-and-narrow", region=[11, 19, 40], fall=14, sea=3),
        c("ledge-margin", region=[13, 13, 40], ledge_shelf=1, sea=4),
        c("long-legs", region=[11, 13, 52], turn_run=6),
    ]),

    # Z2 — decision: how long the party is under the portcullis, and how far the
    # bypass loop runs.
    #
    # The two halves are governed by two different guard families, and the first
    # pass conflated them.
    #
    # *Under the portcullis* is the gated passage — `corridor | SPAN | approach |
    # BAY` — whose length is the REMAINDER `gate_run = Z - (shaft + motif + tee +
    # stair + stand + door)`, and whose own guard is
    #     Dimension.Z >= gate/approach + gate/span + 4
    # read off `gate/passage_plan`. So the felt quantities are `gate/span` (the
    # cells the player crosses under the portcullis) and `gate/approach` (how far
    # off they read it from, floored at MIN_STANDOFF = 6), and BOTH are bought
    # with `Z`, one for one, through the remainder. The first pass moved the six
    # named runs and left `gate/span` at its default in every candidate — six
    # buildings varying everything except the thing the decision is about.
    #
    # *The bypass loop* is `tee_run` (its length along travel) against
    # `strip_depth` (how far off the mainline it runs), and they are locked
    # together from both ends:
    #     strip_depth > tee_run          (else the bar's wall turns along the ward)
    #     tee_run > Dimension.X - strip_depth   (the mainline frame guard)
    # Substituting the second into the first gives `2 * strip_depth > X`, i.e.
    # THE TIGHTEST LEGAL LOOP AT A GIVEN X IS `strip_depth = (X + 2) / 2`, which
    # at X = 20 is exactly the design's 11/10. The design box is already at its
    # own minimum loop, so a shorter loop is a NARROWER ZONE and nothing else —
    # `tight-loop` takes X to 16. Below X = 14 the mainline falls under
    # `disarm_stand::MIN_WIDTH` (6) and the stand refuses.
    "bell:gate-ward": m("bell:gate-ward", 11, [
        c("as-designed"),
        # gate/span 3 -> 8: five more cells under the portcullis. The passage
        # guard then wants Z >= 8 + 8 + 4 = 20 where the design leaves 16, so
        # the zone lengthens by exactly the four cells the guard is short.
        c("long-portcullis", region=[20, 10, 88], **{"gate__span": 8}),
        # The other half of "how long under it": read it from twice as far.
        # approach 8 -> 16 wants gate_run >= 16 + 3 + 4 = 23; 84 leaves 16, so
        # Z = 84 + 7 = 91.
        c("deep-standoff", region=[20, 10, 91], **{"gate__approach": 16}),
        # Both at once, and the widest gate the passage will carry: span 10,
        # approach 12 wants gate_run >= 26 -> Z = 84 + 10 = 94.
        c("long-and-deep", region=[20, 10, 94], **{"gate__span": 10, "gate__approach": 12}),
        # The loop, doubled. `tee_run` 18 needs `strip_depth` 19 above it and a
        # mainline under it (19 > 9 holds at X = 28, which keeps the mainline at
        # the design's 9). Z carries the eight extra cells of junction plus the
        # passage's own 15-cell floor: 12+10+18+16+10+10 = 76, and 92 - 76 = 16.
        c("long-loop", region=[28, 10, 92], tee_run=18, strip_depth=19),
        # The loop at its floor, which is a narrower zone: X = 16 gives
        # strip_depth 9 / tee_run 8 and a mainline of 7 — still over
        # `disarm_stand::MIN_WIDTH` (6) and `watch_bay`'s X >= 6.
        # 12+10+8+16+10+10 = 66, and 82 - 66 = 16.
        c("tight-loop", region=[16, 10, 82], tee_run=8, strip_depth=9),
    ]),

    # Z3 — decision: how long the wade is before the far-side bar.
    #
    # MASSING.md had the wrong knob. The wade is the CAUSEWAY, and the causeway
    # is the remainder piece: `crossing_run = Z - ward_run - junction_run`.
    # `ward_run` is the lower ward's ARENA (`elite_ground`), the fight after the
    # bar, not the water before it. Travel runs Z-max -> Z-min, so the player
    # wades the remainder first, meets the junction with the bar in its flank,
    # and comes out on the arena floor.
    #
    # So the wade is varied by Z against a fixed `ward_run + junction_run`, and
    # the four guards
    #     strip_depth > junction_run
    #     ward_run, junction_run, crossing_run  >  X - strip_depth
    # bound it from below through the mainline's width. That width is not free:
    # `elite_ground` refuses a box under `diameter + 2*flank_margin + 2` = 19 at
    # the design's radius 4 and flank margin 4, so the mainline is pinned at 19
    # and EVERY run must be at least 20. **The wade cannot be shorter than 20
    # cells at the design box's ward width** — see MASSING.md Z3 for the reading.
    # The candidates therefore span the wade upward, 20 -> 56, and buy width on
    # the two rows that are about the ward rather than the water.
    "bell:drowned-ward": m("bell:drowned-ward", 11, [
        c("as-designed"),                                 # wade 20
        c("longer-wade", region=[40, 10, 68]),            # wade 28
        c("long-wade", region=[40, 10, 76]),              # wade 36
        c("longest-wade", region=[40, 10, 96]),           # wade 56
        # A deeper shortcut strip. `junction_run` must clear the mainline (21)
        # and stay under `strip_depth` (27), so 22 is the only room the two
        # guards leave, and the arena and the wade follow it up to 22.
        c("deep-branch", region=[48, 10, 66], strip_depth=27, ward_run=22, junction_run=22),
        # A bigger fight at the end of the wade: radius 4 -> 6 takes
        # `elite_ground`'s width floor to 13 + 8 + 2 = 23, so the mainline
        # widens to 23, every run to 24, and the strip to 25 to stay over the
        # junction. Z = 24 * 3.
        c("wide-ward", region=[48, 10, 72], strip_depth=25, ward_run=24,
          junction_run=24, **{"ring__radius": 6}),
    ]),

    # Z4 — the hub. Decision: is the hearth a room the party rests in, or an
    # alcove they pass? Three guards bound it, all read off the refusal:
    #   hearth_run > X - strip_depth            (framed against the MAINLINE)
    #   Z - junction_run - hearth_run > X - strip_depth
    #   the hearth piece itself needs X - strip_depth >= 6
    # So a smaller hearth is bought with a NARROWER MAINLINE, not a smaller
    # number, and the mainline has a floor of 6 — strip_depth <= 10 at X = 16.
    "bell:chapel-ward": m("bell:chapel-ward", 11, [
        c("as-designed"),
        c("great-hearth", hearth_run=10),
        c("alcove", strip_depth=10, hearth_run=7, junction_run=8),
        c("deep-nook", region=[22, 9, 26], strip_depth=15, hearth_run=8),
        c("long-hub", region=[24, 9, 38], strip_depth=17, junction_run=16, hearth_run=8),
        c("tall-hall", region=[16, 12, 30], hearth_run=10),
    ]),

    # Z5 — decision: the hall's proportion (long nave vs broad room), and how
    # much gallery the bait sits in.
    #
    # Z5 has no branch strip, so its frame guard is measured against the ZONE's
    # own width and not a mainline's: all six of `duct_run`, `motif_run`,
    # `gallery_run`, `store_run`, `door_run` and the remainder `hall_run` must
    # be `> Dimension.X`. That single fact is what refused three of the first
    # pass's six, and it has a consequence worth stating plainly:
    # **a broader keep lengthens every room in it.** Widening X by 4 raises the
    # floor under five named runs and the remainder at once, so `broad-room` is
    # not X + 4 — it is X + 4 and Z + 20.
    #
    # The second binding guard is `rafter_hall`'s density cap,
    #     (X-2) * Z * beam_period  >=  24 * Z + 24 * beam_period
    # over the hall's own interior. At beam_period 4 it reduces to
    # `Z >= 96 / (4*(X-2) - 24)`, which is why `narrow-keep` at X = 9 must give
    # the hall 24 cells: a narrow hall has to be LONG to earn its rafters, or
    # the truss alternative stops applying and the plan refuses.
    "bell:hall-keep": m("bell:hall-keep", 11, [
        c("as-designed"),                                  # hall 16 over X 11
        # The nave, stretched: every named run stays at 12 and Z carries all of
        # it into the remainder. 100 - 60 = 40, a hall 3.6x its own width.
        c("long-nave", region=[11, 11, 100]),
        # A hall nearly as broad as it is long. X = 15 puts the floor under
        # every run at 16, so five rooms cost 80 and the hall takes 16 —
        # proportion 1.07 against the design's 1.45. Density: (15-2)*16*4 = 832
        # against 24*16 + 96 = 480.
        c("broad-room", region=[15, 11, 96], duct_run=16, motif_run=16,
          gallery_run=16, store_run=16, door_run=16),
        # The other extreme of the same guard: X = 9 drops every run's floor to
        # 10, but the density cap then needs the hall itself at 24 or the truss
        # alternative stops applying. 5*10 + 24 = 74.
        c("narrow-keep", region=[9, 11, 74], duct_run=10, motif_run=10,
          gallery_run=10, store_run=10, door_run=10),
        # How much gallery the bait sits in: 12 -> 32, at the design's width.
        # 100 - (12+12+32+12+12) = 20 for the hall, still over X.
        c("long-gallery", region=[11, 11, 100], gallery_run=32),
        # The plinth, deepened. `Y >= duct/drop + MIN_UPPER` wants 13, and
        # `bait_stand` still needs `head + 2` = 7 above the plinth, so Y = 15.
        c("deep-plinth", region=[11, 15, 76], **{"duct__drop": 8}),
    ]),

    # Z6 — decision: how long the dart gallery runs before the arena opens.
    #
    # Same shape as Z3 and for the same reason: every mainline frame guard
    # measures against `X - strip_depth`, and that width is floored by
    # `elite_ground`'s own `X >= diameter + 2*flank_margin + 2` = 19. With the
    # mainline pinned at 19, all four named runs and the shaft's remainder must
    # be at least 20, so **the dart gallery cannot be shortened below 20 at the
    # design box's arena width** — the same finding as Z7's belfry ring, one
    # zone over, and recorded rather than forced.
    #
    # `arena_run` is also NOT the size of the arena: `elite_ground` spends any Z
    # over its minimum on the exit run, never on the circle. A genuinely bigger
    # fight is `arena/radius`, and that raises the mainline's floor with it —
    # radius 6 wants 13 + 8 + 2 = 23, hence `big-arena`'s 24-cell runs.
    "bell:cistern-deep": m("bell:cistern-deep", 11, [
        c("as-designed"),                                            # gallery 20
        # 60 cells of arena + sally + vent, and the gallery takes the rest.
        c("long-gallery", region=[40, 10, 120], gallery_run=40),     # gallery 40
        c("longest-gallery", region=[40, 10, 136], gallery_run=56),  # gallery 56
        # A bigger circle to open into, not a longer run to it.
        c("big-arena", region=[48, 10, 120], strip_depth=25, arena_run=24,
          sally_run=24, vent_run=24, gallery_run=24, **{"arena__radius": 6}),
        # The shortcut, deeper off the mainline. `sally_run` 26 needs
        # `strip_depth` 27 over it and the mainline 19 under it, so X = 46.
        # Z is the sum of all five runs and not the design's 100: at Z = 86 the
        # shaft's remainder reads 0 against a floor of 19 — "20 short: the left
        # must rise to 20" — so 20 + 26 + 20 + 20 + 20 = 106.
        c("deep-sally", region=[46, 10, 106], strip_depth=27, sally_run=26),
        # The fall the player arrives by, doubled: the shaft is the remainder.
        c("long-fall", region=[40, 10, 120]),                        # shaft 40
    ]),

    # Z7 — decision: how long the climb is, and how much room the last fight
    # has. `climb` is not free; the refusal reading gives it as an identity:
    #   climb == (Z - (ring+door+tee+loft+hearth) - landing_run*2) / tread
    #   shaft/sill == climb,  and  Y >= climb + flight/head + 1
    # with landing_run 3, tread 2, head 3. So Z = 2*climb + sum(runs) + 6, and
    # every candidate solves for Z and carries the sill. The upper runs are
    # framed against the mainline (X - strip_depth), so a SHORT ring needs a
    # deeper strip, not a smaller number.
    "bell:bell-tower": m("bell:bell-tower", 11, [
        c("as-designed"),
        c("tall-climb", region=[41, 20, 137], climb=15, **{"shaft__sill": 15}),
        c("generous-ring", region=[41, 18, 145], ring_run=28, loft_run=24, climb=13, **{"shaft__sill": 13}),
        # NO TIGHT-RING CANDIDATE, and that is a finding rather than an omission.
        # `ring_run` is squeezed from both sides — `> X - strip_depth` from the
        # frame, `>= radius*2 + 1 + approach*2` from the belfry — and the belfry
        # also floors the mainline itself at `radius*2 + 1 + flank_margin*2 + 2`.
        # Widening the strip to narrow the mainline therefore starves the ring
        # before it shortens it, and shrinking the radius raises the mainline
        # floor faster than it lowers the run's. At this design box the shortest
        # legal `ring_run` IS the default: the last fight's room can be enlarged
        # and cannot be reduced. Measured over five deduced candidates.
        c("short-climb-big-loft", region=[41, 12, 131], loft_run=30, climb=7, **{"shaft__sill": 7}),
        c("wide-belfry", region=[49, 14, 155], strip_depth=28, ring_run=26, door_run=26, tee_run=27, loft_run=26, hearth_run=26),
    ]),
}


def main():
    for prog, man in MANIFESTS.items():
        # `tools/zone-sheets.py --manifest-dir` looks for `<program-slug>.json`
        # with the slug `program.replace(":", "-")`, so this directory IS a
        # manifest dir and needs no renaming step in front of the driver.
        name = prog.replace(":", "-") + ".json"
        path = os.path.join(OUT, name)
        with open(path, "w") as f:
            json.dump(man, f, indent=2)
            f.write("\n")
        print(f"{name:22s} {len(man['candidates'])} candidates")
    return 0


if __name__ == "__main__":
    sys.exit(main())
