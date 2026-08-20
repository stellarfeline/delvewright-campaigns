"""What each zone is, and what its own records say fills it.

Every string here is transcribed from a document in this campaign — `beats.md`
for the play and the budget, `map-zones.md` for the position, `map-brief.md` for
the massing. Nothing in this file is invented for the drawing: a box with
nothing recorded for it is drawn empty, which is the whole point of the sheets.
"""

# symbol in map.json -> the zone id zones.json declares
SYMBOL = {
    'z0/barrow_shore': 'z0-barrow-shore',
    'z1/cliff_road': 'z1-cliff-road',
    'z2/gate_ward': 'z2-gate-ward',
    'z3/drowned_ward': 'z3-drowned-ward',
    'z4/chapel_ward': 'z4-chapel-ward',
    'z5/keep': 'z5-hall-keep',
    'z6/cistern_deep': 'z6-cistern-deep',
    'z7/zone': 'z7-bell-tower',
}

ORDER = ['z0-barrow-shore', 'z1-cliff-road', 'z2-gate-ward', 'z3-drowned-ward',
         'z4-chapel-ward', 'z5-hall-keep', 'z6-cistern-deep', 'z7-bell-tower']

FACTS = {
    'z0-barrow-shore': dict(
        tag='Z0', name='Barrow Shore', cn='冢泽潮滩', minutes=10,
        floor='the tidal sand, −1.2',
        fills=['the cairn field, one heap per body recovered',
               'the tide-stake line, the flat’s lethal boundary',
               'the tutorial kill',
               'Emeric’s shelf, the last dry ground',
               'at the Dead Ebb, the ground below the stake line and the '
               'several hundred standing on it'],
        does='walks north across open sand until the sand ends at cliff'),
    'z1-cliff-road': dict(
        tag='Z1', name='Cliff Road', cn='崖道', minutes=15,
        floor='the cut ledge, +4.0 (+2.0 at the K2 gap)',
        fills=['the ledge itself as a one-body corridor',
               'the bracket line, the zone’s only map',
               'the K2 gap — a fallen shelf round a blind bend',
               'the shover',
               'the rope store the road passes through'],
        does='walks single file with no room to circle anything it meets'),
    'z2-gate-ward': dict(
        tag='Z2', name='Gatehouse', cn='门楼', minutes=20,
        floor='the gate passage, +2.5',
        fills=['the passage and its ambush',
               'the murder-hole floor above it, a real reachable storey',
               'the portcullis chamber and its winch',
               'the porter’s guardroom',
               'the roof, and the Gatewright fought on it',
               'the drain channel down the passage'],
        does='opens a shut gate outward, from the inside'),
    'z3-drowned-ward': dict(
        tag='Z3', name='Drowned Ward', cn='下沉外庭', minutes=25,
        floor='the ward floor, −1.5; the causeway top, +0.4',
        fills=['the causeway spine and its two weed pinches',
               'two arcades climbable end to end as an upper route',
               'the water-gate tower’s storeys',
               'the sunk boats and the ferry-tally in one of them',
               'at the Dead Ebb, the entire floor as new ground'],
        does='chooses when to leave a raised path for water it has been '
             'taught to fear'),
    'z4-chapel-ward': dict(
        tag='Z4', name='Chapel Ward', cn='礼拜堂中庭', minutes=25,
        floor='the cloister paving, +9',
        fills=['four arcade walks',
               'the three stations of Ide’s round',
               'the collapsed canopy as broken cover',
               'the rubble the corpse-ambush hides in',
               'the banded door',
               'the hour-vault beneath'],
        does='fights a pair in the open — the first fight with room to lose '
             'properly'),
    'z5-hall-keep': dict(
        tag='Z5', name='Hall & Keep', cn='大厅与主楼', minutes=25,
        floor='the keep floor, +12',
        fills=['the hearth as arena cover',
               'the tapestry sequence, read panel by panel along the wall',
               'the roof-post grid Ridd is fought around',
               'the far arch and its chairs',
               'Ancel’s chamber',
               'the keep stair'],
        does='fights a boss in a clear hall, then talks to a dead man'),
    'z6-cistern-deep': dict(
        tag='Z6', name='Cistern Deep', cn='深蓄水池', minutes=25,
        floor='the cistern floor, −0.15; the well bed, −2.3',
        fills=['ranked piers that make the plan legible from any bay',
               'the collapse shaft’s rubble cone as climbable terrain',
               'the supply channel as a lethal line across a uniform floor',
               'the Choir’s echo vault',
               'the well head and its apron',
               'the silt bed the sea uncovers'],
        does='crosses the delve’s largest interior by the bay it is '
             'standing in'),
    'z7-bell-tower': dict(
        tag='Z7', name='Bell Tower', cn='钟塔', minutes=25,
        floor='the ramp and tower foot, +14; the belfry floor, +30',
        fills=['the ramp approach between the collapsed low buildings',
               'the tower foot',
               'the broken first flight and the rope that bridges it',
               'the ringing floor',
               'the louvre stage',
               'a belfry walked AROUND a bell that is itself a building'],
        does='climbs sixteen metres of tower with a broken flight in it'),
}

# The seven ground planes of map-brief.md's massing table, as map.json holds
# them: the param that carries each, and the metres it transcribes.
PLANES = [
    ('invert_y', '−2.6', 'the supply-channel invert'),
    ('well_bed_y', '−2.3', 'the well’s silt bed'),
    ('ward_floor_y', '−1.5', 'the drowned ward’s floor'),
    ('flat_floor_y', '−1.2', 'the tidal sand'),
    ('cistern_y', '−0.15', 'the cistern’s floor'),
    ('tide_y', '0.0', 'THE STANDING TIDE'),
    ('causeway_y', '+0.4', 'the causeway top'),
    ('gate_y', '+2.5', 'the gate passage'),
    ('road_y', '+4.0', 'the cut ledge'),
    ('cloister_y', '+9', 'the cloister’s paving'),
    ('hall_y', '+12', 'the keep’s floor'),
    ('upper_ward_y', '+14', 'the upper ward, the tower foot'),
    ('belfry_y', '+30', 'the belfry floor'),
    ('crown_y', '+39', 'the crown'),
]

# The player's order of arrival, from map-brief.md's journey table. A sequence,
# not a path: it says which structure is stood in front of after which.
JOURNEY = ['z0-barrow-shore', 'z1-cliff-road', 'z2-gate-ward',
           'z3-drowned-ward', 'z4-chapel-ward', 'z5-hall-keep',
           'z6-cistern-deep', 'z3-drowned-ward', 'z7-bell-tower']
