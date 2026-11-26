# 📡 补丁雷达巡检报告

<!-- radar-new-red: 1 -->

- 巡检时间：`2026-11-26T10:31:46Z`（UTC）
- 范围：99 款带 Steam AppID 的游戏（非 Steam 游戏不巡检）
- 规则：Steam 公共分支 build 发布时间 ≤ 14 天算「刚更新」；框架资料 `hooksExe` 为 true 才亮红；build ≤ 90 天且修改器早于它超过 1 天亮黄。公告只展示，不参与判定。
- 没取到 build 信息的游戏，雷达字段保持上次的值不动；只是公告没取到的照常判定，公告标题和链接保留上次的值。

## 概览

| 🔴 红 | 🟡 黄 | 🟢 绿 | ⚪ 本次未取到 | 🚨 新变红 |
|:---:|:---:|:---:|:---:|:---:|
| 2 | 29 | 68 | 0 | 1 |

原因码：`recent-update-hooks` 2 · `recent-update` 15 · `trainer-behind` 14 · `quiet` 68

## 🚨 新变红（1）

这次是红灯，并且上次不是红灯、或者上次的 build 和这次不一样：

- **#60 杀手：暗杀世界** · AppID `1659040` · build `26758069`（2026-11-26）· 框架 [Simple Mod Framework](https://github.com/atampy25/simple-mod-framework) · 上次 `green` / build `26301025`

可直接转发的提醒（只写事实）：

```text
《杀手：暗杀世界》Steam 于 2026-11-26 更新。Simple Mod Framework 可能要等作者发新版才能用，带 Mod 玩的先别更新：Steam 库里右键游戏 → 属性 → 更新 → 改成「仅在启动时更新」。
```

## 🔴 红灯（2）

| # | 游戏 | 原因 | Steam build | 发布时间 (UTC) | 框架 | 新变红 |
|:---:|:---|:---|:---|:---|:---|:---:|
| 60 | 杀手：暗杀世界 | `recent-update-hooks` | `26758069` | 2026-11-26T10:05:20Z | [Simple Mod Framework](https://github.com/atampy25/simple-mod-framework) | 是 |
| 74 | 腐蚀 (本地自建服) | `recent-update-hooks` | `26898638` | 2026-11-25T03:24:10Z | [Oxide (uMod)](https://umod.org/games/rust) |  |

## 🟡 黄灯（29）

| # | 游戏 | 原因 | Steam build | 发布时间 (UTC) | 修改器更新 | 框架 / hooksExe |
|:---:|:---|:---|:---|:---|:---|:---|
| 3 | 巫师 3：狂猎 (次世代版 / 完全版) | `trainer-behind` | `26238013` | 2026-10-29T10:59:52Z | 2024-05-22 | — / `false` |
| 4 | 博德之门 3 | `trainer-behind` | `25605617` | 2026-09-29T14:55:18Z | 2025-04-16 | [BG3 Script Extender](https://github.com/Norbyte/bg3se) / `true` |
| 5 | 艾尔登法环 | `trainer-behind` | `25827938` | 2026-10-20T07:00:45Z | 2026-01-02 | [Mod Engine 2](https://github.com/soulsmods/ModEngine2) / `null` |
| 8 | 幻兽帕鲁 | `trainer-behind` | `25246127` | 2026-09-15T03:01:22Z | 2026-07-10 | [UE4SS Experimental (Palworld)](https://steamcommunity.com/sharedfiles/filedetails/?id=3625223587) / `false` |
| 15 | 骑马与砍杀 2：霸主 | `trainer-behind` | `26566465` | 2026-11-11T15:29:46Z | 2026-08-10 | [Harmony (Bannerlord.Harmony)](https://github.com/BUTR/Bannerlord.Harmony) / `false` |
| 17 | 泰拉瑞亚 | `recent-update` | `26902183` | 2026-11-24T19:15:44Z | 2026-09-16 | [tModLoader](https://github.com/tModLoader/tModLoader) / `false` |
| 18 | 霍格沃茨之遗 | `trainer-behind` | `26175237` | 2026-11-05T16:02:27Z | 2025-12-16 | — / `false` |
| 21 | 英灵神殿 | `recent-update` | `26870846` | 2026-11-25T09:48:52Z | 2026-09-23 | [BepInExPack Valheim](https://github.com/BepInEx/BepInEx) / `false` |
| 24 | 消逝的光芒 2 | `recent-update` | `26889205` | 2026-11-25T13:00:57Z | 2026-10-22 | — / `false` |
| 30 | 幸福工厂 | `recent-update` | `26728002` | 2026-11-18T16:22:51Z | 2026-06-07 | [Satisfactory Mod Loader (SML)](https://docs.ficsit.app/satisfactory-modding/latest/) / `false` |
| 31 | 异星工厂 | `recent-update` | `26700955` | 2026-11-23T14:36:23Z | — | — / `false` |
| 32 | 城市：天际线 | `recent-update` | `25432556` | 2026-11-24T08:59:00Z | — | — / `false` |
| 33 | 文明 6 | `recent-update` | `26595377` | 2026-11-19T18:59:18Z | 2022-12-22 | — / `false` |
| 34 | 十字军之王 3 | `recent-update` | `26785313` | 2026-11-19T14:45:41Z | 2026-10-10 | — / `false` |
| 35 | 钢铁雄心 4 | `recent-update` | `26733403` | 2026-11-19T13:59:46Z | 2026-06-14 | — / `false` |
| 36 | 群星 | `recent-update` | `26639410` | 2026-11-23T13:55:42Z | 2026-06-26 | — / `false` |
| 37 | 全面战争：战锤 3 | `recent-update` | `26810549` | 2026-11-20T12:03:21Z | 2026-09-29 | — / `false` |
| 38 | 全面战争：三国 | `trainer-behind` | `25370317` | 2026-09-17T14:04:42Z | 2025-12-06 | — / `false` |
| 54 | 毁灭战士：永恒 | `trainer-behind` | `25216728` | 2026-09-17T15:08:34Z | 2021-10-29 | — / `false` |
| 62 | 刺客信条：英灵殿 | `trainer-behind` | `26142239` | 2026-11-05T13:57:12Z | 2022-12-10 | [Forger patch manager](https://www.nexusmods.com/assassinscreedodyssey/mods/42) / `false` |
| 67 | 无人深空 | `recent-update` | `26924890` | 2026-11-25T15:50:47Z | 2026-09-13 | — / `false` |
| 68 | 异星探险家 | `trainer-behind` | `25599237` | 2026-10-14T16:49:53Z | 2021-04-07 | [AstroModLoader Classic](https://github.com/atenfyr/AstroModLoader-Classic) / `false` |
| 72 | 七日杀 | `trainer-behind` | `26309840` | 2026-11-02T17:00:28Z | 2026-10-06 | — / `false` |
| 75 | 流放者柯南 | `recent-update` | `26668213` | 2026-11-15T13:05:25Z | — | — / `false` |
| 76 | 中世纪王朝 | `trainer-behind` | `26431490` | 2026-11-10T13:56:03Z | 2026-06-25 | [Medieval Dynasty Mod Loader (MDML)](https://www.nexusmods.com/medievaldynasty/mods/30) / `null` |
| 81 | 欧洲卡车模拟 2 | `recent-update` | `26765198` | 2026-11-18T18:10:44Z | — | — / `false` |
| 82 | 雪地奔驰 | `trainer-behind` | `26218478` | 2026-11-02T09:55:58Z | 2022-12-28 | — / `false` |
| 85 | BeamNG.drive | `recent-update` | `26758896` | 2026-11-19T09:04:14Z | — | — / `false` |
| 90 | 尼尔：机械纪元 | `trainer-behind` | `26534214` | 2026-11-09T08:06:56Z | 2021-03-24 | — / `null` |

## ⚪ 本次未取到（0，字段保持上次的值）

无。

## 🟢 绿灯（68）

#1 赛博朋克 2077、#2 黑神话：悟空、#6 上古卷轴 5：天际重制版、#7 辐射 4、#9 星空、#10 侠盗猎车手 5、#11 荒野大镖客：救赎 2、#12 怪物猎人：世界、#13 只狼：影逝二度、#14 生化危机 4 重制版、#16 星露谷物语、#19 深海迷航、#20 黑暗之魂 3、#22 生化危机 8：村庄、#23 消逝的光芒、#25 辐射：新维加斯、#26 边缘世界、#27 僵尸毁灭工程、#28 森林、#29 森林之子、#39 龙之信条 2、#40 装甲核心 6：境界天火、#41 对马岛之魂：导演剪辑版、#42 战神 4、#43 漫威蜘蛛侠：重制版、#44 地平线：零之曙光、#45 往日不再、#46 死亡搁浅：导演剪辑版、#47 底特律：化身为人、#48 天国：拯救、#49 骑马与砍杀：战团、#50 潜行者：切尔诺贝利的阴影、#51 地铁：离去、#52 控制：终极版、#55 无主之地 3、#56 无主之地 2、#57 生化奇兵：无限、#58 羞辱 2、#59 掠食、#61 刺客信条：奥德赛、#63 刺客信条：起源、#64 孤岛惊魂 5、#65 孤岛惊魂 6、#66 看门狗 2、#69 木筏求生、#70 禁闭求生、#71 丛林地狱、#73 方舟：生存进化、#77 剑士、#78 模拟人生 4、#79 动物园之星、#80 侏罗纪世界：进化 2、#83 极限竞速：地平线 5、#84 神力科莎、#86 女神异闻录 5 皇家版、#87 女神异闻录 3 重制版、#88 最终幻想 7 重制版、#89 最终幻想 16、#91 破晓传说、#92 人中之龙 8、#93 人中之龙 7、#94 星球大战绝地：幸存者、#95 星球大战绝地：陨落的武士团、#96 死亡空间：重制版、#97 死亡细胞、#98 黑帝斯、#99 空洞骑士、#100 杀戮尖塔

## 🧩 框架资料

- 读到的文件：`part-1.json`（34 条）、`part-2.json`（33 条）、`part-3.json`（33 条）
- 覆盖：99 / 99 款巡检目标有可用条目；hooksExe true 13 · false 54 · null 32

<details>
<summary>全部 99 款明细</summary>

| # | 游戏 | 状态 | 原因 | Steam build | 发布时间 (UTC) | 修改器更新 | 最新公告 |
|:---:|:---|:---:|:---|:---|:---|:---|:---|
| 1 | 赛博朋克 2077 | 🟢 | `quiet` | `26161058` | 2026-10-23T13:33:24Z | 2026-10-28 | [REDstreams – Cyberpunk: Edgerunners 2](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1847286114045127) |
| 2 | 黑神话：悟空 | 🟢 | `quiet` | `21393610` | 2026-01-14T07:57:07Z | 2025-10-17 | [Black Myth: Wukong — 30% Off Coming Soon](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1840310314337994) |
| 3 | 巫师 3：狂猎 (次世代版 / 完全版) | 🟡 | `trainer-behind` | `26238013` | 2026-10-29T10:59:52Z | 2024-05-22 | [Patch 5.01 is live!](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1846018067929400) |
| 4 | 博德之门 3 | 🟡 | `trainer-behind` | `25605617` | 2026-09-29T14:55:18Z | 2025-04-16 | [Hotfix #36 Now Live!](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1827626365770693) |
| 5 | 艾尔登法环 | 🟡 | `trainer-behind` | `25827938` | 2026-10-20T07:00:45Z | 2026-01-02 | [Alexander, Warrior Jar Artisan Keycap h…](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1847920302237841) |
| 6 | 上古卷轴 5：天际重制版 | 🟢 | `quiet` | `24914197` | 2026-08-27T14:00:09Z | 2023-12-05 | [Celebrate 15 Years of Skyrim with the A…](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1849192144180604) |
| 7 | 辐射 4 | 🟢 | `quiet` | `24564252` | 2026-08-18T14:00:28Z | 2024-04-29 | [Happy Fallout Day!](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1847286114037070) |
| 8 | 幻兽帕鲁 | 🟡 | `trainer-behind` | `25246127` | 2026-09-15T03:01:22Z | 2026-07-10 | [Please Nominate Palworld for the "Just …](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1849827110442979) |
| 9 | 星空 | 🟢 | `quiet` | `23518663` | 2026-06-11T15:00:15Z | 2026-04-28 | [New worlds to explore with Starfield Cr…](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1835236783563685) |
| 10 | 侠盗猎车手 5 | 🟢 | `quiet` | `24129523` | 2026-07-14T09:01:57Z | 2024-09-19 | [Take Down the Kortz Center and More Hig…](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1848664643345005) |
| 11 | 荒野大镖客：救赎 2 | 🟢 | `quiet` | `13773296` | 2024-03-19T10:12:09Z | 2024-03-20 | [A Bustling Frontier Benefits All Roles …](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1833968530900662) |
| 12 | 怪物猎人：世界 | 🟢 | `quiet` | `15539686` | 2024-10-06T23:59:03Z | 2023-10-19 | [Monster Hunter: World has sold over 30 …](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1839041357022880) |
| 13 | 只狼：影逝二度 | 🟢 | `quiet` | `5794815` | 2020-11-20T01:00:31Z | 2020-10-29 | [Steam Awards are here!](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/2551782186276932328) |
| 14 | 生化危机 4 重制版 | 🟢 | `quiet` | `22377325` | 2026-03-31T01:02:33Z | 2026-02-04 | [Resident Evil Veronica Store Page now o…](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1834602721197786) |
| 15 | 骑马与砍杀 2：霸主 | 🟡 | `trainer-behind` | `26566465` | 2026-11-11T15:29:46Z | 2026-08-10 | [Patch Notes - WS v1.3.7 / BL v1.5.7](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1849192144179132) |
| 16 | 星露谷物语 | 🟢 | `quiet` | `16826371` | 2024-12-22T00:19:35Z | 2024-04-07 | [Stardew Valley Merchandise Spotlight](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1849827110433709) |
| 17 | 泰拉瑞亚 | 🟡 | `recent-update` | `26902183` | 2026-11-24T19:15:44Z | 2026-09-16 | [Terraria 1.4.6: Crossplay Phase One Lau…](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1849827110446549) |
| 18 | 霍格沃茨之遗 | 🟡 | `trainer-behind` | `26175237` | 2026-11-05T16:02:27Z | 2025-12-16 | [WB Games Celebrates Black Friday Saving…](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1849827110443178) |
| 19 | 深海迷航 | 🟢 | `quiet` | `20241558` | 2025-10-03T21:32:59Z | 2021-05-12 | [Subnautica Free Weekend & Series Sale](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1828894815555876) |
| 20 | 黑暗之魂 3 | 🟢 | `quiet` | `10167187` | 2023-01-12T09:00:58Z | 2023-01-15 | [ELDEN RING NIGHTREIGN - Official Pre-Or…](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1791580425958667) |
| 21 | 英灵神殿 | 🟡 | `recent-update` | `26870846` | 2026-11-25T09:48:52Z | 2026-09-23 | [Vote For Valheim in the Steam Awards!](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1850460852981078) |
| 22 | 生化危机 8：村庄 | 🟢 | `quiet` | `22373341` | 2026-03-31T01:03:35Z | 2026-02-04 | [Resident Evil Veronica Store Page now o…](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1834602721197803) |
| 23 | 消逝的光芒 | 🟢 | `quiet` | `24076292` | 2026-07-07T12:09:25Z | 2022-09-02 | [Steam Halloween Sale X Dying Light now …](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1847286114046170) |
| 24 | 消逝的光芒 2 | 🟡 | `recent-update` | `26889205` | 2026-11-25T13:00:57Z | 2026-10-22 | [CLAIM YOUR REWARDS Halloween Showdown 2…](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1849458702689537) |
| 25 | 辐射：新维加斯 | 🟢 | `quiet` | `1510068` | 2018-05-08T22:34:07Z | — | [Fallout Discounted for Steam Holiday De…](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/3819571572127262350) |
| 26 | 边缘世界 | 🟢 | `quiet` | `23969874` | 2026-06-30T17:12:35Z | — | [It's RimWorld's birthday!](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1847286114046348) |
| 27 | 僵尸毁灭工程 | 🟢 | `quiet` | `26486631` | 2026-11-09T14:03:25Z | — | [42.22.2 STABLE Released](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1848664643355564) |
| 28 | 森林 | 🟢 | `quiet` | `20229486` | 2025-10-03T17:00:09Z | — | [Unity security update](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1811772772517783) |
| 29 | 森林之子 | 🟢 | `quiet` | `20228174` | 2025-10-03T18:44:52Z | 2024-05-15 | [Unity security update](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1811772772517758) |
| 30 | 幸福工厂 | 🟡 | `recent-update` | `26728002` | 2026-11-18T16:22:51Z | 2026-06-07 | [Satisfactory Update v1.2.5.1](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1849827110424942) |
| 31 | 异星工厂 | 🟡 | `recent-update` | `26700955` | 2026-11-23T14:36:23Z | — | [Factorio 2.1.25 released as stable](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1849827110441907) |
| 32 | 城市：天际线 | 🟡 | `recent-update` | `25432556` | 2026-11-24T08:59:00Z | — | [Estates & Escapes is out now!](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1849827110445409) |
| 33 | 文明 6 | 🟡 | `recent-update` | `26595377` | 2026-11-19T18:59:18Z | 2022-12-22 | [Black Friday Deals on the Best of 2K.*](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1849827110443060) |
| 34 | 十字军之王 3 | 🟡 | `recent-update` | `26785313` | 2026-11-19T14:45:41Z | 2026-10-10 | [Update 1.21.0.3](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1849827110428649) |
| 35 | 钢铁雄心 4 | 🟡 | `recent-update` | `26733403` | 2026-11-19T13:59:46Z | 2026-06-14 | [Hearts of Iron IV \| To the Bitter End i…](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1849827110428488) |
| 36 | 群星 | 🟡 | `recent-update` | `26639410` | 2026-11-23T13:55:42Z | 2026-06-26 | [Stellaris: Willpower now available!](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1849827110441822) |
| 37 | 全面战争：战锤 3 | 🟡 | `recent-update` | `26810549` | 2026-11-20T12:03:21Z | 2026-09-29 | [Black Friday Sale NOW ON!](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1849458702690712) |
| 38 | 全面战争：三国 | 🟡 | `trainer-behind` | `25370317` | 2026-09-17T14:04:42Z | 2025-12-06 | [Black Friday Sale NOW ON!](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1849458702690723) |
| 39 | 龙之信条 2 | 🟢 | `quiet` | `26256634` | 2026-11-03T23:59:39Z | 2026-11-10 | [Delicious in Dungeon × Dragon's Dogma 2…](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1848557880477490) |
| 40 | 装甲核心 6：境界天火 | 🟢 | `quiet` | `21034069` | 2025-12-16T07:03:12Z | 2023-12-24 | [Release Note for 2025/12/16](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1818752592134841) |
| 41 | 对马岛之魂：导演剪辑版 | 🟢 | `quiet` | `23879181` | 2026-07-08T09:07:57Z | 2024-05-19 | [Improved DualSense Edge support for Gho…](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1836506165580043) |
| 42 | 战神 4 | 🟢 | `quiet` | `11168363` | 2023-05-22T17:15:18Z | 2022-01-22 | [God of War (2018) Available for Up To 6…](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/6250522009517172772) |
| 43 | 漫威蜘蛛侠：重制版 | 🟢 | `quiet` | `23986256` | 2026-07-08T09:10:12Z | 2023-06-22 | [Improved DualSense Edge support for Mar…](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1836506165580047) |
| 44 | 地平线：零之曙光 | 🟢 | `quiet` | `8040161` | 2022-01-26T10:02:24Z | 2020-11-25 | [Horizon Forbidden West Complete Edition…](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/5686430301718251854) |
| 45 | 往日不再 | 🟢 | `quiet` | `19221447` | 2025-07-21T19:21:03Z | 2025-04-26 | [Days Gone Beta Branch Option](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1813674388912015) |
| 46 | 死亡搁浅：导演剪辑版 | 🟢 | `quiet` | `13300582` | 2024-01-29T10:48:49Z | 2022-05-11 | [DEATH STRANDING COLLECTION AVAILABLE NOW](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1849827110430898) |
| 47 | 底特律：化身为人 | 🟢 | `quiet` | `12158144` | 2023-09-28T07:41:26Z | — | [Nominate us for the Labor of Love Steam…](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1784506359154638) |
| 48 | 天国：拯救 | 🟢 | `quiet` | `22623230` | 2026-04-14T15:01:15Z | 2019-07-18 | [Experience the music of Kingdom Come: D…](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1845383656386437) |
| 49 | 骑马与砍杀：战团 | 🟢 | `quiet` | `23983102` | 2026-07-02T11:33:58Z | — | [Viking Conquest 2.072](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1836506165567784) |
| 50 | 潜行者：切尔诺贝利的阴影 | 🟢 | `quiet` | `11567845` | 2023-06-27T10:12:10Z | — | [S.T.A.L.K.E.R.: Shadow of Chornobyl Enh…](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1799817379622830) |
| 51 | 地铁：离去 | 🟢 | `quiet` | `6544595` | 2021-04-15T08:03:41Z | 2021-05-09 | [METRO 2039 - Pre-order Now!](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1846018067944326) |
| 52 | 控制：终极版 | 🟢 | `quiet` | `21225456` | 2025-12-18T09:44:09Z | 2020-08-28 | [CONTROL Resonant Is Out Now!](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1846018067929793) |
| 54 | 毁灭战士：永恒 | 🟡 | `trainer-behind` | `25216728` | 2026-09-17T15:08:34Z | 2021-10-29 | [PC Mods Update](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1807332909579930) |
| 55 | 无主之地 3 | 🟢 | `quiet` | `15245523` | 2024-08-08T16:00:22Z | 2021-04-10 | [Black Friday Deals on the Best of 2K.*](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1849827110443073) |
| 56 | 无主之地 2 | 🟢 | `quiet` | `9218157` | 2022-08-04T22:23:57Z | — | [Black Friday Deals on the Best of 2K.*](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1849827110443068) |
| 57 | 生化奇兵：无限 | 🟢 | `quiet` | `10404041` | 2023-02-09T00:21:02Z | — | [Cozy Up with 2K: The Autumn Sale is Liv…](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1845383656383072) |
| 58 | 羞辱 2 | 🟢 | `quiet` | `17576867` | 2025-03-18T15:00:51Z | 2020-05-13 | [Free Content for Dishonored 2 & Death o…](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/3244179105161288005) |
| 59 | 掠食 | 🟢 | `quiet` | `5297220` | 2020-07-23T14:00:32Z | 2021-01-10 | [Prey: Mooncrash – Typhon Hunter Availab…](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/2416641943191178150) |
| 60 | 杀手：暗杀世界 | 🔴 | `recent-update-hooks` | `26758069` | 2026-11-26T10:05:20Z | 2026-11-07 | [Nominate HITMAN World of Assassination …](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1850460852981912) |
| 61 | 刺客信条：奥德赛 | 🟢 | `quiet` | `17083392` | 2025-02-04T14:00:22Z | 2020-11-28 | [AC Black Flag Resynced out now!](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1837955055363115) |
| 62 | 刺客信条：英灵殿 | 🟡 | `trainer-behind` | `26142239` | 2026-11-05T13:57:12Z | 2022-12-10 | [Assassin’s Creed Valhalla - Title Updat…](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1848664643341476) |
| 63 | 刺客信条：起源 | 🟢 | `quiet` | `16965472` | 2025-01-14T14:00:25Z | 2024-01-29 | [AC Black Flag Resynced out now!](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1837955055363117) |
| 64 | 孤岛惊魂 5 | 🟢 | `quiet` | `18766066` | 2025-07-01T08:34:06Z | — | [FARCRY 5 now 85% off](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1832700592786536) |
| 65 | 孤岛惊魂 6 | 🟢 | `quiet` | `11359732` | 2023-07-27T07:14:53Z | 2023-02-18 | [Celebrating Ubi40 w/ @MCFixer [STREAM R…](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1844751498223771) |
| 66 | 看门狗 2 | 🟢 | `quiet` | `11638094` | 2023-07-06T09:06:31Z | 2020-07-17 | [Achievements Unlocked for Watch Dogs 2](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1790848102593482) |
| 67 | 无人深空 | 🟡 | `recent-update` | `26924890` | 2026-11-25T15:50:47Z | 2026-09-13 | [5 Labor of Love nominations without a w…](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1850460852981401) |
| 68 | 异星探险家 | 🟡 | `trainer-behind` | `25599237` | 2026-10-14T16:49:53Z | 2021-04-07 | [Patch 1.45.1](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1846651706674984) |
| 69 | 木筏求生 | 🟢 | `quiet` | `22312909` | 2026-03-12T15:13:21Z | — | [Raft 1.1.01 Hotfix](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1826992588592889) |
| 70 | 禁闭求生 | 🟢 | `quiet` | `18247588` | 2025-05-12T17:02:33Z | 2024-05-15 | [Grounded 2 Update: The Toxic Tangle – A…](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1822556746169741) |
| 71 | 丛林地狱 | 🟢 | `quiet` | `21698250` | 2026-02-04T09:47:57Z | 2021-02-05 | [12 million survivors in Green Hell - Th…](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1831432155577478) |
| 72 | 七日杀 | 🟡 | `trainer-behind` | `26309840` | 2026-11-02T17:00:28Z | 2026-10-06 | [Developer Update: Bandits Are Coming in…](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1849458702694760) |
| 73 | 方舟：生存进化 | 🟢 | `quiet` | `21291776` | 2025-12-23T16:19:47Z | 2020-11-26 | [ARK Franchise Sale!](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1837955055357193) |
| 74 | 腐蚀 (本地自建服) | 🔴 | `recent-update-hooks` | `26898638` | 2026-11-25T03:24:10Z | — | [PRINTED AND POLISHED](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1848664643342609) |
| 75 | 流放者柯南 | 🟡 | `recent-update` | `26668213` | 2026-11-15T13:05:25Z | — | [(Re-release) November Hotfix 3.1.1](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1849458702686207) |
| 76 | 中世纪王朝 | 🟡 | `trainer-behind` | `26431490` | 2026-11-10T13:56:03Z | 2026-06-25 | [Steam Awards Nominations!](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1849827110442633) |
| 77 | 剑士 | 🟢 | `quiet` | `13871665` | 2024-04-01T16:47:52Z | — | [Community Update: 3 Million Copies Sold](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1833334318577664) |
| 78 | 模拟人生 4 | 🟢 | `quiet` | `25966929` | 2026-10-27T17:00:04Z | — | [Retirement Never Looked So Good](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1849827110443386) |
| 79 | 动物园之星 | 🟢 | `quiet` | `23333923` | 2026-05-28T14:00:02Z | 2020-12-16 | [Planet Zoo 2 - OUT NOW! 💚💚](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1846018067944132) |
| 80 | 侏罗纪世界：进化 2 | 🟢 | `quiet` | `18857191` | 2025-06-19T10:00:04Z | 2023-05-11 | [Jurassic World Evolution 3 is 33% off!](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1835236783574267) |
| 81 | 欧洲卡车模拟 2 | 🟡 | `recent-update` | `26765198` | 2026-11-18T18:10:44Z | — | [Isle of Ireland: Galway](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1849827110424837) |
| 82 | 雪地奔驰 | 🟡 | `trainer-behind` | `26218478` | 2026-11-02T09:55:58Z | 2022-12-28 | [Steam Awards 2026](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1849827110443142) |
| 83 | 极限竞速：地平线 5 | 🟢 | `quiet` | `21856128` | 2026-02-17T15:57:39Z | — | [Reward Car Build - November 20th](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1849827110432680) |
| 84 | 神力科莎 | 🟢 | `quiet` | `14923034` | 2024-07-03T20:16:12Z | — | [Assetto Corsa EVO is OUT NOW in Steam E…](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1789039014339855) |
| 85 | BeamNG.drive | 🟡 | `recent-update` | `26758896` | 2026-11-19T09:04:14Z | — | [Hotfixes for v0.40 Released](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1847286114029423) |
| 86 | 女神异闻录 5 皇家版 | 🟢 | `quiet` | `15515071` | 2024-09-06T00:09:16Z | 2024-09-13 | [Persona Anime Broadcast Sale](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1840310314352081) |
| 87 | 女神异闻录 3 重制版 | 🟢 | `quiet` | `22672075` | 2026-04-14T16:58:23Z | 2026-06-07 | [Persona Anime Broadcast Sale](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1840310314352061) |
| 88 | 最终幻想 7 重制版 | 🟢 | `quiet` | `21888968` | 2026-02-18T04:04:54Z | 2026-11-22 | [Prepurchase Available!](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1842846814445854) |
| 89 | 最终幻想 16 | 🟢 | `quiet` | `17373708` | 2025-03-04T03:09:09Z | 2024-09-17 | [SQUARE ENIX Publisher Sale 2026](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1826992588604014) |
| 90 | 尼尔：机械纪元 | 🟡 | `trainer-behind` | `26534214` | 2026-11-09T08:06:56Z | 2021-03-24 | [Bug Fix Notice](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1848664643354633) |
| 91 | 破晓传说 | 🟢 | `quiet` | `12823607` | 2023-12-12T01:00:21Z | 2024-02-22 | [Tales of Eternia Remastered is now avai…](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1846651706689775) |
| 92 | 人中之龙 8 | 🟢 | `quiet` | `17233673` | 2025-03-24T19:02:31Z | 2024-02-27 | [Save Up to 80% Off on Like a Dragon & Y…](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1849458702690862) |
| 93 | 人中之龙 7 | 🟢 | `quiet` | `7362542` | 2021-09-21T01:00:26Z | 2020-11-13 | [Save Up to 80% Off on Like a Dragon & Y…](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1849458702690848) |
| 94 | 星球大战绝地：幸存者 | 🟢 | `quiet` | `15643690` | 2024-09-12T14:00:39Z | 2025-06-09 | [Members get full access to 2 Star Wars™…](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1819386365102514) |
| 95 | 星球大战绝地：陨落的武士团 | 🟢 | `quiet` | `10360016` | 2023-01-31T12:09:17Z | 2019-11-18 | [May the 4th be with you](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1798454487642670) |
| 96 | 死亡空间：重制版 | 🟢 | `quiet` | `10602756` | 2023-02-27T16:08:18Z | 2023-01-30 | [Battlefield 2042 \| Dead Space](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/5842939267353603796) |
| 97 | 死亡细胞 | 🟢 | `quiet` | `23762174` | 2026-06-16T12:31:17Z | 2024-10-10 | [Dead Cells Stability Patch: Less Null A…](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1835236783570585) |
| 98 | 黑帝斯 | 🟢 | `quiet` | `10929685` | 2023-04-12T14:20:17Z | 2021-09-02 | [New Hades Merchandise!](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1849827110444301) |
| 99 | 空洞骑士 | 🟢 | `quiet` | `22529139` | 2026-03-27T07:37:27Z | 2023-07-13 | [Patch Version 1.5.12620 Now Live](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1828441623103525) |
| 100 | 杀戮尖塔 | 🟢 | `quiet` | `10180494` | 2022-12-20T00:56:37Z | — | [The Neowsletter - October 2026](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1847920302236890) |

</details>

---
*由 `scripts/steam_patch_monitor.py` 生成 · 规则见 `docs/RADAR_V2_CONTRACT.md` 第 2 节*
