# Three Buttons and a Bell

> **Requires delve engine 0.64.0 or newer** — last verified with delvec 1.14.0 on Minecraft Java 1.21.11.

Merrow Landing is a keeper's house at the end of a jetty, and the keeper's boat
is in the shed behind it. Nothing in the house moves for a stranger: the bell
rope is tied up, the store door is barred, the keeper's chest stays shut, and
the shed gate's bolt is pinned fast. Speak to the keeper, do each thing in its
turn, and she will let you take the boat.

A demo level of about ten minutes, for one to four players. No fight.

## Who you will meet

- **Tamsin Merrow** keeps the landing, its bell and its boat. She stands at
  her counter in the hall, and she likes things done in their turn.

## Classes

- **Traveller** — road boots, bread and a flask. You came down the river road
  to borrow a boat.

## Playing it

Start the server, then in the Minecraft Java client at the version the marker
above names: Multiplayer → Direct Connect → the address the host gives you.
Accept the resource pack when the server offers it.

---

## For the owner: what to look for

This level is where "a click target always answers" (spec-0117) is looked at
in the game. Every thing in the house you can press is a real block — a bell,
a door, a chest, a lever, three buttons, a bolt, the keeper's candles, a
boulder, the boards of a barred door — and it answers every press, in every
state, with one line on your action bar and one refusal sound, to you alone.
Nothing opens, flips or shows its screen before its turn, and nothing glows
through a wall. The machine has proved that every state a press can be made in
carries a line (20 lines over 12 pressable things), that each line reaches the
one who pressed, and that the bot can walk the house in order. What it cannot
say is how any of it reads. Walk it once as the Traveller, and **press
everything before its turn, in its turn, and after it.**

You arrive on the jetty. The open doorway ahead and to the left goes into the
keeper's hall; the boarded door ahead and to the right is the store's door
onto the jetty.

1. **The boarded door, from the jetty.** Before anything else, right-click
   it, on any of its four boards. It should say it does not open from this
   side. Does that read as barred, and as a door that opens from somewhere
   else?
2. **Before you speak to the keeper, press everything in the hall.** Inside
   the doorway: the bell on the floor to your left, the boulder in the corner
   behind it, the three buttons low on the left wall, the bolt beside the
   barred shed gate on the far wall, the lever on the far wall behind the
   keeper, the store door and the chest on the right wall, and the keeper's
   four candles by the hearth to your right. Each should give one line and
   the refusal sound (a locked chest's click), and **nothing should move**:
   the door stays shut, the lever stays up, the chest shows no screen. Does
   each line read at the crosshair before it fades? Does the sound read as
   a refusal, not as a click that worked?
3. **The buttons and the bell click and spring by themselves.** A button
   still goes in and comes back out, and the bell still rings, when they
   refuse. Beside the line, does that confuse (it looks like it worked) or
   confirm (the press landed, and here is why nothing came of it)?
4. **The boulder, struck.** Left-click it with your hand. The first blow
   settles it into its socket and says so; every blow after that says it
   will not move again. The block itself does not move.
5. **Speak to the keeper.** She gives you her key and unties things. Now ring
   the bell (it rings and the step completes), then press it again (it says
   it has been rung). The lever can now be thrown once; press it again and
   it says it stays thrown, and it does not flip back.
6. **The store door.** Press it with an empty hand: it should say it is
   locked and that the key opens it. Hold the key and press: it unbars. From
   then on it is an ordinary door you open and shut by hand, and it says
   nothing. Before the key, did a door that does not budge read as barred,
   or as broken? After, does it read as the same door?
7. **The chest.** Open it once its turn comes (after the store door); after
   that it answers that it is empty and shows no screen.
8. **The three buttons and the bolt.** Press the bolt first: it says it is
   pinned. Press the three buttons (each knocks out a pin), then draw the
   bolt; the shed gate opens. Now press a button a fourth time: it should say
   the bolt is already drawn, and count nothing.
9. **The candles.** Once the keeper has spoken, pressing them offers a rest.
   Before that, they say they are hers.
10. **The store, and the glow.** Go through the store door. On the store side
    of the boarded door there is a stone button beside it, and it is outlined
    in light while you stand in the store within six blocks of it. Press the
    door from this side first, on any board: it should say the bar is on this
    side. Then press the button: the boards fall away. Before you open
    it, go back round to the jetty and look at the boarded door from there:
    **you should see no glow through or around the door.**
11. **With a second player:** stand beside a friend while they press any of
    these. You should read nothing and hear nothing; only the one who pressed
    gets the line.

Walk into the boat shed to finish.

## 给主人看的：要看什么

这一关用来在游戏里看「点的东西一定有回应」（spec-0117）。屋里每一样能按的东西都是真正的方块——一口钟、一扇门、一个箱子、一根拉杆、三个按钮、一根门闩、看守的蜡烛、一块大石头、一扇钉死的门上的木板——不管在什么状态下按，它都会回应：在你的动作栏上出一行字，配一声“拒绝”的音效，只给你一个人。没轮到的时候，门不会开，拉杆不会扳，箱子不会弹出界面，也没有任何东西隔着墙发光。机器已经证明：每一种能按的状态都有一行字（12 样能按的东西，共 20 行），每一行都只送到按的那个人，而且机器人能按顺序把屋子走完。它说不了的是这些读起来怎么样。以旅人的身份走一遍，**每样东西都在轮到之前、轮到之时、轮到之后各按一次。**

你出生在码头上。左前方开着的门洞通往看守的大厅；右前方那扇钉着木板的门，是库房朝码头的门。

1. **从码头这边按那扇木板门。** 先别做别的，右键它，四块木板按哪一块都行。它应该告诉你这一侧打不开。读起来是不是“被闩住了”，而且是一扇“从别处能打开”的门？
2. **和看守说话之前，把大厅里的东西都按一遍。** 进门以后：左手边地上的钟，钟后面角落里的大石头，左墙下方的三个按钮，正对面墙上封着铁栏的船棚门旁边的门闩，看守身后那面墙上的拉杆，右墙上的库房门和箱子，还有右手边炉子旁看守的四支蜡烛。每一样都应该给出一行字和那声拒绝音（像锁着的箱子那样咔哒一声），而且**什么都不应该动**：门关着，拉杆不扳，箱子不弹界面。每一行字在消失之前，能不能在准星附近读完？那个声音听起来像“被拒绝了”，还是像“按成功了”的咔哒？
3. **按钮和钟自己会动。** 被拒绝时，按钮照样会按下去再弹回来，钟照样会响。配上那行字，这是让人困惑（看起来好像成功了），还是让人确认（按到了，只是这就是没反应的原因）？
4. **用手打大石头。** 空手左键它。第一下它沉进凹槽，并告诉你；之后每一下都说它不会再动了。方块本身不会移动。
5. **和看守说话。** 她给你钥匙，把东西都解开。这时去敲钟（钟响，这一步完成），再按一次（它说已经敲过了）。拉杆现在能扳一次；再按，它说已经扳过了，并且不会弹回去。
6. **库房的门。** 空手去按：它应该说门锁着，钥匙能打开。拿着钥匙再按：门闩打开。从这以后它就是一扇普通的门，用手开关，什么都不说。拿到钥匙之前，一扇推不动的门读起来是“被闩住了”，还是“坏了”？之后，它读起来还是同一扇门吗？
7. **箱子。** 轮到它时（库房门之后）打开一次；之后再按，它说里面是空的，也不再弹出界面。
8. **三个按钮和门闩。** 先按门闩：它说被销子卡着。按下三个按钮（每个顶掉一根销子），再拉开门闩，船棚的门就开了。这时再按一次按钮：它应该说门闩早就拉开了，并且不再计数。
9. **蜡烛。** 看守说过话以后，按蜡烛就能歇息。在那之前，它们说这是她的蜡烛。
10. **库房，以及发光。** 穿过库房门。在那扇木板门的库房一侧，旁边有一个石头按钮；你站在库房里、离它六格以内时，它会被一圈光勾出来。先从这一侧按这扇门，哪块木板都行：它应该说门杠在这一侧。再按那个按钮：木板掉下来。在打开它之前，绕回码头，从那边看这扇木板门：**你应该看不到任何光透过门或从门边透出来。**
11. **有第二个玩家时：** 站在朋友旁边，让他去按其中任何一样。你应该什么都看不到、什么都听不到；只有按的那个人会收到那行字。

走进船棚即结束。
