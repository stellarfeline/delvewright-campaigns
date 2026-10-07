// The fog flash's network leg, measured on a client-equivalent path: a mineflayer
// client (the harness pin, 4.37.1) on the pinned server running The Thing Beyond the
// Fog's build. It boards the ferry, pulls the tiller as itself, and logs, against
// one monotonic clock, every packet the reveal is made of: the cutscene's camera
// (`camera`), the bolt (`spawn_entity` of minecraft:lightning_bolt) and the fog
// repaints (`chunk_biomes`, with the chunks each names). Every rcon reply is read
// through the shared rejection rule (tools/lib/rcon.mjs).
//
// env: MC_HOST, MC_PORT, CONTAINER (the server container id), NS, OUT (JSON path), RCON_MJS
import mineflayer from "mineflayer";
import { writeFileSync } from "node:fs";
// RCON_MJS: the engine checkout's tools/lib/rcon.mjs (the shared rejection rule).
const { rconChannel } = await import(process.env.RCON_MJS);

const host = process.env.MC_HOST ?? "127.0.0.1";
const port = Number(process.env.MC_PORT);
const rcon = rconChannel(process.env.CONTAINER);
const ns = process.env.NS ?? "the-thing-beyond-the-fog";
const name = "fog-probe";
const t0 = process.hrtime.bigint();
const now = () => Number(process.hrtime.bigint() - t0) / 1e6;
const events = [];
const log = (kind, data) => {
  const e = { t_ms: Math.round(now() * 10) / 10, kind, ...data };
  events.push(e);
  process.stderr.write(JSON.stringify(e) + "\n");
};
const delay = (ms) => new Promise((r) => setTimeout(r, ms));

const bot = mineflayer.createBot({ host, port, username: name, version: "1.21.11", auth: "offline" });
await new Promise((resolve, reject) => {
  bot.once("spawn", resolve);
  bot.once("kicked", (r) => reject(new Error(`kicked: ${r}`)));
  bot.once("error", reject);
});
log("spawn", { pos: bot.entity.position });
const reg = bot.registry;
const boltType = reg.entitiesByName["lightning_bolt"].id;
bot._client.on("chunk_biomes", (p) => {
  const chunks = (p.biomes ?? p.chunkBiomeData ?? []).map((c) => [c.position?.x ?? c.chunkX ?? c.x, c.position?.z ?? c.chunkZ ?? c.z]);
  log("chunk_biomes", { n: chunks.length, chunks });
});
bot._client.on("spawn_entity", (p) => {
  if (p.type === boltType) log("bolt", { x: p.x, y: p.y, z: p.z });
});
bot._client.on("camera", (p) => log("camera", { entity: p.cameraId }));
bot._client.on("game_state_change", (p) => log("game_state_change", { reason: p.reason, value: p.gameMode }));
bot._client.on("update_time", (p) => log("update_time", { age: String(p.age) }));

await delay(3000);
bot.chat("/trigger dw.class set 1");
await delay(2000);
log("rcon", { reply: await rcon.run(`tp ${name} 8204 64 8298`) });
log("rcon", { reply: await rcon.run(`scoreboard players set #party dw.f_boarded 1`) });
await delay(2000);
log("pull", {});
log("rcon", { reply: await rcon.probe(`execute as ${name} at @s run function ${ns}:trig_tiller`) });
await delay(16000);
log("pos_after", { pos: bot.entity.position });
writeFileSync(process.env.OUT, JSON.stringify({ host, port, events }, null, 1) + "\n");
bot.quit();
process.exit(0);
