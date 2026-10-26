# 原型 4：P社与 4X 宏观战略 (Grand Strategy & 4X)

## 📌 代表游戏与引擎映射
| 游戏名称 | Steam AppID | 引擎方案 | 核心控制台 / 注入工具 |
|---|---|---|---|
| 《钢铁雄心 4》(Hearts of Iron IV) | 394360 | Clausewitz Engine | 原生 `~` 控制台 (需非铁人模式) |
| 《群星》(Stellaris) | 281990 | Clausewitz Engine | 原生 `~` 控制台 |
| 《十字军之王 3》(Crusader Kings III) | 1158310 | Clausewitz Engine | `-debug_mode` 启动参数 + 原生控制台 |
| 《维多利亚 3》(Victoria 3) | 529340 | Clausewitz Engine | `-debug_mode` 启动参数 + 原生控制台 |
| 《文明 6》(Civilization VI) | 289070 | Firaxis 专有引擎 | `AppOptions.txt` 启用调试菜单 |
| 《全面战争：战锤 3》(Total War: Warhammer III) | 1142710 | TW Engine 3 | Mod Configuration Tool (MCT) / CT |

---

## 🔍 四级精准技术检索 SOP (4-Tier Retrieval Queries)

### Tier 1: 官方与社区 P社维基 (ParadoxWikis)
- `site:hoi4.paradoxwikis.com "Console commands"`
- `site:stellaris.paradoxwikis.com "Console commands"`
- `site:ck3.paradoxwikis.com "Console commands"`
- `"Civilization VI" "debug console" site:civilization.fandom.com`

### Tier 2: 游戏安装目录事件与决策文件挖掘 (Local Game Files)
- 探索本地国家与事件源码：
  - `<HOI4>\common\national_focus\` (全焦点国策内部 ID)
  - `<HOI4>\events\` (历史事件与随机突发事件触发器)
  - `<CK3>\game\common\traits\` (人物特质与血统基因代码)

### Tier 3: Steam 创意工坊与 Nexus 权威工具 (Workshops & Overhauls)
- 重点定位：Toolpack (全功能图形化沙盒编辑工具)、Easy Cheat Menu、No Division Limit (无指挥官带兵上限)、Instant War (无视世界紧张度即时宣战)。

### Tier 4: 社群高频痛点与国策死锁绕过
- `site:reddit.com/r/hoi4 "ai ic cheat" "fix"`
- `site:reddit.com/r/Stellaris "faster megastructure command"`
- `"ck3" "remove stress command" "trait id"`

---

## 🎯 八大系统维度全息核对清单 (Mandatory 8-Dimension Checklist)

1. **👑 政权接管与全球国家自由切换 (`tag`)**：
   - 随时输入 `tag <TAG>` (如 `tag GER`, `tag SOV`, `tag USA`, `tag CHI`)，瞬间接管任何主要国家或附属国，调配其内阁与内政。
2. **⚡ 瞬间建造与全科技秒速研发 (Instant Construction & Tech)**：
   - `ic`：军工厂、民用工厂、海军船坞、雷达站、核反应堆秒速落成；
   - `research all`：瞬间点亮全部科技树（含四代喷气战机、现代主战坦克与原子弹）。
3. **📜 瞬间国策树焦点与决策解锁 (Focus & Decisions)**：
   - `focus.autocomplete` / `fa`：告别漫长的 70 天等待，国策瞬间点击即刻完成；
   - `focus.nochecks` & `decision.nochecks`：打破所有互斥选项与前置要求限制。
4. **🤝 外交强制无条件服从 (`yesman`)**：
   - 输入 `yesman`，强制所有 AI 国家 100% 同意你的宣战、同盟请求、租借军火法案与屈辱停战条款。
5. **💰 政治点数、指挥点数与战略储备拉满**：
   - `pp 2000` (政治点数自由更换法案与部长)、`cp 100` (指挥力拉满开启强攻)、`fuel 1000000` (百万燃油储备)。
6. **👥 行省适役人口与三军装备无限列装**：
   - `manpower 10000000` (瞬间注入千万适役兵源)；
   - `ale 50000` (向军火库注入 50,000 件全套先进单兵步枪、自行火炮与坦克)。
7. **🌫️ 全球战争迷雾完全驱散 (`fow`)**：
   - 输入 `fow` (Fog of War) 驱散全陆地与公海迷雾，实时洞悉全球敌军海陆空师团集结动态与潜艇位置。
8. **🕊️ 疆域吞并、傀儡政权与白和平停战**：
   - `annex <TAG>` 瞬间将目标国家版图直接并入本国版图；
   - `whitepeace <TAG>` 强制与交战国达成停火恢复和平。

---

## ⚠️ P社控制台三大硬核避坑指南
1. **`ic` 瞬间建造的全局陷阱**：在游戏运行状态下开启 `ic`，**全球所有 AI 国家同样享受秒建效果**！必须在“游戏暂停”状态下输入 `ic`，排满建筑队列，随后再次输入 `ic` 关闭，方可恢复游戏时间；
2. **铁人模式 (Ironman) 限制**：铁人模式下存档被加密且严格封锁控制台，若需体验沙盒乐趣必须新建非铁人存档；
3. **Tag 切换前暂停**：输入 `tag` 切换国家前务必按空格暂停，否则本国原 AI 会在接管几秒内擅自修改你的陆军编制和生产线。
