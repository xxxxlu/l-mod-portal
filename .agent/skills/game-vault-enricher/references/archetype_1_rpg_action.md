# 原型 1：开放世界动作 RPG (Open World Action RPG)

## 📌 代表游戏与引擎映射
| 游戏名称 | Steam AppID | 引擎方案 | 核心控制台 / 注入工具 |
|---|---|---|---|
| 《赛博朋克 2077》(Cyberpunk 2077) | 1091500 | REDengine 4 | Cyber Engine Tweaks (CET Lua) |
| 《巫师 3：狂猎 次世代版》(The Witcher 3: Complete Edition) | 292030 | REDengine 3 | `general.ini` 原生调试控制台 (Next-Gen v4.04+) |
| 《上古卷轴 5：天际》(Skyrim SE/AE) | 489830 | Creation Engine 1 | 原生 `~` 控制台 + SKSE64 |
| 《辐射 4》(Fallout 4) | 377160 | Creation Engine 1 | 原生 `~` 控制台 + F4SE |
| 《星空》(Starfield) | 1716740 | Creation Engine 2 | 原生 `~` 控制台 + SFSE |
| 《刺客信条》系列 (Assassin's Creed) | 各种 | AnvilNext 2.0 | Cheat Engine 表 / AnvilToolkit |

---

## 🔍 四级精准技术检索 SOP (4-Tier Retrieval Queries)

在挖掘此类游戏作弊与 Mod 数据时，必须按以下模板执行结构化检索：

### Tier 1: 官方与开发者数据维基 (Developer Wikis & Dumped Databases)
- **检索关键词模板**：
  - `site:redmodding.org "<GameName>" "gamedata"`
  - `site:uesp.net "Skyrim" "Console Commands" "FormID"`
  - `site:fallout.fandom.com "Fallout 4 console commands" "item IDs"`
  - `"Witcher 3" "console commands" site:witcher.fandom.com`

### Tier 2: 专有底层运行时与开源代码仓 (GitHub Repos & Frameworks)
- **检索关键词模板**：
  - `site:github.com "Cyber Engine Tweaks" "AddToInventory"`
  - `site:github.com "SKSE64" OR "F4SE" "plugins"`
  - `site:github.com "WitcherScript" "console"`

### Tier 3: Nexus Mods 权威专区 (Nexus Mods Architecture)
- 进入目标专区，按 **Downloads (全周期下载量)** 与 **Endorsements (点赞数)** 倒排；
- 重点定位：前置核心库（CET, SKSE, Script Extenders）、全物品箱（Item Spawner）、大地图探索标记增强、无负重限制模组；
- 分析其 `requirements` 依赖链与 Steam 绝对安装路径规范。

### Tier 4: 玩家社群高频痛点与结局规避 (Community Pain Points)
- **检索关键词模板**：
  - `site:reddit.com/r/cyberpunkgame "secret ending" "console command" "SetFactStr"`
  - `site:reddit.com/r/witcher "missable gwent cards" "command"`
  - `"missable quests" "stage ID" "setstage"`

---

## 🎯 八大系统维度全息核对清单 (Mandatory 8-Dimension Checklist)

1. **👑 核心生存与无敌机制**：
   - 完全无敌上帝模式（锁定生命、法印护盾与抗性）；
   - 异常状态与跌落伤害免疫（摔落不死、辐射/中毒免疫）；
   - 瞬间治愈满血满状态与脱离卡死（穿墙 `tcl` / 瞬移 `teleport`）。
2. **💰 货币、负重与属性养成**：
   - 货币无限增加（欧元、克朗、瓶盖、金币）；
   - 背包负重上限扩充或锁死为无限（`Horse Bag 3`, `player.setav carryweight`）；
   - 专精技能点数直升、全技能树点亮与免费洗点。
3. **⚔️ 全套传奇/不朽专属神器与套装 Preset**：
   - 绝版不朽武器的专属识别码或 Hex ID（如 2077 `Preset_Katana_Saburo`、巫师3 `Aerondight EP2`、老滚5 破晓者 `0004E4EE`）；
   - 全套宗师级学派套装、神珍护甲全套一键注入。
4. **🦾 特色核心系统绝学**：
   - 赛博朋克：顶级 5++ 阶斯安威斯坦、网络接入仓、黑墙网关；
   - 巫师 3：全套突变诱发物、高等煎药、炼金魔药；
   - 老滚 5：全龙吼一键习得、毁灭系大师魔法。
5. **🚗 载具与坐骑全图鉴激活**：
   - 车库全买断、标志性超级跑车/机车独立召唤；
   - 顶级马鞍与防惊吓马盲目镜、无限马匹耐力。
6. **📜 任务 Fact 标志位、隐藏结局与救赎**：
   - 修复对话选错锁死的隐藏分支（如 2077 单挑荒坂塔 `sq032_johnny_friend = 1`）；
   - 拯救绝版 NPC、跳过恶性卡关 Bug、解除全员跨性别恋爱限制。
7. **⏱️ 昼夜时间掌控与环境调控**：
   - 世界时间精确时分秒设置（正午打光与赛博雨夜拍照）；
   - 消除全城通缉警星（消除 NCPD 追击 / 消除卫兵赏金）。
8. **🃏 游戏内置迷你游戏与全图鉴收集**：
   - 巫师 3 昆特牌全阵营收集与秒胜；
   - 天际全黑降 Crimson Nirnroot 任务道具一键补齐。

---

## 🚨 存档保护与版本防损红线
1. **跨版本升级崩档排查**：大型次世代补丁（如 2077 2.0+、巫师3 Next-Gen 4.0+）全面废弃了旧版技能树与装备 ID，严禁混入旧版淘汰 ID；
2. **存档物理路径快速备份**：
   - 2077：`%UserProfile%\Saved Games\CD Projekt Red\Cyberpunk 2077\`
   - 巫师 3：`%UserProfile%\Documents\The Witcher 3\gamesaves\`
   - 老滚 5：`%UserProfile%\Documents\My Games\Skyrim Special Edition\Saves\`
