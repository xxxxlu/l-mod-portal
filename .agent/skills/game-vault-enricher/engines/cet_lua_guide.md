# CDPR RED 引擎与 Cyber Engine Tweaks (CET) 规范

## 🎯 核心方案：Cyber Engine Tweaks (CET)
适用于《赛博朋克 2077》(Cyberpunk 2077)。游戏在 2.0 及 2.13 往日之影版本全面重构了义体、专精与属性系统。

---

## 🛠️ 安装与前置配置
1. **安装路径**：解压至 `<Cyberpunk 2077>\bin\x64\`，确保 `version.dll` 与 `plugins/cyber_engine_tweaks/` 就位；
2. **热键绑定**：首次启动游戏，屏幕中央会强制弹出热键设定浮层，按下 `~` 键完成绑定；
3. **控制台唤出**：游戏中随时按 `~` 呼出 Overlay，在最底部的 Console 输入框粘贴 Lua 指令并回车。

---

## 💻 核心语法规则与范例

### 1. 物品添加 (`Game.AddToInventory`)
```lua
-- 语法: Game.AddToInventory("<ItemString>", <Quantity>)
Game.AddToInventory("Items.money", 1000000)
Game.AddToInventory("Items.Preset_Katana_Saburo", 1)
Game.AddToInventory("Items.AdvancedSandevistanApogeePlusPlus", 1)
```

### 2. 角色属性与专精成长 (`PlayerDevelopmentSystem`)
```lua
local p = Game.GetPlayer()
local ds = PlayerDevelopmentSystem.GetInstance(p):GetDevelopmentData(p)
-- 将猎头 (CoolSkill) 升至 60 级
ds:SetLevel(gamedataProficiencyType.CoolSkill, 60, telemetryLevelGainReason.Gameplay)
```

### 3. 全载具解锁 (`Game.GetVehicleSystem`)
```lua
vs = Game.GetVehicleSystem()
vs:EnableAllPlayerVehicles()
```

### 4. 任务 Fact 与隐藏结局 (`Game.GetQuestsSystem`)
```lua
-- 解锁单挑荒坂塔单挑结局（无需等候对话）
Game.GetQuestsSystem():SetFactStr("sq032_johnny_friend", 1)
```

### 5. 环境与通缉消除
```lua
-- 消除 NCPD 警星通缉
Game.GetPreventionSpawnSystem():RequestDespawnPreventionAgents()
-- 时间调至正午 12:00
Game.GetTimeSystem():SetGameTimeByHMS(12, 0, 0)
```
