# Bethesda Creation 引擎 (CE1 / CE2) 控制台与 Hex ID 规范

## 🎯 适用品类与代表游戏
- 《上古卷轴 5：天际 重制版》(Skyrim SE/AE - Steam AppID: 489830)
- 《辐射 4》(Fallout 4 - Steam AppID: 377160)
- 《星空》(Starfield - Creation Engine 2 - Steam AppID: 1716740)
- 《辐射：新维加斯》(Fallout: New Vegas - Gamebryo Engine)

---

## 🛠️ 控制台唤出、前置工具与成就保护

### 1. 呼出快捷键与输入法设置
- **呼出按键**：游戏中直接按下键盘左上角 **`~` (波浪键 / Tilde)** 即可暂停游戏并打开全屏控制台；
- **排错要点**：若无响应，请在 Windows 语言栏中切换为“英语 (美国)”美式键盘输入法，或在游戏根目录的 `Skyrim.ini` / `Fallout4.ini` 中确认 `bAllowConsole=1`。

### 2. 核心前置扩展器 (Script Extenders)
高级模组与复杂脚本必须依赖对应的脚本扩展器启动（如 `skse64_loader.exe`, `f4se_loader.exe`, `sfse_loader.exe`）。扩展器解压至与游戏主 `.exe` 同级的根目录下。

### 3. 成就锁定警告与解除 (Achievement Enablers)
Bethesda 游戏只要在存档中使用过一次控制台或加载了任何 Mod，该存档将被系统打上 `[Modded]` 脏标记并永久禁用 Steam 官方成就。
- **强制必备插件**：
  - 天际 SE：`SSE Engine Fixes` 或 `Achievements Mods Enabler`
  - 辐射 4：`Buffout 4` 或 `Achievements` (F4SE)
  - 星空：`Baka Achievement Enabler` (SFSE)

---

## 💻 8 位十六进制 Hex ID (FormID) 运算机制

Bethesda 引擎所有物品、法术、NPC、任务均分配有一个 8 位的十六进制内部编码 (FormID)，其前两位表示加载顺序 (Load Order Index)：

| 前缀代码 | 归属类型 | 说明 |
|---|---|---|
| `00` | 主游戏本体 (Master ESM) | 如天际金币 `0000000F`、辐射4瓶盖 `0000000F` |
| `01` - `04` | 官方扩展包 (DLCs) | 按玩家安装顺序排列（如黎明守卫、龙裔、远港、核子世界） |
| `FE:xxx` | 轻量化插件 (ESL / ESP-FE) | 现代重制版中由引擎自动动态映射高位偏移 |

> [!TIP]
> **前缀补零省略技巧**：在控制台中输入 FormID 时，前置多余的 `0` 可以省略！
> 例如输入 `player.additem f 10000` 与 `player.additem 0000000F 10000` 效果完全相同。

---

## 🎮 高频核心指令大全

### 1. 角色状态与神级上帝模式
```text
tgm                               # 上帝模式 (Toggle God Mode: 无敌、无限耐力、无限魔法弹药、无限负重)
tim                               # 不死模式 (Toggle Immortal Mode: 会掉血受击，但生命绝不归零死亡)
tcl                               # 穿墙穿模模式 (Toggle Collision: 自由穿墙、悬浮飞行)
tmm 1                             # 点亮大地图所有地标 (Toggle Map Markers: 包含未探明区域)
player.setav carryweight 99999    # 修改角色背包基础负重上限为 99999
player.setav speedmult 150        # 修改角色奔跑移速为 1.5 倍 (默认 100)
showracemenu                      # 打开角色捏脸定制器 (随时自由改名、换脸与变性)
healplayer                        # 瞬间回复角色生命值至满额
```

### 2. 货币与物品派发 (`player.additem`)
```text
player.additem 0000000F 100000    # 增加 100,000 金币 (Skyrim) / 瓶盖 (Fallout 4) / 信用币 (Starfield)
player.additem 0000000A 1000      # 增加 1,000 个开锁器 (Lockpick / Bobby Pin)
player.additem <FormID> <Count>   # 向玩家背囊生成指定数量的武器、防具或药剂
player.removeitem <FormID> <Count># 销毁指定数量的物品
```

### 3. 任务卡关与剧情修复
```text
sqt                               # 显示当前所有活动任务的目标列表 (Show Quest Targets)
getstage <QuestID>                # 查询指定任务当前行进到的阶段号
setstage <QuestID> <StageNumber>  # 强制将任务跳转至指定阶段 (修复 NPC 不刷新的恶性 Bug)
completequest <QuestID>           # 强制标记该任务已圆满完成
resetquest <QuestID>              # 重置任务至初始状态重新触发
```

### 4. 场景探索、NPC 交互与传送
```text
coc <CellID>                      # 传送至指定内部场景 (如 coc qasmoke 传送至天际全物品开发者烟雾房)
player.moveto <RefID>             # 瞬间传送至指定伙伴或 NPC 身旁
player.placeatme <BaseID> 1       # 在自己面前生成指定 NPC 或生物实体
kill                              # 鼠标点击选中目标后输入，直接处死该实体
resurrect                         # 鼠标点击选中尸体后输入，使其复活站起
unlock                            # 鼠标点击锁定的门或宝箱后输入，直接秒破专家/大师级锁
tai                               # 开关全场 AI (Toggle AI: 敌人站桩木偶停止一切动作)
tcai                              # 开关战斗 AI (Toggle Combat AI: 敌人保持巡逻但不会攻击)
```

---

## ⚡ 批处理脚本一键执行 (`bat` 命令)
如果需要一次性获取上百件装备或执行复杂调优，可在游戏根目录建立文本文件（如 `all_weapons.txt`），将控制台指令每行写一条存入其中。
进入游戏后，只需在控制台中输入：
```text
bat all_weapons
```
引擎将以毫秒级瞬间串行执行文件内所有指令，极大提升配置效率与使用体验！
