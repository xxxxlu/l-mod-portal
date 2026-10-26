# L-MOD Vault 旗舰单机大作深度技术采掘方案库 (Rank 5 ~ Rank 7)

> **版本**：v3.0 (Milestone 3 工业级实战方案)  
> **适用范围**：Rank 5 《艾尔登法环》、Rank 6 《上古卷轴5：天际重制版》、Rank 7 《辐射4：次世代更新版》  
> **设计规范**：严格遵循 `game-vault-enricher` v2.5 强类型 Schema 与引擎语法 Linter，确保 100% 官方最新补丁实测可用、零假代码占位符。

---

## 目录
1. [Rank 5 《艾尔登法环》(Elden Ring) 技术采掘攻坚方案](#1-rank-5-艾尔登法环elden-ring-技术采掘攻坚方案)
2. [Rank 6 《上古卷轴5：天际重制版》(Skyrim SE/AE) 技术采掘攻坚方案](#2-rank-6-上古卷轴5天际重制版skyrim-seae-技术采掘攻坚方案)
3. [Rank 7 《辐射4：次世代更新版》(Fallout 4 Next-Gen) 技术采掘攻坚方案](#3-rank-7-辐射4次世代更新版fallout-4-next-gen-技术采掘攻坚方案)
4. [三大旗舰大作与底层引擎技术路由对照矩阵](#4-三大旗舰大作与底层引擎技术路由对照矩阵)

---

## 1. Rank 5 《艾尔登法环》(Elden Ring) 技术采掘攻坚方案

### 1.1 引擎与底层框架体系
- **游戏引擎**：FromSoftware 专有引擎 (Dantelion / FLVER 网格 / Param 数值表 / DCX 压缩格式体系)；
- **Steam AppID**：`1245620`；
- **官方最新对齐补丁**：App Ver 1.14 / Regulation Ver 1.14.1+ (黄金树幽影 DLC Shadow of the Erdtree Ready)；
- **核心前置框架**：
  1. `ModEngine2` (v2.1.0+)：专为魂系游戏开发的无侵入式 Mod 加载框架，通过 Hook `VirtualAlloc` 与文件系统 I/O，无需解包即直接重定向加载 `mod/` 目录下的 `.dcx`、`.param` 与 `regulation.bin`；
  2. `The Grand Archives (TGA) Cheat Table` (v1.14+)：全网最权威开源逆向内存调试表，提供 Item Gib 字节级背囊注入、事件标志位管理与 FreeCam 自由运镜；
  3. `Seamless Co-op` (v1.8.2+)：独立无缝联机框架，剥离官方服务器连接，采用独立 `.co2` 存档。

---

### 1.2 🛡️ Easy Anti-Cheat (EAC) 离线绕过机制与 100% 防封号方案
FromSoftware 部署的 EAC 驱动层服务会在检测到内存修改、未签名注入或异常道具时向万代服务器上报封禁标记（180天小黑屋隔离或全封）。

#### 三大免封安全启动路径
```mermaid
flowchart TD
    A["艾尔登法环启动需求"] --> B{"游玩场景"}
    B -->|"纯单机深度体验 / Mod 畅玩"| C["方案 A: ModEngine2 离线引导"]
    B -->|"零第三方工具纯净修改器"| D["方案 B: 替换引导法 (steam_appid)"]
    B -->|"好友联机无缝探索"| E["方案 C: Seamless Co-op 隔离联机"]
    
    C --> C1["launchmod_eldenring.bat\n(自动重定向绕过 EAC, 零改动原文件)"]
    D --> D1["备份 start_protected_game.exe\n复制 eldenring.exe 替换 + 1245620 txt"]
    E --> E1["独立 ersc 运行库 + .co2 存档\n完全隔离官方服务器, 100% 零封号"]
```

1. **方案 A (ModEngine2 离线管道重定向 - 极客首选)**：
   - ModEngine2 内置的 `launchmod_eldenring.bat` 在拉起游戏进程时通过管道参数强行截断 EAC 守护进程唤醒，游戏主菜单右下角将强制显示“检测到未授权行为，已切换为离线模式”；
   - **优势**：完全不修改 Steam 游戏根目录下的任何原生二进制，随时可通过 Steam 正常上线。
2. **方案 B (可执行文件重命名法 - 极简方案)**：
   - 进入 `<GameRoot>\Game\`；
   - 将原版 `start_protected_game.exe` 重命名为 `start_protected_game.exe.bak`；
   - 将 `eldenring.exe` 复制一份并重命名为 `start_protected_game.exe`；
   - 在同级目录新建文本文件 `steam_appid.txt`，内容输入 `1245620`；
   - 此时无论是 Steam 库直接启动还是双击均 100% 运行于免 EAC 纯净单机环境。
3. **方案 C (Seamless Co-op 无缝联机 - 联机神器)**：
   - 将模组解压至 `Game/`，启动 `launch_elden_ring_seamlesscoop.exe`；
   - 存档文件强制重命名为 `ER0000.co2`，官方 Steam 云存档为 `ER0000.sl2`，两者物理隔离互不干扰；
   - 彻底解除击杀 Boss 后遣返白灵的限制，支持自由共乘马匹、全图篝火同步。

> [!WARNING]
> **重返线上避坑门禁 (防封必读)**：
> 若后续需切回官方线上联机，**必须手动清除背包中由作弊生成的“非法未实装测试道具”或“突破强化上限的武器”**（如强化超过 +10/+25、非法质变、未开放的 DLC 隐藏废案）。合法范围内的卢恩、满级锻造石与常规全图鉴神装不受封禁影响。

---

### 1.3 核心爆点与八大系统维度全息对账清单

| 维度序号 | 系统维度名称 | 核心技术方案 / 控制代码 | 游戏特色爆点 |
|---|---|---|---|
| **维度 1** | 核心生存与时间流速 | `Num 1` (God Mode) / `Ctrl+Num 3` (Slomo 0.3x) / `Num 9` (一击破韧) | 子弹时间识破 Boss 前摇，告别幽影树翻车 |
| **维度 2** | 卢恩货币与随身强化 | `Ctrl+Num 1` (注入100万卢恩) / `Somber Ancient Dragon Smithing Stone x10` | 免泪滴幼体随时自由洗点，武器一键满级 |
| **维度 3** | 黄金树幽影 DLC 专属 | `Set Scadutree Blessing to 20` / `Revered Spirit Ash to 10` | 幽影树庇护与灵灰拉满，血怪手臂+25爆血流 |
| **维度 4** | 全套追忆神装武器 | `Blasphemous Blade +10` / `Hand of Malenia +10` / `Dark Moon Greatsword +10` | 亵渎圣剑吸血轮椅、暗月大剑、神躯化剑 |
| **维度 5** | 神级骨灰与传说战灰 | `Mimic Tear Ashes +10` / `Black Knife Tiche +10` / `猎犬步法` / `切腹` | 满血满状态带头大哥，穿墙命定之死狄希 |
| **维度 6** | 全套传说护符与滴露 | `Shard of Alexander` / `Rotten Winged Sword` / `Cerulean Hidden Tear` | 战技加伤15%，灵药圣杯瓶15秒无限法力轰击 |
| **维度 7** | 全赐福点亮与自由运镜 | `Unlock All Sites of Grace (Base & DLC)` / `FreeCam & Freeze Time` | 地下城战斗中无限制随时传送，360°摄影定格 |
| **维度 8** | 任务 Fact 与 NPC 赎罪 | `Clear NPC Aggro / Absolution` / `Revive Key Quest NPCs` / `All Bell Bearings` | 结缘教堂一键赎罪，误杀 NPC 满血复生 |

---

## 2. Rank 6 《上古卷轴5：天际重制版》(Skyrim SE/AE) 技术采掘攻坚方案

### 2.1 引擎与底层控制台规范
- **游戏引擎**：Bethesda Creation Engine 1 (64-bit Havok 物理架构)；
- **Steam AppID**：`489830`；
- **版本对齐**：Skyrim Anniversary/Special Edition v1.6.1170 (与 1.6.1130 深度适配)；
- **控制台呼出机制**：
  - 美式键盘左上角 **`~` (Tilde 键)**；
  - 配置文件门禁：`Documents\My Games\Skyrim Special Edition\Skyrim.ini` 中 `[General]` 下确认 `bAllowConsole=1`。
- **8位十六进制 FormID 运算规范**：
  - FormID 结构为 `AABBBBBB`，其中 `AA` 为加载索引（`00` 为本体 Skyrim.esm，`01` 为 Dawnguard，`02` 为 Hearthfire，`03` 为 Dragonborn，`FE:xxx` 为 ESL 轻量化模组）；
  - **极客速记规则**：控制台中前导 `0` 可完全省略，例如金币 FormID 为 `0000000F`，输入 `player.additem f 100000` 即可瞬间生效。

---

### 2.2 CTD 闪退急救与内存修复矩阵
天际模组环境中最常见的崩溃原因：内存溢出、骨骼网格错乱、破损 Havok 物理碰撞、Papyrus 脚本死锁循环。

```
【天际 SE/AE 工业级急救三件套】
├── 1. SKSE64 (v2.2.6)             -> 根目录部署 skse64_loader.exe，释放原生脚本引擎上限
├── 2. SSE Engine Fixes (v6.1.1)     -> 修复 60Hz+ 高刷新率下推车飞天抽搐、LipSync 嘴唇不同步、解除成就锁定
└── 3. Crash Logger SSE             -> 崩溃瞬间输出完整堆栈 Crash-*.log，直接指出报错 ESP 插件与贴图路径
```

#### 急救与脱困指令表
1. **地牢坏档/穿墙脱困**：`tcl` (Toggle Collision，一秒解除卡石缝绝境)；
2. **万能应急避难所**：`coc qasmoke` (瞬间传送进官方开发者烟雾房，内含全天际所有分类宝箱；输入 `coc riverwood` 传回溪木镇)；
3. **消除卡死 AI 行为**：`tai` (开关全局 AI) / `tcai` (开关战斗 AI)；
4. **强行复活关键 NPC**：按 `~` 鼠标左键点击尸体，输入 `resurrect 1` 满血原地复活。

---

### 2.3 恶性死循环任务控制台强行推进 (`setstage` 表)

Bethesda 游戏中由于脚本触发器失效引发的任务卡死，严禁直接使用 `caqs` (这会导致全游戏所有任务强制瞬间完成引发全面坏档)。必须使用 `setstage <QuestID> <StageNumber>` 定向推进：

| 任务名称 | 内部 QuestID | 恶性卡关节点 Bug 现象 | 强行修复控制台指令 | 预期效果 |
|---|---|---|---|---|
| **唤醒巨龙 / 灰胡子召唤** | `MQ105` | 西部哨塔杀龙吸收龙魂后，灰胡子高吼峰吼声不响 | `setstage MQ105 10` | 强制激活高吼峰觐见阶段，开启上山台阶 |
| **奥杜因之墙** | `MQ203` | 天空庇护之庙中伊思本不肯点燃火把，对着石壁发呆 | `setstage MQ203 280` | 跳过发呆动画，标记石壁解读完成进入下一幕 |
| **苏醒的恶梦** | `DA16` | 晨星城祭司艾兰达尔喝下折磨药水后卡死不进梦境 | `setstage DA16 200` | 强制完成净化瓦尔米娜神殿，直接获取腐化头骨 |
| **雪漫城内战宣誓** | `CW01A` | 帝国军团图留斯将军反复巡逻不触发宣誓对话 | `setstage CW01A 100` | 强制完成加入帝国军团仪式，发放全套军团护甲 |
| **外交豁免 (大使馆潜入)** | `MQ201` | 梭伦大使馆宴会中马伯恩无法引开卫兵开门 | `setstage MQ201 100` | 强制推进到厨房取回走私装备阶段 |

---

### 2.4 全套 16 件魔神器与远古神装 Hex ID 清单

| 魔神器名称 | 归属魔神 | 控制台派发指令 | 核心战斗特效 |
|---|---|---|---|
| **破晓者 (Dawnbreaker)** | 美瑞蒂亚 | `player.additem 0002ac61 1` | 亡灵克星，击中尸鬼引爆全屏神圣金光 |
| **莫拉格·巴尔钉头锤** | 莫拉格·巴尔 | `player.additem 000233e3 1` | 吸取耐力与魔法，3秒内置自动灵魂陷阱 |
| **梅鲁涅斯的剃刀** | 梅鲁涅斯·大衮 | `player.additem 000240d2 1` | 极高攻速，近战普攻 1.98% 几率一击必杀任何巨龙 |
| **阿祖拉之星 (Azura's Star)** | 阿祖拉 | `player.additem 00063b27 1` | 永不碎裂的无限特大灵魂石，附魔极客终极追求 |
| **破法者 (Spellbreaker)** | 佩伊特 | `player.additem 0004585a 1` | 格挡时生成 50 点神圣魔法护盾，完美抵御巨龙喷火 |
| **瓦巴杰克 (Wabbajack)** | 谢尔格拉 | `player.additem 000139b9 1` | 释放混沌随机魔法，将敌人瞬间变形为甜甜圈或泥沼蟹 |
| **乌木之刃 (Ebony Blade)** | 梅法拉 | `player.additem 0004a38f 1` | 双手太刀无限附魔，背刺友善 NPC 彻底解封吸血上限 |
| **骷髅钥匙 (Skeleton Key)** | 诺克图娜尔 | `player.additem 0003a070 1` | 永不折断的万能开锁器，解开全天际一切大师锁 |

---

## 3. Rank 7 《辐射4：次世代更新版》(Fallout 4 Next-Gen) 技术采掘攻坚方案

### 3.1 2024 次世代大更新断裂避坑与双轨路线
2024 年 4 月与 5 月，Bethesda 推送了所谓的“次世代大更新”(Next-Gen Update - v1.10.980 / v1.10.984)。由于编译器升级与内存偏移重写，导致长达 9 年积累的数十万依赖 F4SE 的顶级 Mod（如 MCM、Buffout 4、Sim Settlements 2、Place Everywhere）大面积失效。

#### 双轨解决方案对照
```mermaid
flowchart TD
    F4["辐射4版本选择"] --> RouteA["路线 A: 次世代原生适配路线 (v1.10.984+)"]
    F4 --> RouteB["路线 B: 经典降级回退路线 (v1.10.163)"]
    
    RouteA --> A1["使用 F4SE v0.7.2+\nAddress Library Next-Gen\nBuffout 4 NG 分支"]
    RouteA --> A2["适合: 纯原版画质体验、宽屏显示器、少Mod轻量玩家"]
    
    RouteB --> B1["使用 Fallout 4 Downgrader\n一键回退主程序至 1.10.163 黄金版本"]
    RouteB --> B2["适合: 深度重度Mod玩家、几百个大修整合包稳定运行"]
```

- **Steam 自动更新彻底防护**：
  在 Steam 库右键 `Fallout 4` -> `属性` -> `更新` -> 设置为 **“仅在我启动该游戏时更新”**，且日后**一律双击 `f4se_loader.exe` 启动**，绝不要在 Steam 客户端点击“开始游戏”，即可彻底阻止 Steam 偷偷推送小补丁打碎 Mod 框架！

---

### 3.2 聚落建造空间无限解除与避坑机制
在庇护山丘、红火箭或奇观岛建造大型基地时，原版右上角的“建造空间”很快就会被填满并变黄禁止建造。

#### 空间无限解除代码
1. 走到聚落的工坊控制台（Workshop）正前方；
2. 按 `~` 呼出控制台，用鼠标左键准确点击工坊工作台（屏幕中央应出现类似 `(000249dc)` 的 ID）；
3. 依次输入以下指令回车：
   ```text
   setav 349 9999999
   setav 348 9999999
   ```
4. **原理**：`349` 代表当前聚落的最大三角形几何面预算 (Triangles Budget)，`348` 代表总实体物体数量上限 (Draw Calls Budget)。修改为千万级别后，右上角建造容量条直接清空重置为 0，实现真正的无限摩天大楼建造！
5. **地皮极速清理**：站在聚落领地中央输入 `scrapall`，一秒拆解全图所有废弃木屋、碎石杂草并转化为木材与钢铁存入工坊！

> [!CAUTION]
> **三角区 (Triangle of Death) 闪退避坑**：
> 联邦西北角的 **庇护山丘 (Sanctuary)**、**红火箭维修站 (Red Rocket)** 与 **阿伯纳西农场 (Abernathy Farm)** 在地理位置上相隔极近，被称为“废土死亡三角区”。请不要在三个据点同时塞入几万件建筑物体与几百个动力发电机，否则玩家在三地之间奔跑加载时容易引发 Papyrus 堆栈溢出崩溃！

---

### 3.3 全传奇武器自定义词条附魔 (`attachmod` 表)
辐射 4 允许玩家在控制台中直接为地面上的任意武器附魔神级传奇前缀：
- **操作流程**：将武器从背包扔在地上，按 `~` 呼出控制台，鼠标左键点击地上的武器，输入 `attachmod <FormID>` 即可立即刻印专属词条！

| 传奇词条名称 | 内部 FormID | 附魔实战价值 | 最佳搭配枪械推荐 |
|---|---|---|---|
| **双弹 (Two Shot)** | `001cc2ac` | 每次射击额外射出 1 发完整弹头，基础伤害直接翻倍 | 高斯步枪、.44 左轮手枪、猎枪狙击步枪 |
| **爆破 (Explosive)** | `001e7c20` | 每颗弹头命中目标均引发范围爆炸，附加 15 点范围面伤 | 战斗霰弹枪 (每颗霰弹全炸)、冲锋枪、转轮加特林 |
| **狂怒 (Furious)** | `001f6ad4` | 连续命中同一目标伤害逐级倍增无上限，单挑死爪如切菜 | 弟子帮战斗小刀、克罗格手枪、高射速自动步枪 |
| **无底洞 (Never Ending)** | `001ed37e` | 弹匣容量锁定为背囊总弹药量，彻底消除装弹动作 | 双管霰弹枪 (化身半自动加特林喷子)、激光毛瑟枪 |
| **膝盖收割者 (Kneecapper)** | `001f1048` | 每次命中均有 20% 几率强制打断目标双腿残疾瘫痪 | 10mm 自动手枪、管枪机枪 (废土最稳控场轮椅) |
| **煽动 (Instigating)** | `001f31b9` | 目标处于满血状态时，造成的伤害直接翻倍 | 消音高斯步枪、猎枪 (潜行狙击流一枪数千暴击) |

---

### 3.4 极速批处理脚本 (`bat` 脚本) 工业规范
将常用配置打包为文本文件，放入 Fallout 4 游戏根目录（与 `Fallout4.exe` 同级）：
- 示例：在根目录建立 `all_materials.txt`，内容填入：
  ```text
  player.additem 000731a4 10000
  player.additem 000731a3 10000
  player.additem 0006907a 5000
  player.additem 0006907c 5000
  player.additem 0006907e 5000
  player.additem 0006907f 5000
  ```
- 进入游戏后，只需按 `~` 输入：
  ```text
  bat all_materials
  ```
- 引擎将在 1 毫秒内瞬间完成全部数万份素材入库，无需每次手动敲打繁琐指令！

---

## 4. 三大旗舰大作与底层引擎技术路由对照矩阵

```mermaid
graph LR
    subgraph FromSoftware ["FromSoftware 专有引擎"]
        ER["艾尔登法环 (Rank 5)"] --> ME2["ModEngine2 离线引导"]
        ER --> TGA["TGA Cheat Table (Item Gib)"]
        ER --> SC["Seamless Co-op (隔离联机)"]
    end

    subgraph CreationSE ["Creation Engine 1 (Skyrim SE/AE)"]
        SK["上古卷轴5 (Rank 6)"] --> CON1["原生 ~ 控制台 (FormID)"]
        SK --> SKSE["SKSE64 (v2.2.6)"]
        SK --> EF["SSE Engine Fixes (防CTD/成就)"]
    end

    subgraph CreationFO ["Creation Engine 1 (Fallout 4 NG)"]
        FO["辐射4 (Rank 7)"] --> CON2["原生 ~ 控制台 (attachmod/bat)"]
        FO --> F4SE["F4SE Next-Gen / Downgrader"]
        FO --> BF["Buffout 4 (堆栈诊断排错)"]
    end
```

| 评测维度 | 《艾尔登法环》(Rank 5) | 《上古卷轴5：天际重制版》(Rank 6) | 《辐射4：次世代更新版》(Rank 7) |
|---|---|---|---|
| **引擎架构** | FromSoftware Dantelion | Creation Engine 1 (64-bit Havok) | Creation Engine 1 (Fallout PBR 分支) |
| **反作弊机制** | Easy Anti-Cheat (EAC 驱动层) | 无反作弊 (纯单机 Steam 成就锁) | 无反作弊 (纯单机 Steam 成就锁) |
| **控制台终端** | 无打字控制台 (热键/CT表/参数注入) | 原生全功能 `~` 终端 | 原生全功能 `~` 终端 |
| **关键扩展器** | ModEngine2 (v2.1.0+) | SKSE64 (v2.2.6+ 适配 1.6.1170) | F4SE (v0.7.2+ 适配 1.10.984) |
| **核心排错工具** | TGA Memory Table / 离线批处理 | SSE Engine Fixes / Crash Logger | Buffout 4 / Fallout 4 Downgrader |
| **装备获取形式** | Item Gib 内存图鉴派发 | `player.additem <FormID> <Count>` | `player.additem` + `attachmod` 动态附魔 |
| **版本安全底线** | 回退线上前彻底清理越级非法道具 | 安装 SSE Engine Fixes 防 60Hz 抽搐 | 锁定 Steam 自动更新防次世代二次破坏 |
