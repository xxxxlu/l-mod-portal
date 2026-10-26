# 原型 6：肉鸽爬塔与牌组构筑 (Roguelike & Deckbuilder)

## 📌 代表游戏与引擎映射
| 游戏名称 | Steam AppID | 引擎方案 | 核心控制台 / 注入工具 |
|---|---|---|---|
| 《杀戮尖塔》(Slay the Spire) | 646570 | Java (LibGDX) | ModTheSpire + BaseMod 开发者控制台 |
| 《哈迪斯 1 & 2》(Hades I & II) | 1145360 / 1145350 | 自研 2D 引擎 (Lua) | 解包 `Content/Scripts/` Lua 注入 |
| 《小丑牌》(Balatro) | 2379780 | Love2D (Lua) | 源码解包 `game.lua` + Steamodded |
| 《死亡细胞》(Dead Cells) | 588650 | Haxe (Heaps.io) | 官方自定义模式 (Custom Mode) + Mods |
| 《雨中冒险 2》(Risk of Rain 2) | 632360 | Unity (C#) | BepInEx + DebugToolkit |
| 《以撒的结合：忏悔》(The Binding of Isaac: Repentance) | 250900 | 专有 C++ 引擎 | `options.ini` 开启 `EnableDebugConsole=1` |

---

## 🔍 四级精准技术检索 SOP (4-Tier Retrieval Queries)

### Tier 1: 官方数据维基与卡牌/遗物代码库
- `site:slay-the-spire.fandom.com "Console" "Commands" "Relic IDs"`
- `site:hades.fandom.com "Traits" "God Boons" "IDs"`
- `site:balatrogame.fandom.com "Jokers" "Vouchers"`
- `"Binding of Isaac" "debug console commands" "item IDs"`

### Tier 2: 专有底层运行时与开源代码仓
- `site:github.com "daviscook477/BaseMod"` (杀戮尖塔控制台基石)
- `site:github.com "Steamodded/sml"` (小丑牌模组装载器)
- `site:github.com "Risk-of-Thunder/R2API"`

### Tier 3: 创意工坊与 Thunderstore 权威模组
- 重点定位：Deck Editor (随心构筑初始牌库)、All Relics Spawner、Seed Reseeder (神种锁定与复现)、Unlock All Profiles (一键全收集全解锁通关存档)。

### Tier 4: 社群高频痛点与高难度进阶讨论
- `site:reddit.com/r/slaythespire "basemod console commands add card"`
- `site:reddit.com/r/balatro "unlock all jokers cheat"`
- `"Hades" "titan blood console command"`

---

## 🎯 八大系统维度全息核对清单 (Mandatory 8-Dimension Checklist)

1. **👑 初始卡组动态注入与牌库净化**：
   - 随心向牌库中直接添加金卡、神话卡与专属能力卡（如杀戮尖塔直接起手注入神化、回响形态、恶魔形态）；
   - 自由删除初始脆弱的白板打击牌与防御牌，甚至移除诅咒牌与虚无寄生牌。
2. **🃏 全套传说遗物、祝福与小丑牌图鉴一键入库**：
   - 小丑牌 (Balatro)：一键获取全部传说 Joker（如卡纳、特里布莱特、约里克），倍率轻松破百亿；
   - 杀戮尖塔：开局自选不朽遗物（日晷、死灵之书、鸟居、卡利珀）；
   - 哈迪斯：自选全套英雄级双重祝福与传奇祝福（雷神海神暴风雨、狩猎爱神心碎）。
3. **📈 进阶难度与热度等级秒级全开 (Ascension / Stake Unlock)**：
   - 杀戮尖塔：直接一键解锁全角色进阶 20 (A20) 极难门槛；
   - 小丑牌：直接解锁全部牌组的金色注额 (Gold Stake) 挑战；
   - 哈迪斯：自由设置 32+ 热度惩罚契约并轻松秒过。
4. **💎 永久局外元养成资源注入 (Meta Progression)**：
   - 哈迪斯：注入 999 泰坦之血、仙露、钻石与千万暗黑石，满级点满夜之圣镜与武器第四形态；
   - 死亡细胞：注入十万细胞，一键灌满传奇铸造炉提升全武器 S 级品质；
   - 杀戮尖塔：全角色等级一键满级，解锁全卡池。
5. **🌱 天胡随机数种子操控与锁定 (Seed Manipulation)**：
   - 复制或固定特定“神级天胡种子”，保证第 1 层必出核心遗物与关键商店；
   - 自由重摇（Reroll）随机数生成器。
6. **💰 局内金币、能量点与出牌上限无限**：
   - 局内金币 99,999，扫空途经的每个商人的所有商品；
   - 每回合能量点数锁定为 99 点，实现无尽永动机连招出牌。
7. **💀 锁血无敌与 Boss 一击必杀**：
   - 无论受到多高段连击伤害生命值永不归零；
   - 一键秒杀当前层 Boss（心智迷宫腐化之心、冥王哈迪斯）。
8. **📜 全画廊图鉴、纪念徽章与全成就达成**：
   - 点亮游戏内所有怪物图鉴、背景设定文献与全结局剧情过场。

---

## ⚠️ 肉鸽游戏模组环境防崩溃规范
1. **ModTheSpire 与 Steam 启动隔离**：杀戮尖塔在 Steam 启动时会明确提供“Play Slay the Spire”与“Play with Mods”两个独立启动通道，使用控制台必须选择后者；
2. **存档隔离机制**：主流肉鸽游戏会自动将模组存档与原版纯净存档拆分存放，保护原生云存档不被污染。
