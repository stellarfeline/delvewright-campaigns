tellraw @s [{"bold":true,"color":"yellow","text":"New objective: "},{"color":"gold","text":"取回冢钥"}]
tellraw @s {"color":"gray","italic":true,"text":"冢钥收在卫戍的保险箱里——去找侧边小房间中的箱子。"}
playsound minecraft:block.note_block.pling player @s
scoreboard players set @s dw.ann_key 1
