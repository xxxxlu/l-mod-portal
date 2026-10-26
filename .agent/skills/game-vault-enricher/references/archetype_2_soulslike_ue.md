# 原型 2：魂系与虚幻引擎 (Soulslike & Unreal Engine)

## 📌 代表游戏与引擎映射
| 游戏名称 | Steam AppID | 引擎方案 | 核心控制台 / 注入工具 |
|---|---|---|---|
| 《黑神话：悟空》(Black Myth: Wukong) | 2358720 | Unreal Engine 5 | RE-UE4SS + `WukongGM` (RunScriptGM) |
| 《艾尔登法环》(Elden Ring) | 1245620 | FromSoftware 专有引擎 | 离线 EAC 绕过 + TGA Cheat Table + ModEngine2 |
| 《匹诺曹的谎言》(Lies of P) | 1627720 | Unreal Engine 4 | UE4SS 调试控制台 + FLiNG Trainer |
| 《堕落之主》(Lords of the Fallen) | 1501750 | Unreal Engine 5 | UE4SS + UEVR / 调试参数 |
| 《遗迹 2》(Remnant II) | 1282100 | Unreal Engine 5 | UE4SS + 存档修改器 (Save Guardian) |
| 《只狼：影逝二度》(Sekiro) | 814380 | FromSoftware 专有引擎 | Sekiro Mod Engine + DSDark3 CT |

---

## 🔍 四级精准技术检索 SOP (4-Tier Retrieval Queries)

### Tier 1: 官方/开发者数据维基与拆包数据
- `site:fextralife.com "Elden Ring" "Weapons" "item ID"`
- `site:fextralife.com "Black Myth Wukong" "Spirits" "Curios"`
- `site:github.com "UE4SS" "UFunction" "BGUFunctionLibraryManaged"`

### Tier 2: 专有底层运行时与开源代码仓
- `site:github.com "UE4SS-RE" "RE-UE4SS"`
- `site:github.com "lazyassin/WukongGM"`
- `site:github.com "soulsmods" "ModEngine2"`
- `"The Grand Archives" "Elden Ring Cheat Table"`

### Tier 3: Nexus Mods 权威专区 (前置与热度倒排)
- 重点定位：离线 EAC 绕过补丁、全景实时地图 HUD (BWMap)、全武器全图鉴存档导入工具、无锁定视角优化；
- 检查模组打包方式（`.pak`, `.ucas`, `ue4ss\Mods\` 路径映射）。

### Tier 4: 玩家社群高频痛点与识破/配装讨论
- `site:reddit.com/r/Eldenring "missable questlines" "Ranni" "Millicent"`
- `site:reddit.com/r/BlackMythWukong "all spirits" "missable bosses"`
- `"black myth wukong" "stutter fix" "engine.ini"`

---

## 🎯 八大系统维度全息核对清单 (Mandatory 8-Dimension Checklist)

1. **👑 核心战斗无敌与子弹时间识破教学**：
   - 全场景慢动作流速（`slomo 0.3` 拆解 Boss 出招前摇，识破弹反从容练习）；
   - 虚幻 5 自由飞行摄影相机（`toggledebugcamera` 360° 无死角穿模拍照）；
   - 隐藏/显示战斗 UI HUD（纯净录屏电影级体验）。
2. **🐵 特色核心机制（精魄变身 / 骨灰战灰 / 假肢忍具）**：
   - 黑神话：全 54 种怪物精魄变身一键入库（`allsoulskill`），特异化变身获得（幽魂大头、火狼广智、不能近战拳法等）；
   - 法环：仿身泪滴 +10、黑刀狄希、全套神圣魔法祷告与红狮子火焰战灰；
   - 只狼：全套顶级义手忍具（金刚铁伞、琉璃火、雾鸦）。
3. **🗡️ 传奇神兵利刃与全套神装**：
   - 如意金箍棒、三尖两刃枪、昆棍通天、大圣全套披挂（凤翅紫金冠/锁子黄金甲等）；
   - 法环：玛莲妮亚义手刀、暗月大剑、亵渎圣剑、全套山羊重铠。
4. **🏺 镇宗法宝、顶级葫芦与圣杯瓶调配**：
   - 全四阶隐藏法宝（辟火罩、定风珠、绣花针、芭蕉扇）；
   - 全套顶级神品葫芦、落伽香藤、醒酒胆与顶级龙膏药酒；
   - 法环：黄金种子、圣杯滴露、灵药圣杯瓶调配露滴。
5. **💊 灵丹妙药永久属性突破与财富自由**：
   - 灵蕴金钱 / 卢恩点数瞬间百万（财富自由）；
   - 九转金丹、太乙紫金丹、三清令宝丹永久提升生命、法力与气力上限；
   - 辰龙草药种子全图鉴收集（六六村自动化种植）。
6. **🗺️ 全土地庙/赐福点点亮与章回自由传送**：
   - 一键点亮全地图 100% 土地庙与野外打坐蒲团（`allmedition 1`）；
   - 战役章回瞬间自由跳转（第一回至第六回水帘洞直达）；
   - 法环全赐福点（包含地底希芙拉河与天空城）一键全亮。
7. **📜 影神图全志异、六根大圆满与全成就解锁**：
   - 影神图妖魔志异全图鉴点亮（`allcard`）；
   - 齐天大圣六根遗物全吸收（`alllegacy` 眼耳鼻舌身意羁绊大圆满）；
   - 八十一难全成就 Steam 官方瞬间达成。
8. **🎥 虚幻5画质微调与密林性能掉帧优化**：
   - 毛发细节与金属光影锐化（`r.Tonemapper.Sharpen 1.5`）；
   - 景深与动态模糊一键移除（消除 3D 眩晕不适感）；
   - 密林显存释放优化（`foliage.DiscardDataOnLoad 1` 提升复杂场景帧率）。

---

## 🚨 反作弊安全与联机封禁防护 (CRITICAL)
- **法环 / FS 引擎作品**：绝对禁止在开启 EAC 状态下进入任何多人联机大厅；
- **黑神话等单机大作**：无联机反作弊封号风险，但使用破坏性 GM 指令（如 `clearrolebag`）前务必在 `%LocalAppData%\b1\Saved\SaveGames\` 备份存档！
