# Massing intent — what the owner is choosing, per zone

Companion to `REMAKE.md`. `REMAKE.md` §3 says what each zone *is*; this says what
is still **open** about its shape, so a contact sheet shows a real choice and the
owner's hour buys a decision instead of a formality.

## Why this file exists

Two measurements forced it, both from the round that built the sheets.

**The seed is not an axis.** A box-split grammar picks alternatives by guards on
the box's dimensions and touches the RNG only where two alternatives apply at
once. Measured over 32 seeds per zone: seven of eight zones produce one building,
five of them pixel-identical. Five zones' own fixture notes already said so —
*"nothing in the gatehouse draws from the seed; it is stated, not chosen"* — and
"seed-varied candidates" survived in the prose because nobody re-read it against
the programs. A sheet built on seeds would have shown six copies of one building
and asked which was preferred.

**Parameters alone are usually refused.** The zones guard their own shapes:
`cliff_road` refuses `fall < 8` and `sea < 3`; `gate_ward` refuses a plinth that
leaves less than `MIN_UPPER` to build in; `chapel_ward` and `cistern_deep` guard
the mainline's frame against the junction's length. A single-parameter sweep
mostly hits a refusal, which is the guard working. **So each row below names the
region change that must move with the parameter** — that is what makes a
candidate legal rather than refused.

A candidate is therefore a **variation**: region, parameters, or seed. Never seed
alone.

## What is *not* on the table

Not offered as choices, and a sheet that appears to offer them is a defect:

- Anything `REMAKE.md` marks owner-verbatim. Z1's knockback-niche cliff path is
  mandatory vocabulary; its niches teach → test → twist across three, and a later
  leg's niche must be readable from an earlier one. That is the fairness of the
  set piece, not a preference.
- Which pieces compose a zone. That is §4's catalogue and it is settled.
- Anything that moves a bonfire's reign relative to a hostile's onset. `DW0478`
  governs it and content does not get to trade it away for a silhouette.

## The eight zones

Each row: **the decision in play terms** — what a player would feel differently —
then the knobs, then the region change that has to accompany them.

### Z0 Barrow Shore — landing, class pick, BF1, dormant Barrow Warden

**Decision: how exposed the landing feels before the first fire.** Whether the
graves read as a field the party crosses or a cluster they walk past.

`barrow_shore` declares **no parameters at all** — it is wholly determined by its
box. That is why it measured 0 pixels of variation across 32 seeds: not a defect,
the correct behaviour of a zone with nothing to vary. **Its only axis is the
region**, so its candidates are box shapes: the same vocabulary at a squarer or
longer footprint, and at one or two courses more headroom.

The Warden is dormant and optional; a wider box is what lets a first-time player
walk past it, which is the choice.

### Z1 Cliff Road — the owner's set piece

**Decision: how far the drop reads, and how much margin the ledge leaves.**

Knobs: `fall` (≥ 8, guarded), `sea` (≥ 3, guarded), `ledge_shelf`.

Region: raising `fall` needs Y; widening `sea` needs X. Both are refused inside
the current box, so **every candidate here is a region change carrying a
parameter change**.

**Hold this zone out of curation until the switchback lands.** As programmed it
is a single run, and a single run has no earlier leg to read the next niche from
— so the observability the set piece rests on is not there to be judged yet.
Showing it now would ask for a decision about a shape that is about to change.

### Z2 Gatehouse + Outer Ward — timed portcullis, watch bay, BF2, Gate Reeve

**Decision: how long the party is under the portcullis, and how far the bypass
loop runs before it comes back.**

Knobs: `door_run`, `motif_run`, `stand_run`, `tee_run`, `stair_run`, `shaft_run`,
`shaft/drop`, `strip_depth`.

Region: `shaft/drop` sets the plinth, and the zone refuses a plinth that leaves
less than `MIN_UPPER` above it — so a deeper drop **must** come with more Y. The
loop's length is `tee_run` + `strip_depth` against Z; lengthening the loop
without Z is refused.

The watch bay's line of sight to the full portcullis cycle is an obligation
(§4 entry O), not a variable — a candidate that shortens the bay until the cycle
is not observable is wrong however it looks.

### Z3 Drowned Lower Ward — the toll road, flooded ward

**Decision: how long the wade is before the far-side bar.**

Knobs: `ward_run`, `junction_run`, `strip_depth`.

Region: `ward_run` is the mainline's own length; the junction guard means a
longer junction needs a deeper box. Vary `ward_run` against Z, and take
`junction_run` with it or the branch reads as an afterthought.

### Z4 Chapel Ward (hub) — the hearth

**Decision: whether the hearth reads as a room the party rests in or an alcove
they pass.**

Knobs: `hearth_run`, `junction_run`, `strip_depth`.

Region: the mainline had to widen to 7 for the nook to exist at all, so the
hearth's size trades directly against the hub's width. This is the zone where
the decision is most nearly a pure parameter — `hearth_run` against a fixed box
is legal across a real range.

As the hub, its junction count is fixed by the topology in `REMAKE.md` §3. Do not
offer candidates that change how many ways lead out of it.

### Z5 Great Hall + Keep — rafters, stores, bait gallery, Hall Marshal

**Decision: the hall's proportion — a long nave or a broad room — and how much
gallery the bait sits in.**

Knobs: `gallery_run`, `door_run`, `motif_run`, `store_run`, `duct_run`,
`duct/drop`.

Region: same plinth guard as Z2 — `duct/drop` deeper needs Y. The hall's
proportion is `gallery_run` against the box's X, so a genuinely different
proportion is a region change, not a parameter one.

Entry B's rule holds: the bait and its watcher must both be legible from the same
places. A candidate that lengthens the gallery until the watcher leaves the
frame has broken the pattern, not varied it.

### Z6 Cistern Deep — dart gallery, grate elite

**Decision: how long the dart gallery runs before the arena opens.**

Knobs: `gallery_run`, `arena_run`, `vent_run`, `sally_run`, `strip_depth`.

Region: every mainline piece's frame guard is measured against the mainline's
width, so widening the arena is a mainline change and the gallery follows. Vary
`gallery_run` and `arena_run` **together**; independently, one of them is refused.

This is the zone the cutaway work was measured on — its top two courses are
solid, so judge it on `plan-mid` and `sec-z`, never on `top`, which showed 0.00%
of frame for a five-course headroom change.

### Z7 Bell Tower — ascent, loft, Bellkeeper

**Decision: how long the climb is, and how much room the last fight has.**

Knobs: `climb`, `ring_run`, `loft_run`, `flight/tread`, `flight/landing_run`,
`flight/head`, `shaft/storey`, `shaft/sill`, `hearth_run`, `tee_run`,
`door_run`, `strip_depth`.

Region: `climb` is bound by identity to the flight's tread count and to the
shaft's sill, and the box must hold `climb + flight/head + 1` in Y. **Raising the
climb is always a Y change**, and the Z length must hold five upper runs plus the
flight's own or the plan refuses.

The most interesting candidate here is the trade between a tall climb and a
generous ring: both want the same budget, and it is a real choice about whether
the tower's memory is the ascent or the fight at the top.

## Rendering these

Judge massing on cutaways, not silhouettes. A `top` shot of a zone carved from
solid mass strips one Y layer and shows more rock — measured at 0.00% of frame
for a change that moves interior walls. `plan-mid` and `sec-z` are the shots that
carry the decision.

A section plane is a lottery: `sec-x`/`sec-z` sit at 50%, and a change that
misses them scores zero. If a candidate looks identical, check it against
`plan-mid` before concluding the knob is inert.

## The acceptance test for a sheet

Before any sheet reaches the owner, the sweep must report **more than one
distinct massing** for that zone. `distinct_massings == 1` is a finding and the
sheet does not ship: it means the knobs chosen for that zone are inert, and
showing it spends her attention to receive no information. That is the failure
this file was written to prevent.
