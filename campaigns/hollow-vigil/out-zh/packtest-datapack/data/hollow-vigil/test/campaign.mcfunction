#> 空洞的守夜: objective completions set dw.campaign (Delvewright mechanism test)
# @dummy
# @timeout 100

function hollow-vigil:setup
scoreboard players set @a dw.qa_the_watch 1
execute as @a run function hollow-vigil:complete_o_gate_watch
execute as @a run function hollow-vigil:complete_o_swear
execute as @a run function hollow-vigil:complete_o_purge
execute as @a run function hollow-vigil:complete_o_key
execute as @a run function hollow-vigil:complete_o_unbar
execute as @a run function hollow-vigil:complete_o_warden
execute as @a run function hollow-vigil:complete_o_altar
assert score @p dw.campaign matches 1
