#> 空洞的守夜: environment sealed on boot (spec-0002)
# @dummy
# @timeout 100

function hollow-vigil:setup
# time set noon -> daytime 6000 (the sole sealing command with a
# vanilla read-back path; gamerules are asserted at compile time).
execute store result score #sealtime dw.sys run time query daytime
assert score #sealtime dw.sys matches 6000
