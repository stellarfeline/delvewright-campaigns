#> 空洞的守夜: interact trigger + item -> complete
# @dummy
# @timeout 100

function hollow-vigil:setup
scoreboard players set @a dw.qa_the_barrow_key 1
scoreboard players set @a dw.o_key 1
give @a minecraft:trial_key 1
scoreboard players set @a dw.i_unbar 1
function hollow-vigil:tick
assert score @p dw.o_unbar matches 1
