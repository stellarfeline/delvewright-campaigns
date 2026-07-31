#> 空洞的守夜: requires_flags gates objective `obj/key`
# @dummy
# @timeout 100

function hollow-vigil:setup
scoreboard players set @a dw.o_key 0
scoreboard players set @a dw.qa_the_barrow_key 1
give @a minecraft:trial_key 1
execute as @a run function hollow-vigil:c_reward_key
assert score @p dw.o_key matches 0
scoreboard players set @a dw.f_halls_quiet 1
execute as @a run function hollow-vigil:c_reward_key
assert score @p dw.o_key matches 1
