tellraw @s [{"bold":true,"color":"yellow","text":"New objective: "},{"color":"gold","text":"肃清回廊"}]
tellraw @s {"color":"gray","italic":true,"text":"玛伦的召唤已经把空洞卫戍从冢土里引了出来——把大门之后回廊里每一个复起的步卒都找出来放倒。"}
playsound minecraft:block.note_block.pling player @s
scoreboard players set @s dw.ann_purge 1
