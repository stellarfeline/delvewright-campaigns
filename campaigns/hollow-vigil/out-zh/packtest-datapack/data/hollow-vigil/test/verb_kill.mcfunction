#> 空洞的守夜: kill wave `wave/hollow-garrison` -> countdown -> complete
# @dummy
# @timeout 100

function hollow-vigil:setup
scoreboard players set @a dw.qa_quiet_the_halls 1
scoreboard players set @a dw.f_vigil_sworn 1
function hollow-vigil:spawn_hollow_garrison
assert score #hollow_garrison dw.wave matches 3
kill @e[tag=dw_wave_hollow_garrison]
execute as @a run function hollow-vigil:k_reward_hollow_garrison
execute as @a run function hollow-vigil:k_reward_hollow_garrison
execute as @a run function hollow-vigil:k_reward_hollow_garrison
function hollow-vigil:tick
assert score @p dw.o_purge matches 1
