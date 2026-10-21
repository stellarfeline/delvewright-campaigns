import json, math, sys
C = sys.argv[1]
ID = "saltstair-a"; V = "0.55.0"
def env(stage, content):
    json.dump({"campaign_id": ID, "content": content, "dsl_version": V, "stage": stage},
              open(f"{C}/{stage}.json", "w"), indent=2); open(f"{C}/{stage}.json","a").write("\n")

env("world", {
  "areas": [], "boundary": {"margin": 8}, "demo_level": True, "horizon": "ocean",
  "premise": "Saltstair is a fishing town on the seaward end of a long green peninsula. One street climbs from the quay to a square at the top in five terraces, each a flight of stone steps above the last, and the houses stand on the terraces. The party arrives on the square in the afternoon and walks the street down to the water.",
  "seed": 20261021, "target_minutes": 10,
  "theme": "A stone-and-timber fishing town stepping down a hillside to its quay, one box per building and per connector.",
  "time": "dusk", "title": "Saltstair", "weather": "clear"})

DAT = [("datum/square",84,"The square's and the chapel's and inn's walk plane."),
       ("datum/upper",80,"The upper street's, the smithy's and the weaver's walk plane; flight 1's floor."),
       ("datum/middle",76,"The middle street's and the merchant's walk plane; flight 2's floor."),
       ("datum/lower",72,"The lower street's and the rope walk's walk plane; flight 3's floor."),
       ("datum/shore",68,"The shore street's and the harbourmaster's walk plane; flight 4's floor."),
       ("datum/quay",64,"The quay's and the warehouse's walk plane; flight 5's floor.")]
facts = [{"id":"fact/region-span-x","note":"The region west to east.","unit":"blocks","value":144.0},
         {"id":"fact/region-span-z","note":"The region north to south.","unit":"blocks","value":224.0},
         {"id":"fact/region-depth","note":"The region's height, from y 40.","unit":"blocks","value":96.0}]
for d,y,n in DAT:
    facts.append({"id":"fact/"+d.split("/")[1]+"-walk","note":n,"unit":"blocks","value":float(y)})
env("geometry-brief", {"facts": facts})

# places: id, x0,z0,x1,z1, datum, kind, ceiling, roof, intent, note
P = [
 ("square",65,96,82,109,"square","way",{"open":6},None,"the square at the top of the town","The chapel west, the inn east, flight 1 down from its south edge."),
 ("flight-1",71,111,76,116,"upper","stair",{"open":8},None,"the first flight, from the square down to the upper street","Six wide and six long; its treads rise four to the square at its north end."),
 ("upper-street",71,118,76,129,"upper","way",{"open":6},None,"the upper street","The smithy west, the weaver's house east."),
 ("flight-2",71,131,76,136,"middle","stair",{"open":8},None,"the second flight","Treads rise four to the upper street."),
 ("middle-street",71,138,76,149,"middle","way",{"open":6},None,"the middle street","The merchant's house west."),
 ("flight-3",71,151,76,156,"lower","stair",{"open":8},None,"the third flight","Treads rise four to the middle street."),
 ("lower-street",71,158,76,169,"lower","way",{"open":6},None,"the lower street","The rope walk east."),
 ("flight-4",71,171,76,176,"shore","stair",{"open":8},None,"the fourth flight","Treads rise four to the lower street."),
 ("shore-street",71,178,76,185,"shore","way",{"open":6},None,"the shore street","The harbourmaster's house west."),
 ("flight-5",71,187,76,192,"quay","stair",{"open":8},None,"the fifth flight, down to the quay","Treads rise four to the shore street."),
 ("quay",58,194,89,200,"quay","way",{"open":6},None,"the quay at the water","A straight stone wall 32 wide; the warehouse at its east end."),
 ("chapel",54,98,63,106,"square","house",{"clearance":6},{"courses":6,"eaves":1},"a small stone chapel with a short tower","Its door is east, onto the square."),
 ("inn",84,97,94,107,"square","house",{"clearance":4},{"courses":6,"eaves":1},"the Lantern, a wide timber-framed inn","Its door is west, onto the square."),
 ("smithy",62,119,69,126,"upper","house",{"clearance":4},{"courses":4,"eaves":1},"a forge with a chimney","Its door is east, onto the upper street."),
 ("weaver",78,118,84,128,"upper","house",{"clearance":4},{"courses":5,"eaves":1},"a narrow house, cloth on the upper floor","Its door is west, onto the upper street."),
 ("merchant",60,139,69,148,"middle","house",{"clearance":5},{"courses":5,"eaves":1},"the tallest house, with a counting room","Its door is east, onto the middle street."),
 ("ropewalk",78,158,84,169,"lower","house",{"clearance":4},{"courses":4,"eaves":1},"a long low rope-walk shed","Its door is west, onto the lower street."),
 ("harbourmaster",62,177,69,184,"shore","house",{"clearance":4},{"courses":4,"eaves":1},"a narrow house with a lamp in its gable","Its door is east, onto the shore street."),
 ("warehouse",80,182,89,192,"quay","house",{"clearance":5},{"courses":5,"eaves":1},"a long stone store with a slate roof","Its door is south, onto the quay."),
]
# seams: a, b, class, face, at, meets, kind, form, stair_in
S = [
 ("square","flight-1","stair","south",6,0,"stair","the first flight: six wide, four up to the square, treads on the flight"),
 ("flight-1","upper-street","walk","south",0,0,"contact","the foot of the first flight running level onto the upper street"),
 ("upper-street","flight-2","stair","south",0,0,"stair","the second flight: six wide, four up to the upper street, treads on the flight"),
 ("flight-2","middle-street","walk","south",0,0,"contact","the foot of the second flight running level onto the middle street"),
 ("middle-street","flight-3","stair","south",0,0,"stair","the third flight: six wide, four up to the middle street, treads on the flight"),
 ("flight-3","lower-street","walk","south",0,0,"contact","the foot of the third flight running level onto the lower street"),
 ("lower-street","flight-4","stair","south",0,0,"stair","the fourth flight: six wide, four up to the lower street, treads on the flight"),
 ("flight-4","shore-street","walk","south",0,0,"contact","the foot of the fourth flight running level onto the shore street"),
 ("shore-street","flight-5","stair","south",0,0,"stair","the fifth flight: six wide, four up to the shore street, treads on the flight"),
 ("flight-5","quay","walk","south",0,13,"contact","the foot of the fifth flight running level onto the middle of the quay"),
 ("square","chapel","walk","west",6,4,"door","the chapel's east door onto the square"),
 ("square","inn","walk","east",6,5,"door","the inn's west door onto the square"),
 ("upper-street","smithy","walk","west",4,3,"door","the smithy's east door onto the upper street"),
 ("upper-street","weaver","walk","east",5,5,"door","the weaver's west door onto the upper street"),
 ("middle-street","merchant","walk","west",5,4,"door","the merchant's east door onto the middle street"),
 ("lower-street","ropewalk","walk","east",5,5,"door","the rope walk's west door onto the lower street"),
 ("shore-street","harbourmaster","walk","west",2,3,"door","the harbourmaster's east door onto the shore street"),
 ("quay","warehouse","walk","north",26,4,"door","the warehouse's south door onto the quay"),
]
def eid(a,b): return f"edge/{a}--{b}"
nodes = [{"id":"node/"+p[0],"intent":p[9],"note":p[10]} for p in P]
edges = [{"a":"node/"+a,"b":"node/"+b,"class":c,"id":eid(a,b)} for a,b,c,*_ in S]
crit = ["node/"+n for n in ["square","flight-1","upper-street","flight-2","middle-street","flight-3","lower-street","flight-4","shore-street","flight-5","quay"]]
env("layout-graph", {"beats":[{"node":"node/quay","objective":"obj/reach-the-quay","quest":"quest/down-to-the-quay"}],
    "critical_path": crit, "edges": edges, "entry":"node/square", "goal":"node/quay", "nodes": nodes})

boxes=[]
for name,x0,z0,x1,z1,d,kind,ceil,roof,_,_ in P:
    b={"ceiling":ceil,"extent":[x1-x0+1,z1-z0+1],"floor":{"datum":"datum/"+d},"node":"node/"+name}
    if roof: b["roof"]=roof
    if name=="square": b["min"]=[65,96]
    boxes.append(b)
seams=[]
for a,b,c,face,at,meets,kind,form in S:
    s={"edge":eid(a,b),"face":face,"form":form,"at":at,"meets":meets}
    if kind=="stair": s["opening"]={"width":6,"height":4}; s["stair_in"]="node/"+b
    elif kind=="door": s["opening"]="door"
    else: s["contact"]={}
    seams.append(s)
views=[
 ("view/from-the-sea",[73.5,66.5,232.5],[73.5,80,150],"The whole town from the water: the stepping of the roofs, the quay wall, the hill behind."),
 ("view/down-the-street",[73.5,85.6,97.5],[73.5,66,200],"The street from the square to the sea: the flights, the kerbs, the houses' facades."),
 ("view/up-the-street",[73.5,65.6,199.5],[73.5,84,100],"The street from the quay: how each terrace meets the next."),
 ("view/the-first-flight",[68.5,81.6,120.5],[73.5,83,112],"One join at eye height: flight 1 between the upper street and the square, with the smithy's corner."),
 ("view/the-merchants-terrace",[48.5,80.6,143.5],[73.5,76,143.5],"From the hillside west: how a house and its terrace meet the ground."),
 ("view/from-the-south-east",[120,110,215],[74,76,150],"The oblique whole, roofs and terraces."),
]
idents=[{"cmp":"eq","fact":"fact/region-span-x","measure":{"axis":"x","of":"region-extent"}},
        {"cmp":"eq","fact":"fact/region-span-z","measure":{"axis":"z","of":"region-extent"}}]
for d,y,n in DAT:
    idents.append({"cmp":"eq","fact":"fact/"+d.split("/")[1]+"-walk","measure":{"datum":d,"of":"datum-y"}})
env("site-plan", {"boxes":boxes,"datums":[{"id":d,"note":n,"y":y} for d,y,n in DAT],
  "fill":{"below":"minecraft:dirt","kind":"open","surface":"minecraft:grass_block",
          "terrain":{"base_y":48,"heightmap":"terrain/peninsula.png","kind":"heightmap","range":51}},
  "identities":idents,"region":{"extent":[144,96,224],"min":[0,40,0]},"seams":seams,
  "views":[{"eye":[math.floor(c) for c in e],"id":i,"look_at":[math.floor(c) for c in l],"note":n+" The site plan states a view in whole cells: each coordinate is the cell holding the camera's point; design/cameras.json carries the exact point."} for i,e,l,n in views],"volumes":[]})

env("quest-plan", {"finale":"quest/down-to-the-quay","quests":[{"act":1,"area":"area/site","depends_on":[],
  "goal":"Walk the main street down from the square to the quay.","id":"quest/down-to-the-quay","mandatory":True,"npcs":[]}]})
env("quests", {"quests":[{"happening":{"text":"The party arrives on the square at the top of the town.","verb":"arrives"},
  "id":"quest/down-to-the-quay",
  "objectives":[{"anchor":"anchor/node-quay","happening":{"text":"The party reaches the quay at the foot of the street.","verb":"arrives"},
     "id":"obj/reach-the-quay","radius":1,"title":"Walk down to the quay","type":"reach-anchor"}],
  "on_complete":[{"happening":{"text":"The street has been walked to the water.","verb":"departs"},"type":"campaign-complete"}],
  "trigger":{"type":"campaign-start"}}]})
env("npcs", {"npcs":[]})
env("classes", {"classes":[{"blurb":"Three loaves for the climb back.","id":"class/visitor",
  "kit":[{"count":3,"item":"minecraft:bread"}],"name":"Visitor"}]})
env("dialogue", {"dialogues":[]})
