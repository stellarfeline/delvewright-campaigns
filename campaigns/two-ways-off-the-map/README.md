# Two Ways Off the Map

> **Requires delve engine 0.63.0 or newer** — last verified with delvec 1.15.0 on Minecraft Java 1.21.11.

A chapel stands on a rock in the sea, its yard walled against the wind. The
boat that takes you off the rock waits at the end of the jetty, and the only
way to the jetty is the old broken wall-walk over the cistern, leapt gap by
gap.

A demo level of five minutes or so, for one to four players. No fight.

## Classes

- **Visitor** — four loaves of bread. You came to see the chapel, and the boat
  is leaving.

## Playing it

Start the server, then in the Minecraft Java client at the version the marker
above names: Multiplayer → Direct Connect → the address the host gives you.
Accept the resource pack when the server offers it.

---

## For the owner: what to look for

This demo level shows one thing: **you can only be where the game lets a body
be.** Before it shipped, the engine flew every jump, fall and swim a player can
make from every place you can stand, and refused two shapes that let a player
off the map: a jump out of the yard into a walled strip with no way back, and a
jump off the jetty into a sea with no way out. Both were rebuilt as they were
found, refused, and repaired. Walk it once as the visitor, and try hard to get
off the map.

1. **The stone (the yard).** In the yard, one low stone stands in front of the
   buttress against the east wall. From the stone, try to sprint-jump onto the
   buttress, and from the buttress over the wall. Can you? The stone was one
   cell closer when the engine refused the yard: from there the two jumps
   reached the wall top and dropped a body into the old burying ground behind
   it, walled high on every side. Try the other stones and the corners too:
   can you get onto any wall at all?
2. **The plank (the jetty).** Halfway out along the jetty, a block of planks
   stands against the rail. Jump from it over the rail into the sea. Can you
   swim back and climb out? The way out is the stair off the jetty's side near
   its head. Without that stair the engine refused the jetty: from the plank a
   body gets onto the rail and over it, and nothing round the sea is low enough
   to climb out on.
3. **The lid (the wall-walk).** The wall-walk is five leaps: one, two and three
   gaps on the flat, two gaps up onto the high platform, and three gaps down off
   it under a stone lid laid across the cistern's walls. Does every leap feel
   makeable on a sprint, the last one too with the lid over your head? The
   bot has already made all five. Fall into the cistern on purpose: you land
   in water, and the one stair, at the near end by the gate, brings you back
   up onto the first platform, so a fall starts the course again. Is there any
   way out of the water but that stair, or any way to the jetty but the five
   leaps?

The machine has already confirmed: from every place a body can reach, by every
walk, fall, jump, swim and climb out the game's physics allows, a body can get
back to the way through, and nobody in the sea or the cistern is stranded;
a body that falls into the cistern lands in water, unhurt, and the bot has
waded from under the high platform back up the stair to the first platform; each of the five
leaps lands from every facing within five degrees of straight and either of the
last two ticks before the edge, under the game's rules and the bot's; and a
sixth leap of five columns on the flat was refused because not every one of
those landings makes it. What you judge is whether, playing, you can find a way
off the map that the machine missed.

## 给主人看的：要看什么

这个演示关卡只展示一件事：**你只能去到游戏允许一个身体去到的地方。** 发布之前，引擎从每一个你能站的地方，把玩家能做的每一次跳、每一次落、每一次游都飞了一遍，并且拒绝了两种能让玩家离开地图的形状：一种是从院子里跳进一条四面高墙、出不来的窄地；另一种是从栈桥上跳进海里、再也爬不上来。这两处都先按发现时的样子造出来，被拒绝，再修好。以访客的身份走一遍，使劲想办法离开地图。

1. **那块石头（院子）。** 院子里，东墙扶壁前面立着一块矮石头。从石头上助跑，试着跳上扶壁，再从扶壁跳过墙去。跳得过去吗？引擎拒绝这座院子的时候，石头离扶壁近一格：从那里，两跳就能上到墙头，再落进墙后那片四面高墙围着的旧墓地。其他石头和墙角也都试一试：你能爬上任何一面墙吗？
2. **那块木板（栈桥）。** 沿栈桥走到一半，栏杆边立着一块木板。从它上面跳过栏杆进海里。你能游回来、爬上岸吗？出路是栈桥靠近尽头那一侧下水的台阶。没有那道台阶的时候，引擎拒绝了这座栈桥：从木板上，一个身体能上到栏杆顶再翻过去，而海的四周没有一处低到能爬上来。
3. **那块石盖板（墙头步道）。** 墙头步道要跳五次：平地上隔一格、两格、三格各一次，隔两格往上跳到高台，再从高台隔三格往下跳——这一跳头顶上横着一块搭在蓄水池两边墙上的石盖板。助跑的话，每一跳感觉都跳得过去吗，包括头顶压着石盖板的最后一跳？机器人已经把五跳都跳过了。故意掉进蓄水池：你会落进水里，只有靠近大门那一头的一道台阶能把你带回第一个平台——掉下去就从头再来。除了这道台阶，水里还有别的路能上去吗？除了这五跳，还有别的路能到栈桥吗？

机器已经确认：从一个身体能到达的每一个地方，沿着游戏物理允许的每一种走、落、跳、游和爬出水，身体都能回到正路上，海里和蓄水池里都没有人会被困住；掉进蓄水池的身体落在水里，毫发无伤，机器人已经从高台下面蹚水走回台阶、上到第一个平台；五次跳跃中的每一次，朝向偏离正前方五度以内、在边缘前最后两个刻里任意一刻起跳，按游戏的规则和机器人的物理都能落稳；另有一次平地隔四格（五列）的第六跳被拒绝了，因为不是每一种起跳都能落稳。你要判断的只是：真正玩起来，你能不能找到一条机器漏掉的、离开地图的路。
