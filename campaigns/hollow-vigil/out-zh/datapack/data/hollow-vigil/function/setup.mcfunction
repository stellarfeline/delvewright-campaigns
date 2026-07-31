# Environment sealing (spec-0002): box garden — nothing left to vanilla chance.
gamerule spawn_mobs false
gamerule advance_time false
gamerule advance_weather false
gamerule fire_spread_radius_around_player 0
gamerule mob_griefing false
time set noon
scoreboard objectives add dw.class trigger
scoreboard objectives add dw.classed dummy
scoreboard objectives add dw.dlg_shown dummy
scoreboard objectives add dw.dlg_hedric trigger
scoreboard objectives add dw.dlg_maren trigger
scoreboard objectives add dw.o_gate_watch dummy
scoreboard objectives add dw.o_swear dummy
scoreboard objectives add dw.o_purge dummy
scoreboard objectives add dw.o_key dummy
scoreboard objectives add dw.o_unbar dummy
scoreboard objectives add dw.o_warden dummy
scoreboard objectives add dw.o_altar dummy
scoreboard objectives add dw.qa_the_watch dummy
scoreboard objectives add dw.q_the_watch dummy
scoreboard objectives add dw.qa_quiet_the_halls dummy
scoreboard objectives add dw.q_quiet_the_halls dummy
scoreboard objectives add dw.qa_the_barrow_key dummy
scoreboard objectives add dw.q_the_barrow_key dummy
scoreboard objectives add dw.qa_break_the_vigil dummy
scoreboard objectives add dw.q_break_the_vigil dummy
scoreboard objectives add dw.campaign dummy
scoreboard objectives setdisplay sidebar dw.campaign
scoreboard objectives add dw.wave dummy
scoreboard objectives add dw.f_deep_open dummy
scoreboard objectives add dw.f_halls_quiet dummy
scoreboard objectives add dw.f_vigil_broken dummy
scoreboard objectives add dw.f_vigil_sworn dummy
scoreboard objectives add dw.f_warden_risen dummy
scoreboard objectives add dw.f_warned dummy
scoreboard objectives add dw.i_unbar trigger
scoreboard objectives add dw.ann_purge dummy
scoreboard objectives add dw.ann_key dummy
scoreboard objectives add dw.ann_unbar dummy
scoreboard objectives add dw.ann_warden dummy
scoreboard objectives add dw.ann_altar dummy
forceload add 0 0 8 8
forceload add 0 9 8 15
forceload add 9 9 17 15
forceload add 18 9 26 15
forceload add 27 10 37 14
forceload add 38 10 44 14
forceload add 45 10 55 14
forceload add 56 10 66 14
forceload add 67 10 77 14
forceload add 78 10 84 14
forceload add 85 9 91 15
forceload add 85 16 91 22
forceload add 83 -4 93 8
place template hollow-vigil:keep-spawn-hall 0 64 0
place template hollow-vigil:keep-room-small-c 0 64 9
place template hollow-vigil:keep-gate-room 9 64 15 counterclockwise_90
place template hollow-vigil:keep-room-small-b 18 64 15 counterclockwise_90
place template hollow-vigil:keep-stair 37 64 10 clockwise_90
place template hollow-vigil:keep-corridor-straight 38 68 14 counterclockwise_90
place template hollow-vigil:keep-stair 55 68 10 clockwise_90
place template hollow-vigil:keep-stair 66 72 10 clockwise_90
place template hollow-vigil:keep-stair 77 76 10 clockwise_90
place template hollow-vigil:keep-corridor-straight 78 80 14 counterclockwise_90
place template hollow-vigil:keep-corridor-tee 85 80 15 counterclockwise_90
place template hollow-vigil:keep-room-small-a 85 80 16
place template hollow-vigil:keep-boss-hall 93 80 8 180
fill 3 65 8 5 67 8 minecraft:air
fill 3 65 9 5 67 9 minecraft:air
fill 8 65 11 8 67 13 minecraft:air
fill 9 65 11 9 67 13 minecraft:air
fill 17 65 11 17 67 13 minecraft:air
fill 18 65 11 18 67 13 minecraft:air
fill 26 65 11 26 67 13 minecraft:air
fill 27 65 11 27 67 13 minecraft:air
fill 37 69 11 37 71 13 minecraft:air
fill 38 69 11 38 71 13 minecraft:air
fill 44 69 11 44 71 13 minecraft:air
fill 45 69 11 45 71 13 minecraft:air
fill 55 73 11 55 75 13 minecraft:air
fill 56 73 11 56 75 13 minecraft:air
fill 66 77 11 66 79 13 minecraft:air
fill 67 77 11 67 79 13 minecraft:air
fill 77 81 11 77 83 13 minecraft:air
fill 78 81 11 78 83 13 minecraft:air
fill 84 81 11 84 83 13 minecraft:air
fill 85 81 11 85 83 13 minecraft:air
fill 87 81 9 89 83 9 minecraft:air
fill 87 81 15 89 83 15 minecraft:air
fill 87 81 16 89 83 16 minecraft:air
fill 87 81 8 89 83 8 minecraft:air
summon minecraft:villager 4 65 8 {NoAI:1b,Invulnerable:1b,Silent:1b,PersistenceRequired:1b,NoGravity:1b,Rotation:[180f,0f],Tags:["dw_npc","dw_npc_hedric"],CustomName:"值守人赫德里克",CustomNameVisible:1b,VillagerData:{profession:"minecraft:none",type:"minecraft:plains",level:1}}
summon minecraft:interaction 4 65 8 {width:1.0f,height:2.0f,response:1b,Invulnerable:1b,Tags:["dw_npc_hedric"]}
summon minecraft:villager 11 65 12 {NoAI:1b,Invulnerable:1b,Silent:1b,PersistenceRequired:1b,NoGravity:1b,Rotation:[90f,0f],Tags:["dw_npc","dw_npc_maren"],CustomName:"守望者玛伦",CustomNameVisible:1b,VillagerData:{profession:"minecraft:none",type:"minecraft:plains",level:1}}
summon minecraft:interaction 11 65 12 {width:1.0f,height:2.0f,response:1b,Invulnerable:1b,Tags:["dw_npc_maren"]}
setblock 88 81 20 minecraft:chest
item replace block 88 81 20 container.0 with minecraft:trial_key 1
summon minecraft:interaction 2 65 12 {width:1.0f,height:2.0f,response:1b,Invulnerable:1b,Tags:["dw_i_unbar"]}
summon minecraft:item_display 2 65 12 {Glowing:1b,Tags:["dw_marker","dw_i_unbar"],CustomName:"打开深处之门",CustomNameVisible:1b,billboard:"center",item:{id:"minecraft:lantern",count:1}}
setworldspawn 4 65 4
scoreboard players set #init dw.sys 1
