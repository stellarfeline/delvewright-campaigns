scoreboard players set @s dw.o_key 1
tellraw @s [{"color":"green","text":"Objective complete: "},{"color":"white","text":"取回冢钥"}]
playsound minecraft:entity.experience_orb.pickup player @s
function hollow-vigil:check_q_the_barrow_key
