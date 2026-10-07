// Repro: board, stand at STAND, pull the tiller by the real interaction path (a right-click
// recorded on the tiller's interaction entity, as the tick reads it), wait out the scene,
// report where the client ends up; then a second pull.
import mineflayer from "mineflayer";
const { rconChannel } = await import(process.env.RCON_MJS);
const rcon = rconChannel(process.env.CONTAINER);
const name = "repro-probe";
const delay = (ms) => new Promise((r) => setTimeout(r, ms));
const stand = (process.env.STAND ?? "8204 64 8298").split(" ").map(Number);
const bot = mineflayer.createBot({ host: "127.0.0.1", port: Number(process.env.MC_PORT), username: name, version: "1.21.11", auth: "offline" });
await new Promise((res, rej) => { bot.once("spawn", res); bot.once("kicked", rej); bot.once("error", rej); });
const out = { stand, events: [] };
const say = (k, v) => { out.events.push([k, v]); process.stderr.write(`${k} ${JSON.stringify(v)}\n`); };
await delay(2500);
bot.chat("/trigger dw.class set 1");
await delay(2500);
say("tp", await rcon.run(`tp ${name} ${stand[0] + 0.5} ${stand[1]} ${stand[2] + 0.5}`));
await delay(1500);
say("board", await rcon.run(`scoreboard players set #party dw.f_boarded 1`));
const pull = async (label) => {
  const e = Object.values(bot.entities).find((x) => x.name === "interaction" && Math.abs(x.position.x - Number(process.env.TX)) < 1 && Math.abs(x.position.z - Number(process.env.TZ)) < 1);
  say(label + ":interaction", e ? e.position : null);
  if (e) bot.activateEntity(e);
};
await pull("pull1");
await delay(14000);
say("after1", bot.entity.position);
say("tp", await rcon.run(`tp ${name} ${stand[0] + 0.5} ${stand[1]} ${stand[2] + 0.5}`));
await delay(1500);
await pull("pull2");
await delay(3000);
say("effects2", Object.keys(bot.entity.effects ?? {}));
await delay(10000);
say("after2", bot.entity.position);
console.log(JSON.stringify(out));
bot.quit(); process.exit(0);
