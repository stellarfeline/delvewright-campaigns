scoreboard players set @s dw.campaign 1
advancement grant @s only hollow-vigil:campaign_complete
tellraw @s [{"color":"gold","text":"空洞的守夜 — complete."},{"text":"\n"},{"color":"gray","text":"A Delvewright delve."}]
title @s title {"bold":true,"color":"gold","text":"Delve Complete"}
title @s subtitle {"color":"yellow","text":"空洞的守夜"}
playsound minecraft:ui.toast.challenge_complete player @s
tellraw @a {"color":"dark_gray","text":"[Delvewright] complete dw.campaign 1"}
