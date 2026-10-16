# 一物置于一处

> **Requires delve engine 0.51.0 or newer** — last verified with delvec 1.13.0 on Minecraft Java 1.21.11.

![从进场的位置看礼拜堂正厅，顺着过道望向祭坛](media/nave.jpg)

明天天一亮，温丁十字的男丁要到礼拜堂来应名，名字由阁楼上的人念。那份名册在圣器室的箱子里躺了一整年。今晚得把它送上阁楼的楼梯，摆上读经台，再在台子上方的钩子上挂一盏灯，好让守夜的人看得见名册还在。

一到四人，十来分钟。你在黄昏时分到来，身份是**教区文书**，身上带着圣器室的钥匙和一点面包。

## 怎么玩

先启动服务器，再用上面那行标注的版本打开 Minecraft Java 版客户端：多人游戏 → 直接连接 → `localhost:25565`。服务器会推送资源包，请接受：中文文本就在里面。

## 这一关要演示什么

这是“**把东西放到一个地方**”的演示关。凡是写着“放”“挂”“交”的目标，只有东西真的离开你的手、留在那个地方时才算完成：你把它拿在手上，对着那个地方使用，就在那一下，背包里少了一件。引擎还会拿每个目标的第一个动词去对照真正让它完成的动作；标题说的是一回事、奖励的是另一回事，就拒绝构建。

## 要留意的地方

1. **光走到那里什么也不会完成。** 先什么都别拿，顺着西墙边的楼梯上到阁楼。读经台和铁链下的钩子已经在那儿了。站到它们跟前，有没有哪个目标完成？空着手去用读经台：是不是只出来一句话，说名册该放在这里，别的什么也没发生？
2. **点下去的那一刻，名册离手。** 从祭坛旁的圣器室箱子里取出名册。打开背包：应该有一份《温丁十字征召名册》。上到阁楼，把名册拿在手上，对读经台使用。点下去的那一刻，名册是不是就从背包里没了？“把名册放上读经台”是不是也在同一下完成？
3. **读经台上看得见它。** 读经台的斜面上，现在是不是摊着一本书？（想打开也可以，见下面“这一关没有演示的东西”。）
4. **灯也是一样。** 从楼梯脚下的木桶里取出守夜灯，再上阁楼，拿在手上，对读经台旁那条铁链的下端使用。点下去时灯是不是离了手？铁链下是不是挂上了一盏灯，照亮了读经台？
5. **手里拿错了东西。** 拿着名册去点钩子，或者拿着灯去点读经台。是不是不认，手里的东西也还在？
6. **两个人一起。** 如果有第二位玩家，让一个人拿着名册，另一个人空手去点读经台。是不是只有递上名册的那位才算完成，也只有那位的名册被拿走？

## 机器验证记录

最终发布的构建（`delvec build`，退出码 0，构建两次，逐字节相同：115 个文件）：

```
act binding (DW1045): 4 of 4 English title(s) read against 4 objective(s); 0 head(s) the lexicon does not know; 0 untitled; 0 refused
```

- PackTest：21 项必过测试全部通过，其中包括 `verb_interact`：它在玩家手上和背包里各放一份名册，点一下读经台，确认目标已完成、名册数量少了一份（2 变 1）。
- 机器人走关键路径：6 步全部通过——选职业、开箱子、开木桶、拿着名册用读经台、拿着灯用钩子、结局。
- 服务器实际写出的世界与引擎的模型在每个比对格（1153 格）上都一致，只有 2 格草方块被墙压成了泥土。
- 把名册那个目标的 `takes_item` 去掉，构建就会被拒：

```
DW1045 [error] quests /content/quests/0/objectives/2/title: objective `obj/lay-the-roll` is titled "Lay the roll on the lectern": its head `lay` → give, and its completion `interact + requires_item` → use, present, so the title tells the player to do something the game does not reward (spec-0114). Either change the completion to the act the title names: add `takes_item: true`, so one `minecraft:paper` leaves the hand that presents it; or re-head the title with a word of what the completion performs (use, present: `use`, `present`, `activate`)
```

- 上线检查（staging gate）：135 项中有 2 项没有绑定，都是演示关本来就没有的设计记录（`drill3-01`、`drill3-03`）。要开服，需要用这道检查自带的放行参数。

## 这一关没有演示的东西

- **读经台上的名册读不了。** 读经台显示出一本书，是因为方块本身标着“有书”，而放置一个方块能说的也就这么多：书里写了什么，写不进去。打开读经台，书是空白的。冒险模式下书拿不下来，所以名册会一直摆在那里。
- **摆在读经台上的是一本书，拿在手里的是一张纸。** 读经台上只能显示书。
