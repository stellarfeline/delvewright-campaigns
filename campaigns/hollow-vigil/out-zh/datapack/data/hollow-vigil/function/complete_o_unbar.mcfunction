scoreboard players set @s dw.o_unbar 1
tellraw @s [{"color":"green","text":"Objective complete: "},{"color":"white","text":"打开深处之门"}]
playsound minecraft:entity.experience_orb.pickup player @s
scoreboard players set @s dw.f_deep_open 1
function hollow-vigil:check_q_the_barrow_key
