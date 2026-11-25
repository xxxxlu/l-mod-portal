# 原型 3：沙盒与生存建造 (Sandbox & Survival Crafting)

## 📌 代表游戏与引擎映射
| 游戏名称 | Steam AppID | 引擎方案 | 核心控制台 / 注入工具 |
|---|---|---|---|
| 《幻兽帕鲁》(Palworld) | 1623730 | Unreal Engine 5 | UE4SS + Palworld Save Tools / RCON |
| 《英灵神殿》(Valheim) | 892970 | Unity (Mono) | `-console` 原生控制台 + BepInEx |
| 《深海迷航》(Subnautica) | 264710 | Unity (Mono) | `F3+F8` 原生开发者面板 + QMods / BepInEx |
| 《雾锁王国》(Enshrouded) | 1203630 | Holistic 专有引擎 | Cheat Engine Table / FLiNG Trainer |
| 《方舟：生存飞升》(ARK: Survival Ascended) | 2399830 | Unreal Engine 5 | 原生 Tab 开发者控制台 |
| 《森林之子》(Sons of the Forest) | 1326470 | Unity | RedKit / BepInEx + Console Mods |

---

## 🔍 四级精准技术检索 SOP (4-Tier Retrieval Queries)

### Tier 1: 官方开发者 Wiki 与实体生成表 (Prefab / Entity Tables)
- `site:valheim.fandom.com "Console Commands" "spawn list"`
- `site:subnautica.fandom.com "Spawn IDs" "Commands"`
- `"Palworld" "Item IDs" "Pal IDs" site:palworld.wiki.gg`

### Tier 2: 专有底层运行时与开源代码仓
- `site:github.com "BepInEx" "Valheim"`
- `site:github.com "cheahjs/palworld-save-tools"`
- `site:github.com "SubnauticaModding"`

### Tier 3: Nexus Mods 权威专区 (热度与下载量倒排)
- 重点定位：自由建造无材料消耗、负重无限扩展、小地图战争迷雾完全驱散、战利品 100% 掉落、生物捕捉率 100% 强化。

### Tier 4: 社群高频痛点与存档卡死修复
- `site:reddit.com/r/Palworld "stuck under map" "teleport command"`
- `site:reddit.com/r/valheim "lost items on death" "recover command"`
- `"Subnautica" "cyclops stuck" "commands"`

---

## 🎯 八大系统维度全息核对清单 (Mandatory 8-Dimension Checklist)

1. **👑 核心生存锁死与无敌状态 (God & Immortality)**：
   - 生命、耐力、体能永久锁死不减；
   - 饥饿、口渴、体温（极寒/酷热）、氧气呼吸与辐射槽完全冻结；
   - 怪物无视（隐形幽灵模式 `ghost`），避免高阶掠食者干扰建造。
2. **🔨 自由建造与零材料消耗 (Free Crafting & Instant Build)**：
   - 激活上帝建造模式（`debugmode` -> 按 B 键免材料自由摆放建筑）；
   - 无视工作台等级、电力门槛与科技树先决条件直接合成所有顶级道具。
3. **🐾 实体生物召唤与捕捉率 100% (Entity / Pal Spawner)**：
   - 准星前方直接刷出指定稀有/闪光/传奇生物（如帕鲁唤冬兽、空涡龙）；
   - 捕兽夹、帕鲁球、恐龙捕捉麻醉弹 100% 必定捕获成功。
4. **🎒 负重无限与背包扩容 (Infinite Carry Weight)**：
   - 彻底解除石头、木材、矿石等超重导致无法奔跑的限制，背包负重设定为 999,999。
5. **📍 坐标瞬移与全图战争迷雾驱散 (Coordinates Teleport & Fog of War)**：
   - 瞬移至指定地下城、BOSS巢穴或死亡掉落包位置；
   - 一键解锁大地图所有传送塔与全景地形。
6. **🚀 飞行模式与穿透地表卡死脱出 (Free Flight & Noclip)**：
   - 任意开启穿墙飞行（如 Valheim 按 Z 自由飞天），轻松修筑摩天大厦与树屋；
   - 掉落穿模卡入地心时一键重置坐标返回地面。
7. **⏱️ 世界环境调控与掉落倍率 (Drop Rates & World Settings)**：
   - 采矿砍树掉落倍率调整为 10 倍，稀有遗迹素材掉率 100%；
   - 昼夜时间冻结（永昼/永夜自由设定），雨雪沙暴天气一键驱散。
8. **📦 科技点数与自动化流水线全开**：
   - 远古科技点数一键注入，解锁全套工业级自动化流水线与重型火器。

---

## 🚨 联机服务器防坑与专用服务器 (Dedicated Server) 规范
- **单人本地档 vs 联机服**：上述指令均针对**单人单机存档**；若在多人生存服使用，须通过服务器管理员后台认证密码（如 `adminpassword <pass>`）提权为 Admin 方可执行；
- **防档坏策略**：生成超大型生物时切忌在狭小基地内输入过大数量（如生成 100 只大型巨兽可能导致物理引擎崩溃卡死存档）。
