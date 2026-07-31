scoreboard players set @s dw.o_purge 1
tellraw @s [{"color":"green","text":"Objective complete: "},{"color":"white","text":"肃清回廊"}]
playsound minecraft:entity.experience_orb.pickup player @s
scoreboard players set @s dw.f_halls_quiet 1
function hollow-vigil:check_q_quiet_the_halls
