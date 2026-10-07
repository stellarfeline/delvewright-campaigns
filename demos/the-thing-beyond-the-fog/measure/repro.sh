#!/usr/bin/env bash
# usage: STAND="x y z" TX=<x> TZ=<z> repro.sh <build-tree> _
# The owner's walk, reproduced: boot the pinned validation server over one build in its own compose project with an
# ephemeral loopback port, run repro.mjs against it as a host client, tear down.
set -euo pipefail
E=~/Documents/projects/delvewright-worktrees/wt-thing-beyond-fog
S=~/Documents/projects/delvewright-worktrees/tbf-scratch
B=$1; OUT=$2
eval "$(grep '^export EULA=' ~/.zshrc)"; echo "EULA=$EULA"; [ "$EULA" = TRUE ]
here=$E/validation
project=dw-tbf-repro   # STAND, TX, TZ: the stand cell and the tiller interaction
export DELVE_OUTPUT="$B"
export DELVE_DOCKERFILE="$here/Dockerfile.delve"
. "$here/lib/delve-image.sh"
dw_export_delve_image "$project"
. "$E/tools/lib/server-heap.sh"
COMPOSE=(docker compose -p "$project" -f "$here/compose.yaml" -f "$here/ephemeral-port.yaml" --profile validate)
cleanup() { "$here/fresh-volumes.sh" --project "$project" >/dev/null 2>&1 || true; }
trap cleanup EXIT
"$here/fresh-volumes.sh" --project "$project"
"${COMPOSE[@]}" up -d --build server pack
CID="$("${COMPOSE[@]}" ps -q server)"
for _ in $(seq 1 120); do
  h="$(docker inspect -f '{{.State.Health.Status}}' "$CID" 2>/dev/null || echo none)"
  [ "$h" = healthy ] && break
  sleep 5
done
echo "server health: $h"
[ "$h" = healthy ]
# setup finishes placement on a tick loop after boot; wait for its sentinel
for _ in $(seq 1 120); do
  r="$(docker exec "$CID" rcon-cli 'scoreboard players get #placed dw.sys' 2>&1 || true)"
  case "$r" in *"has 1 "*) break;; esac
  sleep 2
done
echo "placed: $r"
PORT="$("${COMPOSE[@]}" port server 25565 | sed 's/.*://')"
echo "port: $PORT"
( cd "$S/fog-net" && STAND="$STAND" TX="$TX" TZ="$TZ" MC_HOST=127.0.0.1 MC_PORT="$PORT" CONTAINER="$CID" RCON_MJS="$E/tools/lib/rcon.mjs" node repro.mjs )
echo "fog-timing exit: $?"
