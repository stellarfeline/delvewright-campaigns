tellraw @s [{"bold":true,"color":"yellow","text":"New objective: "},{"color":"gold","text":"宣告终结"}]
tellraw @s {"color":"gray","italic":true,"text":"走到大厅尽头的祭坛前，越过初代守望者倒下的地方。"}
playsound minecraft:block.note_block.pling player @s
scoreboard players set @s dw.ann_altar 1
