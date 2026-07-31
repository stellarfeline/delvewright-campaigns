scoreboard players enable @a dw.class
scoreboard players enable @a dw.dlg_hedric
scoreboard players enable @a dw.dlg_maren
scoreboard players enable @a dw.i_unbar
execute as @a unless score @s dw.classed matches 1 unless score @s dw.dlg_shown matches 1 run function hollow-vigil:show_class
execute as @a[scores={dw.class=1}] run function hollow-vigil:class_apply_warden_blade
execute as @a[scores={dw.class=2}] run function hollow-vigil:class_apply_moor_ranger
execute as @a[scores={dw.class=3}] run function hollow-vigil:class_apply_barrow_friar
execute as @a[scores={dw.dlg_hedric=1}] run function hollow-vigil:dlg_hedric_1
execute as @a[scores={dw.dlg_hedric=2}] run function hollow-vigil:dlg_hedric_2
execute as @a[scores={dw.dlg_hedric=3}] run function hollow-vigil:dlg_hedric_3
execute as @a[scores={dw.dlg_hedric=4}] run function hollow-vigil:dlg_hedric_4
execute as @a[scores={dw.dlg_hedric=5}] run function hollow-vigil:dlg_hedric_5
execute as @a[scores={dw.dlg_hedric=6}] run function hollow-vigil:dlg_hedric_6
execute as @a[scores={dw.dlg_hedric=7}] run function hollow-vigil:dlg_hedric_7
execute as @a[scores={dw.dlg_maren=1}] run function hollow-vigil:dlg_maren_1
execute as @a[scores={dw.dlg_maren=2}] run function hollow-vigil:dlg_maren_2
execute as @a[scores={dw.dlg_maren=3}] run function hollow-vigil:dlg_maren_3
execute as @a[scores={dw.dlg_maren=4}] run function hollow-vigil:dlg_maren_4
execute as @a[scores={dw.dlg_maren=5}] run function hollow-vigil:dlg_maren_5
execute as @a[scores={dw.dlg_maren=6}] run function hollow-vigil:dlg_maren_6
execute as @a[scores={dw.dlg_maren=7}] run function hollow-vigil:dlg_maren_7
execute as @a if score @s dw.qa_quiet_the_halls matches 1 if score @s dw.f_vigil_sworn matches 1 unless score @s dw.o_purge matches 1 unless score @s dw.ann_purge matches 1 run function hollow-vigil:announce_o_purge
execute as @a if score @s dw.qa_the_barrow_key matches 1 if score @s dw.f_halls_quiet matches 1 unless score @s dw.o_key matches 1 unless score @s dw.ann_key matches 1 run function hollow-vigil:announce_o_key
execute as @a if score @s dw.qa_the_barrow_key matches 1 if score @s dw.o_key matches 1 unless score @s dw.o_unbar matches 1 unless score @s dw.ann_unbar matches 1 run function hollow-vigil:announce_o_unbar
execute as @a if score @s dw.qa_break_the_vigil matches 1 if score @s dw.f_warden_risen matches 1 unless score @s dw.o_warden matches 1 unless score @s dw.ann_warden matches 1 run function hollow-vigil:announce_o_warden
execute as @a if score @s dw.qa_break_the_vigil matches 1 if score @s dw.o_warden matches 1 if score @s dw.f_vigil_broken matches 1 unless score @s dw.o_altar matches 1 unless score @s dw.ann_altar matches 1 run function hollow-vigil:announce_o_altar
execute as @a if score @s dw.qa_quiet_the_halls matches 1 if score @s dw.f_vigil_sworn matches 1 unless score @s dw.o_purge matches 1 if score #hollow_garrison dw.wave matches ..0 run function hollow-vigil:complete_o_purge
execute as @a[scores={dw.i_unbar=1..}] if score @s dw.qa_the_barrow_key matches 1 if score @s dw.o_key matches 1 unless score @s dw.o_unbar matches 1 if items entity @s container.* minecraft:trial_key run function hollow-vigil:complete_o_unbar
execute as @a[scores={dw.i_unbar=1..}] run scoreboard players reset @s dw.i_unbar
execute as @a if score @s dw.qa_break_the_vigil matches 1 if score @s dw.f_warden_risen matches 1 unless score @s dw.o_warden matches 1 if score #first_warden dw.wave matches ..0 run function hollow-vigil:complete_o_warden
execute as @a if score @s dw.qa_break_the_vigil matches 1 if score @s dw.o_warden matches 1 if score @s dw.f_vigil_broken matches 1 unless score @s dw.o_altar matches 1 if entity @s[x=87,dx=2,y=80,dy=2,z=-4,dz=2] run function hollow-vigil:complete_o_altar
