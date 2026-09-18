"""Where every place of Vesperhold stands, in piece coordinates.

Local axes: x east, y up, z south; world north is -z, so the approach is the
south end of the piece. Boxes are inclusive cell ranges of the space a body
walks in; walls stand outside them. Every module of the generator reads its
numbers from here, and so does the layout chart, so the chart is the castle.
"""

X, Y, Z = 172, 104, 292

# ------------------------------------------------------------------ heights
VALLEY = 8          # feet on the valley floor; y7 is its surface
CASTLE = 24         # feet on the crag top, the ward, the causeway deck
DAIS = 28           # feet in the antechamber and the throne hall
WALK = 36           # feet on the wall walks and in the tower rooms
BELL = 52           # feet on the bell deck
UNDER = 12          # feet in the undercroft

# ------------------------------------------------------------------ the crag
# The rock the castle stands on: its top course is CASTLE - 1. Sheer on the
# south and west, where the side route runs along a shelf cut into its face.
CRAG = (12, 167, 2, 171)            # x0, x1, z0, z1
SHELF_SOUTH = (4, 75, 172, 177)     # the shelf under the south curtain
SHELF_WEST = (4, 11, 128, 177)      # the shelf under the west curtain


class Place:
    def __init__(self, key, name, box, floor, height, note=""):
        self.key, self.name, self.box = key, name, box
        self.floor, self.height, self.note = floor, height, note

    @property
    def x0(self): return self.box[0]
    @property
    def x1(self): return self.box[1]
    @property
    def z0(self): return self.box[2]
    @property
    def z1(self): return self.box[3]


P = {}
def place(key, name, box, floor, height, note=""):
    P[key] = Place(key, name, box, floor, height, note)

# the approach
place("wayside-shrine", "Wayside Shrine", (80, 95, 276, 287), VALLEY, 0, "roofless; the Causeway Fire")
place("pilgrim-road", "Pilgrim Road", (84, 91, 237, 275), VALLEY, 0, "open road across the valley floor")
place("causeway-stair", "Causeway Stair", (84, 91, 220, 235), VALLEY, 0, "an open flight on an arcaded ramp, valley floor to deck")
place("hanging-causeway", "Hanging Causeway", (84, 91, 176, 219), CASTLE, 0, "deck on piers")
place("barbican", "Barbican", (76, 99, 153, 171), CASTLE, 10, "gatehouse; two gate towers; the postern in the west tower's west face")
# the west cliffs
place("postern-ledge", "Postern Ledge", (5, 75, 172, 176), CASTLE, 0, "shelf, west from the postern in the gate tower's west face")
place("cliff-path", "Cliff Path", (5, 9, 128, 176), CASTLE, 0, "shelf, north along the west face")
place("stables", "Stables", (16, 47, 132, 147), CASTLE, 7, "back door west onto the cliff path, east door into the ward")
# the ward
place("outer-ward", "Outer Ward", (52, 123, 100, 151), CASTLE, 0, "open hub; the portcullis winch on its south wall")
place("barracks", "Barracks", (126, 149, 144, 163), CASTLE, 8, "")
place("armory", "Armory", (152, 159, 146, 155), CASTLE, 6, "the false chest")
place("keep-steps", "Keep Steps", (76, 91, 94, 99), CASTLE, 7, "porch before the Keep Doors")
place("cloister-lane", "Cloister Lane", (52, 57, 60, 99), CASTLE, 0, "walled lane from the ward to the cloister")
# the cathedral quarter
place("cloister-garth", "Cloister Garth", (16, 47, 60, 91), CASTLE, 0, "open garth inside four arcades; the Cloister Fire")
place("well-house", "Well-House", (18, 25, 62, 69), CASTLE, 6, "in the garth's north-west corner")
place("chapel-of-hours", "Chapel of Hours", (16, 51, 32, 55), CASTLE, 22, "nave east-west; rose window on the west front; altar east")
place("scriptorium", "Scriptorium", (16, 31, 96, 111), CASTLE, 8, "the ledger; the Psalter Wall in its south wall")
place("psalter-stair", "Psalter Stair", (17, 19, 113, 127), UNDER, 14, "cut down through the rock, north to south, behind the Psalter Wall")
# the undercroft
place("crypt-of-wardens", "Crypt of Wardens", (26, 49, 104, 127), UNDER, 9, "")
place("well-stair", "Well Stair", (18, 23, 62, 79), UNDER, 14, "from the well-house floor down to the pool passage")
place("undertide-pool", "Undertide Pool", (24, 47, 68, 91), UNDER, 10, "under the garth; the well at its centre")
# the heights
place("rampart-stair", "Rampart Stair", (125, 140, 120, 135), CASTLE, 14, "stair tower off the ward's east side; a short wall walk joins its top to the east rampart")
place("east-rampart", "East Rampart", (152, 159, 21, 129), WALK, 0, "wall walk on the east curtain")
place("watch-tower", "Watch Tower", (148, 163, 4, 19), WALK, 7, "Brother Pellam's stall")
place("buttress-walk", "Buttress Walk", (34, 146, 12, 15), WALK, 0, "high walk along the north edge")
place("bell-tower-stair", "Bell Tower Stair", (16, 31, 8, 23), WALK, 15, "the Warden's Door in its east wall")
place("belfry", "Belfry", (16, 31, 8, 23), BELL, 10, "open bell deck; spire over it")
# the keep
place("great-hall", "Great Hall", (60, 107, 60, 91), CASTLE, 18, "the Almoner's Door in its west wall")
place("antechamber", "Antechamber", (76, 91, 47, 55), DAIS, 7, "the Throne Fire")
place("throne-hall", "Throne Hall", (60, 107, 20, 43), DAIS, 22, "")

# the east side, off the road
place("chandlery-yard", "Chandlery Yard", (142, 164, 130, 143), CASTLE, 0, "behind the garden gate; the Chandler at his vat, the chandlery on the curtain")
place("spur-passage", "Spur Passage", (145, 147, 119, 126), CASTLE, 3, "a vaulted way under the rampart spur, the yard to the garden")
place("hedge-garden", "Hedge Garden", (111, 150, 18, 118), CASTLE, 0, "east of the keep: the parterre and dry fountain at the south, the orchard, the summerhouse at the north")
place("summerhouse", "Summerhouse", (138, 146, 24, 33), CASTLE, 5, "an open pavilion; the Hedge Knight")
FOUNTAIN = (134, 100)               # the dry fountain's plinth, in the parterre

# the pockets off the road, one or more from every region of the route
place("sally-tower", "Sally Tower", (116, 120, 167, 174), VALLEY, 8, "the south mural tower east of the causeway, a door in its foot on the valley floor")
place("hall-of-arms", "Hall of Arms", (94, 98, 165, 175), CASTLE, 4, "the barbican's east gate tower, hollowed at the gate level")
place("bastion", "Bastion", (12, 16, 166, 171), CASTLE, 4, "a storeroom in the south-west bastion, its door off the west shelf")
place("ossuary", "Ossuary", (58, 70, 115, 129), UNDER, 6, "under the ward, down the dry fountain: the gallery and the charnel chamber")
place("ringers-stair", "Ringers' Stair", (21, 33, 15, 23), CASTLE, 12, "down the bell tower's foot from the stair hall to a door into the Founders' Yard")
place("founders-yard", "Founders' Yard", (34, 52, 18, 30), CASTLE, 0, "north of the chapel, under the buttress walk: the casting pit and the Bellfounder")
place("arbalest-turret", "Arbalest Turret", (163, 169, 97, 103), WALK, 4, "the mural tower on the east curtain, off the rampart walk")
place("gallows-walk", "Gallows Walk", (84, 108, 5, 9), CASTLE, 0, "the ground under the north curtain behind the keep")
place("buttery", "Buttery", (112, 120, 72, 81), CASTLE, 5, "off the great hall's east wall")

# The side route, end to end: the postern in the barbican's south face, west
# along the south shelf, round the south-west corner, north along the west
# shelf, in at the stables' back door.
SIDE_ROUTE = [
    ("postern", (76, 173)),
    ("south-west corner", (7, 175)),
    ("west shelf, at the stables", (7, 139)),
    ("stables back door", (13, 139)),
]
