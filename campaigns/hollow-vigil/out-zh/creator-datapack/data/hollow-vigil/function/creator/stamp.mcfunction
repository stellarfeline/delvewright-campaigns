scoreboard players reset @s dw.note
execute store result storage hollow-vigil:note x int 1 run data get entity @s Pos[0]
execute store result storage hollow-vigil:note y int 1 run data get entity @s Pos[1]
execute store result storage hollow-vigil:note z int 1 run data get entity @s Pos[2]
data modify storage hollow-vigil:note area set value "none"
execute if entity @s[x=0,dx=93,y=64,dy=20,z=-4,dz=26] run data modify storage hollow-vigil:note area set value "area/keep"
data modify storage hollow-vigil:note npc set value "none"
execute positioned as @s as @e[tag=dw_npc,sort=nearest,limit=1] if entity @s[tag=dw_npc_hedric] run data modify storage hollow-vigil:note npc set value "npc/hedric"
execute positioned as @s as @e[tag=dw_npc,sort=nearest,limit=1] if entity @s[tag=dw_npc_maren] run data modify storage hollow-vigil:note npc set value "npc/maren"
execute store result storage hollow-vigil:note o_gate_watch int 1 run scoreboard players get @s dw.o_gate_watch
execute store result storage hollow-vigil:note o_swear int 1 run scoreboard players get @s dw.o_swear
execute store result storage hollow-vigil:note o_purge int 1 run scoreboard players get @s dw.o_purge
execute store result storage hollow-vigil:note o_key int 1 run scoreboard players get @s dw.o_key
execute store result storage hollow-vigil:note o_unbar int 1 run scoreboard players get @s dw.o_unbar
execute store result storage hollow-vigil:note o_warden int 1 run scoreboard players get @s dw.o_warden
execute store result storage hollow-vigil:note o_altar int 1 run scoreboard players get @s dw.o_altar
function hollow-vigil:creator/emit with storage hollow-vigil:note
