scoreboard players set @s dw.o_warden 1
tellraw @s [{"color":"green","text":"Objective complete: "},{"color":"white","text":"击破初代守望者"}]
playsound minecraft:entity.experience_orb.pickup player @s
scoreboard players set @s dw.f_vigil_broken 1
function hollow-vigil:check_q_break_the_vigil
