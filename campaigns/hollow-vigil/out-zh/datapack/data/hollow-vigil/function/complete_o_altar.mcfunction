scoreboard players set @s dw.o_altar 1
tellraw @s [{"color":"green","text":"Objective complete: "},{"color":"white","text":"宣告终结"}]
playsound minecraft:entity.experience_orb.pickup player @s
function hollow-vigil:check_q_break_the_vigil
