# 原型 5：殖民模拟与自动化工厂 (Colony Sim & Automation)

## 📌 代表游戏与引擎映射
| 游戏名称 | Steam AppID | 引擎方案 | 核心控制台 / 注入工具 |
|---|---|---|---|
| 《边缘世界》(RimWorld) | 294100 | Unity (C# Mono) | 内置开发人员模式 (Dev Mode) + Harmony |
| 《异星工厂》(Factorio) | 427520 | 专有 C++ 引擎 | 原生 `/` / `/c` Lua 控制台 |
| 《幸福工厂》(Satisfactory) | 526870 | Unreal Engine 5 | `~` 原生控制台 + SMM (Satisfactory Mod Manager) |
| 《缺氧》(Oxygen Not Included) | 457140 | Unity (C#) | `debug_enable.txt` 调试模式 + Backspace 菜单 |
| 《戴森球计划》(Dyson Sphere Program) | 1366540 | Unity (C#) | BepInEx + DSP Cheat Mods |

---

## 🔍 四级精准技术检索 SOP (4-Tier Retrieval Queries)

### Tier 1: 官方开发者维基与 Lua API 手册
- `site:wiki.factorio.com "Console" "Commands" "Lua"`
- `site:rimworldwiki.com "Development mode" "Debug commands"`
- `"Oxygen Not Included" "debug commands" site:oxygennotincluded.fandom.com`

### Tier 2: 专有底层运行时与开源代码仓
- `site:github.com "pardeike/Harmony"` (RimWorld 基础 Hook 框架)
- `site:github.com "BepInEx" "DysonSphereProgram"`
- `site:github.com "satisfactorymodding"`

### Tier 3: 创意工坊与社区顶级模组
- 重点定位：Character Editor (边缘世界人物属性/特质编辑器)、Infinite Power (无限电力电网)、Instant Research (瞬时科技)、No Infestations (彻底禁用地下虫巢袭击)。

### Tier 4: 社群高频痛点与物流死锁解法
- `site:reddit.com/r/factorio "kill all biters command"`
- `site:reddit.com/r/RimWorld "resurrect pawn dev mode"`
- `"Satisfactory" "unlock alternate recipes command"`

---

## 🎯 八大系统维度全息核对清单 (Mandatory 8-Dimension Checklist)

1. **👑 殖民者生理心理锁死与特质自定义**：
   - 心情值永久锁死为 100%（永不发生悲观、绝望崩溃或屠杀狂暴）；
   - 一键清除所有伤残、毒瘾成瘾与慢性绝症，断肢器官瞬间再生治愈；
   - 技能全 20 级大师点满，添加双火热情与神级正面特质（神行客、超级免疫、坚韧）。
2. **🏭 蓝图瞬间建造与零材料秒落成**：
   - RimWorld 勾选 God Mode，点击任何高科技建筑（如宇宙飞船反应堆、地热发电机）瞬间平地落成；
   - 消除繁琐的搬运材料、平整地面与建筑工漫长施工等待。
3. **⚡ 科技树瞬间全开 (Instant Research Tree)**：
   - Factorio：`/c game.player.force.research_all_technologies()` 瞬间点亮从蒸汽机到星际火箭全部科技；
   - Satisfactory：一键解锁全部里程碑、MAM 硬盘分析与全部副产物替代配方。
4. **🔌 无限电力电网与热量/氧气平衡**：
   - 放置单格产生无限吉瓦电力的虚拟发电机，彻底告别电网过载断电停产危机；
   - 缺氧 (ONI)：一键调节气体压力与室内舒适温度，杜绝二氧化碳窒息与过热停机。
5. **🐛 外星异虫、污染威胁与袭击一键清除**：
   - Factorio：一键击杀全地图所有虫巢与潜伏异虫，彻底消除全图工业污染值（让虫子永久丧失进攻欲望）；
   - RimWorld：Dev Mode 一键平息当前突发海盗空投袭击或清除全地图机械族集群。
6. **📦 高级材料与物流实体精准生成**：
   - 在鼠标指定坐标或储物仓内直接注入海量精密零件、先进芯片、玻璃钢、铀燃料棒与太空合金。
7. **🌍 地图资源富集与无限矿脉**：
   - 将脚下的铜矿、铁矿、煤炭、原油泉修改为“无限储量”矿脉，永不枯竭，无需频繁搬迁采矿场。
8. **⏱️ 全局生产流水线百倍超频加速**：
   - 提升游戏全局时间流速至 5x / 10x，全自动流水线极速吞吐产出。

---

## ⚠️ 自动化沙盒模式排错与存档安全
1. **Factorio 成就警示**：在《异星工厂》中使用任何以 `/c` 开头的 Lua 脚本指令，系统会自动弹出确认警告，并永久禁用该存档的 Steam 官方成就；
2. **实体过多卡死防范**：切忌使用控制台一次性生成数万个散落物在地表，否则可能导致 Unity 物理寻路引擎堵塞并导致严重单核掉帧卡死。
