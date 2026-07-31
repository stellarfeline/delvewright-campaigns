tellraw @s [{"bold":true,"color":"yellow","text":"New objective: "},{"color":"gold","text":"打开深处之门"}]
tellraw @s {"color":"gray","italic":true,"text":"深处之门在转角房间里等着——发光的灯笼就是记号。手持冢钥打开它。"}
playsound minecraft:block.note_block.pling player @s
scoreboard players set @s dw.ann_unbar 1
