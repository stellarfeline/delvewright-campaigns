#!/bin/bash
# usage: clearing.sh <keyframes.txt> <from-tick> <out.txt>
#
# The clearing measured through the pinned 1.21.11 client's own classes (FogEdge.java).
#   CLIENT_JAR  the pinned client jar with its signatures stripped
#   CLIENT_CP   its libraries, ':'-joined (the 1.21.11 version manifest's library list)
#   JAVA_HOME   a Java 21
# <keyframes.txt> is `tick x y z yaw pitch` per line, read off the build's emitted
# `cs_tick_*` driver (one `tp` per keyframe); every keyframe from <from-tick> on is an eye.
# The box is the clearing's painted extent, exactly as the emitted `fillbiome` lines cover it.
set -eu
here=$(cd "$(dirname "$0")" && pwd)
J="$JAVA_HOME/bin"
CP="$CLIENT_JAR:$CLIENT_CP"
work=$(mktemp -d "${TMPDIR:-$here}/clearing.XXXXXX")
"$J/javac" -proc:none -d "$work" -cp "$CP" "$here/FogEdge.java"
EYES=$(awk -v t="$2" '$1>=t {printf "%s,%s,%s ", $2,$3,$4}' "$1")
"$J/java" -cp "$CP:$work" FogEdge 8166 28 8218 8266 100 8378 320 476 $EYES -- \
  "standin@8215.5,65,8299.5" "face@8215.5,92.5,8222.5" "top@8215,150,8215" "wingW@8172,120,8212" \
  "clawE@8258,130,8215" "seaS@8231,63,8385" "seaE@8272,63,8300" "seaN@8215,63,8160" 2>&1 \
  | sed -E 's#^.*\[STDOUT\]: ##' | grep -v '^\[' > "$3"
cat "$3"
