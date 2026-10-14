# 空壳镇

> **Requires delve engine 0.43.0 or newer** — last verified with delvec 1.13.0 on Minecraft Java 1.21.11.

![从大车道望向索尔特洛的街](media/the-street-from-the-road.jpg)

索尔特洛原本是个捕鲱鱼的小镇，后来鱼群走了。秋天，镇上的人把能找到的大车全装满，搬去了内陆，能带走的东西一样没留。只有一个人多留了一潮：摆渡人安塞尔·塔罗。妹妹给他留了一个包裹，不拿到手，他不开船。

一个十分钟左右的演示关卡，一到四人。没有战斗。

## 你会遇见

- **安塞尔·塔罗**，索尔特洛的摆渡人。是他写信叫你们来的。他在码头上等着，一只眼睛盯着潮水。

## 职业

- **搬运者** —— 安塞尔的信，一盏提灯。别人没法回来取的东西，由你去搬。

## 开始游玩

启动服务器，然后用上方标记所写版本的 Minecraft Java 客户端：多人游戏 → 直接连接 → `localhost:25565`。服务器提示资源包时，请选择接受。

![索尔特洛俯瞰](media/saltlow-from-above.jpg)

---

## 给主人：这一关要看什么

这一关用来在游戏里检验"容器必须声明"（spec-0105）。机器已经证明了容器普查：六个容器——四个是摆设（两栋被搬空的房子里各一个箱子、一个木桶），一个是战利品（烟熏炉），一个是 `collect` 目标（装包裹的箱子）；没有哪个地点把摆设和要紧的容器混放在一起，也没有哪个地点的摆设容器超过两个；到达提示在机器人的选职业命令和传送之间送达。机器说不出来的是：这些东西**读起来**怎么样。请以搬运者的身份走一遍，遇到想开的东西就照常去开。

1. **到达时那一句提示，只出现一次。** 选好职业后，聊天栏会出现一行字，伴随木桶盖合上的声音：*Saltlow went inland in the autumn and took everything that would carry. Its barrels and chests stand empty now; only what was left on purpose is still here.*（中文客户端显示的是对应译文。）然后沿街往下走。这一句话能不能让你不去开织网匠小屋（左手第一扇门）和杂货铺（右手第一扇门）里的箱子和木桶？如果你还是开了，请留意那个空格子给你的感觉：是"提示说得对"，还是"提示被无视了"。
2. **装包裹的箱子看起来就是要紧的那个。** 安塞尔让你去玛拉的房子（码头前左手最后一扇门），取她床脚的箱子。那栋房子里只有这一个容器。不看提示的话，它摆在地铺旁边，能不能一眼认出就是它？
3. **装了东西的烟熏炉读起来像一次意外收获。** 熏鱼房（右手第二扇门）不在任务路线上。靠后墙的烟熏炉里有一条生鲑鱼、一块木炭，成品格里有两条熏鳕鱼。在一个被搬空的小镇里，它值不值得打开？有了到达提示在先，发现它时会不会让你意外？拿走鳕鱼之后，烟熏炉应该会点起火来熏那条鲑鱼——看看这是否读起来像熏鱼房又活了过来。
4. **每个盛物件都像是房间的一部分，并且在冒险模式下能取出东西。** 玛拉床边的箱子和熏鱼房的烟熏炉是这一关里装着东西的两个。它们应当像本来就属于那个房间的家具，而不是旁边临时加的一个盒子；在冒险模式下应当都能打开并取走里面的物品。（展示框、盔甲架和酿造台没有做：引擎目前还不能把它们作为盛物件放置，酿造台也不在建筑块允许清单里。）

### 这一关守住的那条拒绝规则

引擎会拒绝在要紧的容器旁边摆放摆设容器。我们复制了一份这个关卡，在玛拉的房子（装包裹的箱子所在的房间）里多放了一个木桶，构建随即停止（退出码 3）：

```
container census: 7 container cell(s) in the assembled world (minecraft:barrel: 3, minecraft:chest: 3, minecraft:smoker: 1); 1 loot, 1 collect, 0 device, 5 decoration; notice declared; by place: node/chandlers: 2, node/marras-house: 2, node/net-house: 2, node/smokehouse: 1; arrangement: 1 mixed place(s), 0 over the cap of 2 decoration cell(s) per place.
DW1024 [error] build: 1 mixed place(s) and 0 place(s) over the cap of 2 scenery container cell(s): scenery containers stay few, and a container that matters never stands among them.
  MIXED — `node/marras-house`: the container(s) that matter, `minecraft:chest` at [8222, 64, 8197] (collect `obj/fetch-the-parcel`), stand among the scenery container(s) `minecraft:barrel` at [8226, 64, 8198] (scenery). A player searching for what matters opens every one of them. Fill every scenery container in this place so each pays off, replace it in the place's piece or program with furniture that is not a container, or move the one that matters to a place where every container pays off. A trap among loot is allowed; a needed item among empty containers is not.
```

带着包裹去和安塞尔说话，关卡就结束了。
